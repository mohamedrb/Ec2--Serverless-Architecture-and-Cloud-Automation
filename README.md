# Ec2--Serverless-Architecture-and-Cloud-Automation
 Serverless Architecture &amp;amp; Cloud Automation
Assignment 1: Automated Instance Management Using AWS Lambda and Boto3
Objective: In this assignment, you will gain hands-on experience with AWS Lambda and Boto3, Amazon's SDK for Python. You will create a Lambda function that will automatically manage EC2 instances based on their tags.
Task: You're tasked to automate the stopping and starting of EC2 instances based on tags. Specifically:
1. Setup:
   - Create two EC2 instances.
   - Tag one of them as `Auto-Stop` and the other as `Auto-Start`.
2. Lambda Function Creation:
   - Set up an AWS Lambda function.
   - Ensure that the Lambda function has the necessary IAM permissions to describe, stop, and start EC2 instances.
3. Coding:
   - Using Boto3 in the Lambda function:
     - Detect all EC2 instances with the `Auto-Stop` tag and stop them.
     - Detect all EC2 instances with the `Auto-Start` tag and start them.
4. Testing:
   - Manually invoke the Lambda function.
   - Confirm that the instance tagged `Auto-Stop` stops and the one tagged `Auto-Start` starts.
Instructions:
1. EC2 Setup:
   - Navigate to the EC2 dashboard and create two new t2.micro instances (or any other available free-tier type).
   - Tag the first instance with a key `Action` and value `Auto-Stop`.
   - Tag the second instance with a key `Action` and value `Auto-Start`.

 <img width="940" height="460" alt="image" src="https://github.com/user-attachments/assets/ead8b589-40ec-4124-8f84-7b16b407daf3" />

<img width="940" height="500" alt="image" src="https://github.com/user-attachments/assets/606364bc-e471-48a0-832e-e0367a18b2fa" />

 
2. Lambda IAM Role:
   - In the IAM dashboard, create a new role for Lambda.
   - Attach the `AmazonEC2FullAccess` policy to this role. (Note: In a real-world scenario, you would want to limit permissions for better security.)

 <img width="940" height="476" alt="image" src="https://github.com/user-attachments/assets/129a5fdb-3d80-410b-b105-23adfd2a102c" />

3. Lambda Function:
   - Navigate to the Lambda dashboard and create a new function.
   - Choose Python 3.x as the runtime.
   - Assign the IAM role created in the previous step.
   - Write the Boto3 Python script to:
     1. Initialize a boto3 EC2 client.
     2. Describe instances with `Auto-Stop` and `Auto-Start` tags.
     3. Stop the `Auto-Stop` instances and start the `Auto-Start` instances.
     4. Print instance IDs that were affected for logging purposes.

import boto3
ec2 = boto3.client('ec2')
def lambda_handler(event, context):
    # Find Auto-Stop instances
    stop_response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag:Action',
                'Values': ['auto-stop']
            },
            {
                'Name': 'instance-state-name',
                'Values': ['running']
            }
        ]
    )
    stop_instances = []
    for reservation in stop_response['Reservations']:
        for instance in reservation['Instances']:
            stop_instances.append(instance['InstanceId'])
    if stop_instances:
        ec2.stop_instances(InstanceIds=stop_instances)
        print(f"Stopped instances: {stop_instances}")
    else:
        print("No Auto-Stop instances found.")
    # Find Auto-Start instances
    start_response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag:Action',
                'Values': ['auto-start']
            },
            {
                'Name': 'instance-state-name',
                'Values': ['stopped']
            }
        ]
    )

    start_instances = []

    for reservation in start_response['Reservations']:
        for instance in reservation['Instances']:
            start_instances.append(instance['InstanceId'])

    if start_instances:
        ec2.start_instances(InstanceIds=start_instances)
        print(f"Started instances: {start_instances}")
    else:
        print("No Auto-Start instances found.")

    return {
        'statusCode': 200,
        'body': {
            'started_instances': start_instances,
            'stopped_instances': stop_instances
        }
    }

4. Manual Invocation:
   - After saving your function, manually trigger it.
   - Go to the EC2 dashboard and confirm that the instances' states have changed according to their tags.
