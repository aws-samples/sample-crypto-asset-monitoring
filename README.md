# 🔐 AWS Crypto Asset Monitoring

A sample solution for monitoring and securing AWS crypto assets across your organization using AWS services like AWS CloudTrail, AWS Config, AWS Security Hub, AWS Security Lake, Amazon Athena, and Amazon QuickSight. This example provides a foundation that you can customize and build upon to meet your specific requirements.

## 🔐 1. Project Overview

AWS Crypto Asset Monitoring provides an example framework for monitoring the security and usage of cryptographic assets across your AWS organization. This sample solution demonstrates how you can identify unused or misconfigured KMS keys, certificates, and Secrets Manager secrets, helping you maintain proper security hygiene and optimize costs.

By leveraging AWS CloudTrail, AWS Config, AWS Security Hub, AWS Security Lake, Amazon Athena, and Amazon QuickSight, this example solution demonstrates:

- How to gain visibility into crypto asset usage across your organization
- Methods for automated detection of security issues and compliance violations
- Examples of interactive dashboards for monitoring and reporting
- Sample AWS Config rules for detecting unused crypto assets that you can adapt to your needs

## 🧩 2. Solution Components

This example solution consists of the following components that you can customize and extend:

- **AWS CloudTrail**: Captures API activity related to crypto assets
- **AWS Config Rules**: Custom rules to detect unused or misconfigured crypto assets, you can use this pattern to create more config rules to meet your needs.
  - AWS Key Management Service (AWS KMS) unused keys detection
  - AWS Secrets Manager unused secrets detection
  - AWS Certificate Manager (ACM) certificates pending DNS validation
- **AWS Security Hub**: Centralizes findings from AWS Config rules
- **AWS Security Lake**: Stores and normalizes security data for analysis
- **Amazon Athena**: Queries for analyzing crypto asset usage and security events collected by AWS Security Lake
- **Amazon QuickSight**: Dashboards for visualizing crypto asset metrics

## 🔄 3. Technical Implementation Details

This solution implements a comprehensive monitoring pipeline for crypto assets:

### Data Flow Architecture

The solution implements a comprehensive monitoring pipeline with four distinct layers:

1. **Detection Layer**:
   - **AWS CloudTrail** captures all API activity related to crypto assets
   - **AWS Config** rules (implemented as AWS Lambda functions) continuously evaluate crypto assets against best practices
   - **AWS Security Hub** provides additional security checks and standards compliance evaluation

2. **Collection Layer**:
   - **AWS Security Hub** centralizes and normalizes findings from AWS Config rules
   - **AWS Security Lake** stores security data for long-term analysis and querying

3. **Analysis Layer**:
   - **Amazon Athena** queries extract specific insights from AWS Security Lake data
   - Queries target security findings, usage patterns, and compliance status of crypto assets

4. **Visualization Layer**:
   - **Amazon QuickSight** dashboards transform analyzed data into visual insights
   - Interactive visualizations help identify security issues, optimize costs, and ensure compliance

### AWS Config Rules Implementation

The custom AWS Config rules are implemented as AWS Lambda functions in Python:

- **AWS KMS Unused Keys Detection**: The `check_unused_keys.py` AWS Lambda function evaluates AWS KMS keys that haven't been used for a configurable period (default 90 days). It uses the AWS KMS API to check the `LastUsedDate` of each key and marks keys as non-compliant if they exceed the threshold.

  ```python
  # Example from check_unused_keys.py
  def evaluate_key(kms, key_id, now):
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
  ```

- **AWS Secrets Manager Unused Secrets**: The `unusedSecret.py` AWS Lambda function identifies secrets that haven't been accessed. It checks the `LastAccessedDate` of each secret and marks secrets as non-compliant if they haven't been accessed.

- **AWS Certificate Manager Validation**: The certificate validation AWS Lambda function checks for certificates with pending DNS validation, helping you identify certificates that may need attention.

### CloudFormation Templates

The solution includes multi-region AWS CloudFormation templates designed to be deployed as StackSets:

- Templates create the necessary AWS Identity and Access Management (IAM) roles with least-privilege permissions
- AWS Lambda functions are embedded directly in the templates for easy deployment
- AWS Config rules are configured to run on a schedule (default: every 24 hours)
- Parameters allow customization of thresholds and other settings

### Athena Queries

The Amazon Athena queries are designed to work with the AWS Security Lake schema:

- Queries target the `amazon_security_lake_table_*_sh_findings_2_0` tables
- They extract specific fields related to crypto assets and their compliance status
- Results can be filtered by account, region, time period, and other dimensions

## 🏗️ Architecture Diagram

![AWS Crypto Asset Monitoring Architecture](/img/arch-diagram.png)

## ✅ 3. Prerequisites

