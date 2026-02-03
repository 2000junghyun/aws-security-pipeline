# aws-responder

## Overview

- A collection of AWS Lambda functions designed to perform **automated response actions** triggered by cloud-based threat detection systems
- Responds immediately to incidents such as **credential theft, excessive resource creation, and IAM policy abuse**
- Each subdirectory is an independent responder module with its own logic and `README.md`

## Projects

| Directory | Description |
| --- | --- |
| `deactivate-access-key` | Deactivates exposed or misused access keys in real time |
| `restrict-user-policy` | Removes EC2-related IAM permissions and attaches a Deny policy to the user |
| `terminate-ec2-instances` | Detects and stops EC2 instances launched recently (within 15 minutes) |

## How to Use

- Each project directory includes:
    - Lambda function code (`lambda_function.py`)
    - A dedicated `README.md` with usage instructions and implementation details
- See each folder's documentation for deployment and integration steps

## Shared Tech Stack

- AWS Lambda
- Python 3.9
- AWS IAM / EC2
- Boto3
- Event-driven integration with classifier Lambdas

## Directory Structure

```bash
aws-responder/
├── deactivate-access-key/
│   └── README.md
├── restrict-user-policy/
│   └── README.md
├── terminate-ec2-instances/
│   └── README.md
└── README.md  # ← now this file
```

## Motivation

- Goes beyond detection by enabling **real-time, automated mitigation** of cloud threats
- Built on serverless architecture for **scalability, speed, and easy integration**
- Designed to complement classifier modules and form a complete **cloud security automation pipeline**