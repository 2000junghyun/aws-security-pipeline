# Malicious File Classifier

## Overview

- A static malware analysis pipeline automatically triggered when a file is uploaded to an S3 bucket
- Performs **Threat Intelligence (TI) matching**, **metadata-based classification**, **content signature comparison**, and **fuzzy hash similarity analysis** via AWS Lambda

## Tech Stack

- AWS Lambda
- Python 3.9
- S3 Event Trigger
- Static Analysis Techniques:
    - Threat Intelligence Matching
    - Metadata Classification
    - Content Signature Comparison
    - Fuzzy Hash Similarity Check

## Directory Structure

```bash
.
├── lambda_function.py                 # Lambda entry point
├── run_lambda.py                      # Local test runner
├── fuzzy_hash_db/                     # Fuzzy hash DB for similarity analysis
└── utils/
     ├── static_analyzer/
     │   ├── ext_filter.py             # Extension-based filter
     │   ├── mime_checker.py           # MIME type checker
     │   └── size_checker.py           # File size filter
     ├── ti_checker.py                 # Threat Intelligence lookup module
     ├── metadata_classifier.py        # Metadata-based classification logic
     ├── content_signature_checker.py  # Signature-based matching logic
     └── fuzzy_hash_analyzer.py        # ssdeep-based similarity analyzer

```

## How to Use

### Local Testing

```bash
python run_lambda.py

```

- Simulates an S3 event using `test_files/event.json`

### Deploy to AWS

1. Zip Lambda code and dependencies:
    
    ```bash
    zip -r lambda_package.zip lambda_function.py utils/ modules/ fuzzy_hash_db/
    
    ```
    
2. Upload to AWS Lambda and set an S3 event as the trigger

> Ensure the Lambda role has proper IAM policies to access the S3 bucket
> 

## Features / Main Logic

- **TI Lookup**
    
    Checks if the uploaded file matches known malicious indicators from threat intel sources
    
- **Metadata Classification**
    
    Analyzes static file properties (e.g., size, extension, MIME type) and applies rule-based classification
    
- **Content Signature Matching**
    
    Compares file contents against known malicious signature patterns
    
- **Fuzzy Hash Comparison**
    
    Uses the `ssdeep` algorithm to assess similarity to known malware samples
    
- **[+] Extensible Architecture**
    
    Additional analysis modules (e.g., AI-based, ATS) can be easily integrated into the pipeline
    

## Future Work

- Integrate AI-based content analysis
- Implement ATS (Automated Threat Scoring) module
- Provide a web frontend for file submission and result visualization

## Motivation / Impact

- Simulates a **cloud-native static malware analysis system** designed for performance, modularity, and extensibility
- Combines signature-, heuristic-, and intelligence-based methods to achieve **automated threat detection in a serverless architecture**