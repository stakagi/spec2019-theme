import json
import os
import uuid
from datetime import datetime

import boto3
import requests

from boto3.dynamodb.conditions import Key, Attr


def user_create(event, context):
    user_table = boto3.resource('dynamodb').Table(os.environ['USER_TABLE'])
    # wallet_table = boto3.resource('dynamodb').Table(os.environ['WALLET_TABLE'])
    body = json.loads(event['body'])
    user_table.put_item(
        Item={
            'id': str(body['id']),
            'name': body['name']
        }
    )
    # wallet_table.put_item(
    #     Item={
    #         'id': str(uuid.uuid4()),
    #         'userId': body['id'],
    #         'amount': 0
    #     }
    # )
    return {
        'statusCode': 200,
        'body': json.dumps({'result': 'ok'})
    }


def wallet_charge(event, context):
    # wallet_table = boto3.resource('dynamodb').Table(os.environ['WALLET_TABLE'])
    history_table = boto3.resource('dynamodb').Table(os.environ['PAYMENT_HISTORY_TABLE'])
    body = json.loads(event['body'])
    # result = wallet_table.scan(
    #     ScanFilter={
    #         'userId': {
    #             'AttributeValueList': [
    #                 body['userId']
    #             ],
    #             'ComparisonOperator': 'EQ'
    #         }
    #     }
    # )
    # user_wallet = result['Items'].pop()
    # total_amount = user_wallet['amount'] + body['chargeAmount']
    # wallet_table.update_item(
    #     Key={
    #         'id': user_wallet['id']
    #     },
    #     AttributeUpdates={
    #         'amount': {
    #             'Value': total_amount,
    #             'Action': 'PUT'
    #         }
    #     }
    # )
    history_table.put_item(
        Item={
            'userId': body['userId'],
            'transactionId': body['transactionId'],
            'chargeAmount': body['chargeAmount'],
            'locationId': body['locationId'],
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    )
    requests.post(os.environ['NOTIFICATION_ENDPOINT'], json={
        'transactionId': body['transactionId'],
        'userId': body['userId'],
        'chargeAmount': body['chargeAmount'],
        # 'totalAmount': int(total_amount)
        'totalAmount': 0
    })

    return {
        'statusCode': 202,
        'body': json.dumps({'result': 'Assepted. Please wait for the notification.'})
    }


def wallet_use(event, context):
    # wallet_table = boto3.resource('dynamodb').Table(os.environ['WALLET_TABLE'])
    history_table = boto3.resource('dynamodb').Table(os.environ['PAYMENT_HISTORY_TABLE'])
    body = json.loads(event['body'])
    # result = wallet_table.scan(
    #     ScanFilter={
    #         'userId': {
    #             'AttributeValueList': [
    #                 body['userId']
    #             ],
    #             'ComparisonOperator': 'EQ'
    #         }
    #     }
    # )
    # user_wallet = result['Items'].pop()
    # total_amount = user_wallet['amount'] - body['useAmount']
    # if total_amount < 0:
    #     return {
    #         'statusCode': 400,
    #         'body': json.dumps({'errorMessage': 'There was not enough money.'})
    #     }

    # wallet_table.update_item(
    #     Key={
    #         'id': user_wallet['id']
    #     },
    #     AttributeUpdates={
    #         'amount': {
    #             'Value': total_amount,
    #             'Action': 'PUT'
    #         }
    #     }
    # )
    history_table.put_item(
        Item={
            'userId': body['userId'],
            'transactionId': body['transactionId'],
            'useAmount': body['useAmount'],
            'locationId': body['locationId'],
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    )
    requests.post(os.environ['NOTIFICATION_ENDPOINT'], json={
        'transactionId': body['transactionId'],
        'userId': body['userId'],
        'useAmount': body['useAmount'],
        # 'totalAmount': int(total_amount)
        'totalAmount': 0
    })

    return {
        'statusCode': 202,
        'body': json.dumps({'result': 'Assepted. Please wait for the notification.'})
    }


def wallet_transfer(event, context):
    # wallet_table = boto3.resource('dynamodb').Table(os.environ['WALLET_TABLE'])
    history_table = boto3.resource('dynamodb').Table(os.environ['PAYMENT_HISTORY_TABLE'])
    body = json.loads(event['body'])
    # from_wallet = wallet_table.scan(
    #     ScanFilter={
    #         'userId': {
    #             'AttributeValueList': [
    #                 body['fromUserId']
    #             ],
    #             'ComparisonOperator': 'EQ'
    #         }
    #     }
    # ).get('Items').pop()
    # to_wallet = wallet_table.scan(
    #     ScanFilter={
    #         'userId': {
    #             'AttributeValueList': [
    #                 body['toUserId']
    #             ],
    #             'ComparisonOperator': 'EQ'
    #         }
    #     }
    # ).get('Items').pop()

    # from_total_amount = from_wallet['amount'] - body['transferAmount']
    # to_total_amount = from_wallet['amount'] + body['transferAmount']
    # if from_total_amount < 0:
    #     return {
    #         'statusCode': 400,
    #         'body': json.dumps({'errorMessage': 'There was not enough money.'})
    #     }

    # wallet_table.update_item(
    #     Key={
    #         'id': from_wallet['id']
    #     },
    #     AttributeUpdates={
    #         'amount': {
    #             'Value': from_total_amount,
    #             'Action': 'PUT'
    #         }
    #     }
    # )
    # wallet_table.update_item(
    #     Key={
    #         'id': to_wallet['id']
    #     },
    #     AttributeUpdates={
    #         'amount': {
    #             'Value': to_total_amount,
    #             'Action': 'PUT'
    #         }
    #     }
    # )
    history_table.put_item(
        Item={
            'userId': body['fromUserId'],
            'transactionId': body['transactionId'],
            'useAmount': body['transferAmount'],
            'locationId': body['locationId'],
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    )
    history_table.put_item(
        Item={
            'userId': body['toUserId'],
            'transactionId': body['transactionId'],
            'chargeAmount': body['transferAmount'],
            'locationId': body['locationId'],
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    )
    requests.post(os.environ['NOTIFICATION_ENDPOINT'], json={
        'transactionId': body['transactionId'],
        'userId': body['fromUserId'],
        'useAmount': body['transferAmount'],
        'totalAmount': int(0), # TODO 集計結果を返す
        'transferTo': body['toUserId']
    })
    requests.post(os.environ['NOTIFICATION_ENDPOINT'], json={
        'transactionId': body['transactionId'],
        'userId': body['toUserId'],
        'chargeAmount': body['transferAmount'],
        'totalAmount': int(0), # TODO 集計結果を返す
        'transferFrom': body['fromUserId']
    })

    return {
        'statusCode': 202,
        'body': json.dumps({'result': 'Assepted. Please wait for the notification.'})
    }


def get_user_summary(event, context):
    # wallet_table = boto3.resource('dynamodb').Table(os.environ['WALLET_TABLE'])
    user_table = boto3.resource('dynamodb').Table(os.environ['USER_TABLE'])
    history_table = boto3.resource('dynamodb').Table(os.environ['PAYMENT_HISTORY_TABLE'])
    params = event['pathParameters']
    user = user_table.get_item(
        Key={'id': params['userId']}
    )
    # wallet = wallet_table.scan(
    #     ScanFilter={
    #         'userId': {
    #             'AttributeValueList': [
    #                 params['userId']
    #             ],
    #             'ComparisonOperator': 'EQ'
    #         }
    #     }
    # ).get('Items').pop()
    # payment_history = history_table.query(
    #     KeyConditionExpression=Key('userId').eq(params['userId'])
    # )
    # sum_charge = 0
    # sum_payment = 0
    # times_per_location = {}
    # for item in payment_history['Items']:
    #     sum_charge += item.get('chargeAmount', 0)
    #     sum_payment += item.get('useAmount', 0)
    #     location_name = _get_location_name(item['locationId'])
    #     if location_name not in times_per_location:
    #         times_per_location[location_name] = 1
    #     else:.;.;.;.uhn
    #         times_per_location[location_name] += 1
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'userName': user['Item']['name'],
            'currentAmount': user['Item']['amount'],
            'totalChargeAmount': user['Item']['totalChargeAmount'],
            'totalUseAmount': user['Item']['totalUseAmount'],
            'timesPerLocation': user['Item']['timesPerLocation']
        })
    }


def get_payment_history(event, context):
    # wallet_table = boto3.resource('dynamodb').Table(os.environ['WALLET_TABLE'])
    history_table = boto3.resource('dynamodb').Table(os.environ['PAYMENT_HISTORY_TABLE'])
    params = event['pathParameters']
    # wallet = wallet_table.scan(
    #     ScanFilter={
    #         'userId': {
    #             'AttributeValueList': [
    #                 params['userId']
    #             ],
    #             'ComparisonOperator': 'EQ'
    #         }
    #     }
    # ).get('Items').pop()
    payment_history_result = history_table.query(
        KeyConditionExpression=Key('userId').eq(params['userId'])
    )
    

    payment_history = []
    for p in payment_history_result['Items']:
        if 'chargeAmount' in p:
            p['chargeAmount'] = int(p['chargeAmount'])
        if 'useAmount' in p:
            p['useAmount'] = int(p['useAmount'])
        p['locationName'] = _get_location_name(p['locationId'])
        del p['locationId']
        payment_history.append(p)

    sorted_payment_history = list(sorted(
        payment_history,
        key=lambda x:x['timestamp'],
        reverse=True))

    return {
        'statusCode': 200,
        'body': json.dumps(sorted_payment_history)
    }


def _get_location_name(location_id):
    locations = requests.get(os.environ['LOCATION_ENDPOINT']).json()
    return locations[str(location_id)]


def summary_user_wallet(event, context):
    
    user_table = boto3.resource('dynamodb').Table(os.environ['USER_TABLE'])
    history_table = boto3.resource('dynamodb').Table(os.environ['PAYMENT_HISTORY_TABLE'])

    userId = event['Records'][0]['dynamodb']['NewImage']["S"]

    payment_history = history_table.query(
        KeyConditionExpression=Key('userId').eq(userId)
    )

    total_amount = 0
    sum_charge = 0
    sum_payment = 0
    times_per_location = {}
    for item in payment_history['Items']:
        sum_charge += item.get('chargeAmount', 0)
        sum_payment += item.get('useAmount', 0)
        location_name = _get_location_name(item['locationId'])
        if location_name not in times_per_location:
            times_per_location[location_name] = 1
        else:
            times_per_location[location_name] += 1

    user_table.update_item(
        Key={
            'userId': userId
        },
        UpdateExpression="set amount = :amt, totalChargeAmount=:camt, totalUseAmount=:uamt, timesPerLocation=:tm",
        ExpressionAttributeValues={
            ':amt': total_amount,
            ':camt': sum_charge,
            ':uamt': sum_payment,
            ':tm': times_per_location
        }
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps({'result': 'ok'})
    }
