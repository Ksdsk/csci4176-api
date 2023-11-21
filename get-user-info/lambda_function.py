import json
import boto3
import bcrypt

# Initialize the DynamoDB client
dynamodb = boto3.client('dynamodb')

# Define the name of your DynamoDB table
table_name = 'user_table'

def lambda_handler(event, context):
    try:
        # Extract user login data
        user_id = event['user_id']

        # Retrieve user data from DynamoDB based on email
        user_data = get_user(user_id)
        
        if user_data:
            body = {
                'message': 'Success', 
                'id': user_data['id']['S'],
                'email': user_data['email']['S']
            }

            # Belbin
            if user_data['belbin_traits']:
                body["belbin_traits"]["teamworker"] = user_data['belbin_traits']["teamworker"]['N']
                body["belbin_traits"]["resource_investigator"] = user_data['belbin_traits']["resource_investigator"]['N']
                body["belbin_traits"]["implementer"] = user_data['belbin_traits']["implementer"]['N']
                body["belbin_traits"]["completer_finisher"] = user_data['belbin_traits']["completer_finisher"]['N']
                body["belbin_traits"]["monitor_evaluator"] = user_data['belbin_traits']["monitor_evaluator"]['N']
                body["belbin_traits"]["shaper"] = user_data['belbin_traits']["shaper"]['N']
                body["belbin_traits"]["specialist"] = user_data['belbin_traits']["specialist"]['N']
                body["belbin_traits"]["coordinator"] = user_data['belbin_traits']["coordinator"]['N']
                body["belbin_traits"]["plant"] = user_data['belbin_traits']["plant"]['N']

            # Phone
            if user_data['phone_number']:
                body["phone_number"] = user_data["phone_number"]
            
            response = {
                'statusCode': 200,
                'body': json.dumps({'message': 'Success', "info" :body})
            }

        else:
            response = {
                'statusCode': 404,
                'body': json.dumps({'message': 'User not found'})
            }

    except Exception as e:
        # Handle any errors and return an error response
        response = {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
    
    return response

def get_user(user_id):
    # Retrieve user data from DynamoDB based on email
    response = dynamodb.scan(
        TableName=table_name,
        FilterExpression='id = :id',
        ExpressionAttributeValues={':id': {'S': user_id}}
    )
    
    items = response.get('Items', [])
    
    if items:
        return items[0]
    else:
        return None