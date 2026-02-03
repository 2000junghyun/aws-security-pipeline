import json

def lambda_handler(event, context):
    print(f"[OK] Received event")

    try:
        # 핵심 정보 추출
        classifier_source = event.get('classifierSource', 'UnknownSource')
        detail = event.get('event', event).get('detail', {})        
        event_id = detail.get('eventID', 'N/A')
        event_time = detail.get('eventTime', 'N/A')
        region = detail.get('awsRegion', 'N/A')
        user_identity = detail.get('userIdentity', {}).get('arn', 'N/A')
        source_ip = detail.get('sourceIPAddress', 'N/A')        
        event_name = detail.get('eventName', 'N/A')        

        # 로그 생성
        log_message = (
            f"classifier_source={classifier_source}\n"
            f"event_id={event_id}\n"
            f"event_time={event_time}\n"
            f"event_name={event_name}\n"
            f"user={user_identity}\n"
            f"source_ip={source_ip}\n"
            f"region={region}\n"
        )
        print(log_message)
        
        print(f"[OK] Malicious event logged")

        return {
            'statusCode': 200,
            'body': 'Malicious event logged successfully.'
        }

    except Exception as e:
        print(f"[Error] Failed to create log: {e}")
        return {
            'statusCode': 500,
            'body': 'Failed to create log.'
        }