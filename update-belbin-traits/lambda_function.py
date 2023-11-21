import json
import boto3

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
            raise Exception(f'User {user_id} Does Not Exist')
        
        # Create an item to put into DynamoDB
        points = {
            "ResourceInvestigator": event["belbin_traits"]["resource_investigator"],
            "Teamworker": event["belbin_traits"]["teamworker"],
            "Co-ordinator": event["belbin_traits"]["coordinator"],
            "Plant": event["belbin_traits"]["plant"],
            "MonitorEvaluator": event["belbin_traits"]["monitor_evaluator"],
            "Specialist": event["belbin_traits"]["specialist"],
            "Shaper": event["belbin_traits"]["shaper"],
            "Implementer": event["belbin_traits"]["implementer"],
            "CompleterFinisher": event["belbin_traits"]["completer_finisher"]
        }
        points_attribute_values = {f':{key}': {'N': str(value)} for key, value in points.items()}
        query = "SET belbin_traits = :belbin_traits"
        
        # Update the item in DynamoDB
        dynamodb.update_item(TableName=table_name, 
                             Key={'id': {'S': user_id}}, 
                             UpdateExpression=query,
                             ExpressionAttributeValues={':belbin_traits': {'M': points_attribute_values}}
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

def user_exists(user_id):
    # Check if a user with the same email already exists
    response = dynamodb.scan(
        TableName=table_name,
        FilterExpression='id = :id',
        ExpressionAttributeValues={':id': {'S': user_id}}
    )
    
    return len(response.get('Items', [])) > 0
