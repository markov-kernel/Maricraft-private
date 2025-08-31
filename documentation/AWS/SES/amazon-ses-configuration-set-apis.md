# Amazon SES Configuration Set API Documentation

## Overview
Configuration sets in Amazon SES are groups of rules that you can apply to emails sent through the service. They enable event tracking, custom domain configuration, reputation monitoring, and various delivery options.

## Complete List of Configuration Set API Endpoints

### 1. Core Configuration Set Operations

#### CreateConfigurationSet
- **Purpose**: Create a new configuration set
- **Endpoint**: `POST /v2/email/configuration-sets`
- **Required Parameters**:
  - `ConfigurationSetName` (string) - The name of the configuration set
- **Optional Parameters**:
  - `ArchivingOptions` - Configure email archiving settings
  - `DeliveryOptions` - Associate with dedicated IP pools
  - `ReputationOptions` - Enable/disable reputation tracking
  - `SendingOptions` - Enable/disable email sending
  - `SuppressionOptions` - Configure suppression list preferences
  - `Tags` - Key-value pairs for organizing resources
  - `TrackingOptions` - Custom domain for open/click tracking
  - `VdmOptions` - Virtual Deliverability Manager settings
- **Email Tracking**: Enables comprehensive event tracking when combined with event destinations

#### DeleteConfigurationSet
- **Purpose**: Delete an existing configuration set
- **Endpoint**: `DELETE /v2/email/configuration-sets/{ConfigurationSetName}`
- **Required Parameters**:
  - `ConfigurationSetName` (string) - The name of the configuration set to delete
- **Optional Parameters**: None
- **Email Tracking**: Removes all associated event tracking configurations

#### GetConfigurationSet (DescribeConfigurationSet in v1)
- **Purpose**: Retrieve detailed information about a specific configuration set
- **Endpoint**: `GET /v2/email/configuration-sets/{ConfigurationSetName}`
- **Required Parameters**:
  - `ConfigurationSetName` (string) - The name of the configuration set
- **Optional Parameters**: None
- **Email Tracking**: Returns current tracking configuration including event destinations

#### ListConfigurationSets
- **Purpose**: List all configuration sets in the current AWS region
- **Endpoint**: `GET /v2/email/configuration-sets`
- **Required Parameters**: None
- **Optional Parameters**:
  - `NextToken` (string) - Pagination token
  - `PageSize` (integer) - Number of results per page
- **Email Tracking**: Lists all configuration sets available for email tracking

### 2. Configuration Set Settings Operations

#### PutConfigurationSetSendingOptions
- **Purpose**: Enable or disable email sending for a configuration set
- **Endpoint**: `PUT /v2/email/configuration-sets/{ConfigurationSetName}/sending`
- **Required Parameters**:
  - `ConfigurationSetName` (string)
  - `SendingEnabled` (boolean)
- **Optional Parameters**: None
- **Email Tracking**: Controls whether emails using this configuration set are sent

#### PutConfigurationSetDeliveryOptions
- **Purpose**: Associate configuration set with dedicated IP pools
- **Endpoint**: `PUT /v2/email/configuration-sets/{ConfigurationSetName}/delivery-options`
- **Required Parameters**:
  - `ConfigurationSetName` (string)
- **Optional Parameters**:
  - `TlsPolicy` - Require TLS for email delivery
  - `SendingPoolName` - Name of dedicated IP pool
- **Email Tracking**: Affects delivery tracking metrics

#### PutConfigurationSetTrackingOptions
- **Purpose**: Configure custom domain for open and click tracking
- **Endpoint**: `PUT /v2/email/configuration-sets/{ConfigurationSetName}/tracking-options`
- **Required Parameters**:
  - `ConfigurationSetName` (string)
- **Optional Parameters**:
  - `CustomRedirectDomain` (string) - Custom domain for tracking URLs
- **Email Tracking**: Essential for open and click tracking functionality

#### PutConfigurationSetReputationOptions
- **Purpose**: Configure reputation tracking settings
- **Endpoint**: `PUT /v2/email/configuration-sets/{ConfigurationSetName}/reputation-options`
- **Required Parameters**:
  - `ConfigurationSetName` (string)
- **Optional Parameters**:
  - `ReputationMetricsEnabled` (boolean) - Enable CloudWatch reputation metrics
  - `LastFreshStart` (timestamp) - Reset reputation tracking date
- **Email Tracking**: Enables bounce and complaint rate monitoring

#### PutConfigurationSetSuppressionOptions
- **Purpose**: Configure account suppression list preferences
- **Endpoint**: `PUT /v2/email/configuration-sets/{ConfigurationSetName}/suppression-options`
- **Required Parameters**:
  - `ConfigurationSetName` (string)
- **Optional Parameters**:
  - `SuppressedReasons` (array) - Types of suppressions (BOUNCE, COMPLAINT)
- **Email Tracking**: Manages automatic suppression based on bounce/complaint events

