import json
from HelloBlazePreprocessLambda import preprocess

def lambda_handler(event, context):
    preprocess(event['s3-dataset-uri'])
    return {
        'statusCode': 200,
        'body': json.dumps("PREPROCESS SUCCESSFULLY!")
    }