Before deploying this example solution, ensure you have:

- An AWS Organizations setup with a management account
- Administrative permissions in the management account
- AWS CloudTrail enabled in your organization
- AWS Config enabled in your organization
- AWS Security Hub enabled in your organization
- AWS Security Lake enabled in your organization
- Amazon Athena and Amazon QuickSight access

Supported AWS Regions:
- All commercial AWS regions where the required services are available

## 🚀 4. Deployment Instructions

The following instructions will help you set up this example solution. Feel free to modify these steps to better suit your specific environment and requirements.

### ☁️ 4.1 Central Account Setup

#### Enable CloudTrail at Organization Level

1. Sign in to the AWS Management Console in your organization's management account
2. Navigate to the CloudTrail console
3. Create a new organization trail with the following settings:
   - Enable for all accounts in the organization
   - Enable for all regions
   - Store logs in a centralized S3 bucket

For detailed instructions, refer to:
- [Creating an Organization Trail](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/creating-trail-organization.html)
- [Multi-Region Trail Configuration](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/receive-cloudtrail-log-files-from-multiple-regions.html)

#### Enable Security Hub at Organization Level

1. Sign in to the AWS Management Console in your organization's management account
2. Navigate to the Security Hub console
3. Enable Security Hub for the organization
4. Designate a delegated administrator account

