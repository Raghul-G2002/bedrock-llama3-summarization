import boto3
import os
import json

def summarize_audio_file():
    #Create bedrock runtime client
    bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')
    with open('transcribe.txt', "r") as f:
        transcript = f.read()

    #Write the prompt Template
    prompt_template = f"""
    I need to summarize the conversation between Dhoni and Interviewer. The transcript of the conversation is between the <data> XML like tags

    <data>
    {transcript}
    </data>

    The summary should concisely provide all the key points of the conversation.

    Write the JSON output and nothing more.

    Here is the JSON output:
    """

    #kwargs for the Llama3 70B instruct model
    kwargs = {
        "modelId": "meta.llama3-8b-instruct-v1:0",
        "contentType": "application/json",
        "accept": "application/json",
        "body": json.dumps(
            {
                "prompt":prompt_template,
                "max_gen_len":512,
                "temperature":0.5,
                "top_p":0.9
                }
        )
    }

    #let's call the model to get the response
    response = bedrock_runtime.invoke_model(**kwargs)

    response_body = json.loads(response['body'].read())
    # summary = response_body['generation'][0]['summary']

    return response_body
# print(summarize_audio_file())