import json
import requests


def func_website(message, context):
    response = {}
    try:
        response["Callback"] = message["Callback"]
    except:
        pass
    response["job_id"] = message["job_id"]
    response["Link"] = message["Link"]
    response["timestamp"] = message["timestamp"]

    url = message["Link"]

    try:
        response["Result"] = requests.get(url).elapsed.total_seconds()
    except requests.exceptions.RequestException as e:
        print(e)
        response["Error"] = "Requesting error"

    # print('hello form func website')
    # return "hello return from website"
    return response
