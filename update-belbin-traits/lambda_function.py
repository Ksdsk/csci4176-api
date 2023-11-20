import json
import boto3
import uuid

# Initialize the DynamoDB client
dynamodb = boto3.client('dynamodb')

# Define the name of your DynamoDB table
table_name = 'user_table'

def lambda_handler(event, context):
    try:
        # Extract user data
        points = {}
        points["Resource Investigator"] = event["belbin_traits"]["resource_investigator"]
        points["Teamworker"] = event["belbin_traits"]["teamworker"]
        points["Co-ordinator"] = event["belbin_traits"]["coordinator"]
        points["Plant"] = event["belbin_traits"]["plant"]
        points["Monitor Evaluator"] = event["belbin_traits"]["monitor_evaluator"]
        points["Specialist"] = event["belbin_traits"]["specialist"]
        points["Shaper"] = event["belbin_traits"]["shaper"]
        points["Implementer"] = event["belbin_traits"]["implementer"]
        points["Completer Finisher"] = event["belbin_traits"]["completer_finisher"]
        
        user_id = event["user_id"]

        if not user_exists(user_id):
            raise Exception("User Does Not Exist")
        
        # Create an item to put into DynamoDB
        points = {
            ':ri': {'N': event["belbin_traits"]["resource_investigator"]},
            ':tm': {'N': event["belbin_traits"]["teamworker"]},
            ':co': {'N': event["belbin_traits"]["coordinator"]},
            ':pt': {'N': event["belbin_traits"]["plant"]},
            ':me': {'N': event["belbin_traits"]["monitor_evaluator"]},
            ':sp': {'N': event["belbin_traits"]["specialist"]},
            ':sh': {'N': event["belbin_traits"]["shaper"]},
            ':im': {'N': event["belbin_traits"]["implementer"]},
            ':cf': {'N': event["belbin_traits"]["completer_finisher"]},
        }

        query = "SET ri = :ri, tm = :tm, co = :co, pt = :pt, me = :me, sp = :sp, sh = :sh, im = :im, cf = :cf"
        
        # Update the item in DynamoDB
        dynamodb.update_item(TableName=table_name, 
                             Key={id: user_id}, 
                             UpdateExpression=query,
                             ExpressionAttributeValues=points
                             )
        
        # Return a successful response
        response = {
            'status': 200,
            'body': json.dumps({'message': 'User added successfully', 'id': user_id})
        }
    except Exception as e:
        # Handle specific errors and return an error response
        error_message = str(e)
        response = {
            'status': 500,
            'body': json.dumps({'error': error_message})
        }
    
    return response

def user_exists(email):
    # Check if a user with the same email already exists
    response = dynamodb.scan(
        TableName=table_name,
        FilterExpression='email = :email',
        ExpressionAttributeValues={':email': {'S': email}}
    )
    
    return len(response.get('Items', [])) > 0
