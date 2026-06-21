import boto3
from datetime import datetime, timezone, timedelta

s3 = boto3.client('s3')

BUCKET_NAME = 'my-s3-cleanup-bucket-12345'

def lambda_handler(event, context):

    cutoff_date = datetime.now(timezone.utc) - timedelta(minutes=3)

    response = s3.list_objects_v2(Bucket=BUCKET_NAME)

    deleted_files = []

    if 'Contents' not in response:
        print("Bucket is empty.")
        return

    for obj in response['Contents']:

        key = obj['Key']
        last_modified = obj['LastModified']

        if last_modified < cutoff_date:

            s3.delete_object(
                Bucket=BUCKET_NAME,
                Key=key
            )

            deleted_files.append(key)
            print(f"Deleted: {key}")

    if not deleted_files:
        print("No files older than 30 days found.")

    return {
        'statusCode': 200,
        'deleted_files': deleted_files
    }
