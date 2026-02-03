import json
import boto3

iam_client = boto3.client('iam')

def lambda_handler(event, context):
    classifire_source = event.get('classifierSource', 'Unknown')
    print(f"[OK] Invocation received from: {classifire_source}")
    
    event = event.get('event')
    detail = event.get('detail')
    user_name = detail.get('userIdentity').get('userName')

    if not user_name:
        print("[ERROR] userName not provided.")
        return {'statusCode': 400, 'body': 'userName missing.'}

    print(f"[OK] Processing user: {user_name}")

    try:
        remove_policies(user_name)
        print("[OK] EC2-related permissions removed successfully.")

        attach_deny_policies(user_name)
        print("[OK] EC2-related deny policy attached successfully.")

        return {
            'statusCode': 200,
            'body': f'EC2 permissions removed for user {user_name}.'
        }

    except Exception as e:
        print(f"[!] Error processing IAM permissions: {e}")
        return {'statusCode': 500, 'body': 'Internal server error.'}


def remove_policies(user_name):
    # Attached (Managed) 정책 제거
    attached_policies = iam_client.list_attached_user_policies(UserName=user_name)['AttachedPolicies']
    for policy in attached_policies:
        policy_name = policy['PolicyName']
        print(f"→ Detaching managed policy: {policy_name}")
        iam_client.detach_user_policy(
            UserName=user_name,
            PolicyArn=policy['PolicyArn']
        )

    # Inline 정책 제거
    inline_policies = iam_client.list_user_policies(UserName=user_name)['PolicyNames']
    for policy_name in inline_policies:
        print(f"→ Deleting inline policy: {policy_name}")
        iam_client.delete_user_policy(
            UserName=user_name,
            PolicyName=policy_name
        )


def attach_deny_policies(user_name):
    deny_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Deny",
                "Action": [
                    "ec2:RunInstances",
                    "ec2:StartInstances",
                    "ec2:RebootInstances",
                    "ec2:CreateTags"
                ],
                "Resource": "*"
            }
        ]
    }

    iam_client.put_user_policy(
        UserName=user_name,
        PolicyName="DenyEC2Permissions",
        PolicyDocument=json.dumps(deny_policy)
    )