# Terminate EC2 instances

## Overview

- A Lambda-based response function that detects and automatically stops **recently launched EC2 instances** in response to AWS events
- Invoked by upstream threat detection systems (e.g., mass resource creation detectors) to **quickly neutralize potentially malicious instances**
- Immediately halts **excessive resource usage or malicious instance activity**, helping prevent the spread of security incidents

## Tech Stack

- AWS Lambda
- Python 3.9
- AWS EC2 (via Boto3)

## Directory Structure

```bash
.
├── lambda_function.py                # Lambda function to stop EC2 instances
└── README.md
```

## How It Works

- Queries EC2 instances with `running` or `pending` status at the time of execution
- Compares each instance’s `LaunchTime` with the current time to identify **instances launched within the past 15 minutes**
- Calls `stop_instances()` to stop identified instances
- Logs all processed instance IDs, along with success or failure messages

## Features / Main Logic

- **Detect Recently Launched Instances**
    
    Uses `describe_instances()` to retrieve all active EC2 instances
    
    Filters for instances launched within the last 15 minutes
    
- **Automated Instance Stopping**
    
    Executes `stop_instances()` to stop each flagged EC2 instance immediately
    
- **Logging and Exception Handling**
    
    Logs success/failure for each instance stop operation
    
    Captures and logs exceptions during `describe` or `stop` API calls
    
- **Classifier Integration Support**
    
    Logs the source of invocation using `event['classifierSource']`
    
    Designed for seamless integration with multiple classifier systems
    
## Results
**CloudWatch Log**

<img width="1042" height="181" alt="image" src="https://github.com/user-attachments/assets/fa4a80d3-4832-432a-89c4-ccce444c562e" />

<br><br>

**EC2 Instances**

<img width="2432" height="477" alt="image2" src="https://github.com/user-attachments/assets/a5d4a5e8-d297-43f2-a8e0-4761d635a404" />

## Motivation / Impact

- Provides **real-time mitigation** for scenarios where an attacker launches a large number of instances
- Improves the **response speed of automated cloud security pipelines** by acting immediately after detection
- Can be extended to support termination, notification, or integration with cost control systems
