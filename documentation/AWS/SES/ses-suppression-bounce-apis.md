# Amazon SES Suppression List and Bounce Handling APIs Documentation

## Overview
This document comprehensively covers all Amazon SES API endpoints related to suppression list management, bounce handling, and email deliverability management.

## API Version
All endpoints documented here are part of the Amazon SES API v2 (version 2019-09-27).

---

## Suppression List Management APIs

### 1. PutSuppressedDestination
**Purpose**: Adds an individual email address to the account-level suppression list.

**Endpoint**: `PUT /v2/email/suppression/addresses`

**Required Parameters**:
- `EmailAddress` (string): The email address to add to the suppression list
- `Reason` (string): The reason for suppression. Valid values: `BOUNCE` | `COMPLAINT`

**Optional Parameters**: None

**Impact on Deliverability**: 
- Prevents sending to the specified email address
- Helps maintain sender reputation by avoiding known problematic addresses
- Email addresses remain on the list until explicitly removed

---

### 2. GetSuppressedDestination
**Purpose**: Retrieves information about a specific email address on the suppression list.

**Endpoint**: `GET /v2/email/suppression/addresses/{EmailAddress}`

**Required Parameters**:
- `EmailAddress` (string): The email address to query (passed in URL path)

**Optional Parameters**: None

**Response Fields**:
- `EmailAddress`: The suppressed email address
- `Reason`: Why the address was suppressed (BOUNCE or COMPLAINT)
- `LastUpdateTime`: When the suppression was last updated
- `Attributes`: Additional metadata including:
  - `MessageId`: Original message ID that caused suppression
  - `FeedbackId`: Feedback ID from bounce/complaint

**Impact on Deliverability**: 
- Diagnostic tool to understand why an address is suppressed
- Helps in troubleshooting delivery issues

---

### 3. ListSuppressedDestinations
**Purpose**: Retrieves a paginated list of all email addresses on the suppression list.

**Endpoint**: `GET /v2/email/suppression/addresses`

**Required Parameters**: None

**Optional Parameters**:
- `StartDate` (timestamp): Filter addresses added after this date
- `EndDate` (timestamp): Filter addresses added before this date
- `Reasons` (array): Filter by suppression reasons. Valid values: `BOUNCE` | `COMPLAINT`
- `PageSize` (integer): Number of results per page (max 100)
- `NextToken` (string): Pagination token for retrieving next page

**Response Fields**:
- `SuppressedDestinationSummaries`: Array of suppressed addresses with:
  - `EmailAddress`
  - `Reason`
  - `LastUpdateTime`
- `NextToken`: Token for next page (if more results exist)

**Impact on Deliverability**: 
- Allows bulk review of suppressed addresses
- Essential for suppression list maintenance and auditing

---

### 4. DeleteSuppressedDestination
**Purpose**: Removes an individual email address from the suppression list.

**Endpoint**: `DELETE /v2/email/suppression/addresses/{EmailAddress}`

**Required Parameters**:
- `EmailAddress` (string): The email address to remove (passed in URL path)

**Optional Parameters**: None

**Impact on Deliverability**: 
- Allows sending to previously suppressed addresses
- Should be used cautiously - removing valid bounces can harm reputation
- Best practice: Only remove after verifying the address is now valid

---

## Bulk Suppression List Operations

### 5. CreateImportJob
**Purpose**: Creates a bulk import job to add or remove multiple email addresses from the suppression list.

**Endpoint**: `POST /v2/email/import-jobs`

**Required Parameters**:
- `ImportDataSource`:
  - `S3Url` (string): S3 location of the import file (CSV or JSON format)
  - `DataFormat` (string): Format of the file. Valid values: `CSV` | `JSON`
- `ImportDestination`:
  - `SuppressionListDestination`:
    - `SuppressionListImportAction` (string): Action to perform. Valid values:
      - `PUT`: Add addresses to suppression list (overwrites if exists)
      - `DELETE`: Remove addresses from suppression list

**Optional Parameters**: None

**Response Fields**:
- `JobId`: Unique identifier for the import job

