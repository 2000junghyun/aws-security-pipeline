import boto3

iam = boto3.client('iam')

def lambda_handler(event, context):
    classifire_source = event.get('classifierSource', 'Unknown')
    print(f"[OK] Invocation received from: {classifire_source}")

    # 핵심 정보 추출
    detail = event.get('event', event)
    access_key_id = detail.get('detail', {}).get('userIdentity', {}).get('accessKeyId')
    user_name = detail.get('detail', {}).get('userIdentity', {}).get('userName')

    if not access_key_id or not user_name:
        print("[WARN] Missing accessKeyId or userName in event.")
        return {'statusCode': 400, 'body': 'Missing required information.'}

    try:
        # Access Key 비활성화
        iam.update_access_key(
            UserName=user_name,
            AccessKeyId=access_key_id,
            Status='Inactive'
        )
        print(f"[OK] Deactivated access key: {access_key_id} for user: {user_name}")
        return {
            'statusCode': 200,
            'body': f'Access key {access_key_id} deactivated for user {user_name}'
        }

    except iam.exceptions.NoSuchEntityException:
        print("[ERROR] No such user or access key.")
        return {'statusCode': 404, 'body': 'User or access key not found.'}

    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return {'statusCode': 500, 'body': 'Internal server error.'}