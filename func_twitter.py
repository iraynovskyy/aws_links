import json
import os


def func_twitter(event, context):
    response = {}
    response["job_id"] = event["job_id"]
    response["Link"] = event["Link"]
    response["timestamp"] = event["timestamp"]

    link = event["Link"]
    # print('hello form func twitter')
    response["Result"] = "HaD Not sTarTeD iT yEt:)"
    return response
