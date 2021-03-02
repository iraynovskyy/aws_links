import json


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
