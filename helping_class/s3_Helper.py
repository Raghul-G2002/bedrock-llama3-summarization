import boto3
import json
import os

class s3_Helper:
    
    def __init__(self):

        #Get the account id being used
        sts_client = boto3.client('sts')
        response = sts_client.get_caller_identity()
        account_id = response['Account']

        #Create a Boto3 client for S3 Service
        self.s3_client = boto3.client('s3', region_name='us-east-1')
    
    def list_objects(self, bucket_name):
        try:
            response = self.s3_client.list_objects_v2(Bucket = bucket_name)
            
            #Check if the bucket has any objects
            if 'Contents' in response:
                for obj in response['Contents']:
                    key = obj['Key']
                    creation_time = obj['LastModified']
                    print(f"Object: {key} created at {creation_time}")
            else:
                print(f"Bucket {bucket_name} is empty")
        except Exception as e:
            print(f"Error: {e}")
    
    def upload_file(self, bucket_name, file_name):
        try:
            self.s3_client.upload_file(file_name, bucket_name, file_name)
            print(f"File {file_name} uploaded to bucket {bucket_name}")
        except Exception as e:
            print(f"Error: {e}")
    
    def download_object(self, bucket_name, object_name):
        try:
            self.s3_client.download_file(bucket_name, object_name, object_name)
            print(f"Object {object_name} downloaded from bucket {bucket_name}")
        except Exception as e:
            print(f"Error: {e}")