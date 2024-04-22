import os

# Set local path to your frontend build directory

import os
import boto3
from config import BUCKET_NAME, AWS_REGION, LOCAL_PATH
from botocore.exceptions import ClientError

def deploy_website_to_s3():
    # Create an S3 client
    s3 = boto3.client('s3', region_name=AWS_REGION)

    # Upload files to S3 bucket
    for root, dirs, files in os.walk(LOCAL_PATH):
        for file in files:
            local_file_path = os.path.join(root, file)
            s3_file_path = os.path.relpath(local_file_path, LOCAL_PATH)
            s3_file_path = os.path.normpath(s3_file_path)  # Normalize file path
            s3.upload_file(local_file_path, BUCKET_NAME, s3_file_path)

    print(f"Static website deployed successfully to S3 bucket '{BUCKET_NAME}'.")


def enable_static_website_hosting():
    try:
        # Create an S3 client
        s3 = boto3.client('s3')

        # Enable static website hosting
        s3.put_bucket_website(
            Bucket=BUCKET_NAME,
            WebsiteConfiguration={
                'IndexDocument': {'Suffix': 'index.html'}
                # Add 'ErrorDocument' configuration if needed
            }
        )

        # Set the correct Content-Type for each file
        for root, dirs, files in os.walk(LOCAL_PATH):
            for file in files:
                local_file_path = os.path.join(root, file)
                s3_file_path = os.path.relpath(local_file_path, LOCAL_PATH)
                s3_file_path = os.path.normpath(s3_file_path)  # Normalize file path

                # Determine the Content-Type based on the file extension
                content_type = 'text/html' if file.endswith('.html') else 'application/javascript' if file.endswith('.js') else None

                if content_type:
                    # Upload the file with the correct Content-Type
                    with open(local_file_path, 'rb') as data:
                        s3.put_object(
                            Bucket=BUCKET_NAME,
                            Key=s3_file_path,
                            Body=data,
                            ContentType=content_type
                        )

        # Get the bucket website endpoint
        bucket_website_endpoint = f"http://{BUCKET_NAME}.s3-website.{s3.meta.region_name}.amazonaws.com"

        print(f"Static website hosting enabled for S3 bucket '{BUCKET_NAME}'.")
        print(f"Your website URL: {bucket_website_endpoint}")
    except ClientError as e:
        print(f"Error: {e.response['Error']['Message']}")

if __name__ == '__main__':
    deploy_website_to_s3()
    enable_static_website_hosting()