For detailed instructions, refer to:
- [AWS Security Hub Organization Setup](https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-accounts-orgs.html)
- [Security Hub Delegated Administrator](https://docs.aws.amazon.com/securityhub/latest/userguide/designate-orgs-admin-account.html)

#### Enable Security Lake with Rollup Region

1. Sign in to the AWS Management Console in your organization's management account
2. Navigate to the Security Lake console
3. Enable Security Lake for the organization
4. Configure a rollup region for centralized data collection

For detailed instructions, refer to:
- [AWS Security Lake Organization Setup](https://docs.aws.amazon.com/security-lake/latest/userguide/getting-started-org.html)
- [Security Lake Regions Configuration](https://docs.aws.amazon.com/security-lake/latest/userguide/regions.html)

#### Enable AWS Config at Organization Level

1. Sign in to the AWS Management Console in your organization's management account
2. Navigate to the AWS Config console
3. Enable AWS Config for the organization
4. Set up an aggregator to collect data from all accounts

For detailed instructions, refer to:
- [AWS Config Organization Setup](https://docs.aws.amazon.com/config/latest/developerguide/config-rule-multi-account-deployment.html)
- [AWS Config Aggregator](https://docs.aws.amazon.com/config/latest/developerguide/aggregate-data.html)

### ⚙️ 4.2 Config Rules Deployment

This example includes sample AWS Config rules for detecting unused crypto assets. You can deploy these rules using CloudFormation StackSets to apply them across your organization, and modify them to meet your specific requirements.

#### KMS Unused Keys Detection

1. Navigate to the CloudFormation console
2. Create a new StackSet using the template: `config-rules/kms/kms-unused-multiregion.yaml`
3. Deploy the StackSet to all accounts in your organization
4. The Lambda function `config-rules/kms/check_unused_keys.py` will be deployed to evaluate KMS keys

The KMS unused keys detection rule works as follows:
- The Lambda function runs on a schedule (every 24 hours by default)
- It lists all KMS keys in the account and region
- For each customer-managed key, it checks the `LastUsedDate` metadata
- Keys that haven't been used for more than the threshold period (90 days by default) are marked as non-compliant
- Findings are sent to AWS Config and forwarded to Security Hub

You can customize the threshold period by modifying the `ThresholdDays` parameter in the CloudFormation template:

```yaml
Parameters:
  ThresholdDays:
    Type: Number
    Default: 90
    Description: Number of days after which an unused KMS key is considered non-compliant
    MinValue: 1
    MaxValue: 365
```

#### Secrets Manager Unused Secrets Detection

1. Navigate to the CloudFormation console
2. Create a new StackSet using the template: `config-rules/secretsManager/unusedSecretsConfigRule-multiregion.yaml`
3. Deploy the StackSet to all accounts in your organization
4. The Lambda function `config-rules/secretsManager/unusedSecret.py` will be deployed to evaluate Secrets Manager secrets

The Secrets Manager unused secrets detection rule:
- Evaluates all secrets in the account and region
- Checks the `LastAccessedDate` of each secret
- Marks secrets that have never been accessed or haven't been accessed recently as non-compliant
- Includes creation and last accessed dates in the finding annotation

For detailed instructions on using CloudFormation StackSets, refer to:
- [AWS CloudFormation StackSets Documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/what-is-cfnstacksets.html)
- [AWS Config Rules Deployment Guide](aws-config-rules-deployment-guide.md): Detailed instructions for deploying Config rules across your organization

### 🔍 4.3 Athena Queries Setup

This example includes sample Athena queries for analyzing crypto asset usage and security events. These queries are provided as starting points that you can customize and extend. They are organized by service:

- **AWS KMS Queries** (`athena-queries/kms/`):
  - `kms-access-denied.sql`: Identifies access denied events for AWS KMS keys
  - `kms-keys-without-autorotation.sql`: Identifies AWS KMS keys without automatic rotation enabled
  - `kms-operation.sql`: Analyzes AWS KMS operation patterns
  - `kms-unused-cmks.sql`: Identifies potentially unused customer master keys

- **AWS Certificate Manager Queries** (`athena-queries/certs/`):
  - `cert-dns-validation-pending.sql`: Identifies certificates with pending DNS validation
  - `cert-expiring-check.sql`: Identifies certificates that are expiring soon
  - `cert-operation-brkdown.sql`: Analyzes certificate operation patterns
  - `certs-issued.sql`: Lists certificates that have been issued
  - `certs-revoked.sql`: Lists certificates that have been revoked

- **AWS Secrets Manager Queries** (`athena-queries/secretsManager/`):
  - `sm-access-denied.sql`: Identifies access denied events for secrets
  - `sm-deleted.sql`: Lists secrets that have been deleted
  - `sm-get-ops.sql`: Analyzes secret retrieval operations
  - `sm-operations-brkdwn.sql`: Analyzes AWS Secrets Manager operation patterns
  - `sm-rotation-not-enabled.sql`: Identifies secrets without rotation enabled
  - `sm-unused-secrets.sql`: Identifies potentially unused secrets

These queries are designed to work with the Security Lake schema. For example, the `kms-unused-cmks.sql` query:

```sql
SELECT
  accountid,
  region,
  time_dt AS finding_time,
  REGEXP_EXTRACT(observables[1].value, 'arn:aws:kms:[^"]+') AS kms_arn,
  compliance.status AS compliance_status,
  unmapped['ProductFields.aws/config/ConfigRuleName'] AS config_rule_name,
  finding_info.created_time_dt AS config_evaluation_time
FROM amazon_security_lake_glue_db_us_east_1.amazon_security_lake_table_us_east_1_sh_findings_2_0
WHERE
  finding_info.title = 'kms-unused-key-check'
  AND compliance.status = 'FAILED';
```

This query:
- Targets the AWS Security Lake findings table
- Filters for findings from the AWS KMS unused keys AWS Config rule
- Extracts key information like account ID, region, AWS KMS ARN, and evaluation time
- Focuses on non-compliant findings (status = 'FAILED')

To use these queries:
1. Navigate to the Amazon Athena console
2. Ensure that Amazon Athena is configured to query your AWS Security Lake data
3. Copy and paste the desired query from the appropriate file
4. Run the query and analyze the results
5. Save the query results as a dataset for use in Amazon QuickSight

For detailed instructions on using Athena with Security Lake, refer to:
- [Querying Security Lake Data with Athena](https://docs.aws.amazon.com/athena/latest/ug/querying-security-lake.html)

### 📊 4.4 QuickSight Dashboard Creation

This example includes sample Amazon QuickSight dashboards for visualizing crypto asset metrics. You can use these as templates and customize them to fit your specific monitoring needs. Follow the detailed instructions in:

- [Dataset Creation Guide](amazon-quicksight-dataset-creation-guide.md): Instructions for creating QuickSight datasets from Athena queries
- [Dashboard Creation Guide](amazon-quicksight-dashboard-creation-guide.md): Instructions for creating QuickSight dashboards from the datasets

Sample dashboard images are provided for reference in the dashboard creation guide. You can view examples of:
- AWS KMS Dashboard: For monitoring AWS KMS key usage, rotation status, and access patterns
- AWS Certificate Manager Dashboard: For monitoring certificate expirations, validations, and usage patterns
- AWS Secrets Manager Dashboard: For monitoring secret usage patterns, rotation status, and access events

For additional QuickSight features and customization options, refer to:
- [Amazon QuickSight Documentation](https://docs.aws.amazon.com/quicksight/latest/user/welcome.html)

## 📖 5. Usage Guide

This section provides guidance on how you might use and extend this example solution to meet your specific monitoring needs.

### Interpreting the Dashboards

The Amazon QuickSight dashboards provide insights into the following areas:

- **AWS KMS Key Usage**: Monitor key usage patterns, identify unused keys, and detect access denied events
- **AWS Certificate Manager**: Track certificate expirations, validations, and issuance/revocation patterns
- **AWS Secrets Manager Usage**: Monitor secret usage patterns, identify unused secrets, and detect access denied events

### Common Monitoring Scenarios

- **Identifying Unused Crypto Assets**: Use the dashboards to identify KMS keys and secrets that haven't been used in a specified period
- **Detecting Access Issues**: Monitor access denied events to identify potential permission issues
- **Certificate Lifecycle Management**: Track certificate expirations and ensure timely renewal
- **Compliance Monitoring**: Ensure crypto assets are configured according to best practices (e.g., rotation enabled)

### Responding to Alerts

When the dashboards or AWS Config rules identify issues:

1. Review the details of the finding in Security Hub
2. Investigate the root cause using the provided information
3. Take appropriate remediation actions (e.g., update permissions, rotate secrets, renew certificates)
4. Document the incident and resolution for compliance purposes

## 🔧 6. Troubleshooting

### Common Issues and Solutions

As you implement and customize this example solution, you might encounter the following issues:

- **Missing Data in Dashboards**:
  - Verify that AWS CloudTrail is properly configured and logging to AWS Security Lake
  - Check that Amazon Athena queries are correctly set up to query AWS Security Lake data
  - Ensure Amazon QuickSight has appropriate permissions to access Amazon Athena

- **AWS Config Rule Failures**:
  - Check AWS Lambda function logs for error messages
  - Verify that the AWS Lambda functions have appropriate permissions
  - Ensure AWS Config is properly configured in all accounts

- **AWS Security Hub Integration Issues**:
  - Verify that AWS Security Hub is enabled in all accounts
  - Check that the delegated administrator account is properly configured
  - Ensure findings are being properly aggregated from all regions

### Support Resources

For additional support:
- Review the AWS documentation for each service
- Check AWS service quotas if you encounter limits
- Contact AWS Support for service-specific issues

## 🛠️ 7. Customization and Extension

This solution is designed to be a starting point that you can customize and extend to meet your specific requirements. Here are some ways you can adapt the solution:

### Modifying Config Rules

You can customize the AWS Config rules to adjust thresholds, add additional checks, or modify the evaluation logic:

1. **Adjust Thresholds**: 
   - Modify the `ThresholdDays` parameter in the AWS CloudFormation templates to change how long a crypto asset can remain unused before being flagged
   - Example: Change from 90 days to 30 days for more aggressive monitoring

2. **Add New Checks**:
   - Use the existing AWS Lambda functions as templates to create new checks
   - Example: Create a rule to check for AWS KMS keys with specific tags or encryption algorithms

3. **Modify Evaluation Logic**:
   - Edit the Lambda functions to change how compliance is determined
   - Example: Add exceptions for specific keys based on tags or naming conventions

### Extending Athena Queries

The provided Amazon Athena queries can be extended or modified to extract additional insights:

1. **Add Filtering Dimensions**:
   - Modify queries to filter by additional dimensions like tags, key types, or specific accounts
   - Example: Add a WHERE clause to focus on production accounts only

2. **Create Trend Analysis**:
   - Extend queries to analyze trends over time
   - Example: Compare the number of unused keys month-over-month

3. **Combine Data Sources**:
   - Join AWS Security Lake data with other data sources for richer analysis
   - Example: Join with cost data to estimate savings from removing unused keys

### Creating Custom Dashboards

You can create custom Amazon QuickSight dashboards tailored to your organization's needs:

1. **Role-Based Dashboards**:
   - Create dashboards for different roles (security teams, application teams, management)
   - Example: Executive dashboard showing high-level compliance metrics

2. **Service-Specific Dashboards**:
   - Create detailed dashboards focused on specific services
   - Example: Comprehensive AWS KMS dashboard with usage patterns, rotation status, and access issues

3. **Compliance Dashboards**:
   - Build dashboards focused on specific compliance requirements
   - Example: Dashboard showing crypto assets that don't meet your organization's security standards

## 📚 8. References

- [AWS CloudTrail Documentation](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html)
- [AWS Config Documentation](https://docs.aws.amazon.com/config/latest/developerguide/WhatIsConfig.html)
- [AWS Security Hub Documentation](https://docs.aws.amazon.com/securityhub/latest/userguide/what-is-securityhub.html)
- [AWS Security Lake Documentation](https://docs.aws.amazon.com/security-lake/latest/userguide/what-is-security-lake.html)
- [Amazon Athena Documentation](https://docs.aws.amazon.com/athena/latest/ug/what-is.html)
- [Amazon QuickSight Documentation](https://docs.aws.amazon.com/quicksight/latest/user/welcome.html)
- [AWS Key Management Service Documentation](https://docs.aws.amazon.com/kms/latest/developerguide/overview.html)
- [AWS Certificate Manager Documentation](https://docs.aws.amazon.com/acm/latest/userguide/acm-overview.html)
- [AWS Secrets Manager Documentation](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html)
- [AWS CloudFormation Documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html)
