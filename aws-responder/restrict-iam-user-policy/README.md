# Restrict IAM user policy

## Overview

- A Lambda-based response function that removes all EC2-related IAM permissions from a user and attaches an **explicit Deny policy** based on the username extracted from the AWS event
- Automatically invoked by upstream threat detection systems (e.g., resource creation detectors)
- Immediately **blocks potential abuse** and restricts the user's ability to interact with EC2 resources

## Tech Stack

- AWS Lambda
- Python 3.9
- AWS IAM (via Boto3)

## Directory Structure

```bash

.
├── lambda_function.py           # Lambda function for IAM permission restriction
└── README.md
```

## How It Works

- Extracts `userIdentity.userName` from the event
- For the identified user:
    - Removes all **attached managed policies and inline policies**
    - Adds an **inline deny policy** that blocks all major EC2 actions
- Logs the outcome and returns the appropriate HTTP status code (success or failure)

## Features / Main Logic

- **Remove All IAM Policies**
    
    Uses `list_attached_user_policies()` and `list_user_policies()`
    
    to remove all attached and inline policies associated with the user
    
- **Attach Deny Policy**
    
    Adds an inline policy that explicitly denies critical EC2 actions
    
    such as `RunInstances`, `StartInstances`, `RebootInstances`, and `CreateTags`
    
- **Automated Threat Response Flow**
    
    Designed to be called by a classifier Lambda, with `classifierSource` for source tracing
    
    Parses the user from `event['event']['detail']['userIdentity']['userName']`
    
- **Built-in Exception Handling**
    
    Logs and returns proper error messages if user information is missing
    
    or if IAM operations fail unexpectedly
    
## Results
**CloudWatch Log**

<img width="475" height="158" alt="image" src="https://github.com/user-attachments/assets/f73b6dba-a4e2-4528-b247-1e8eef97dc62" />

<br><br>

**IAM User Policy**

<img width="1234" height="413" alt="image2" src="https://github.com/user-attachments/assets/56764177-5a26-4478-a31e-d378ebed20f9" />


## Motivation / Impact

- **Immediately restricts EC2 access for users suspected of abuse or privilege escalation**
- Prevents malicious activity such as mass instance creation or unauthorized tagging
- Contributes to building an **automated and resilient cloud IAM response system**
