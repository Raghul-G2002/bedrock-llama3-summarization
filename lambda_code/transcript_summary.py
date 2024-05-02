import boto3
import json


s3_client = boto3.client('s3', region_name='us-east-1')
bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')

def lambda_handler(event, context):

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # #A Normal Check
    # if "-transcript.json" not in key:
    #     return "Not a Transcript File"
    
    try:
        file_content = ""
        response = s3_client.get_object(Bucket=bucket, Key=key)
        file_content = response['Body'].read().decode('utf-8')

        #Read the transcript file in the particular format
        transcript = extract_transcript(file_content)

        print(f"Transcript: {transcript}")

        #Call the bedrock api to summarize the transcript
        summary = bedrock_llama3_summarization(transcript)

        #Push the summary into the Same S3 Bucket
        s3_client.put_object(Body=json.dumps(summary), Bucket=bucket, Key='results.json', ContentType = 'text/plain')

    except Exception as e:
        print(e)
        return {
            'statusCode':200,
            'body':json.dumps("Error Occured")
        }
    
    return {
        'statusCode':200,
        'body':json.dumps("Success")
    }



#Read the transcript file from S3 and changes that into a particular format
def extract_transcript(file_content):

    file_content = json.loads(file_content)

    output_text = ""
    current_speaker = ""

    items = file_content['results']['items']

    for item in items:
        speaker_label = item['speaker_label']
        content = item['alternatives'][0]['content']

        if speaker_label is not None and speaker_label != current_speaker:
            current_speaker = speaker_label
            if speaker_label == "spk_0":
                output_text += "\n Dhoni: "
            else:
                output_text += "\n Mandira Bedi: "
        
        output_text += content + " "
    return output_text


def bedrock_llama3_summarization(transcript):

    #Call the bedrock api to summarize the transcript
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