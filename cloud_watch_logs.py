import boto3
import json
import os
#Written Helpers to navigate the cloud watch
from helping_class.CloudWatchHelper import CloudWatch_Helper

#create a bedrock client
bedrock = boto3.client('bedrock', region_name='us-east-1')

#Create Cloudwatch object
cloudwatch = CloudWatch_Helper()

log_group_name = "bedrock-logs"

#Create a log group
cloudwatch.create_log_group(log_group_name)

#Creating a logging config
loggingConfig = {
    'cloudWatchConfig': {
        'logGroupName':log_group_name,
        'roleArn':'arn:aws:iam::228947353622:role/bedrock-logs-aws-iam-raghulg',
        'largeDataDeliveryS3Config': {
            'bucketName':"bedrock-logs-sample",
            'keyPrefix':"amazon_bedrock_large_data_delivery",
        }
    },
    's3Config': {
        'bucketName':"bedrock-logs-sample",
        'keyPrefix':"amazon_bedrock_logs",
    },
    'textDataDeliveryEnabled': True
}

#Put the model logs
bedrock.put_model_invocation_logging_configuration(loggingConfig = loggingConfig)

print(bedrock.get_model_invocation_logging_configuration())

#Create a bedrock runtime client
bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')

#Create a Model
prompt = "Write an article about Mahendra Singh Dhoni, formerly known as MSD."

kwargs = {
  "modelId": "amazon.titan-text-express-v1",
  "contentType": "application/json",
  "accept": "application/json",
  "body": json.dumps(
      {
          "inputText":prompt,
          "textGenerationConfig":
          {
              "maxTokenCount":4096,
              "stopSequences":["User:"],
              "temperature":0.8,
              "topP":0.9
              }
              }
  )
}

response = bedrock_runtime.invoke_model(**kwargs)
response_body = json.loads(response['body'].read())

generated_text = response_body['results'][0]['outputText']
print(generated_text)

#print cloud watch recent logs
print(cloudwatch.print_recent_logs(log_group_name))