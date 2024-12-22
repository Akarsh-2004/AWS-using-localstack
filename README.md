Overview

This project demonstrates a cloud-based system that processes CSV files, extracts metadata, and stores information using LocalStack for local development. The system mimics the functionality of AWS services and follows a complete workflow for file processing and data management.
----------------------------------------------------------------------------------------------------------
Technologies Used

AWS Lambda: For processing uploaded CSV files and handling SQS messages.

Amazon S3: To store uploaded CSV files.

Amazon DynamoDB: To store extracted metadata.

Amazon SQS: For decoupling file processing and database updates.

LocalStack: To emulate AWS services locally.

Python: For Lambda function logic.

Libraries: boto3, csv, logging, etc.
----------------------------------------------------------------------------------------------------------
Workflow Description

1. CSV File Upload

The user uploads a CSV file to an Amazon S3 bucket.

File upload is typically performed through a command-line interface or a script.

2. Trigger Lambda Function

The upload action triggers an S3 event (e.g., s3:ObjectCreated:).

The event activates an AWS Lambda function configured to process the uploaded file.

3. Metadata Extraction

The Lambda function retrieves the uploaded file from the S3 bucket.

It parses the file using a CSV reader and extracts the following metadata:

Filename

Upload timestamp

File size

Row count

Column count

Column names

4. Send Messages to SQS

The extracted metadata is structured as a message.

Messages are sent to an Amazon SQS queue for asynchronous processing.

5. Process Messages

A second AWS Lambda function polls the SQS queue for messages.

This function processes each message and updates the corresponding data in DynamoDB. Updates may involve:

Inserting new records.

Updating existing records.

6. Logging and Monitoring

All operations are logged in Amazon CloudWatch for monitoring and debugging.

Logs include information about Lambda executions, errors, and performance metrics.

Local Development Using LocalStack

LocalStack is used to simulate AWS services locally for testing and development. The following services are emulated:

S3

Lambda

DynamoDB

SQS
----------------------------------------------------------------------------------------------
Prerequisites

Docker: Ensure Docker is installed and running.

LocalStack: Install LocalStack (pip install localstack).

AWS CLI: Configure the AWS CLI for local use (aws configure).

Steps to Set Up

Start LocalStack:

localstack start

Create Required Resources:

Create an S3 bucket:

aws --endpoint-url=http://localhost:4566 s3 mb s3://csv-bucket

Create an SQS queue:

aws --endpoint-url=http://localhost:4566 sqs create-queue --queue-name csv-processing-queue

Create a DynamoDB table:

aws --endpoint-url=http://localhost:4566 dynamodb create-table \
  --table-name MetadataTable \
  --attribute-definitions AttributeName=Filename,AttributeType=S \
  --key-schema AttributeName=Filename,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST

Deploy Lambda Functions:

Package and deploy the Lambda functions using AWS CLI or SAM.

How to Run the System

Start LocalStack:

localstack start

Upload a CSV File:
Use the AWS CLI to upload a file:

aws --endpoint-url=http://localhost:4566 s3 cp sample.csv s3://csv-bucket

Monitor Processing:

Check SQS for messages.

Verify DynamoDB table entries for processed metadata.

View Logs:
Access CloudWatch logs for debugging and performance insights.
