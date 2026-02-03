import os
import boto3

SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN')

def lambda_handler(event, context):
    try:
        # 핵심 정보 추출
        detail = event.get('event', event).get('detail')
        source_ip = detail.get('sourceIPAddress', 'N/A')
        user_identity = detail.get('userIdentity', {}).get('arn', 'N/A')
        region = detail.get('awsRegion', 'N/A')
        event_name = detail.get('eventName', 'N/A')
        event_time = detail.get('eventTime', 'N/A')
        classifier_source = event.get('classifierSource', 'UnknownSource')

        # 본문
        message = f"""[Threat Alert] Malicious Activity Detected

- Classifier Source: {classifier_source}
- Event: {event_name}
- Matched Threat IP: {source_ip}
- User: {user_identity}
- Region: {region}
- Time: {event_time}

Please verify and take action as necessary.
"""

        sns = boto3.client('sns')
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject=f'[Threat Detected] Source: {classifier_source}',
            Message=message
        )
        print("[OK] SNS alert sent")

        return {
            'statusCode': 200,
            'body': 'SNS alert sent successfully.'
        }

    except Exception as e:
        print(f"[Error] Failed to send SNS alert: {e}")
        return {
            'statusCode': 500,
            'body': 'Failed to send SNS alert.'
        }