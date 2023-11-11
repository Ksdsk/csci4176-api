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
        email = event['email']
        password = event['password']
        
        # Retrieve user data from DynamoDB based on email
        user_data = get_user_by_email(email)
        
        if user_data:
            # Verify the provided password against the stored hashed password
            if verify_password(password, user_data['hash_password']['S']):
                response = {
                    'statusCode': 200,
                    'body': json.dumps({'message': 'Login successful', 'id': user_data['id']['S']})
                }
            else:
                response = {
                    'statusCode': 401,
                    'body': json.dumps({'message': 'Invalid password'})
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

def get_user_by_email(email):
    # Retrieve user data from DynamoDB based on email
    response = dynamodb.scan(
        TableName=table_name,
        FilterExpression='email = :email',
        ExpressionAttributeValues={':email': {'S': email}}
    )
    
    items = response.get('Items', [])
    
    if items:
        return items[0]
    else:
        return None

def verify_password(plain_password, hashed_password):
    # Verify the password using bcrypt
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
