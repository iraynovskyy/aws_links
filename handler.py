import json
import time
import logging
import uuid


def hello(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully01!",
        "input": event
    }

    response = {
        # "isBase64Encoded": 1,
        "statusCode": 200,
        # "headers": {"headerName": "headerValue"},
        "body": json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration

    # return {
    #     "message": "Go Serverless v1.0! Your function executed successfully!",
    #     "event": event
    # }



