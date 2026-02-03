# Threat IP classifier

## Overview

- Detects and responds to unauthorized access based on a predefined list of threat IPs
- Compares the `sourceIPAddress` from incoming events against an IP list stored in S3
- If a threat IP is detected, response Lambda functions are automatically invoked to block access, send alerts, and log the incident

## Tech Stack

- AWS Lambda
- Python 3.9
- S3
- Boto3 (AWS SDK for Python)

## Directory Structure

```bash
.
├── lambda_function.py                # Lambda entry point for IP checking and dispatch
├── utils/
│   └── responder_dispatcher.py       # Logic for invoking response Lambda functions
└── README.md

```

## How It Works

- When the Lambda function is triggered, it loads the threat **IP list** from a specified S3 bucket
- It extracts the `sourceIPAddress` from the event and checks whether it appears in the list
- If the IP is not in the list, the event is ignored
- If the IP matches a known threat, response Lambda functions are invoked


## Features / Main Logic

- **S3-Based IP List Loading**
    
    Dynamically loads allow/block lists from S3 to support flexible policy management
    
- **Real-Time Threat Detection**
    
    Compares the `sourceIPAddress` in AWS events against known threat indicators
    
- **Automated Response Execution**
    
    Automatically invokes Lambda functions to block credentials, send alerts, and log incidents
    
- **Modular Design**
    
    Easily extendable with additional Lambda functions or logic components

## Result
<img width="904" height="278" alt="image" src="https://github.com/user-attachments/assets/c5523e55-3380-48c7-9b77-c521998eef58" />

    

## Future Work

- Implement IP list caching to reduce S3 access
- Add support for CIDR-based IP matching
- Integrate with external threat intelligence feeds (e.g., AbuseIPDB, OTX)

## Motivation / Impact

- Provides an automated, IP-based defense system to mitigate credential theft and privilege abuse
- Designed for scalability and easy integration in serverless security operations
