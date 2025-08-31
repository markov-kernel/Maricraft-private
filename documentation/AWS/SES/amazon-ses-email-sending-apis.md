# Amazon SES Email Sending APIs - Complete Reference

## Overview

Amazon Simple Email Service (SES) provides multiple APIs for sending emails, each designed for specific use cases. This document provides a comprehensive reference for all email sending related API endpoints.

## API Versions

Amazon SES offers two API versions:
- **SES API v1** - Original API with methods like SendEmail, SendRawEmail, SendTemplatedEmail, SendBulkTemplatedEmail
- **SES API v2** - Modern API with improved functionality and unified SendEmail method with content types

## Email Sending APIs

### 1. SendEmail (SES API v1)

**Purpose**: Composes an email message and immediately queues it for sending. This is the simplest API for sending basic emails without templates or attachments.

**Required Parameters**:
- `Source` - The email address that is sending the email (must be verified)
- `Destination` - The destination for this email, composed of To:, CC:, and BCC: fields
  - `ToAddresses` - Array of recipient addresses
  - `CcAddresses` - Array of CC addresses (optional)
  - `BccAddresses` - Array of BCC addresses (optional)
- `Message` - The message to be sent
  - `Subject` - The subject of the message
    - `Data` - The textual data of the content
    - `Charset` - The character set of the content (optional)
  - `Body` - The message body
    - `Text` - The content of the message in text format (optional)
    - `Html` - The content of the message in HTML format (optional)

**Optional Parameters**:
- `ConfigurationSetName` - The name of the configuration set to use
- `ReplyToAddresses` - The reply-to email address(es) for the message
- `ReturnPath` - The email address that bounces and complaints are forwarded to
- `SourceArn` - Used for sending authorization
- `ReturnPathArn` - Used for sending authorization
- `Tags` - Message tags in the form of name/value pairs

**Use Cases**:
- Simple transactional emails
- System notifications
- Basic email communications without attachments
- Quick email sending without template management

**Rate Limits**: Subject to your account's sending quota and maximum send rate

**Special Requirements**:
- Cannot send attachments (use SendRawEmail instead)
- Maximum message size: 10 MB
- Must include at least one recipient
- The total number of recipients (To:, CC:, and BCC:) cannot exceed 50

---

### 2. SendRawEmail (SES API v1)

**Purpose**: Sends an email message with complete control over the email headers and MIME structure. Required for sending attachments, custom headers, or complex MIME messages.

**Required Parameters**:
- `RawMessage` - The raw email message
  - `Data` - The raw email message itself (base64-encoded)

**Optional Parameters**:
- `Source` - The identity's email address (if not provided, must be in the raw message "From" header)
- `Destinations` - A list of destinations for the message (if not provided, extracted from raw message headers)
- `FromArn` - Used for sending authorization
- `SourceArn` - Used for sending authorization
- `ReturnPathArn` - Used for sending authorization
- `Tags` - Message tags for tracking
- `ConfigurationSetName` - Configuration set to use

**Use Cases**:
- Sending emails with attachments
- Custom email headers
- Multipart MIME messages (text + HTML)
- Calendar invitations
- Digitally signed emails
- Complex email formatting requirements

**Rate Limits**: 
- Subject to account sending quota and maximum send rate
- Messages larger than 10MB subject to bandwidth throttling (as low as 40MB/s)

**Special Requirements**:
- Maximum message size: 10 MB (including attachments)
- Maximum 500 MIME parts
- Raw message must be base64-encoded
- Must comply with RFC 2821 (7-bit ASCII)
- Message must contain proper headers and body separated by blank line

---

### 3. SendTemplatedEmail (SES API v1)

**Purpose**: Sends personalized emails using pre-created email templates stored in Amazon SES.

**Required Parameters**:
- `Source` - The email address that is sending the email
- `Destination` - The destination for this email
  - `ToAddresses` - Array of recipient addresses
  - `CcAddresses` - Array of CC addresses (optional)
  - `BccAddresses` - Array of BCC addresses (optional)
- `Template` - The template to use when sending this email
- `TemplateData` - JSON object with replacement values for template variables

