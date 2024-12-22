import json
import boto3
import csv
from io import StringIO
from datetime import datetime
import logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Metadata')

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        
        try:
            # Get the CSV file from S3
            response = s3.get_object(Bucket=bucket, Key=key)
            csv_content = response['Body'].read().decode('utf-8')
            
            # Process the CSV file
            csv_reader = csv.reader(StringIO(csv_content))
            headers = next(csv_reader)
            row_count = sum(1 for _ in csv_reader)
            column_count = len(headers)
            
            # Prepare metadata
            metadata = {
                'filename': key,
                'upload_timestamp': datetime.now().isoformat(),
                'file_size_bytes': response['ContentLength'],
                'row_count': row_count,
                'column_count': column_count,
                'column_names': headers
            }
            
            # Store metadata in DynamoDB
            table.put_item(Item=metadata)
            logger.info(f'Metadata stored successfully for {key}')
            
            return {
                'statusCode': 200,
                'body': json.dumps('Metadata stored successfully!')
            }
        
        except Exception as e:
            logger.error(f'Error processing file {key} from bucket {bucket}: {str(e)}')
            return {
                'statusCode': 500,
                'body': json.dumps(f'Error processing file: {str(e)}')
            }