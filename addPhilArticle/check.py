import json
import boto3
import decimal
from boto3.dynamodb.types import DYNAMODB_CONTEXT
from boto3.dynamodb.conditions import Key

# Inhibit Inexact Exceptions
DYNAMODB_CONTEXT.traps[decimal.Inexact] = 0
# Inhibit Rounded Exceptions
DYNAMODB_CONTEXT.traps[decimal.Rounded] = 0

def check_new_article(link):
    client = boto3.resource('dynamodb')
    table = client.Table('philNewsFeed')
    exist = len(table.query(
            IndexName = "link-index",
            KeyConditionExpression=Key('link').eq(link)
        )['Items'])
    if not exist:
        print("New article found!")
        return link