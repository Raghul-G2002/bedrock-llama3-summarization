import os
import boto3
import uuid
import json
import time

#create a s3 client
s3_client = boto3.client('s3', region_name = 'us-east-1')

#create a transcribe client
transcribe = boto3.client('transcribe', region_name = 'us-east-1')

def create_s3_bucket(bucket_name):
    #Create a S3 bucket
    s3_client.create_bucket(Bucket = bucket_name)

    #Upload a file to S3 bucket
    file = "audio.mp3"
    s3_client.upload_file(file, bucket_name, file)

    return bucket_name

def create_transcribe_client(bucket_name, file):
    job_name = "transcribe_job_" + str(uuid.uuid4())
    job_uri = "s3://" + bucket_name + "/" + file
    transcribe.start_transcription_job(
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

    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName = job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        time.sleep(2)

    if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        
        #Load the transcrribe
        transcribe_key = f"{job_name}.json"
        transcribe_obj = s3_client.get_object(Bucket = bucket_name, Key = transcribe_key)
        transcribe_text = transcribe_obj['Body'].read().decode('utf-8')
        transcribe_json = json.loads(transcribe_text)

        output_text = ""
        current_speaker = None

        items = transcribe_json['results']['items']

        for item in items:
            speaker_label = item.get('speaker_label', None)
            content = item['alternatives'][0]['content']

            if speaker_label is not None and speaker_label != current_speaker:
                current_speaker = speaker_label
                if speaker_label == "spk_0":
                    output_text += "\n Dhoni: "
                else:
                    output_text += "\n Mandira Bedi: "
            
            output_text += content + " "
        
        #Save the transcribe to a file
        with open('transcribe.txt', 'w') as f:
            f.write(output_text)

# bucket_name = create_s3_bucket("audiotranscribemsdhoni")
# create_transcribe_client(bucket_name, "audio.mp3")

    