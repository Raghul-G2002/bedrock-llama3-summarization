import boto3
import os

from helping_class.Lambda_Helper import Lambda_Helper
from helping_class.s3_Helper import S3_Helper
import time

def main():
    lambda_helper = Lambda_Helper()
    s3_helper = S3_Helper()
    
    bucket_name_text = "transcribe-event-1"
    #First part of the Architecture

    #Environment Variables for the lambda function
    lambda_helper.lambda_environ_variables = {'S3BUCKETNAMETEXT':bucket_name_text}
    lambda_helper.deploy_function(["lambda_code/object_transcript.py"], function_name = "Lambda_Transcribe")


    #Trigger the Lambda Function
    lambda_helper.filter_rules_suffix = ".mp3"
    lambda_helper.add_lambda_trigger(bucket_name_text, function_name="Lambda_Transcribe")

    #Upload the file to S3 Bucket
    s3_helper.upload_file(bucket_name_text, "audio.mp3")
    time.sleep(10)

    s3_helper.list_objects(bucket_name_text)

    #Download the Summary Object from the S3 Bucket
    s3_helper.download_object(bucket_name_text, "results.json")
    #Second part of the Architecture // To more simplify
    # bucket_name_text = "transcribe-event-1"

    # #Let's deploy the lambda function
    # lambda_helper.deploy_function(["lambda_code/transcript_summary.py"], function_name = "Lambda_Summarize")

    # #Let's trigger the Lambda Function
    # lambda_helper.filter_rules_suffix = ".json"
    # lambda_helper.add_lambda_trigger(bucket_name_text)

    # #Let's upload the transcript file to S3 Bucket to invoke the Lambda Function
    # s3_helper.upload_file(bucket_name_text, "transcript.json")

    # time.sleep(10)

    # #Let's list the objects available in the S3 Bucket
    # s3_helper.list_objects(bucket_name_text)

    # #Let's download the summary file from the S3 Bucket
    # s3_helper.download_object(bucket_name_text, "results.json")

if __name__ == "__main__":
    main()
