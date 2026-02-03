# Deactivate access key

## Overview

- A Lambda-based response function that extracts the **Access Key ID and user name** from AWS event data and deactivates the associated access key
- Automatically invoked by upstream detection systems (e.g., threat IP classifier, resource creation detector)
- Immediately **disables compromised or misused credentials** to contain potential security breaches in real time

## Tech Stack

- AWS Lambda
- Python 3.9
- AWS IAM (via Boto3)

## Directory Structure

```bash
.
├── lambda_function.py                # Lambda function to deactivate access keys
└── README.md
```

## How It Works

- Parses the values of `userIdentity.accessKeyId` and `userIdentity.userName` from the incoming event
- Calls the IAM API (`update_access_key`) to set the access key status to `'Inactive'`
- Logs success or failure and returns appropriate HTTP status codes

## Features / Main Logic

- **Precise Target Identification**
    
    Extracts both `accessKeyId` and `userName` from the event to ensure exact targeting
    
- **IAM Integration for Credential Control**
    
    Uses `iam.update_access_key()` to instantly deactivate the compromised access key
    
- **Robust Error Handling**
    
    Gracefully handles missing users or keys with `NoSuchEntityException`
    
    Catches unexpected exceptions and logs detailed error messages
    
- **Classifier Integration Support**
    
    Supports invocation from other classifier Lambdas using the `event['classifierSource']` field to track the source of the call
    
## Result
**CloudWatch Log**

<img width="773" height="92" alt="image (1)" src="https://github.com/user-attachments/assets/3fc79938-9fe3-4fc6-b121-798894d1b02a" />

<br><br>

**IAM User Policy**

<img width="1230" height="415" alt="image (2)" src="https://github.com/user-attachments/assets/853a5e10-e3bb-4488-8b82-23842182b582" />


## Motivation / Impact

- **Immediately blocks stolen or misused credentials**, reducing risk of further compromise
- Prevents attacks such as mass EC2 provisioning, data exfiltration, or privilege escalation
- Serves as a key component in building an **automated cloud threat response system**
