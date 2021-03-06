import boto3
import botocore
import os


s3 = boto3.client(
  "s3",
  aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
  aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)


def upload_image_to_s3(folder_name, file, acl="public-read"):
  try:
    s3.upload_fileobj(
      file,
      os.getenv('S3_BUCKET_NAME'),
      f"user-{folder_name}/{file.filename}",
      ExtraArgs={
        "ACL": acl,
        "ContentType": file.content_type
      }
    )

  except Exception as e:
    print(f"Error Occured During Upload: {e}")
    return e

  return f"user-{folder_name}/{file.filename}"
