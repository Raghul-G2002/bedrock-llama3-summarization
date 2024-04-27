from summarize_audio_file import summarize_audio_file
from transcribe_audio_file import create_s3_bucket, create_transcribe_client

def main():
    bucket_name = create_s3_bucket("msdhonitranscribe")
    create_transcribe_client(bucket_name=bucket_name, file="audio.mp3")
    summarized_text = summarize_audio_file()
    print(summarized_text)

if __name__ == "__main__":
    main()