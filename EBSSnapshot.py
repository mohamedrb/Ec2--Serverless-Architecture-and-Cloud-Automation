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
