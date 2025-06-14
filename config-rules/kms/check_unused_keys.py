import boto3
import datetime
import json
import logging
import os
from typing import Dict, List, Any, Optional

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Get configuration from environment variables with defaults
THRESHOLD_DAYS = int(os.environ.get('THRESHOLD_DAYS', 90))
BATCH_SIZE = 100  # AWS Config limit for put_evaluations

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda function to check for unused KMS keys.
    
    Args:
        event: The event dict from AWS Lambda
        context: The context object from AWS Lambda
        
    Returns:
        Dict containing the result of the evaluation
    """
    logger.info(f"Starting evaluation with threshold of {THRESHOLD_DAYS} days")
    
    try:
        evaluations = get_kms_key_evaluations()
        submit_evaluations(evaluations, event['resultToken'])
        return {"statusCode": 200, "body": json.dumps({"message": "Evaluation completed successfully"})}
    except Exception as e:
        logger.error(f"Error in lambda_handler: {str(e)}", exc_info=True)
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}

def get_kms_key_evaluations() -> List[Dict[str, Any]]:
    """
    Evaluate all customer-managed KMS keys for usage.
    
    Returns:
        List of evaluation results for AWS Config
    """
    kms = boto3.client('kms')
    now = datetime.datetime.utcnow()
    evaluations = []
    
    paginator = kms.get_paginator('list_keys')
    for page in paginator.paginate():
        for key in page['Keys']:
            key_id = key['KeyId']
            try:
                evaluation = evaluate_key(kms, key_id, now)
                if evaluation:
                    evaluations.append(evaluation)
            except Exception as e:
                logger.error(f"Error processing key {key_id}: {str(e)}", exc_info=True)
    
    return evaluations

def evaluate_key(kms, key_id: str, now: datetime.datetime) -> Optional[Dict[str, Any]]:
    """
    Evaluate a single KMS key for compliance.
    
    Args:
        kms: The KMS client
        key_id: The ID of the key to evaluate
        now: The current time for comparison
        
    Returns:
        Evaluation result dict or None if key should be skipped
    """
    metadata = kms.describe_key(KeyId=key_id)['KeyMetadata']
    
    # Skip keys that are not customer-managed or not enabled
    if metadata['KeyManager'] != 'CUSTOMER' or metadata['KeyState'] != 'Enabled':
        return None
    
    last_used_date = metadata.get('LastUsedDate')
    if not last_used_date:
        compliance = 'NON_COMPLIANT'
        annotation = "Key has never been used."
    else:
        age = (now - last_used_date.replace(tzinfo=None)).days
        if age > THRESHOLD_DAYS:
            compliance = 'NON_COMPLIANT'
            annotation = f"Key has not been used for {age} days."
        else:
            compliance = 'COMPLIANT'
            annotation = f"Key used {age} days ago."
    
    return {
        'ComplianceResourceType': 'AWS::KMS::Key',
        'ComplianceResourceId': key_id,
        'ComplianceType': compliance,
        'Annotation': annotation,
        'OrderingTimestamp': now
    }

def submit_evaluations(evaluations: List[Dict[str, Any]], result_token: str) -> None:
    """
    Submit evaluation results to AWS Config in batches.
    
    Args:
        evaluations: List of evaluation results
        result_token: The result token from the AWS Config event
    """
    config = boto3.client('config')
    
    # Submit evaluations in batches of 100 (AWS Config limit)
    for i in range(0, len(evaluations), BATCH_SIZE):
        batch = evaluations[i:i + BATCH_SIZE]
        logger.info(f"Submitting batch of {len(batch)} evaluations")
        config.put_evaluations(
            Evaluations=batch,
            ResultToken=result_token
        )
