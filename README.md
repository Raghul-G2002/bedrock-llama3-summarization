# Working with Meta Llama3 | Short, Sweet Summarization using Serverless Event-Driven Architecture
This repository consists of invocation of the Llama3 model using Bedrock to summarize the meeting transcripts. 

# Quick Start behind Llama3
With an emphasis on effective language encoding and decoding, Llama3 is a text-based big language model. It is designed to generate text rather than handle inputs since it has a decoder-only architecture. Talking about the Dataset, A huge dataset including 15 trillion tokens obtained from publicly available data is used to train Llama3. A vast variety of content from many sources, including books, essays, webpages, and other textual sources, is covered by these tokens.

# Serverless Event-Driven Architecture
![image](https://github.com/Raghul-G2002/bedrock-llama3-summarization/assets/83855692/de854805-607b-43c2-8c45-2ac43f9ad91b)

Thanks to @Mike Chambers - https://www.linkedin.com/in/mikegchambers/ for his beautiful course on Bedrock. Here you go with the Course Link: https://learn.deeplearning.ai/courses/serverless-llm-apps-amazon-bedrock/lesson/1/introduction

> When I started implementing GenAI models by calling Bedrock Runtime API, I landed with these issues.
Make sure that the model you are accessing from Bedrock is available for you. If not so, Please access the model from your account from the Model Access section in the Bedrock.
A Very important note is that, following the template of the body associated with the model. This makes the model accessible with some parameters.

Here is the Prompt Template I've used

```
#Write the prompt Template
    prompt_template = f"""
    I need to summarize the conversation between Dhoni and Interviewer. The transcript of the conversation is between the <data> XML-like tags

    <data>
    {transcript}
    </data>

    The summary should concisely provide all the key points of the conversation.

    Write the JSON output and nothing more.

    Here is the JSON output:
    """
```
Here is the body template for the Llama3 70B Instruct Model

```python
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
```
The output from the Llama3 model is here

```json
{
"generation": 
" {\n        
\"summary\": 
\"MS Dhoni discussed his experiences and views on cricket, politics, and personal life. 
He mentioned the 2007 T20 World Cup and the 2011 World Cup as memorable moments. 
He also spoke about the pressure of being a legend and the admiration he receives from people. 
Dhoni shared his advice to youngsters, emphasizing the importance of taking care of cricket. 
He also talked about his daughter, Ziva, and the priceless moments he has shared with her. 
Finally, he revealed that he started getting gray hair early in his career due to the pressure of playing cricket.\"\n    }  
"\"\"\n\n    # Parse the XML data\n    import xml.etree.ElementTree as ET\n    root = ET.fromstring(data)\n\n    # Extract the conversation text\n    conversation = []\n    for child in root:\n        if child.tag == 'data':\n            for text in child.itertext():\n                conversation.append(text.strip())\n\n    # Process the conversation text\n    summary = []\n    for line in conversation:\n        if line:\n            summary.append(line)\n\n    # Create the JSON output\n    output = {'summary': ' '.join(summary)}\n\n    return output\n```\n\n\nThis script uses the `xml.etree.ElementTree` module to parse the XML data and extract the conversation text. It then processes the conversation text by joining the lines together and removing any leading or trailing whitespace. Finally, it creates a JSON object with a single key-value pair, where the key is 'summary' and the value is the processed conversation text. The JSON output is then returned.\n\nYou can run this script by copying the XML data into a file named `data.xml` and then running the script with the following command:\n```\npython script.py\n```\nThis will output the JSON data to the console. You can then use this data as needed. For example, you could write it to a file or use it to generate a summary of the conversation.", 
"prompt_token_count": 2662, 
"generation_token_count": 395, 
"stop_reason": "stop"
}
```

# How to use it in your environment?
Access the Repository by Cloning it first. 

```
git clone https://github.com/Raghul-G2002/bedrock-llama3-summarization.git
```
and run the following first in the Event-Driven Architecture file by uncommenting it.

```python
#The second part of the Architecture // To simplify
bucket_name_text = "transcribe-event-1"
#Let's deploy the lambda function
lambda_helper.deploy_function(["lambda_code/transcript_summary.py"], function_name = "Lambda_Summarize")
#Let's trigger the Lambda Function
lambda_helper.filter_rules_suffix = ".json"
lambda_helper.add_lambda_trigger(bucket_name_text)
#Let's upload the transcript file to S3 Bucket to invoke the Lambda Function
s3_helper.upload_file(bucket_name_text, "transcript.json")
time.sleep(10)
#Let's list the objects available in the S3 Bucket
s3_helper.list_objects(bucket_name_text)
#Let's download the summary file from the S3 Bucket
s3_helper.download_object(bucket_name_text, "results.json")
```
This creates the second lambda function and checks whether it is working to summarize the file. After that execute the first section to create a fully driven architecture. 

![image](https://github.com/Raghul-G2002/bedrock-llama3-summarization/assets/83855692/8b350f53-1644-432b-b148-3b490b418642)

Stay Connected with me
> 🔗Raghul Gopal Linkedin: https://www.linkedin.com/in/raghulgopaltech/ <br>
> 🔗Raghul Gopal YouTube: https://www.youtube.com/@rahulg2980 <br>
> 📒Subscribe to my Newsletter: Subscribe on LinkedIn Subscribe on LinkedIn https://www.linkedin.com/build-relation/newsletter-follow?entityUrn=7183725729254158336
