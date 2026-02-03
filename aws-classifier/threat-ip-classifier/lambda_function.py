import os
import boto3
from utils.responder_dispatcher import threat_handler

# 환경 변수
S3_BUCKET = os.environ.get('THREAT_IP_BUCKET')
S3_KEY = os.environ.get('THREAT_IP_KEY')

s3 = boto3.client('s3')

def lambda_handler(event, context):
    try:
        # S3에서 위협 IP 리스트 로드
        s3_response = s3.get_object(Bucket=S3_BUCKET, Key=S3_KEY)
        ip_list = s3_response['Body'].read().decode('utf-8').splitlines()
        threat_ips = set(ip.strip() for ip in ip_list if ip and not ip.startswith("#"))

        print("[OK] Threat IPs loaded successfully")

        # source IP 비교
        source_ip = event.get('detail', {}).get('sourceIPAddress', 'N/A')

        if not source_ip:
            print("[WARN] sourceIPAddress not found in event")
            return {'statusCode': 400, 'body': 'sourceIPAddress not found'}

        print(f"[INFO] Source IP: {source_ip}")

        if source_ip not in threat_ips:
            print("[INFO] IP is not in threat list. Ignored.")
            return {'statusCode': 200, 'body': 'Normal IP. No action taken.'}

        print("[ALERT] Threat IP detected")

        # 대응 함수 호출
        threat_handler(event)

        return {'statusCode': 200, 'body': 'Threat handled successfully'}

    except Exception as e:
        print(f"[ERROR] {e}")
        return {'statusCode': 500, 'body': 'Internal server error'}