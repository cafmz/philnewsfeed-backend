import json
import boto3
import decimal
from boto3.dynamodb.types import DYNAMODB_CONTEXT
from boto3.dynamodb.conditions import Key, Attr

# Inhibit Inexact Exceptions
DYNAMODB_CONTEXT.traps[decimal.Inexact] = 0
# Inhibit Rounded Exceptions
DYNAMODB_CONTEXT.traps[decimal.Rounded] = 0

def get_article(event, context):
    client = boto3.resource('dynamodb')
    table = client.Table('philNewsFeed')
    print(table.table_status)
    try:
        results = []
        last_evaluated_key = None
        while True:
            if last_evaluated_key:
                resp = table.scan(
                    TableName = "philNewsFeed",
                    ExclusiveStartKey=last_evaluated_key
                )
            else:
                resp = table.scan(TableName = "philNewsFeed")
            
            last_evaluated_key = resp.get('LastEvaluatedKey')
            results.extend(resp['Items'])
            
            if not last_evaluated_key:
                break
            
        return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': "*",
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
        'body': results
        }
    except Exception as e:
        print(e)