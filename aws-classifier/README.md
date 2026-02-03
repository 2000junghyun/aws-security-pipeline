# aws-classifier

A collection of AWS Lambda-based classification pipelines for automated threat detection and response.

Each subdirectory contains an independent module with its own purpose, logic, and README documentation.

## Projects

| Subdirectory | Description |
| --- | --- |
| `threat-ip-classifier` | Detects and responds to unauthorized access based on a predefined list of malicious IPs |
| `resource-creation-detector` | Detects mass EC2 instance creation events and triggers automated response actions |
| `malicious-file-classifier` | Performs static analysis on uploaded files and classifies them as malicious or benign |

## How to Use

Each subdirectory contains:

- Its own source code (`lambda_function.py`, etc.)
- A `README.md` file with setup instructions, architecture, and usage details

Please refer to each project's README for in-depth information and deployment guides.

## Tech Stack (shared)

- AWS Lambda
- CloudWatch Logs & Alarms
- Python 3.9
- S3, SNS, IAM, Boto3
- Modular & event-driven architecture

## Structure

```bash
aws-classifier/
├── threat-ip-classifier/
│   └── README.md
├── resource-creation-detector/
│   └── README.md
├── malicious-file-classifier/
│   └── README.md
└── README.md  # ← now this file
```

## Motivation

Security threats in the cloud environment come in many forms. This repository provides modular, serverless detection and response systems to help security engineers **quickly respond to threats** such as:

- Unauthorized access by known threat actors
- Excessive resource provisioning
- Malware uploads through open S3 buckets or user submissions