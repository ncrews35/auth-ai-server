import os
import json
from db import DBTable


def get_key(event, context):
    user_id = event.get('user')
    provider_id = event.get('provider')

    keys_table = DBTable(os.getenv('KEYS_TABLE'))
    key = keys_table.get_sort('user_id', user_id, 'provider_id', provider_id)

    if key:
        return {
            'statusCode': 200,
            'body': json.dumps(key)
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({
                'message': 'Key not found'
            })
        }