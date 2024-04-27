import boto3
import json
import os
import datetime
from botocore.exceptions import ClientError

class CloudWatch_Helper:

    def __init__(self):

        #Create a Boto3 client for CloudWatch logs service
        self.cloudwatch_logs_client = boto3.client('logs', region_name='us-east-1')

    def create_log_group(self, log_group_name):

        #Create a log group
        try:
            response = self.cloudwatch_logs_client.create_log_group(
                logGroupName=log_group_name
            )
            print(f"{log_group_name} has been created successfully")
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceAlreadyExistsException':
                print(f"{log_group_name} already exists")
            else:
                print(f"Error creating {log_group_name}: {e}")

    def print_recent_logs(self, log_group_name, minutes = 5):

        try:
            endtime = int(datetime.datetime.now().timestamp()*1000) #current time in milliseconda
            starttime = endtime - (minutes*60*1000) # 5 minutes in milliseconds

            #Fetch Log streams (Assumes logs are stored in streams within the log group)
            streams = self.cloudwatch_logs_client.describe_log_streams(
                logGroupName=log_group_name,
                orderBy='LastEventTime',
                descending=True
            )

            for stream in streams.get('logStreams', []):
                events = self.cloudwatch_logs_client.get_log_events(
                    logGroupName=log_group_name,
                    logStreamName=stream['logStreamName'],
                    startTime=starttime,
                    endTime=endtime
                )
            
            for event in events.get('events', []):
                try:
                    json_data = json.loads(event['message'])
                    print(json.dumps(json_data, indent=4))
                except json.JSONDecodeError:
                    print(event['message'])
                print("="*100)

        except ClientError as e:
            print(f"Error fetching logs: {e}")