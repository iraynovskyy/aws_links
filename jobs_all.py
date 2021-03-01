import boto3
import json
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])


def lambda_jobs_get_all(event, context):
    resp = table.scan()
    records = []

    for item in resp['Items']:
        records.append(item)

    # body = {
    #     "message": "Go Serverless v1.0! Your function executed successfully!",
    #     "input": event
    # }

    response = {
        # "isBase64Encoded": 1,
        "statusCode": 200,
        # "headers": {"headerName": "headerValue"},
        "body": json.dumps(records)
    }
    return response
