import boto3
import datetime
import json

config = boto3.client('config')
secrets = boto3.client('secretsmanager')

def lambda_handler(event, context):
    invoking = json.loads(event['invokingEvent'])
    mtype = invoking.get('messageType')

    evaluations = []
    now = datetime.datetime.now(datetime.timezone.utc)

    if mtype == 'ScheduledNotification':
        # Periodic mode: scan all secrets in region
        paginator = secrets.get_paginator('list_secrets')
        for page in paginator.paginate():
            for s in page.get('SecretList', []):
                arn = s['ARN']
                evaluations.append(evaluate_secret(arn, now))
    else:
        # Config change-triggered
        ci = invoking.get('configurationItem')
        if ci and ci.get('resourceType') == 'AWS::SecretsManager::Secret':
            arn = ci['ARN']
            evaluations.append(evaluate_secret(arn, now))
        else:
            # No applicable resource—return nothing
            pass

    # Send all evaluations
    if evaluations:
        config.put_evaluations(
            Evaluations=evaluations,
            ResultToken=event['resultToken']
        )


def evaluate_secret(secret_arn, now):
    try:
        resp = secrets.describe_secret(SecretId=secret_arn)
        created = resp.get('CreatedDate')
        last = resp.get('LastAccessedDate')

        annotation = []
        if created:
            annotation.append(f"Created: {created.strftime('%Y-%m-%d')}")
        else:
            annotation.append("No creation date")

        if last:
            days = (now - last).days
            annotation.append(f"Last accessed: {days} days ago")
            comp = 'NON_COMPLIANT' if days > 1 else 'COMPLIANT'
        else:
            comp = 'NON_COMPLIANT'
            annotation.append("Never accessed")

    except Exception as e:
        comp = 'NON_COMPLIANT'
        annotation = [f"Error: {str(e)}"]

    return {
        'ComplianceResourceType': 'AWS::SecretsManager::Secret',
        'ComplianceResourceId': secret_arn.split(':secret:')[-1],
        'ComplianceType': comp,
        'Annotation': ' | '.join(annotation)[:256],
        'OrderingTimestamp': now
    }
