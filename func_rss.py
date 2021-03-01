import json
import feedparser


def func_rss(message, context):
    response = {}
    try:
        response["Callback"] = message["Callback"]
    except KeyError:
        pass
    response["job_id"] = message["job_id"]
    response["Link"] = message["Link"]
    response["timestamp"] = message["timestamp"]

    link = message["Link"]
    try:
        dataFeeds = feedparser.parse(link)
        response["Result"] = dataFeeds.entries[-5:]
    except BaseException as e:
        response["Error"] = e
    return response

#
# def func_rss(event, context):
#     print('hello form func rss')
#     return "hello return from rss"
#
