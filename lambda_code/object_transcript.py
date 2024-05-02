import json
import boto3
import uuid
import os

#Create a S3 Client
s3_client = boto3.client('s3', region_name='us-east-1')

#Create a Transcribe Client
transcribe_client = boto3.client('transcribe', region_name='us-east-1')

def lambda_handler(event, context):
    #Get the Bucket name and key from the event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    try:
        job_name = "transcribe_job_" + str(uuid.uuid4())
        job_uri = "s3://" + bucket_name + "/" + key
        transcribe_client.start_transcription_job(
        TranscriptionJobName = job_name,
        Media = {
            'MediaFileUri': job_uri
        },
        MediaFormat = 'mp3',
        LanguageCode = 'en-US',
        OutputBucketName = bucket_name,
        Settings = {
            'ShowSpeakerLabels':True,
            'MaxSpeakerLabels':2
        }
        )
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }
    return {
        'statusCode':200,
        'body':json.dumps("Success")
    }
        
        


