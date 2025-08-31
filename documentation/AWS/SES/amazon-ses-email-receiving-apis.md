# Amazon SES Email Receiving API Endpoints Documentation

This document provides comprehensive documentation for all Amazon SES email receiving related API endpoints.

## Table of Contents
1. [Receipt Rule Set Management](#receipt-rule-set-management)
2. [Receipt Rule Management](#receipt-rule-management)
3. [IP Filter Management](#ip-filter-management)
4. [Email Receiving Actions](#email-receiving-actions)
5. [Active Rule Set Management](#active-rule-set-management)

---

## Receipt Rule Set Management

### CreateReceiptRuleSet
**Purpose**: Creates an empty receipt rule set.

**Required Parameters**:
- `RuleSetName` (String): The name of the rule set to create

**Optional Parameters**: None

**Integration Possibilities**:
- Used as the initial step before creating receipt rules
- Can create multiple rule sets but only one can be active at a time

---

### CloneReceiptRuleSet
**Purpose**: Creates a receipt rule set by cloning an existing one. All receipt rules and configurations are copied to the new receipt rule set.

**Required Parameters**:
- `OriginalRuleSetName` (String): The name of the rule set to clone
- `RuleSetName` (String): The name of the new rule set to create

**Optional Parameters**: None

**Integration Possibilities**:
- Useful for creating backup or test versions of existing rule sets
- Allows rapid deployment of similar configurations

---

### DeleteReceiptRuleSet
**Purpose**: Deletes the specified receipt rule set that is not currently active. Also deletes all receipt rules it contains.

**Required Parameters**:
- `RuleSetName` (String): The name of the receipt rule set to delete

**Optional Parameters**: None

**Integration Possibilities**:
- Cannot delete the currently active rule set
- Must disable email receiving or activate another rule set first

---

### ListReceiptRuleSets
**Purpose**: Lists the receipt rule sets that exist under your AWS account in the current AWS Region.

**Required Parameters**: None

**Optional Parameters**:
- `NextToken` (String): Token for pagination from previous call

**Response Elements**:
- `RuleSets` (Array): Array of ReceiptRuleSetMetadata objects
- `NextToken` (String): Token for retrieving additional results

**Integration Possibilities**:
- Supports pagination for handling large numbers of rule sets
- Returns metadata including creation timestamps

---

### DescribeReceiptRuleSet
**Purpose**: Returns the details of the specified receipt rule set.

**Required Parameters**:
- `RuleSetName` (String): The name of the receipt rule set to describe

**Optional Parameters**: None

**Response Elements**:
- `Metadata` (Object): Rule set metadata
- `Rules` (Array): List of receipt rules in the rule set

**Integration Possibilities**:
- Provides complete rule set configuration for backup or analysis
- Includes all rules and their actions

---

## Receipt Rule Management

### CreateReceiptRule
**Purpose**: Creates a receipt rule with specified actions, recipients, and configuration.

**Required Parameters**:
- `RuleSetName` (String): The rule set to add this rule to
- `Rule` (Object): Rule configuration including:
  - `Name` (String): Rule name
  - `Enabled` (Boolean): Whether the rule is active
  - `TlsPolicy` (String): "Require" or "Optional"
  - `Recipients` (Array): Email addresses/domains
  - `Actions` (Array): Actions to perform
  - `ScanEnabled` (Boolean): Enable spam/virus scanning

**Optional Parameters**:
- `After` (String): Name of existing rule to place this rule after

**Integration Possibilities**:
- Supports multiple actions per rule
- Can be positioned in specific order within rule set

---

### UpdateReceiptRule
**Purpose**: Updates an existing receipt rule.

**Required Parameters**:
- `RuleSetName` (String): The rule set containing the rule
- `Rule` (Object): Updated rule configuration

**Optional Parameters**: None

**Integration Possibilities**:
- Allows modification of all rule properties
- Maintains rule position in the rule set

---

### DeleteReceiptRule
**Purpose**: Deletes the specified receipt rule.

**Required Parameters**:
- `RuleName` (String): The name of the rule to delete
- `RuleSetName` (String): The rule set containing the rule

**Optional Parameters**: None

**Integration Possibilities**:
- Removes rule from the active processing chain
- Does not affect other rules in the set

---

### DescribeReceiptRule
**Purpose**: Returns the details of the specified receipt rule.

**Required Parameters**:
- `RuleName` (String): The name of the receipt rule
- `RuleSetName` (String): The rule set containing the rule

**Optional Parameters**: None

**Response Elements**:
- `Rule` (Object): Complete rule configuration

**Integration Possibilities**:
- Useful for rule validation and debugging
- Returns all actions and settings

---

### ReorderReceiptRuleSet
**Purpose**: Reorders the receipt rules within a receipt rule set.

**Required Parameters**:
- `RuleSetName` (String): The rule set to reorder
- `RuleNames` (Array): Ordered list of all rule names

**Optional Parameters**: None

**Integration Possibilities**:
- Must include all rules in the rule set
- Changes processing order of rules

---

## IP Filter Management

### CreateReceiptFilter
**Purpose**: Creates a new IP address filter to allow or block emails from specific IP addresses or ranges.

**Required Parameters**:
- `Filter` (Object):
  - `Name` (String): Filter name
  - `IpFilter` (Object):
    - `Cidr` (String): IP address or range (CIDR notation)
    - `Policy` (String): "Allow" or "Block"

**Optional Parameters**: None

**Integration Possibilities**:
- Works at the connection level before receipt rules
- Can block spam sources or allow trusted IPs

---

### ListReceiptFilters
**Purpose**: Lists all IP address filters associated with your AWS account.

**Required Parameters**: None

**Optional Parameters**: None

**Response Elements**:
- `Filters` (Array): List of ReceiptFilter objects

**Integration Possibilities**:
- No pagination needed (typically small number of filters)
- Returns complete filter configurations

---

### DeleteReceiptFilter
**Purpose**: Deletes the specified IP address filter.

**Required Parameters**:
- `FilterName` (String): The name of the filter to delete

**Optional Parameters**: None

**Integration Possibilities**:
- Immediately stops filtering for that IP range
- Does not affect receipt rules

---

## Email Receiving Actions

### S3Action
**Purpose**: Saves received emails to an Amazon S3 bucket.

**Parameters**:
- `BucketName` (String, Required): S3 bucket name
- `ObjectKeyPrefix` (String, Optional): Prefix for S3 object keys
- `KmsKeyArn` (String, Optional): KMS key for encryption
- `IamRoleArn` (String, Optional): IAM role for cross-account access
- `TopicArn` (String, Optional): SNS topic for notifications

**Integration Possibilities**:
- Stores complete email including headers and attachments
- Supports encryption and cross-account access
- Can trigger Lambda via S3 events

---

### LambdaAction
**Purpose**: Invokes an AWS Lambda function with email metadata.

**Parameters**:
- `FunctionArn` (String, Required): Lambda function ARN
- `InvocationType` (String, Optional): "Event" (async) or "RequestResponse" (sync)
- `TopicArn` (String, Optional): SNS topic for notifications

**Integration Possibilities**:
- Enables custom email processing logic
- Can control mail flow with sync invocation
- Lambda receives email metadata and can fetch from S3

---

### SNSAction
**Purpose**: Publishes the complete email content to an Amazon SNS topic.

**Parameters**:
- `TopicArn` (String, Required): SNS topic ARN
- `Encoding` (String, Optional): "UTF-8" or "Base64"

**Integration Possibilities**:
- Limited to 150KB emails
- Enables fan-out to multiple subscribers
- Good for email notifications and alerts

---

### BounceAction
**Purpose**: Returns a bounce response to the sender.

**Parameters**:
- `SmtpReplyCode` (String, Required): SMTP reply code
- `Message` (String, Required): Bounce message
- `Sender` (String, Required): Bounce sender address
- `StatusCode` (String, Optional): Enhanced status code
- `TopicArn` (String, Optional): SNS topic for notifications

**Integration Possibilities**:
- Rejects unwanted emails at SMTP level
- Can provide custom bounce messages
- Useful for blocking specific recipients

---

### WorkmailAction
**Purpose**: Delivers the email to Amazon WorkMail.

**Parameters**:
- `OrganizationArn` (String, Required): WorkMail organization ARN
- `TopicArn` (String, Optional): SNS topic for notifications

**Integration Possibilities**:
- Integrates with WorkMail for corporate email
- Maintains WorkMail features like calendaring
- Requires WorkMail setup

---

### AddHeaderAction
**Purpose**: Adds a custom header to the received email.

**Parameters**:
- `HeaderName` (String, Required): Header name to add
- `HeaderValue` (String, Required): Header value

**Integration Possibilities**:
- Useful for email tracking and classification
- Often combined with other actions
- Can add multiple headers with multiple actions

---

### StopAction
**Purpose**: Terminates the evaluation of the receipt rule set.

**Parameters**:
- `Scope` (String, Required): "RuleSet"
- `TopicArn` (String, Optional): SNS topic for notifications

**Integration Possibilities**:
- Prevents further rule processing
- Useful for high-priority rules
- Can still send notifications

---

## Active Rule Set Management

### SetActiveReceiptRuleSet
**Purpose**: Sets the specified receipt rule set as the active receipt rule set.

**Required Parameters**:
- `RuleSetName` (String, Optional): Name of rule set to activate (null to disable)

**Optional Parameters**: None

**Integration Possibilities**:
- Only one rule set can be active at a time
- Setting to null disables all email receiving
- Changes take effect immediately

---

### DescribeActiveReceiptRuleSet
**Purpose**: Returns the metadata and receipt rules for the currently active receipt rule set.

**Required Parameters**: None

**Optional Parameters**: None

**Response Elements**:
- `Metadata` (Object): Active rule set metadata
- `Rules` (Array): List of rules in the active set

**Integration Possibilities**:
- Useful for monitoring current configuration
- Returns null if no rule set is active
- Shows complete active email receiving setup

---

## Important Notes

1. **Rate Limits**: Most operations can be executed no more than once per second.

2. **Region Specific**: Email receiving is only available in certain AWS regions.

3. **Prerequisites**:
   - Verified domain in Amazon SES
   - MX record pointing to SES endpoint
   - IAM permissions for SES to access other services

4. **Email Size Limits**:
   - Maximum email size (including headers): 40MB for S3 storage
   - Maximum email size for SNS: 150KB
   - Lambda synchronous invocation timeout: 30 seconds

5. **Processing Order**:
   - IP filters are evaluated first
   - Receipt rules are evaluated in order within the active rule set
   - First matching rule's actions are executed
   - Use StopAction to prevent further rule evaluation

6. **Action Limits**:
   - Multiple actions can be added to a single rule
   - Actions are executed in the order specified
   - All actions must succeed for the email to be considered successfully processed