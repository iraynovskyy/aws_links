import json
import os
import time
from datetime import datetime
import logging
import uuid
import boto3
from urllib.parse import urlparse
import feedparser

'''
INPUT = {
  "links": [
    "https://facebook.com",
    "https://investorshub.advfn.com/boards/rss.aspx?board_id=22658",
    "https://tesla.com",
    "https://twitter.com",
    "http://feedparser.org/docs/examples/rss20.xml",
    "https://www.feedotter.com/feed"
  ]
}
'''

# KEY_TABLE_NAME = os.environ['KEY_TABLE']
CLIENT = boto3.client('stepfunctions')
CLIENT_db = boto3.client('dynamodb')
REGION = os.environ.get('us-east-2')

# client = boto3.client('stepfunctions')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])


def link_type(url):
    link = urlparse(url)

    if link.hostname in ("twitter.com", "twittter.com", "twttr.com", "www.twitter.fr", "www.twitter.jp"):
        return ("Twitter")
    elif len(feedparser.parse(url).entries) != 0:
        return ("RSS")
    else:
        return ("Website")


def lambda_handler(event, context):
    try:
        links = list(event["links"])
    except KeyError:
        return {
            'Error': "Links are not provided 007"
        }

    if "callback" in event:
        callback = event["callback"]
    #     print('callback is in event')
    # else:
    #     print('callback is NOT in event')

    response = []
    for link in links:
        job_id = str(uuid.uuid1())  # 90a0fce-sfhj45-fdsfsjh4-f23f

        input = {}

        input["job_id"] = job_id
        input["Link"] = link
        input["timestamp"] = str(datetime.now().timestamp())
        input["linkType"] = link_type(link)
        try:
            input["Callback"] = callback
        except:
            pass

        CLIENT.start_execution(
            stateMachineArn=os.environ["STATE_MACHINE"],
            name=job_id,
            input=json.dumps(input)
        )

        item = {
            'job_id': job_id,
            'timestamp': input["timestamp"],
            'link': link,
            'linkType': input["linkType"],
            'state': 'Processing'
        }
        try:
            item['callback'] = callback
            print('callback was included in this event.')
        except UnboundLocalError:
            pass

        table.put_item(Item=item)
        # CLIENT_db.put_item(
        #
        #     TableName=KEY_TABLE_NAME,
        #
        #     Item={
        #         'job_id': {'S': job_id},
        #         'timestamp': {'S': input["timestamp"]},
        #         'link': {'S': link},
        #         'linkType': {'S': 'Website'},
        #     }
        # )
        response.append(job_id)

    return {"idList": response}
