# aws-logger

## Overview

- A Lambda function that generates **structured security logs** from threat detection events, including classifier source, user, IP address, event name, and more
- Invoked by classifier or responder modules to ensure **consistent log formatting across the pipeline**

## Tech Stack

- AWS Lambda
- Python 3.9

## Directory Structure

```bash
.
├── lambda_function.py                # Lambda function for security event logging
└── README.md
```

## How It Works

- Parses key fields such as `eventName`, `eventTime`, `eventID`, `userIdentity`, `sourceIPAddress`, and `awsRegion`
- Logs the `classifierSource` to identify which system triggered the event
- Outputs all fields using a **predefined log format**
- Returns a status code (`200` or `500`) based on success or failure

## Features / Main Logic

- **Structured Logging of Key Event Data**
    
    Collects essential fields from detected events and logs them for audit or review
    
- **Consistent Log Format**
    
    Outputs logs using a `key=value` structure for better readability and post-analysis
    
- **Classifier Source Tracking**
    
    Supports source tracing by logging the `classifierSource` field
    
- **Built-in Error Handling**
    
    Captures exceptions during log generation and returns a `500` status code on failure
    
## Result
<img width="461" height="207" alt="image" src="https://github.com/user-attachments/assets/f952cf66-0bf5-4845-ba6a-1bbb76ea0706" />


## Motivation / Impact

- Ensures **visibility and traceability** for threat events occurring in the cloud
- Supports security audits, anomaly investigations, and response tracking
- Acts as a lightweight and extensible logging module tightly integrated with detection and response functions
