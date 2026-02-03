# Mass resource creation classifier

## Overview

- A serverless pipeline that detects and responds to **mass EC2 instance creation events** within a short time window
- Triggered by the sequence: CloudWatch Alarm → SNS → Lambda → CloudTrail query
- When suspicious users are identified, the `threat_handler` function is invoked to disable access, notify stakeholders, and log the incident

## Tech Stack

- AWS Lambda
- Python 3.9
- CloudWatch Logs Insights
- Boto3 (AWS SDK for Python)

## Directory Structure

```bash
.
├── lambda_function.py                # Lambda function to detect and respond to mass EC2 creation
├── utils/
│   └── responder_dispatcher.py       # Response handler module
└── README.md
```

## How It Works

- Triggered by a CloudWatch Alarm via SNS
- Uses the `StateChangeTime` as a reference to query CloudTrail logs from 5 minutes before to 5 minutes after
- Filters for `RunInstances` events and extracts suspicious users
- Calls response Lambda functions per user to disable access keys, restrict IAM policies, send notifications, and log the activity

## Features / Main Logic

- **Logs Insights Query Execution**
    
    Detects mass resource creation by querying `RunInstances` events in CloudTrail logs
    
- **User Information Parsing & Deduplication**
    
    Aggregates user data and deduplicates based on access key ID
    
- **Automated Threat Response**
    
    Invokes dedicated responder functions through the `responder_dispatcher.py` module
    
- **Modular Design**
    
    Cleanly separated logic for better extensibility and maintainability

## Result
<img width="618" height="434" alt="image2" src="https://github.com/user-attachments/assets/a31753f1-baa9-41a5-89f3-1e7e731083cd" />


## Future Work

- Add thresholds for triggering alerts (e.g., more than 10 instances created within 5 minutes)
- Expand detection to other sensitive events like `CreateUser`, `CreateAccessKey`
- Implement automated reporting for identified suspicious users

## Motivation / Impact

- Enables **automated detection and response** to attacks involving large-scale resource creation
- Prevents abuse and cost leakage by proactively monitoring and mitigating excessive or unauthorized activity
- Enhances operational security automation in cloud environments
