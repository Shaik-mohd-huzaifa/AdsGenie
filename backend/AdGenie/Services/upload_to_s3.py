import boto3
import os
from dotenv import load_dotenv


load_dotenv()

# AWS credentials (replace with your actual credentials)
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")

# Initialize the S3 client with the provided credentials
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    aws_session_token=AWS_SESSION_TOKEN,  # Only if using temporary credentials
    region_name=AWS_DEFAULT_REGION,
)

# S3 bucket and file details
bucket_name = os.getenv("BUCKET_NAME")
file_path = os.getenv("FILE_PATH")
s3_object_key = os.getenv("S3_OBJECT_KEY")

# Upload the file to the S3 bucket
try:
    s3_client.upload_file(file_path, bucket_name, s3_object_key)
    print(
        f"File '{file_path}' uploaded successfully to '{bucket_name}/{s3_object_key}'"
    )
except Exception as e:
    print(f"Error uploading file: {e}")