**Impact on Deliverability**: 
- Enables efficient bulk management of suppression list
- Critical for migrating suppression data or large-scale list maintenance
- Requires production access (not available in sandbox)

---

### 6. GetImportJob
**Purpose**: Retrieves the status and details of a bulk import job.

**Endpoint**: `GET /v2/email/import-jobs/{JobId}`

**Required Parameters**:
- `JobId` (string): The import job ID (passed in URL path)

**Optional Parameters**: None

**Response Fields**:
- `JobId`: The import job identifier
- `JobStatus`: Current status (CREATED | PROCESSING | COMPLETED | FAILED)
- `ImportDestination`: Where data was imported
- `ImportDataSource`: Source of imported data
- `CreatedTimestamp`: When job was created
- `CompletedTimestamp`: When job completed
- `ProcessedRecordsCount`: Number of records processed
- `FailedRecordsCount`: Number of failed records
- `FailureInfo`: Error details if job failed
  - `ErrorMessage`
  - `FailedRecordsS3Url`: S3 location of failed records

**Impact on Deliverability**: 
- Monitoring tool for bulk operations
- Essential for troubleshooting failed imports

---

### 7. ListImportJobs
**Purpose**: Lists all import jobs with their current status.

**Endpoint**: `POST /v2/email/import-jobs/list`

**Required Parameters**: None

**Optional Parameters**:
- `ImportDestinationType` (string): Filter by destination type. Valid values: `SUPPRESSION_LIST` | `CONTACT_LIST`
- `PageSize` (integer): Results per page
- `NextToken` (string): Pagination token

**Response Fields**:
- `ImportJobs`: Array of import job summaries
- `NextToken`: Token for next page

**Impact on Deliverability**: 
- Provides overview of all bulk suppression operations
- Helps track historical changes to suppression list

---

## Account-Level Suppression Management

### 8. PutAccountSuppressionAttributes
**Purpose**: Configures which types of events automatically add addresses to the suppression list.

**Endpoint**: `PUT /v2/email/account/suppression`

**Required Parameters**: None

**Optional Parameters**:
- `SuppressedReasons` (array): List of reasons that trigger automatic suppression. Valid values:
  - `BOUNCE`: Auto-suppress on hard bounces
  - `COMPLAINT`: Auto-suppress on complaints
  - Empty array: Disables automatic suppression

**Impact on Deliverability**: 
- Controls automatic suppression behavior account-wide
- Critical for reputation management
- Recommended: Enable both BOUNCE and COMPLAINT

---

### 9. GetAccount
**Purpose**: Retrieves account-level information including suppression settings and sending status.

**Endpoint**: `GET /v2/email/account`

**Required Parameters**: None

**Optional Parameters**: None

**Response Fields** (relevant to suppression/bounce handling):
- `SendingEnabled`: Whether account can send emails
- `EnforcementStatus`: Account reputation status (HEALTHY | PROBATION | SHUTDOWN)
- `SuppressionAttributes`:
  - `SuppressedReasons`: Currently configured auto-suppression reasons
- `SendQuota`:
  - `Max24HourSend`: Maximum emails in 24 hours
  - `MaxSendRate`: Maximum emails per second
  - `SentLast24Hours`: Emails sent in last 24 hours

**Impact on Deliverability**: 
- Provides overall account health status
- Shows if sending is paused due to reputation issues
- Essential for monitoring account standing

---

## Sending Control APIs

### 10. GetAccountSendingEnabled (SES API v1)
**Purpose**: Returns whether email sending is enabled for the account.

**Endpoint**: SES API v1 endpoint

**Required Parameters**: None

**Optional Parameters**: None

**Response Fields**:
- `Enabled` (boolean): Whether sending is enabled

**Impact on Deliverability**: 
- Quick check if account can send emails
- Often disabled due to bounce/complaint issues

---

### 11. UpdateAccountSendingEnabled (SES API v1)
**Purpose**: Enables or disables email sending for the entire account.

**Endpoint**: SES API v1 endpoint

**Required Parameters**:
- `Enabled` (boolean): Whether to enable or disable sending