**Optional Parameters**:
- `ConfigurationSetName` - Configuration set name
- `ReplyToAddresses` - Reply-to addresses
- `ReturnPath` - Return path for bounces
- `SourceArn` - For sending authorization
- `ReturnPathArn` - For sending authorization
- `TemplateArn` - ARN of the template
- `Tags` - Message tags

**Use Cases**:
- Personalized marketing emails
- Customized transactional emails
- User onboarding sequences
- Notification emails with dynamic content

**Rate Limits**: Subject to account sending quota and maximum send rate

**Special Requirements**:
- Template must exist in SES
- Maximum 50 recipients per call (across To:, CC:, BCC:)
- TemplateData must be valid JSON with escaped quotes
- Template variables must match those defined in the template

---

### 4. SendBulkTemplatedEmail (SES API v1)

**Purpose**: Sends personalized emails to multiple destinations using a single API call with custom data for each recipient.

**Required Parameters**:
- `Source` - The email address that is sending the email
- `Template` - The name of the template to use
- `Destinations` - Array of destination objects, each containing:
  - `Destination` - Recipient information
    - `ToAddresses` - Array of recipient addresses
    - `CcAddresses` - Array of CC addresses (optional)
    - `BccAddresses` - Array of BCC addresses (optional)
  - `ReplacementTemplateData` - JSON string with recipient-specific values (optional)
  - `ReplacementTags` - Message tags specific to this destination (optional)

**Optional Parameters**:
- `ConfigurationSetName` - Configuration set to use
- `DefaultTemplateData` - Default JSON data for template variables
- `DefaultTags` - Default message tags
- `ReplyToAddresses` - Reply-to addresses
- `ReturnPath` - Return path for bounces
- `ReturnPathArn` - For sending authorization
- `SourceArn` - For sending authorization
- `TemplateArn` - ARN of the template

**Use Cases**:
- Newsletter campaigns
- Bulk notifications with personalization
- Mass marketing emails
- Batch processing of transactional emails

**Rate Limits**:
- Maximum 50 destinations per API call
- Subject to account's maximum sending rate
- May need multiple calls for large recipient lists

**Special Requirements**:
- Each destination counts against sending quota
- Template must exist in SES
- All template variables must have values (either specific or default)

---

### 5. SendEmail (SES API v2)

**Purpose**: The unified email sending method in API v2 that supports multiple content types through a single endpoint.

**Required Parameters**:
- `FromEmailAddress` - The email address to send the email from
- `Destination` - An object that contains the recipients of the email
  - `ToAddresses` - Array of "To" recipients
  - `CcAddresses` - Array of "CC" recipients (optional)
  - `BccAddresses` - Array of "BCC" recipients (optional)
- `Content` - The content of the email (type depends on content format chosen)

**Content Types**:

#### Simple Content:
```json
{
  "Simple": {
    "Subject": {
      "Data": "Subject text",
      "Charset": "UTF-8"
    },
    "Body": {
      "Text": {
        "Data": "Text body",
        "Charset": "UTF-8"
      },
      "Html": {
        "Data": "HTML body",
        "Charset": "UTF-8"
      }
    }
  }
}
```

#### Raw Content:
```json
{
  "Raw": {
    "Data": "Base64 encoded raw email message"
  }
}
```

#### Template Content:
```json
{
  "Template": {
    "TemplateName": "MyTemplate",
    "TemplateArn": "arn:aws:ses:region:account-id:template/MyTemplate",
    "TemplateData": "{ \"name\": \"John\" }"
  }
}
```

**Optional Parameters**:
- `ReplyToAddresses` - Reply-to email addresses
- `FeedbackForwardingEmailAddress` - Email address for feedback forwarding
- `FeedbackForwardingEmailAddressIdentityArn` - ARN for cross-account feedback
- `EmailTags` - Tags for categorizing the email
- `ConfigurationSetName` - Configuration set to use
- `ListManagementOptions` - List management headers

**Use Cases**:
- All email sending scenarios in modern applications
- Replacement for v1 API methods
- Unified interface for simple, raw, and templated emails

**Rate Limits**: Subject to account sending quota and maximum send rate

---

### 6. SendBulkEmail (SES API v2)

**Purpose**: Sends unique emails to multiple destinations in a single API call.

