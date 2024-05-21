import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table_name = 'YOUR_TABLE_NAME'  # Substitua por: ${AWS::StackName}-table

def handler(event, context):
    table = dynamodb.Table(table_name)
    http_method = event['httpMethod']
    if http_method == 'POST':
        return create_item(event, table)
    elif http_method == 'GET':
        return get_item(event, table)
    elif http_method == 'PUT':
        return update_item(event, table)
    elif http_method == 'DELETE':
        return delete_item(event, table)
    else:
        return response(400, {'error': 'Unsupported method'})

def create_item(event, table):
    try:
        item = json.loads(event['body'])
        table.put_item(Item=item)
        return response(200, {'message': 'Item created', 'item': item})
    except ClientError as e:
        return response(400, {'error': str(e)})

def get_item(event, table):
    try:
        key = event['queryStringParameters']
        result = table.get_item(Key=key)
        return response(200, {'item': result.get('Item')})
    except ClientError as e:
        return response(400, {'error': str(e)})

def update_item(event, table):
    try:
        key = event['queryStringParameters']
        update_expression = 'SET '
        expression_attribute_values = {}
        item = json.loads(event['body'])
        for k, v in item.items():
            update_expression += f'{k} = :{k}, '
            expression_attribute_values[f':{k}'] = v
        update_expression = update_expression[:-2]
        table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
        )
        return response(200, {'message': 'Item updated', 'item': item})
    except ClientError as e:
        return response(400, {'error': str(e)})

def delete_item(event, table):
    try:
        key = event['queryStringParameters']
        table.delete_item(Key=key)
        return response(200, {'message': 'Item deleted'})
    except ClientError as e:
        return response(400, {'error': str(e)})

def response(status_code, body):
    return {
        'statusCode': status_code,
        'body': json.dumps(body),
        'headers': {
            'Content-Type': 'application/json',
        },
    }
