import boto3
import zipfile
import json
import os
import time

class Lambda_Helper:

    def __init__(self):
        
        # Get the account ID being used
        sts_client = boto3.client('sts')
        response = sts_client.get_caller_identity()
        account_id = response['Account']

        #Create a boto3 client for the Lambda Service
        self.lambda_client = boto3.client('lambda', region_name='us-east-1')
        self.function_name = 'summarizer'
        self.role_arn = f"arn:aws:iam::{account_id}:role/lambda_role"
        self.function_description = 'Summarizer Lambda Function'
        self.lambda_arn = ""
        self.lambda_environ_variables = {}
        self.filter_rules_suffix = ""

        #Create a boto3 client for the S3 Service (More specifically for this use case)
        self.s3_client = boto3.client('s3', region_name='us-east-1')
    
    def deploy_function(self, code_file_names, function_name = "", module_name = "lambda_function"):

        if function_name:
            self.function_name = function_name
        else:
            print(f"Using function name: {self.function_name}")
        
        #Create a zip file with the code file
        print("Creating zip file")
        zip_file_path = "lambda_function.zip"

        with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
            for code_file_name in code_file_names:
                zip_file.write(code_file_name, arcname=code_file_name)
        
        try:
            print('Looking for existing function ...')
            self.lambda_client.get_function(FunctionName=self.function_name)

            #If the function exists, update its code
            print('Updating function ...')
            response = self.lambda_client.update_function_code(
                FunctionName=self.function_name,
                ZipFile=open(zip_file_path, 'rb').read(),
                Publish=True
            )

            print(f"Function updated: {response} Code Updated:{response['LastModified']}")
            self.lambda_arn = response['FunctionArn']
            print("Done")

        except self.lambda_client.exceptions.ResourceNotFoundException:
            #If the function doesn't exist, create it
            print('Creating function ...')
            response = self.lambda_client.create_function(
                FunctionName = self.function_name,
                Handler = f"{module_name}.lambda_handler",
                Role = self.role_arn,
                Runtime = 'python3.11',
                Role = self.role_arn,
                Description = self.function_description,
                Timeout = 120,
                Code = {
                    'Zipfile':open(zip_file_path, 'rb').read()
                },
                Environment = {"Variables":self.lambda_environ_variables}
            )

            print(f"Function created: {response}")
            self.lambda_arn = response['FunctionArn']
            print("Done")
    
    def add_lambda_trigger(self, bucket_name, function_name = ""):

        if function_name:
            self.function_name = function_name
        else:
            print(f"Using function name: {self.function_name}")
        
        try:
            policy = self.lambda_client.get_policy(FunctionName=self.function_name)['Policy']
            policy = json.loads(policy)

            for statement in policy['Statement']:
                if statement['Action'] == 'lambda:InvokeFunction' and self.lambda_arn in statement['Resource']:
                    print("Lambda trigger already exists")
                    self.lambda_client.remove_permission(
                        FunctionName=self.function_name,
                        StatementId=statement['Sid']
                    )

                    print(f"Removed existing permission: {statement['Sid']}")
        except self.lambda_client.exceptions.ResourceNotFoundException:
            print("Function not found")
        
        except Exception as e:
            print(f"Error: {e}")
            return
        
        #Granting the access to the bucket to invoke the lambda function
        try:
            print("Granting access to the bucket to invoke the lambda function")
            response = self.lambda_client.add_permission(
                FunctionName = self.function_name,
                Action = 'lambda:InvokeFunction',
                Principal = 's3.amazonaws.com',
                statementId = 's3-trigger-permission',
                SourceArn = f"arn:aws:s3:::{bucket_name}"
            )
            print_out = json.dumps(json.loads(response['Statement']), indent=4)
            print(f"Permission added with Statement:{print_out}")
        
        except Exception as e:
            print(f"Error: {e}")
        
        #Add bucket notification (S3 Event Notification) to trigger the Lambda function
        lambda_arn = self.lambda_client.get_function(
            FunctionName = self.function_name
        )['Configuration']['FunctionArn']

        time.sleep(5)

        notification_configuration = {
            'LambdaFunctionConfigurations': [
                {
                    'LambdaFunctionArn': lambda_arn,
                    'Events': ['s3:ObjectCreated:*'],
                    'Filter': {
                        'Key': {
                            'FilterRules': [
                                {
                                    'Name': 'suffix',
                                    'Value': self.filter_rules_suffix
                                }
                            ]
                        }
                    }
                }
            ]
        }

        try:
            self.s3_client.put_bucket_notification_configuration(
                Bucket = bucket_name,
                NotificationConfiguration = notification_configuration
            )
            print(f"Bucket notification added to trigger the Lambda function")

        except Exception as e:
            print(f"Error: {e}")
