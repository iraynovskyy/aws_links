import requests
import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])


def func_result_processing(message, context):
    if "Error" in message:
        state = "Error"
        result = message["Error"]
    else:
        state = "Success"
        result = message["Result"]

    table.update_item(
        Key={
            'job_id': message["job_id"]
        },
        UpdateExpression='SET #state = :value, #result = :result, #timestamp = :timestamp',
        ExpressionAttributeValues={
            ':value': state,
            ':result': str(result),
            ':timestamp': str(message["timestamp"])
        },
        ExpressionAttributeNames={
            "#state": "state",
            "#result": "result",
            "#timestamp": "timestamp"
        }
    )
    data = {}
    try:
        if "Error" in message:
            data['Error'] = message["Error"]
        else:
            data['Result'] = message["Result"]
        requests.post(message["Callback"], data=json.dumps(data), headers={'Content-Type': 'application/json'})
    except requests.exceptions.RequestException:
        return ({"Error": "CallbackEr"})
    except KeyError:
        return ({})

# import json
# import os
# import time
# import boto3

#
# def func_result_processing(event, context):
#     print('hello form func end_result and write into DB')
#     return "hello return from the last function. Success"
