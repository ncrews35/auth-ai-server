import os
import boto3 as boto

AWS_KEY_ID = os.getenv("AWS_KEY_ID")
AWS_SECRET = os.getenv("AWS_SECRET")
REGION = os.getenv('AWS_REGION')

dynamodb = boto.resource(
    "dynamodb",
    region_name=REGION,
    aws_access_key_id=AWS_KEY_ID,
    aws_secret_access_key=AWS_SECRET
)


class DBTable:

    def __init__(self, table_name):
        self.table = dynamodb.Table(table_name)

    def put(self, item):
        self.table.put_item(Item=item)

    def update(self, key, value, attr, newValue):
        self.table.update_item(
            Key={key: value},
            UpdateExpression='SET ' + attr + ' = :val1',
            ExpressionAttributeValues={':val1': newValue}
        )

    def get(self, key, value):
        r = self.table.get_item(Key={key: value})
        if r:
            return r.get('Item')
        return None

    def get_sort(self, key, value, sort, sort_value):
        r = self.table.get_item(Key={key: value, sort: sort_value})
        return r.get('Item')

    def delete(self, key, value):
        self.table.delete_item(Key={key: value})

    def batch_write(self, items):
        with self.table.batch_writer() as batch:
            for item in items:
                batch.put_item(Item=item)

    def batch_get(self, key, value, sort, sort_values):
        results = []
        for sort_value in sort_values:
            results.append(self.get_sort(key, value, sort, sort_value))

        return results