**Optional Parameters**: None

**Impact on Deliverability**: 
- Emergency stop for email sending
- Useful with CloudWatch alarms for automatic pausing
- Can be triggered by high bounce/complaint rates

---

## Feedback and Bounce Notification APIs

### 12. PutEmailIdentityFeedbackAttributes
**Purpose**: Configures bounce and complaint forwarding for a specific email identity.

**Endpoint**: `PUT /v2/email/identities/{EmailIdentity}/feedback`

**Required Parameters**:
- `EmailIdentity` (string): Email address or domain
- `EmailForwardingEnabled` (boolean): Whether to forward bounce/complaint notifications

**Optional Parameters**: None

**Impact on Deliverability**: 
- Controls email-based bounce/complaint notifications
- Must have at least one feedback mechanism (email or SNS)
- Forwards to Return-Path address specified in original email

---

### 13. SetIdentityFeedbackForwardingEnabled (SES API v1)
**Purpose**: Legacy API for configuring feedback forwarding.

**Endpoint**: SES API v1 endpoint

**Required Parameters**:
- `Identity` (string): Email address or domain
- `ForwardingEnabled` (boolean): Enable/disable forwarding

**Optional Parameters**: None

**Impact on Deliverability**: 
- Similar to PutEmailIdentityFeedbackAttributes
- Can only disable if SNS topics configured for bounces/complaints

---

## Event Handling and Monitoring

### 14. Event Types for Bounce/Complaint Handling
When configuring event destinations, the following event types are relevant:

- `BOUNCE`: Hard bounce events (permanent delivery failures)
- `COMPLAINT`: Spam complaints from recipients
- `DELIVERY`: Successful deliveries
- `DELIVERY_DELAY`: Temporary delivery issues
- `REJECT`: SES rejected the email (virus, policy violation)

**Configuration**: Set up via Configuration Sets and Event Destinations to:
- Send to SNS topics
- Store in Kinesis Data Firehose
- Publish to CloudWatch

---

## Best Practices for Implementation

### 1. Automatic Suppression Configuration
```python
# Enable automatic suppression for bounces and complaints
response = sesv2_client.put_account_suppression_attributes(
    SuppressedReasons=['BOUNCE', 'COMPLAINT']
)
```

### 2. Bulk Suppression List Management
```python
# Create import job to add addresses in bulk
response = sesv2_client.create_import_job(
    ImportDataSource={
        'S3Url': 's3://my-bucket/suppression-list.csv',
        'DataFormat': 'CSV'
    },
    ImportDestination={
        'SuppressionListDestination': {
            'SuppressionListImportAction': 'PUT'
        }
    }
)
```

### 3. Regular Suppression List Review
```python
# List suppressed addresses with filtering
response = sesv2_client.list_suppressed_destinations(
    Reasons=['BOUNCE'],
    StartDate=datetime.now() - timedelta(days=30),
    PageSize=100
)
```

### 4. Safe Address Removal
```python
# Only remove after verification
if verify_email_address(email):
    response = sesv2_client.delete_suppressed_destination(
        EmailAddress=email
    )
```

---

## Impact on Email Deliverability

### Positive Impacts:
1. **Reputation Protection**: Prevents sending to invalid addresses
2. **Reduced Bounce Rate**: Automatically filters problematic addresses
3. **ISP Relationships**: Shows responsible sending practices
4. **Cost Savings**: Reduces wasted sends to invalid addresses

### Considerations:
1. **False Positives**: Temporary issues might suppress valid addresses
2. **List Maintenance**: Regular review needed to remove outdated suppressions
3. **Migration Challenges**: Moving suppression data between regions/accounts
4. **Compliance**: May need to honor unsubscribes separately from suppressions

---

## Error Handling

Common errors across these APIs:
- `BadRequestException` (400): Invalid parameters
- `NotFoundException` (404): Resource doesn't exist
- `TooManyRequestsException` (429): Rate limit exceeded
- `LimitExceededException` (400): Account limits reached

Rate limits vary by endpoint but typically allow 1-10 requests per second.