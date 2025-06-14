# 🔐 AWS Crypto Asset Monitoring

A sample solution for monitoring and securing AWS crypto assets across your organization using AWS Security services, Athena queries, and QuickSight dashboards. This example provides a foundation that you can customize and build upon to meet your specific requirements.

## 🔐 1. Project Overview

AWS Crypto Asset Monitoring provides an example framework for monitoring the security and usage of cryptographic assets across your AWS organization. This sample solution demonstrates how you can identify unused or misconfigured KMS keys, certificates, and Secrets Manager secrets, helping you maintain proper security hygiene and optimize costs.

By leveraging AWS CloudTrail, AWS Config, Security Hub, Security Lake, Athena, and QuickSight, this example solution demonstrates:

- How to gain visibility into crypto asset usage across your organization
- Methods for automated detection of security issues and compliance violations
- Examples of interactive dashboards for monitoring and reporting
- Sample AWS Config rules for detecting unused crypto assets that you can adapt to your needs

## 🧩 2. Solution Components

This example solution consists of the following components that you can customize and extend:

- **AWS CloudTrail**: Captures API activity related to crypto assets
- **AWS Config Rules**: Custom rules to detect unused or misconfigured crypto assets, you can use this pattern to create more config rules to meet your needs.
  - KMS unused keys detection
  - Secrets Manager unused secrets detection
  - Certificates pending DNS validation
- **AWS Security Hub**: Centralizes findings from AWS Config rules
- **AWS Security Lake**: Stores and normalizes security data for analysis
- **Amazon Athena**: Queries for analyzing crypto asset usage and security events collected by Security Lake
- **Amazon QuickSight**: Dashboards for visualizing crypto asset metrics

## 🏗️ Architecture Diagram

![AWS Crypto Asset Monitoring Architecture](/img/arch-diagram.png)

## ✅ 3. Prerequisites

Before deploying this example solution, ensure you have:

- An AWS Organizations setup with a management account
- Administrative permissions in the management account
- AWS CloudTrail enabled in your organization
- AWS Config enabled in your organization
- Security Hub enabled in your organization
- Security Lake enabled in your organization
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

#### Secrets Manager Unused Secrets Detection

1. Navigate to the CloudFormation console
2. Create a new StackSet using the template: `config-rules/secretsManager/unusedSecretsConfigRule-multiregion.yaml`
3. Deploy the StackSet to all accounts in your organization
4. The Lambda function `config-rules/secretsManager/unusedSecret.py` will be deployed to evaluate Secrets Manager secrets

For detailed instructions on using CloudFormation StackSets, refer to:
- [AWS CloudFormation StackSets Documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/what-is-cfnstacksets.html)

### 🔍 4.3 Athena Queries Setup

This example includes sample Athena queries for analyzing crypto asset usage and security events. These queries are provided as starting points that you can customize and extend. They are organized by service:

- **KMS Queries** (`athena-queries/kms/`):
  - `kms-access-denied.sql`: Identifies access denied events for KMS keys
  - `kms-keys-without-autorotation.sql`: Identifies KMS keys without automatic rotation enabled
  - `kms-operation.sql`: Analyzes KMS operation patterns
  - `kms-unused-cmks.sql`: Identifies potentially unused customer master keys

- **Certificate Manager Queries** (`athena-queries/certs/`):
  - `cert-dns-validation-pending.sql`: Identifies certificates with pending DNS validation
  - `cert-expiring-check.sql`: Identifies certificates that are expiring soon
  - `cert-operation-brkdown.sql`: Analyzes certificate operation patterns
  - `certs-issued.sql`: Lists certificates that have been issued
  - `certs-revoked.sql`: Lists certificates that have been revoked

- **Secrets Manager Queries** (`athena-queries/secretsManager/`):
  - `sm-access-denied.sql`: Identifies access denied events for secrets
  - `sm-deleted.sql`: Lists secrets that have been deleted
  - `sm-get-ops.sql`: Analyzes secret retrieval operations
  - `sm-operations-brkdwn.sql`: Analyzes Secrets Manager operation patterns
  - `sm-rotation-not-enabled.sql`: Identifies secrets without rotation enabled
  - `sm-unused-secrets.sql`: Identifies potentially unused secrets

To use these queries:
1. Navigate to the Athena console
2. Ensure that Athena is configured to query your Security Lake data
3. Copy and paste the desired query from the appropriate file
4. Run the query and analyze the results

For detailed instructions on using Athena with Security Lake, refer to:
- [Querying Security Lake Data with Athena](https://docs.aws.amazon.com/athena/latest/ug/querying-security-lake.html)

### 📊 4.4 QuickSight Dashboard Creation

This example includes sample QuickSight dashboards for visualizing crypto asset metrics. You can use these as templates and customize them to fit your specific monitoring needs. Follow the detailed instructions in:

- [Dataset Creation Guide](amazon-quicksight-dataset-creation-guide.md): Instructions for creating QuickSight datasets from Athena queries
- [Dashboard Creation Guide](amazon-quicksight-dashboard-creation-guide.md): Instructions for creating QuickSight dashboards from the datasets

Sample dashboard PDFs are provided for reference:
- [KMS Dashboard](quicksight/dashboard/KMS-dashboard.pdf): Sample dashboard for KMS key monitoring
- [Certificate Manager Dashboard](quicksight/dashboard/certs-dashboard.pdf): Sample dashboard for certificate monitoring
- [Secrets Manager Dashboard](quicksight/dashboard/Secrets_Manager_dashboard.pdf): Sample dashboard for secrets monitoring

For additional QuickSight features and customization options, refer to:
- [Amazon QuickSight Documentation](https://docs.aws.amazon.com/quicksight/latest/user/welcome.html)

## 📖 5. Usage Guide

This section provides guidance on how you might use and extend this example solution to meet your specific monitoring needs.

### Interpreting the Dashboards

The QuickSight dashboards provide insights into the following areas:

- **KMS Key Usage**: Monitor key usage patterns, identify unused keys, and detect access denied events
- **Certificate Management**: Track certificate expirations, validations, and issuance/revocation patterns
- **Secrets Manager Usage**: Monitor secret usage patterns, identify unused secrets, and detect access denied events

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
  - Verify that CloudTrail is properly configured and logging to Security Lake
  - Check that Athena queries are correctly set up to query Security Lake data
  - Ensure QuickSight has appropriate permissions to access Athena

- **AWS Config Rule Failures**:
  - Check Lambda function logs for error messages
  - Verify that the Lambda functions have appropriate permissions
  - Ensure AWS Config is properly configured in all accounts

- **Security Hub Integration Issues**:
  - Verify that Security Hub is enabled in all accounts
  - Check that the delegated administrator account is properly configured
  - Ensure findings are being properly aggregated from all regions

### Support Resources

For additional support:
- Review the AWS documentation for each service
- Check AWS service quotas if you encounter limits
- Contact AWS Support for service-specific issues

## 📚 7. References

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
