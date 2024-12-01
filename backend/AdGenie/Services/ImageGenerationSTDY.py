import boto3
import json
import base64
import io
import os
from dotenv import load_dotenv


load_dotenv()

AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")

# S3 Configuration
AWS_ACCESS_KEY_ID_PERSONAL = os.getenv("AWS_ACCESS_KEY_ID_PERSONAL")
AWS_SECRET_ACCESS_KEY_PERSONAL = (os.getenv("AWS_SECRET_ACCESS_KEY_PERSONAL"),)
AWS_DEFAULT_REGION_PERSONAL = os.getenv("AWS_DEFAULT_REGION_PERSONAL")

# Create a Bedrock Runtime client in the AWS Region of your choice.
bedrock = boto3.client(
    "bedrock-runtime",
    region_name=AWS_DEFAULT_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    aws_session_token=AWS_SESSION_TOKEN,
)


def generateImageAndSaveInS3(prompt, filename, foldername, aspect_ratio):
    response = bedrock.invoke_model(
        modelId="stability.stable-image-ultra-v1:0",
        body=json.dumps({"prompt": prompt, "aspect_ratio": aspect_ratio, "seed": 0}),
    )
    output_body = json.loads(response["body"].read().decode("utf-8"))
    base64_output_image = output_body["images"][0]
    image_data = base64.b64decode(base64_output_image)
    image = io.BytesIO(image_data)
    # image.save("image.png")

    # Initialize the S3 client with the provided credentials
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID_PERSONAL,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY_PERSONAL,
        # aws_session_token=AWS_SESSION_TOKEN,  # Only if using temporary credentials
        region_name=AWS_DEFAULT_REGION_PERSONAL,
    )

    # S3 bucket and file details
    bucket_name = "ads-campaign-generated-image"
    s3_object_key = (
        f"{foldername}/{filename}"  # The S3 key where the image will be stored
    )

    # Convert the image data to a file-like object using BytesIO
    image_data_io = io.BytesIO(image_data)

    # Upload the image to S3
    try:
        response = s3_client.upload_fileobj(
            image_data_io,
            bucket_name,
            s3_object_key,
            ExtraArgs={"ContentType": "image/jpeg"},
        )
        print(f"Image uploaded successfully to {bucket_name}/{s3_object_key}")
        return True
    except Exception as e:
        print(f"Error uploading image: {e}")
        return e


prompt = "Create an ad for GreenEarth Co. featuring an eco-friendly green reusable bag with natural elements like leaves and water drops. Use a minimal background with green, beige, and earthy tones. Add the text 'Save the Planet, One Bag at a Time!' in Lora font or a similar serif style, with handwritten accents. Blend urban and nature visuals for a modern, sustainable lifestyle. Appeal to young professionals and families. Include the GreenEarth Co. logo as a subtle watermark. Keep it clean and creative."
