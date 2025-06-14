# 🔐 AWS Config Rules Deployment Guide for Crypto Asset Monitoring

This guide provides an example approach for deploying AWS Config rules across multiple accounts and regions to monitor crypto assets in your AWS organization. You can customize and extend these patterns to meet your specific requirements.

## 🌐 1. AWS Config Installation Across Accounts and Regions

This sample solution demonstrates how AWS Config can be enabled across all accounts and regions in your organization to monitor crypto assets. This multi-account, multi-region approach provides visibility into your organization's security posture, which you can adapt to your specific needs.

### 🏢 Organization-wide Setup

1. **Enable AWS Config at the Organization Level**:
   - AWS Config must be enabled in the organization's management account
   - Configuration should be deployed to all member accounts
   - An aggregator should be set up to collect data from all accounts
   - [AWS Config Multi-Account Multi-Region Data Aggregation](https://docs.aws.amazon.com/config/latest/developerguide/aggregate-data.html)

2. **Multi-Region Configuration**:
   - AWS Config must be enabled in all regions where you have resources
   - Configuration recorders should be set up in each region
   - Rules should be deployed consistently across regions
   - [Setting Up AWS Config with the Console](https://docs.aws.amazon.com/config/latest/developerguide/gs-console.html)

3. **Delegated Administrator**:
   - Designate a member account as the delegated administrator for AWS Config
   - This account will have permissions to manage Config across the organization
   - Centralized management simplifies rule deployment and finding aggregation
   - [Delegated Administrator for AWS Config](https://docs.aws.amazon.com/config/latest/developerguide/config-delegated-administrator.html)

## ☁️ 2. CloudFormation Templates for Config Rules

This example solution uses CloudFormation templates to deploy custom AWS Config rules that monitor crypto assets. These sample templates demonstrate how to create rules that work across multiple regions and accounts, which you can use as a foundation for your own implementations.

### 📄 Template Structure

The CloudFormation templates (e.g., `unusedSecretsConfigRule-multiregion.yaml`) include:

1. **Parameters**:
   - `PrimaryRegion`: Specifies the region where IAM resources will be created
   - `RoleName`: Defines the name of the IAM role to be created
   - [CloudFormation Parameters](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/parameters-section-structure.html)

2. **Conditions**:
   - `IsPrimaryRegion`: Determines if the current region is the primary region
   - [CloudFormation Conditions](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/conditions-section-structure.html)

3. **Resources**:
   - **IAM Role**: Created only in the primary region
   - **Lambda Function**: Created in all regions, using the IAM role from the primary region
   - **Lambda Permission**: Allows AWS Config to invoke the Lambda function
   - **Config Rule**: Defines the rule configuration and evaluation frequency
   - [AWS Config Rules Resource Type Reference](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configrule.html)

### 🔍 Rule Implementation

The Lambda functions implement the logic for evaluating resources:

- **Unused Secrets Detection**: Identifies secrets in AWS Secrets Manager that haven't been accessed in the last 90 days
- **Certificate DNS Validation Pending**: Identifies ACM certificates that are pending DNS validation
- [Custom Lambda Rules for AWS Config](https://docs.aws.amazon.com/config/latest/developerguide/evaluate-config_develop-rules_lambda-functions.html)

These rules help maintain proper security hygiene and identify potential issues with crypto assets.

## 🔄 3. AWS Config Integration with Security Hub and Security Lake

This example shows how AWS Config findings can flow into Security Lake for security monitoring, addressing the challenge that there's no direct integration between these services.

### 🔀 Integration Flow

1. **AWS Config → Security Hub**:
   - AWS Config rules generate findings when resources are non-compliant
   - These findings are automatically sent to AWS Security Hub
   - Security Hub aggregates findings from multiple sources, including AWS Config
   - [AWS Config Integration with Security Hub](https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-standards-fsbp-controls.html)

2. **Security Hub → Security Lake**:
   - Security Hub findings are ingested into Security Lake
   - This indirect path allows Config findings to appear in Security Lake
   - Security Lake normalizes and stores the data for analysis
   - [Security Hub Integration with Security Lake](https://docs.aws.amazon.com/security-lake/latest/userguide/security-hub-integration.html)

3. **Benefits of this Approach**:
   - Centralized view of security findings across the organization
   - Standardized format for security data
   - Enhanced query capabilities through Athena integration
   - [Querying Security Lake Data](https://docs.aws.amazon.com/security-lake/latest/userguide/query-data.html)

## 👤 4. Service-Linked Role in Delegated Admin Account

This section demonstrates how to set up the service-linked roles that AWS Config requires to operate across an organization, which you can adapt for your environment.

### 🔑 Service-Linked Role Setup

1. **Purpose**:
   - Service-linked roles provide the necessary permissions for AWS Config to operate
   - These roles have predefined permissions that AWS Config requires
   - They are created automatically when you enable certain features
   - [Service-Linked Roles for AWS Config](https://docs.aws.amazon.com/config/latest/developerguide/using-service-linked-roles.html)

2. **Enabling in Delegated Admin Account**:
   - The delegated administrator account needs specific service-linked roles
   - These roles allow the account to manage Config across the organization
   - They are created automatically when you designate the delegated administrator
   - [Using Service-Linked Roles for AWS Organizations](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_integrate_services.html#orgs_integrate_services-using_slrs)

3. **Required Permissions**:
   - `AWSServiceRoleForConfig`: Allows AWS Config to call AWS services on your behalf
   - `AWSServiceRoleForOrganizations`: Allows integration with AWS Organizations
   - [AWS Managed Policies for AWS Config](https://docs.aws.amazon.com/config/latest/developerguide/security-iam-awsmanpol.html)

## 📚 5. Creating a Stack Set

This example shows how to use stack sets to deploy CloudFormation templates across multiple accounts and regions in your organization, providing a pattern you can follow for your own deployments.

### 💻 Stack Set Creation Command

#### For Unused Secrets Config Rule

```bash
aws cloudformation create-stack-set \
  --stack-set-name check-unused-secrets-org \
  --template-body file://unusedSecretsConfigRule-multiregion.yaml  \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameters \
    ParameterKey=PrimaryRegion,ParameterValue="us-east-1" \
    ParameterKey=RoleName,ParameterValue="check-unused-secrets-role" \
  --permission-model SERVICE_MANAGED \
  --auto-deployment Enabled=true,RetainStacksOnAccountRemoval=false \
  --region us-east-1
```

#### For Unused KMS Keys Config Rule

```bash
aws cloudformation create-stack-set \
  --stack-set-name unusedSecretsConfigRule-multiregion-demo \
  --template-body file://unusedSecretsConfigRule-multiregion.yaml  \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameters \
    ParameterKey=PrimaryRegion,ParameterValue="us-west-1" \
    ParameterKey=RoleName,ParameterValue="unusedSecretsConfigRule-multiregion-role" \
  --permission-model SERVICE_MANAGED \
  --auto-deployment Enabled=true,RetainStacksOnAccountRemoval=false \
  --region us-east-1
```

### 📝 Parameter Explanation

- `--stack-set-name`: Defines the name of the stack set (e.g., check-unused-secrets-org)
- `--template-body`: Specifies the local path to the CloudFormation template
- `--capabilities CAPABILITY_NAMED_IAM`: Acknowledges that the template will create named IAM resources
- `--parameters`: Provides values for the template parameters:
  - `PrimaryRegion`: Specifies the region where IAM resources will be created (e.g., "us-east-1" or "us-west-1")
  - `RoleName`: Sets the name for the IAM role
- `--permission-model SERVICE_MANAGED`: Uses the service-managed permissions model, which works with AWS Organizations
  - **Important**: When using SERVICE_MANAGED permission model, you must use the `--deployment-targets` parameter when creating stack instances
- `--auto-deployment`: Configures automatic deployment:
  - `Enabled=true`: Automatically deploys to new accounts added to the organization
  - `RetainStacksOnAccountRemoval=false`: Removes stacks when accounts leave the organization
- `--region us-east-1`: Specifies the region where the stack set is created (not where it's deployed)

[AWS CloudFormation create-stack-set Command Reference](https://docs.aws.amazon.com/cli/latest/reference/cloudformation/create-stack-set.html)

## 🚀 6. Deploying Stack Instances

This section demonstrates how to deploy stack instances to specific accounts and regions after creating a stack set, showing an approach you can customize for your organization.

### 💻 Stack Instances Deployment Command

#### For Certificate DNS Validation Pending Check

```bash
aws cloudformation create-stack-instances \
  --stack-set-name cert-dns-validation-pending-check \
  --deployment-targets 'OrganizationalUnitIds=["ou-xxxx-xxxxxxxx"]' \
  --regions us-east-1 us-east-2 us-west-2 \
  --region us-east-1
```

#### For Unused KMS Keys Check

```bash
aws cloudformation create-stack-instances \
  --stack-set-name unusedSecretsConfigRule-multiregion-demo \
  --deployment-targets 'OrganizationalUnitIds=["ou-xxxx-xxxxxxxx"]','Accounts=[111122223333]',AccountFilterType=INTERSECTION \
  --regions us-west-1 \
  --region us-east-1
```

### 📝 Command Explanation

- `--stack-set-name`: Specifies the name of the stack set to deploy
- `--deployment-targets`: Defines where to deploy the stack instances:
  - **IMPORTANT**: When using the SERVICE_MANAGED permission model, you must use the `--deployment-targets` parameter
  - `OrganizationalUnitIds=["ou-xxxx-xxxxxxxx"]`: Deploys to all accounts in the specified organizational unit
  - `Accounts=[account-id]`: Specifies individual accounts for deployment
  - `AccountFilterType=INTERSECTION`: When both OUs and accounts are specified, this deploys only to accounts that are both in the specified OU AND in the specified account list
- `--regions`: Lists the regions where the stack instances will be deployed
- `--region us-east-1`: Specifies the region where the command is executed (not where stacks are deployed)

[AWS CloudFormation create-stack-instances Command Reference](https://docs.aws.amazon.com/cli/latest/reference/cloudformation/create-stack-instances.html)

### 🔄 Alternative Deployment Options

Instead of deploying to specific OUs, you can deploy to:

1. **Specific Accounts**:
   ```bash
   --deployment-targets 'AccountIds=["111122223333","444455556666"]'
   ```

2. **All Accounts in the Organization**:
   ```bash
   --deployment-targets 'OrganizationalUnitIds=["root-id"]'
   ```

3. **Different Regions**:
   - Modify the `--regions` parameter to include different AWS regions

4. **Filtering Options with AccountFilterType**:
   - `INTERSECTION`: Deploy only to accounts that are both in the specified OU AND in the specified account list
   - `DIFFERENCE`: Deploy to accounts in the specified OU EXCEPT those in the specified account list
   - `UNION`: Deploy to ALL accounts in the specified OU AND all accounts in the specified account list
   - `NONE`: Deploy to all accounts in the specified OU regardless of the account list

[Working with Stack Sets](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/what-is-cfnstacksets.html)

## 📋 Conclusion

This example solution demonstrates one approach to deploying AWS Config rules across your organization to monitor crypto assets. You can adapt and extend this sample to fit your specific needs. The multi-account, multi-region approach shown here provides a starting point for gaining visibility into your security posture through integration with Security Hub and Security Lake.

Remember to adjust the deployment commands based on your organization's structure and requirements. You can build upon this foundation to create a monitoring system tailored to your specific crypto asset security needs.

## 📚 Additional Resources

- [AWS Config Developer Guide](https://docs.aws.amazon.com/config/latest/developerguide/WhatIsConfig.html)
- [AWS CloudFormation User Guide](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html)
- [AWS Security Hub User Guide](https://docs.aws.amazon.com/securityhub/latest/userguide/what-is-securityhub.html)
- [AWS Security Lake User Guide](https://docs.aws.amazon.com/security-lake/latest/userguide/what-is-security-lake.html)
- [AWS Organizations User Guide](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_introduction.html)
