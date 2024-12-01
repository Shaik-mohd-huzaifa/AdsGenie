import base64
import boto3
import json
import os
import random
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

AWS_DEFAULT_REGION=os.getenv("AWS_DEFAULT_REGION")
AWS_ACCESS_KEY_ID=os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY=os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_SESSION_TOKEN=os.getenv("AWS_SESSION_TOKEN")

# Create a Bedrock Runtime client in the AWS Region of your choice.
client = boto3.client("bedrock-runtime", region_name=AWS_DEFAULT_REGION, aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, aws_session_token=AWS_SESSION_TOKEN)        

# Set the model ID, e.g., Titan Image Generator G1.
model_id = "amazon.titan-image-generator-v1"
# model_id = "amazon.titan-image-generator-v1"

def generateImageAndSaveToS3(model_id,height, width, filename, foldername):
    prompt = "A car made out of Ballons"

    # Generate a random seed.
    seed = random.randint(0, 2147483647)

    # Format the request payload using the model's native structure.
    native_request = {
        "taskType": "TEXT_IMAGE",
        "textToImageParams": {"text": prompt},
        "imageGenerationConfig": {
            "numberOfImages": 1,
            "quality": "standard",
            "cfgScale": 8.0,
            "height": height,
            "width": width,
            "seed": seed,
        },
    }

    # Convert the native request to JSON.
    request = json.dumps(native_request)

    # Invoke the model with the request.
    response = client.invoke_model(modelId=model_id, body=request)

    # Decode the response body.
    model_response = json.loads(response["body"].read())

    # Extract the image data.
    base64_image_data = model_response["images"][0]

    # Save the generated image to a local folder.
    i, output_dir = 1, "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Check for existing files to avoid overwriting.
    while os.path.exists(os.path.join(output_dir, f"titan_{i}.png")):
        i += 1

    # Decode base64 image data
    image_data = base64.b64decode(base64_image_data)

    # Save to local file system
    image_path = os.path.join(output_dir, f"titan_{i}.png")
    with open(image_path, "wb") as file:
        file.write(image_data)

    # Initialize the S3 client with the provided credentials
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        aws_session_token=AWS_SESSION_TOKEN,  # Only if using temporary credentials
        region_name=AWS_DEFAULT_REGION
    )
    
    # S3 bucket and file details
    bucket_name = 'ads-campaign-generated-images'
    s3_object_key = f'{foldername}/{filename}.png'  # The S3 key where the image will be stored

    # Convert the image data to a file-like object using BytesIO
    image_data_io = BytesIO(image_data)

    # Upload the image to S3
    try:
        response = s3_client.upload_fileobj(image_data_io, bucket_name, s3_object_key, ExtraArgs={'ContentType': 'image/png'})
        print(f"Image uploaded successfully to {bucket_name}/{s3_object_key}")
        print(response)
    except Exception as e:
        print(f"Error uploading image: {e}")

generateImageAndSaveToS3(model_id, 512, 512, "512X512", "actorImages")