Assignment 2: Automated S3 Bucket Cleanup Using AWS Lambda and Boto3
Objective: To gain experience with AWS Lambda and Boto3 by creating a Lambda function that will automatically clean up old files in an S3 bucket.
Task: Automate the deletion of files older than 30 days in a specific S3 bucket.
Instructions:
1. S3 Setup:
   - Navigate to the S3 dashboard and create a new bucket.
   - Upload multiple files to this bucket, ensuring that some files are older than 30 days (you may need to adjust your system's date temporarily for this or use old files).
 
 <img width="940" height="522" alt="image" src="https://github.com/user-attachments/assets/03be99e0-800a-4f06-abe4-d5429a2e03b0" />

 <img width="940" height="487" alt="image" src="https://github.com/user-attachments/assets/1a789003-038b-4f0e-b944-d2a714028844" />


2. Lambda IAM Role:
   - In the IAM dashboard, create a new role for Lambda.
   - Attach the `AmazonS3FullAccess` policy to this role. (Note: For enhanced security in real-world scenarios, use more restrictive permissions.)
 <img width="940" height="489" alt="image" src="https://github.com/user-attachments/assets/775f50c0-111c-40f0-8e0b-0c604c26791b" />

3. Lambda Function:
   - Navigate to the Lambda dashboard and create a new function.
   - Choose Python 3.x as the runtime.
   - Assign the IAM role created in the previous step.
   - Write the Boto3 Python script to:
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

     1. Initialize a boto3 S3 client.
     2. List objects in the specified bucket.
     3. Delete objects older than 30 days.
     4. Print the names of deleted objects for logging purposes.
     <img width="940" height="474" alt="image" src="https://github.com/user-attachments/assets/ca994a3d-f178-4fae-9e6e-4a68ac706abd" />

4. Manual Invocation:
   - After saving your function, manually trigger it.
   - Go to the S3 dashboard and confirm that only files newer than 30 days remain.
 

Assignment 3: Monitor Unencrypted S3 Buckets Using AWS Lambda and Boto3
Objective: To enhance your AWS security posture by setting up a Lambda function that detects any S3 bucket without server-side encryption.
Task: Automate the detection of S3 buckets that don't have server-side encryption enabled.
Instructions:
1. S3 Setup:
   - Navigate to the S3 dashboard and create a few buckets. Ensure that a couple of them don't have server-side encryption enabled.
2. Lambda IAM Role:
   - In the IAM dashboard, create a new role for Lambda.
   - Attach the `AmazonS3ReadOnlyAccess` policy to this role.
3. Lambda Function:
   - Navigate to the Lambda dashboard and create a new function.
   - Choose Python 3.x as the runtime.
   - Assign the IAM role created in the previous step.
   - Write the Boto3 Python script to:
     1. Initialize a boto3 S3 client.
     2. List all S3 buckets.
     3. Detect buckets without server-side encryption.
     4. Print the names of unencrypted buckets for logging purposes.
<img width="940" height="493" alt="image" src="https://github.com/user-attachments/assets/2e6fa9a4-7ae6-49a1-87ad-0aa5faa69fec" />

 

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
 <img width="940" height="476" alt="image" src="https://github.com/user-attachments/assets/b582a2c0-3199-499d-934f-9e896d4eb387" />

4. Manual Invocation:
   - After saving your function, manually trigger it.
   - Review the Lambda logs to identify the buckets without server-side encryption.
Assignment 4: Automatic EBS Snapshot and Cleanup Using AWS Lambda and Boto3
Objective: To automate the backup process for your EBS volumes and ensure that backups older than a specified retention period are cleaned up to save costs.
Task: Automate the creation of snapshots for specified EBS volumes and clean up snapshots older than 30 days.
Instructions:
1. EBS Setup:
   - Navigate to the EC2 dashboard and identify or create an EBS volume you wish to back up.
   - Note down the volume ID.
2. Lambda IAM Role:
   - In the IAM dashboard, create a new role for Lambda.
   - Attach policies that allow Lambda to create EBS snapshots and delete them (`AmazonEC2FullAccess` for simplicity, but be more restrictive in real-world scenarios).
3. Lambda Function:
   - Navigate to the Lambda dashboard and create a new function.
   - Choose Python 3.x as the runtime.
   - Assign the IAM role created in the previous step.
   - Write the Boto3 Python script to:
     1. Initialize a boto3 EC2 client.
     2. Create a snapshot for the specified EBS volume.
     3. List snapshots and delete those older than 30 days.
     4. Print the IDs of the created and deleted snapshots for logging purposes.

 
<img width="940" height="501" alt="image" src="https://github.com/user-attachments/assets/61ead420-0dde-475a-8b28-d9bca96e27d1" />

<img width="940" height="497" alt="image" src="https://github.com/user-attachments/assets/e1b45401-30c8-4c82-a9fc-7d2f772e98b3" />


 

import boto3
from datetime import datetime, timezone, timedelta
ec2 = boto3.client('ec2')
# Replace with your EBS Volume ID
VOLUME_ID = 'vol-049d90958aa44ee5c'
def lambda_handler(event, context):

    # Create Snapshot
    snapshot = ec2.create_snapshot(
        VolumeId=VOLUME_ID,
        Description='Automated Lambda Backup'
    )

    snapshot_id = snapshot['SnapshotId']
    print(f"Created Snapshot: {snapshot_id}")

    # Find snapshots older than 30 days
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=30)

    snapshots = ec2.describe_snapshots(
        OwnerIds=['self']
    )

    deleted_snapshots = []
    for snap in snapshots['Snapshots']:

        if snap['VolumeId'] == VOLUME_ID:
            start_time = snap['StartTime']

            if start_time < cutoff_date:
                ec2.delete_snapshot(
                    SnapshotId=snap['SnapshotId']
                )

                deleted_snapshots.append(
                    snap['SnapshotId']
                )
                print(
                    f"Deleted Snapshot: {snap['SnapshotId']}"
                )

    return {
        'statusCode': 200,
        'created_snapshot': snapshot_id,
        'deleted_snapshots': deleted_snapshots
    }

<img width="940" height="481" alt="image" src="https://github.com/user-attachments/assets/f926945b-e209-4600-98d0-f6d9d4d4ea10" />

 

4. Event Source (Bonus):
   - Attach an event source, like Amazon CloudWatch Events, to trigger the Lambda function at your desired backup frequency (e.g., every week).
5. Manual Invocation:
   - After saving your function, either manually trigger it or wait for the scheduled event.
   - Go to the EC2 dashboard and confirm that the snapshot is created and old snapshots are deleted.