**Required Parameters**:
- `FromEmailAddress` - The email address to send from
- `DefaultContent` - Default email content
- `BulkEmailEntries` - Array of bulk email entries (up to 50)

**Optional Parameters**:
- `FeedbackForwardingEmailAddress` - For feedback forwarding
- `FeedbackForwardingEmailAddressIdentityArn` - For cross-account scenarios
- `DefaultEmailTags` - Default tags for all emails
- `ConfigurationSetName` - Configuration set to use

**Use Cases**:
- Sending different content to multiple recipients
- Bulk transactional emails with unique content
- Efficient batch processing

**Rate Limits**:
- Maximum 50 destination objects per call
- Subject to account's sending rate

---

## Sending Methods Comparison

| Method | API Version | Attachments | Templates | Bulk Send | Max Recipients |
|--------|-------------|-------------|-----------|-----------|----------------|
| SendEmail (v1) | v1 | No | No | No | 50 |
| SendRawEmail | v1 | Yes | No | No | Unlimited* |
| SendTemplatedEmail | v1 | No | Yes | No | 50 |
| SendBulkTemplatedEmail | v1 | No | Yes | Yes | 50 per destination |
| SendEmail (v2) | v2 | Yes** | Yes | No | 50 |
| SendBulkEmail | v2 | Yes** | Yes | Yes | 50 destinations |

*Limited by message size and sending quota
**When using Raw content type

## Global Limitations and Quotas

### Message Size Limits
- Maximum message size: 10 MB (including attachments)
- Messages larger than 10MB rejected
- Bandwidth throttling for large messages

### Recipient Limits
- Maximum 50 recipients per message (To + CC + BCC)
- Each recipient counts against daily sending quota

### Sending Quotas
- **Sandbox**: 200 emails/24 hours, 1 email/second
- **Production**: Based on reputation and history
  - Max24HourSend: Rolling 24-hour limit
  - MaxSendRate: Emails per second limit

### Template Limits
- Maximum 10,000 templates per account
- Maximum template size: 500 KB
- Unlimited template variables

### MIME Restrictions
- Maximum 500 MIME parts per message
- Must use 7-bit ASCII encoding
- Headers must comply with RFC 2821

## Best Practices

1. **Choose the Right API**:
   - Use SendEmail (v1/v2) for simple emails
   - Use SendRawEmail for attachments or custom headers
   - Use template methods for personalized bulk sending

2. **Handle Rate Limits**:
   - Implement exponential backoff
   - Monitor sending quota with GetSendQuota
   - Spread bulk sends over time

3. **Error Handling**:
   - Set up bounce and complaint handling
   - Monitor rendering failures for templates
   - Use configuration sets for tracking

4. **Performance Optimization**:
   - Use SendBulkTemplatedEmail for mass emails
   - Batch recipients efficiently
   - Pre-validate email addresses

5. **Security**:
   - Verify sending domains/addresses
   - Use IAM policies for access control
   - Implement DKIM signing

## IAM Permissions Required

To use these APIs, the following IAM actions must be allowed:
- `ses:SendEmail`
- `ses:SendRawEmail`
- `ses:SendTemplatedEmail`
- `ses:SendBulkTemplatedEmail`

For v2 API:
- `ses:SendEmail` (v2 namespace)
- `ses:SendBulkEmail`

## Migration Guide (v1 to v2)

1. **SendEmail v1 → SendEmail v2 (Simple)**:
   - Change parameter names (Source → FromEmailAddress)
   - Wrap content in Simple content type

2. **SendRawEmail → SendEmail v2 (Raw)**:
   - Use Raw content type
   - Same base64 encoding requirements

3. **SendTemplatedEmail → SendEmail v2 (Template)**:
   - Use Template content type
   - Similar parameter structure

4. **SendBulkTemplatedEmail → SendBulkEmail v2**:
   - New bulk structure with BulkEmailEntries
   - More flexible content options

## Additional Resources

- [Amazon SES API Reference](https://docs.aws.amazon.com/ses/latest/APIReference/)
- [Amazon SES Developer Guide](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/)
- [AWS SDK Documentation](https://aws.amazon.com/tools/)
- [SES Sending Quotas](https://docs.aws.amazon.com/ses/latest/dg/manage-sending-quotas.html)