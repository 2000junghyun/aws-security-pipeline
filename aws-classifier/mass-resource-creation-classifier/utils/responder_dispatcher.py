import os
import json
import boto3

RESPONSER_LAMBDA = os.environ.get('RESPONSER_LAMBDA_ARN') # Access Key 비활성화
RESPONSER_LAMBDA_2 = os.environ.get('RESPONSER_LAMBDA_ARN_2') # 최근 생성된 instance 중지
RESPONSER_LAMBDA_3 = os.environ.get('RESPONSER_LAMBDA_ARN_3') # IAM 정책 제한 (EC2)

NOTIFIER_LAMBDA = os.environ.get('NOTIFIER_LAMBDA_ARN')
LOGGER_LAMBDA = os.environ.get('LOGGER_LAMBDA_ARN')

lambda_client = boto3.client('lambda')

def threat_handler(event):
    payload = {
        "classifierSource": "Classifier_MassResourceCreation",
        "event": event
    }

    # Responser Lambda 호출
    lambda_client.invoke(
        FunctionName=RESPONSER_LAMBDA,
        InvocationType='Event',
        Payload=json.dumps(payload)
    )
    print("[OK] Responser_DenyingAccessKey lambda invoked")

    lambda_client.invoke(
        FunctionName=RESPONSER_LAMBDA_2,
        InvocationType='Event',
        Payload=json.dumps(payload)
    )
    print("[OK] Responser_StopEC2Instances lambda invoked")

    lambda_client.invoke(
        FunctionName=RESPONSER_LAMBDA_3,
        InvocationType='Event',
        Payload=json.dumps(payload)
    )
    print("[OK] Responser_RestrictIAMPolicy_EC2 lambda invoked")

    # Notifier Lambda 호출
    lambda_client.invoke(
        FunctionName=NOTIFIER_LAMBDA,
        InvocationType='Event',
        Payload=json.dumps(payload)
    )
    print("[OK] Notifier lambda invoked")

    # Logger Lambda 호출
    lambda_client.invoke(
        FunctionName=LOGGER_LAMBDA,
        InvocationType='Event',
        Payload=json.dumps(payload)
    )
    print("[OK] Logger lambda invoked")