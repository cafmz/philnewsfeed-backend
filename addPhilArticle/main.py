import json
import boto3
import decimal
from boto3.dynamodb.types import DYNAMODB_CONTEXT
from boto3.dynamodb.conditions import Key
from sites.aeon import aeon_rss

# Inhibit Inexact Exceptions
DYNAMODB_CONTEXT.traps[decimal.Inexact] = 0
# Inhibit Rounded Exceptions
DYNAMODB_CONTEXT.traps[decimal.Rounded] = 0

def add_article(event, context):
    client = boto3.resource('dynamodb')
    table = client.Table('philNewsFeed')
    print(table.table_status)
    try:
        scrap_sites = [aeon_rss("https://aeon.co/feed.rss"),]
        with table.batch_writer() as batch:
            for sites in scrap_sites:
                for elements in sites:
                    resp = batch.put_item(
                        Item={
                            "id":elements['id'],
                            "name":elements['name'],
                            "title":elements['title'],
                            "link":elements['link'],
                            "published":elements['published'],
                        })
        
        return {
            'statusCode': 200,
        }
        
    except Exception as e:
        print("\nDatabase operation failed. See exception:")
        raise e