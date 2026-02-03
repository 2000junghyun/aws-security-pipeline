import json
import boto3
import datetime

ec2_client = boto3.client('ec2')

def lambda_handler(event, context):
    try:
        classifire_source = event.get('classifierSource', 'Unknown')
        print(f"[OK] Invocation received from: {classifire_source}")

        # 최근 생성된 인스턴스 중지/종료
        stopped_ids = ec2_instance_handler()

        print(f"[OK] Stopped instances: {stopped_ids if stopped_ids else 'None'}")

    except Exception as e:
        print(f"[ERROR] Lambda execution failed: {e}")

    return {
        'statusCode': 200,
        'body': json.dumps('EC2 instance stop function executed successfully.')
    }


def ec2_instance_handler():
    stopped_ids = []
    try:
        response = ec2_client.describe_instances(
            Filters=[
                {'Name': 'instance-state-name', 'Values': ['running', 'pending']},
            ]
        )

        now_utc = datetime.datetime.now(datetime.timezone.utc)

        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                launch_time = instance['LaunchTime']

                # 최근 15분 이내에 생성된 인스턴스 식별
                if now_utc - launch_time < datetime.timedelta(minutes=15):
                    print(f"[OK] Recently launched instance found: {instance_id} (Launch Time: {launch_time})")
                    try:
                        ec2_client.stop_instances(InstanceIds=[instance_id])
                        stopped_ids.append(instance_id)
                        print(f"[OK] Successfully stopped instance: {instance_id}")
                    except Exception as e:
                        print(f"[ERROR] Failed to stop instance {instance_id}: {e}")

    except Exception as e:
        print(f"[ERROR] Failed to describe instances: {e}")
    
    return stopped_ids