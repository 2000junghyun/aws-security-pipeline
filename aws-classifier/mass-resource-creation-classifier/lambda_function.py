import os
import json
import time
import boto3
from dateutil import parser
from datetime import datetime, timedelta, timezone
from utils.responder_dispatcher import threat_handler

CLOUDTRAIL_LOG_GROUP_NAME = os.environ.get('CLOUDTRAIL_LOG_GROUP_NAME')
logs_client = boto3.client('logs')


def lambda_handler(event, context):
    print(f"[OK] Received event")

    # 1. SNS 메시지 파싱
    alarm_time = parse_sns_message(event)
    if not alarm_time:
        return {'statusCode': 400, 'body': json.dumps('Invalid SNS message.')}

    # 2. 로그 조회 시간 범위 계산
    end_time_ms = int(alarm_time.timestamp() * 1000)
    start_time_ms = int((alarm_time - timedelta(minutes=5)).timestamp() * 1000)
    print(f"Alarm at {alarm_time.isoformat()}")
    print(f"Query window: {datetime.fromtimestamp(start_time_ms / 1000, tz=timezone.utc)} ~ {datetime.fromtimestamp(end_time_ms / 1000, tz=timezone.utc)}")

    # 3. Logs Insights 쿼리 실행
    query_string = """
        fields @timestamp, userIdentity.arn as arn, userIdentity.accessKeyId as accessKeyId, userIdentity.userName as userName, eventTime, eventName, awsRegion, sourceIPAddress
        | filter eventName = 'RunInstances'
        | sort @timestamp desc
        | limit 10
    """
    results = run_logs_insights_query(start_time_ms, end_time_ms, query_string)
    if results is None:
        return {'statusCode': 500, 'body': json.dumps('Internal server error.')}

    # 4. 사용자 정보 추출
    users = extract_users_from_results(results)
    if not users:
        print("[OK] No suspicious users found.")
        return {'statusCode': 200, 'body': json.dumps('No suspicious users found.')}

    print(f"[OK] Found users:")

    # 5. 사용자별로 대응 함수 호출
    try:
        handle_users(users)
        return {'statusCode': 200, 'body': 'Threats handled successfully'}
    except Exception as e:
        print(f"[ERROR] Error during function invoke: {e}")
        return {'statusCode': 500, 'body': json.dumps('Internal server error.')}


# SNS 메시지 파싱 함수
def parse_sns_message(event):
    try:
        sns_message = json.loads(event['Records'][0]['Sns']['Message'])
        alarm_time = parser.isoparse(sns_message['StateChangeTime'])
        return alarm_time
    except Exception as e:
        print(f"[Error] Error parsing SNS message: {e}")
        return None


# Logs Insights 쿼리 실행 및 결과 반환
def run_logs_insights_query(start_time_ms, end_time_ms, query_string):
    try:
        query_id = logs_client.start_query(
            logGroupName=CLOUDTRAIL_LOG_GROUP_NAME,
            startTime=start_time_ms,
            endTime=end_time_ms,
            queryString=query_string
        )['queryId']
        print(f"Started query: {query_id}")

        # 최대 30초 대기
        response = None
        wait_time = 0
        while (response is None or response['status'] in ['Running', 'Scheduled']) and wait_time < 30:
            time.sleep(1)
            wait_time += 1
            response = logs_client.get_query_results(queryId=query_id)

        print(f"Query status: {response['status']}")
        if response['status'] != 'Complete':
            raise Exception("Logs query did not complete in time.")

        return response['results']
    except Exception as e:
        print(f"[ERROR] Error during query: {e}")
        return None


# Logs Insights 쿼리 결과에서 사용자 정보 파싱
def extract_users_from_results(results):
    users = {}
    for result in results:
        user = {}
        for field in result:
            if field['field'] == 'arn' and field['value']:
                user['arn'] = field['value']
            elif field['field'] == 'userName' and field['value']:
                user['userName'] = field['value']
            elif field['field'] == 'accessKeyId' and field['value']:
                user['accessKeyId'] = field['value']
            elif field['field'] == 'eventTime' and field['value']:
                user['eventTime'] = field['value']
            elif field['field'] == 'eventName' and field['value']:
                user['eventName'] = field['value']
            elif field['field'] == 'awsRegion' and field['value']:
                user['awsRegion'] = field['value']
            elif field['field'] == 'sourceIPAddress' and field['value']:
                user['sourceIPAddress'] = field['value']
        if user:
            users[user['accessKeyId']] = user  # accessKeyId로 중복 제거
    return list(users.values())


# 사용자별로 이벤트 포맷 구성 및 대응 함수 호출
def handle_users(users):
    for user in users:
        handled_event = {
            "detail": {
                "userIdentity": {
                    "arn": user.get("arn", ""),
                    "accessKeyId": user.get("accessKeyId", ""),
                    "userName": user.get("userName", "")
                },
                "eventTime": user.get("eventTime", ""),
                "eventName": user.get("eventName", ""),
                "awsRegion": user.get("awsRegion", ""),
                "sourceIPAddress": user.get("sourceIPAddress", "")
            }
        }
        print(json.dumps(handled_event))
        threat_handler(handled_event)