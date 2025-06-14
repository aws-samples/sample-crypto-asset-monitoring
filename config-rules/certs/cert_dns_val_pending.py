import boto3
import json

acm = boto3.client('acm')

def lambda_handler(event, context):
    evaluations = []
    response = acm.list_certificates(CertificateStatuses=['PENDING_VALIDATION'])
    for cert_summary in response['CertificateSummaryList']:
        cert_arn = cert_summary['CertificateArn']
        cert_details = acm.describe_certificate(CertificateArn=cert_arn)
        cert = cert_details['Certificate']
        
        if (cert['Type'] == 'AMAZON_ISSUED' and
            cert['Status'] == 'PENDING_VALIDATION' and
            cert['DomainValidationOptions'][0]['ValidationMethod'] == 'DNS'):
            
            evaluations.append({
                'ComplianceResourceType': 'AWS::ACM::Certificate',
                'ComplianceResourceId': cert_arn,
                'ComplianceType': 'NON_COMPLIANT',
                'Annotation': 'Public ACM cert is pending DNS validation',
                'OrderingTimestamp': cert['CreatedAt']
            })

    # Default case when no non-compliant resources found
    if not evaluations:
        evaluations.append({
            'ComplianceResourceType': 'AWS::::Account',
            'ComplianceResourceId': event['accountId'],
            'ComplianceType': 'COMPLIANT',
            'OrderingTimestamp': json.loads(event['invokingEvent'])['notificationCreationTime']
        })

    config = boto3.client('config')
    config.put_evaluations(
        Evaluations=evaluations,
        ResultToken=event['resultToken']
    )
