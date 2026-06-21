import boto3
from botocore.exceptions import ClientError

s3 = boto3.client('s3')

def lambda_handler(event, context):
    print("Loading Bucket Details")
    buckets = s3.list_buckets()

    unencrypted_buckets = []

    for bucket in buckets['Buckets']:
        print("Loading Bucket Details: " + bucket['Name'])
        bucket_name = bucket['Name']

        try:
            s3.get_bucket_encryption(
                Bucket=bucket_name
            )

        except ClientError as e:

            error_code = e.response['Error']['Code']

            if error_code == 'ServerSideEncryptionConfigurationNotFoundError':
                unencrypted_buckets.append(bucket_name)
                print(f"Unencrypted Bucket: {bucket_name}")

    if not unencrypted_buckets:
        print("All buckets have server-side encryption enabled.")

    return {
        'statusCode': 200,
        'unencrypted_buckets': unencrypted_buckets    }