#### PutConfigurationSetVdmOptions
- **Purpose**: Configure Virtual Deliverability Manager options
- **Endpoint**: `PUT /v2/email/configuration-sets/{ConfigurationSetName}/vdm-options`
- **Required Parameters**:
  - `ConfigurationSetName` (string)
- **Optional Parameters**:
  - `VdmOptions` - VDM configuration object
- **Email Tracking**: Advanced deliverability monitoring and optimization

### 3. Event Destination Operations

#### CreateConfigurationSetEventDestination
- **Purpose**: Create event destination for publishing email events
- **Endpoint**: `POST /v2/email/configuration-sets/{ConfigurationSetName}/event-destinations`
- **Required Parameters**:
  - `ConfigurationSetName` (string)
  - `EventDestination` (object) containing:
    - `Name` (string) - Event destination name
    - `Enabled` (boolean)
    - Destination type (one of):
      - `CloudWatchDestination`
      - `KinesisFirehoseDestination`
      - `SnsDestination`
    - `MatchingEventTypes` (array) - Events to track
- **Optional Parameters**: None
- **Email Tracking**: Core functionality for event tracking

#### UpdateConfigurationSetEventDestination
- **Purpose**: Modify existing event destination configuration
- **Endpoint**: `PUT /v2/email/configuration-sets/{ConfigurationSetName}/event-destinations/{EventDestinationName}`
- **Required Parameters**:
  - `ConfigurationSetName` (string)
  - `EventDestinationName` (string)
  - `EventDestination` (object) - Updated configuration
- **Optional Parameters**: Same as CreateConfigurationSetEventDestination
- **Email Tracking**: Modify which events are tracked and where they're sent

#### GetConfigurationSetEventDestinations
- **Purpose**: Retrieve list of event destinations for a configuration set
- **Endpoint**: `GET /v2/email/configuration-sets/{ConfigurationSetName}/event-destinations`
- **Required Parameters**:
  - `ConfigurationSetName` (string)
- **Optional Parameters**: None
- **Email Tracking**: View current event tracking configuration

#### DeleteConfigurationSetEventDestination
- **Purpose**: Remove an event destination from a configuration set
- **Endpoint**: `DELETE /v2/email/configuration-sets/{ConfigurationSetName}/event-destinations/{EventDestinationName}`
- **Required Parameters**:
  - `ConfigurationSetName` (string)
  - `EventDestinationName` (string)
- **Optional Parameters**: None
- **Email Tracking**: Stops tracking events to the specified destination

### 4. Legacy Reputation Monitoring API (v1)

#### UpdateConfigurationSetReputationMetricsEnabled
- **Purpose**: Enable/disable reputation metrics publishing to CloudWatch
- **API Version**: v1 (legacy)
- **Required Parameters**:
  - `ConfigurationSetName` (string)
  - `Enabled` (boolean)
- **Optional Parameters**: None
- **Email Tracking**: Publishes bounce/complaint rates to CloudWatch

## Event Types for Email Tracking

Configuration sets can track the following email events:

1. **SEND** - The send request was successful and SES will attempt to deliver
2. **REJECT** - SES determined the email contained malware/virus
3. **BOUNCE** - Hard bounce from recipient's mail server
4. **COMPLAINT** - Recipient marked email as spam
5. **DELIVERY** - Successfully delivered to recipient's mail server
6. **OPEN** - Recipient opened the email (requires tracking enabled)
7. **CLICK** - Recipient clicked a link (requires tracking enabled)
8. **RENDERING_FAILURE** - Template rendering failed
9. **DELIVERY_DELAY** - Temporary delivery issue
10. **SUBSCRIPTION** - Recipient updated subscription preferences

## Event Destination Types

1. **Amazon CloudWatch**
   - Metrics and dimensions for real-time monitoring
   - Supports custom dimensions for categorization

2. **Amazon Kinesis Data Firehose**
   - Stream events to S3, Redshift, or Elasticsearch
   - Requires IAM role with appropriate permissions

3. **Amazon SNS**
   - Real-time notifications for critical events
   - Useful for immediate bounce/complaint handling

## Important Considerations

- **Rate Limits**: Most operations limited to 1 request per second
- **Permissions**: Requires appropriate IAM permissions (e.g., `ses:CreateConfigurationSet`)
- **API Versions**: SES API v2 is recommended over v1 for new implementations
- **Default Configuration Sets**: Can be assigned to verified identities for automatic application
- **Reputation Thresholds**: 
  - Bounce rate should stay under 5% (review triggered at 10%)
  - Complaint rate should stay under 0.1% (review triggered at 0.5%)

## Usage Example

To implement comprehensive email tracking:

1. Create a configuration set with tracking options
2. Add event destinations for desired event types
3. Enable reputation monitoring
4. Apply configuration set when sending emails
5. Monitor events through chosen destinations (CloudWatch, Kinesis, SNS)

This enables complete visibility into email delivery, engagement, and reputation metrics.