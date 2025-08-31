# Amazon SES Monitoring and Statistics APIs - Complete Documentation

## Overview
This document provides comprehensive information about all Amazon SES monitoring and analytics related API endpoints, including both SES v1 and v2 APIs.

## Table of Contents
1. [Send Statistics APIs](#send-statistics-apis)
2. [Configuration and Event Monitoring APIs](#configuration-and-event-monitoring-apis)
3. [Receipt Rule Monitoring APIs](#receipt-rule-monitoring-apis)
4. [SES v2 Advanced Monitoring APIs](#ses-v2-advanced-monitoring-apis)
5. [CloudWatch Integration](#cloudwatch-integration)

---

## Send Statistics APIs

### 1. GetSendStatistics
**Purpose**: Provides sending statistics for the current AWS Region, returning data points representing the last two weeks of sending activity.

**Endpoint**: Classic SES API
**Rate Limit**: Maximum once per second

**Request Parameters**: None

**Response Elements**:
- `SendDataPoints.member.N`: Array of SendDataPoint objects
  - Each data point represents a 15-minute interval
  - Contains statistics for that period

**Metrics Provided**:
- Send attempts
- Bounces
- Complaints
- Delivery attempts
- Rejects
- Timestamp for each 15-minute interval

---

### 2. GetSendQuota
**Purpose**: Provides the sending limits for the Amazon SES account.

**Endpoint**: Classic SES API
**Rate Limit**: Maximum once per second

**Request Parameters**: None

**Response Elements**:
- `Max24HourSend` (Double): Maximum number of emails allowed in 24 hours
  - Value of "-1" indicates unlimited quota
- `MaxSendRate` (Double): Maximum emails per second SES can accept
  - Actual acceptance rate may be lower
- `SentLast24Hours` (Double): Number of emails sent in previous 24 hours

---

## Configuration and Event Monitoring APIs

### 3. ListConfigurationSets
**Purpose**: Lists all configuration sets associated with your Amazon SES account in the current AWS Region.

**Rate Limit**: Maximum once per second

**Request Parameters**:
- `NextToken` (optional): Pagination token
- `MaxItems` (optional): Maximum number of configuration sets to return (up to 1000)

**Response Elements**:
- List of configuration sets
- NextToken for pagination if more results exist

---

### 4. DescribeConfigurationSet
**Purpose**: Returns detailed information about a specific configuration set including event destinations.

**Rate Limit**: Maximum once per second

**Request Parameters**:
- `ConfigurationSetName` (required): Name of the configuration set
- `ConfigurationSetAttributeNames` (optional): List of attributes to retrieve
  - eventDestinations
  - trackingOptions
  - deliveryOptions
  - reputationOptions

**Response Elements**:
- `ConfigurationSet`: Configuration set details
- `EventDestinations`: List of event destinations (CloudWatch, SNS, Kinesis Firehose)
- `TrackingOptions`: Custom domain settings for tracking
- `DeliveryOptions`: TLS requirements
- `ReputationOptions`: Reputation tracking settings

---

### 5. GetConfigurationSetEventDestinations (SES v2)
**Purpose**: Retrieves a list of event destinations associated with a configuration set.

**Endpoint**: `/v2/email/configuration-sets/{ConfigurationSetName}/event-destinations`
**Method**: GET

**Event Types Monitored**:
- SEND - Email send attempts
- REJECT - Emails rejected due to content issues
- BOUNCE - Hard bounces
- COMPLAINT - Spam complaints
- DELIVERY - Successful deliveries
- OPEN - Email opens
- CLICK - Link clicks
- RENDERING_FAILURE - Template rendering failures
- DELIVERY_DELAY - Temporary delivery issues
- SUBSCRIPTION - Subscription preference changes

**Supported Destinations**:
- Amazon CloudWatch
- Amazon EventBridge
- Amazon Kinesis Firehose
- Amazon Pinpoint
- Amazon SNS

---

## Receipt Rule Monitoring APIs

### 6. DescribeActiveReceiptRuleSet
**Purpose**: Returns metadata and receipt rules for the currently active receipt rule set.

**Rate Limit**: Maximum once per second

**Request Parameters**: None

**Response Elements**:
- `Metadata`: 
  - Rule set name
  - Creation timestamp
- `Rules`: Array of ReceiptRule objects containing:
  - Recipients
  - Actions
  - Enabled status
  - TLS policy

---

### 7. DescribeReceiptRule
**Purpose**: Returns details of a specific receipt rule.

**Rate Limit**: Maximum once per second

**Request Parameters**:
- `RuleName` (required): Name of the receipt rule
- `RuleSetName` (required): Name of the rule set containing the rule

**Response Elements**:
- Rule name
- Actions to perform
- Recipients and domains
- Enabled status
- Scan status
- TLS policy

---

### 8. ListReceiptRuleSets
**Purpose**: Lists all receipt rule sets under your AWS account.

**Rate Limit**: Maximum once per second

**Request Parameters**:
- `NextToken` (optional): Pagination token

**Response Elements**:
- List of receipt rule sets
- NextToken for pagination

---

## SES v2 Advanced Monitoring APIs

### 9. GetAccount (SES v2)
**Purpose**: Retrieves comprehensive account-level information and capabilities.

**Endpoint**: `/v2/email/account`
**Method**: GET

**Monitoring Data Provided**:
- **Account Status**:
  - Production access state
  - Reputation status (HEALTHY, PROBATION, SHUTDOWN)
  - Sending enabled/disabled status
- **Send Quota Details**:
  - Max24HourSend
  - MaxSendRate
  - SentLast24Hours
- **Advanced Features**:
  - VDM (Virtual Deliverability Manager) attributes
  - Engagement metrics
  - Suppression attributes
  - Dedicated IP settings

---

### 10. GetBlacklistReports (SES v2)
**Purpose**: Checks if your dedicated IP addresses appear on email blacklists.

**Endpoint**: `/v2/email/deliverability-dashboard/blacklist-report`
**Method**: GET

**Request Parameters**:
- `BlacklistItemNames` (required): List of dedicated IP addresses to check

**Response Elements**:
- Blacklist description
- Listing time
- RBL (Real-time Blackhole List) name

---

### 11. GetMessageInsights (SES v2)
**Purpose**: Provides detailed information about a specific message including events.

**Endpoint**: `/v2/email/insights/{MessageId}/`
**Method**: GET
**Rate Limit**: Maximum once per second

**Request Parameters**:
- `MessageId` (required): Unique message identifier

**Response Elements**:
- `FromEmailAddress`: Sender address
- `Subject`: Email subject
- `EmailTags`: Applied tags
- `Insights`: Detailed event tracking including:
  - Bounce details (type, subtype, diagnostic code)
  - Complaint information
  - Delivery status
  - ISP information

---

### 12. BatchGetMetricData (SES v2)
**Purpose**: Retrieves batches of metric data for your sending activity.

**Endpoint**: `/v2/email/metrics/batch`
**Method**: POST
**Rate Limits**: 
- 16 API calls per second
- 160 queries per second (cumulative)

**Available Metrics**:
- SEND
- COMPLAINT
- PERMANENT_BOUNCE
- TRANSIENT_BOUNCE
- OPEN
- CLICK
- DELIVERY
- DELIVERY_OPEN
- DELIVERY_CLICK
- DELIVERY_COMPLAINT

**Dimensions**:
- EMAIL_IDENTITY
- CONFIGURATION_SET
- ISP

**Request Structure**:
```json
{
  "Queries": [
    {
      "Id": "query1",
      "Namespace": "VDM",
      "Metric": "DELIVERY",
      "Dimensions": {
        "EMAIL_IDENTITY": "example.com"
      },
      "StartDate": "2023-01-01T00:00:00Z",
      "EndDate": "2023-01-31T23:59:59Z"
    }
  ]
}
```

---

### 13. GetDomainStatisticsReport (SES v2)
**Purpose**: Retrieves inbox placement and engagement rates for sending domains.

**Request Parameters**:
- `Domain` (required): The domain to get statistics for
- `StartDate` (required): Start date in Unix time
- `EndDate` (required): End date in Unix time

**Metrics Provided**:
- Inbox placement rates
- Engagement metrics
- Domain reputation data

---

### 14. GetSuppressedDestination (SES v2)
**Purpose**: Retrieves information about a specific email address on the suppression list.

**Endpoint**: `/v2/email/suppression/addresses/{EmailAddress}`
**Method**: GET

**Response Elements**:
- Email address
- Reason for suppression
- Last update time

---

### 15. ListSuppressedDestinations (SES v2)
**Purpose**: Lists all email addresses on the suppression list.

**Endpoint**: `/v2/email/suppression/addresses`
**Method**: GET

**Request Parameters**:
- `StartDate` (optional): Filter for addresses added after this date
- `EndDate` (optional): Filter for addresses added before this date
- `Reason` (optional): Filter by suppression reason (BOUNCE, COMPLAINT)
- `PageSize` (optional): Number of results per page
- `NextToken` (optional): Pagination token

---

### 16. GetDeliverabilityDashboardOptions (SES v2)
**Purpose**: Retrieves status of the Deliverability Dashboard feature.

**Features When Enabled**:
- Access to reputation metrics
- Deliverability metrics for domains
- Predictive inbox placement tests
- Blacklist monitoring
- Domain authentication status

---

## CloudWatch Integration

### Event Publishing to CloudWatch
Amazon SES can publish the following event types to CloudWatch:

1. **Email Sending Events**:
   - Send attempts
   - Rejects
   - Bounces (hard and soft)
   - Complaints
   - Deliveries
   - Delivery delays

2. **Engagement Events**:
   - Opens (HTML emails only)
   - Clicks
   - Unsubscribes

### CloudWatch Metrics Levels

1. **Account-Level Metrics** (Automatic):
   - Published automatically across entire AWS account
   - Accessed via GetSendStatistics API
   - Basic sending metrics

2. **Fine-Grained Metrics** (Configuration Required):
   - Categorized by message tags
   - Requires configuration set with CloudWatch event destination
   - Custom dimensions available

### CloudWatch API for SES Metrics
```bash
# Example: Retrieve click metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/SES \
  --metric-name Click \
  --statistics Sum \
  --period 86400 \
  --start-time 2023-01-01T00:00:00Z \
  --end-time 2023-12-31T23:59:59Z \
  --dimensions Name=MessageTag,Value=campaign=summer2023
```

---

## Best Practices for Monitoring

1. **Regular Monitoring**:
   - Check sending statistics daily
   - Monitor bounce and complaint rates
   - Track reputation metrics

2. **Set Up Alarms**:
   - Bounce rate > 5%
   - Complaint rate > 0.1%
   - Sending quota usage > 80%

3. **Use Configuration Sets**:
   - Enable fine-grained tracking
   - Separate campaigns for better analytics
   - Track custom metrics with message tags

4. **Leverage Event Publishing**:
   - Real-time event streaming
   - Integration with other AWS services
   - Custom processing pipelines

5. **Monitor Suppression List**:
   - Regular review of suppressed addresses
   - Understand suppression reasons
   - Implement re-engagement strategies

---

## Rate Limits Summary

| API Endpoint | Rate Limit |
|--------------|------------|
| GetSendStatistics | 1 per second |
| GetSendQuota | 1 per second |
| DescribeConfigurationSet | 1 per second |
| ListConfigurationSets | 1 per second |
| DescribeActiveReceiptRuleSet | 1 per second |
| GetMessageInsights | 1 per second |
| BatchGetMetricData | 16 per second (160 queries/sec) |

---

## SDK Support

All APIs are supported across:
- AWS CLI
- AWS SDK for .NET
- AWS SDK for Java
- AWS SDK for JavaScript/Node.js
- AWS SDK for Python (Boto3)
- AWS SDK for PHP
- AWS SDK for Ruby
- AWS SDK for Go
- AWS SDK for C++
- AWS Tools for PowerShell

---

## Additional Resources

- [Amazon SES Developer Guide - Monitoring](https://docs.aws.amazon.com/ses/latest/dg/monitor-sending-activity.html)
- [Amazon SES API Reference](https://docs.aws.amazon.com/ses/latest/APIReference/Welcome.html)
- [Amazon SES API v2 Reference](https://docs.aws.amazon.com/ses/latest/APIReference-V2/Welcome.html)
- [CloudWatch Metrics for Amazon SES](https://docs.aws.amazon.com/ses/latest/dg/event-publishing-retrieving-cloudwatch.html)