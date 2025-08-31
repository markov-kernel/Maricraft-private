# Amazon SES Contact List and Subscription Management API Documentation

## Overview
Amazon Simple Email Service (SES) API v2 provides comprehensive contact list and subscription management capabilities. This document covers all contact/subscription related API endpoints, their parameters, and GDPR/compliance considerations.

## API Endpoints

### 1. CreateContactList
**Purpose**: Creates a contact list for managing email recipients and their subscription preferences.

**Endpoint**: `POST /v2/email/contact-lists`

**Required Parameters**:
- `ContactListName` (string): Name of the contact list

**Optional Parameters**:
- `Description` (string): Description of the contact list
- `Tags` (array): Tags associated with the contact list
  - `Key` (string)
  - `Value` (string)
- `Topics` (array): Interest groups/themes within the list
  - `DefaultSubscriptionStatus` (string)
  - `Description` (string)
  - `DisplayName` (string)
  - `TopicName` (string)

**GDPR/Compliance Considerations**:
- Only one contact list is allowed per AWS account
- A list can have a maximum of 20 topics
- Contact lists support subscription management for GDPR compliance

### 2. GetContactList
**Purpose**: Returns contact list metadata. It does not return any information about the contacts present in the list.

**Endpoint**: `GET /v2/email/contact-lists/{ContactListName}`

**Required Parameters**:
- `ContactListName` (URI parameter): Name of the contact list

**Optional Parameters**: None

**Response Elements**:
- Contact list metadata including name, description, topics, and tags

### 3. UpdateContactList
**Purpose**: Updates contact list metadata. This operation does a complete replacement.

**Endpoint**: `PUT /v2/email/contact-lists/{ContactListName}`

**Required Parameters**:
- `ContactListName` (URI parameter): Name of the contact list

**Optional Parameters**:
- `Description` (string): New description
- `Topics` (array): Updated topics list

**GDPR/Compliance Considerations**:
- Complete replacement operation - ensure all topics are included to avoid accidental deletion

### 4. DeleteContactList
**Purpose**: Deletes a contact list and all of the contacts on that list.

**Endpoint**: `DELETE /v2/email/contact-lists/{ContactListName}`

**Required Parameters**:
- `ContactListName` (URI parameter): Name of the contact list to delete

**Optional Parameters**: None

**GDPR/Compliance Considerations**:
- Permanently removes all contacts and their subscription preferences
- Cannot be undone - ensure proper data retention policies are followed

### 5. CreateContact
**Purpose**: Creates a contact, which is an end-user who is receiving the email, and adds them to a contact list.

**Endpoint**: `POST /v2/email/contact-lists/{ContactListName}/contacts`

**Required Parameters**:
- `ContactListName` (URI parameter): Name of contact list
- `EmailAddress` (string): Contact's email address

**Optional Parameters**:
- `AttributesData` (string): Additional contact attributes
- `TopicPreferences` (array): Contact's topic subscription preferences
  - `SubscriptionStatus` (string): OPT_IN or OPT_OUT
  - `TopicName` (string)
- `UnsubscribeAll` (boolean): Indicates if contact is unsubscribed from all topics

**GDPR/Compliance Considerations**:
- Automatically creates contacts when sending to addresses not on the list
- Respects opt-in/opt-out preferences per topic
- Supports unsubscribe from all topics for complete opt-out

### 6. GetContact
**Purpose**: Returns a contact from a contact list.

**Endpoint**: `GET /v2/email/contact-lists/{ContactListName}/contacts/{EmailAddress}`

**Required Parameters**:
- `ContactListName` (URI parameter)
- `EmailAddress` (URI parameter)

**Optional Parameters**: None

**Response Elements**:
- `AttributesData` (string): Contact attribute data
- `ContactListName` (string)
- `CreatedTimestamp` (timestamp)
- `EmailAddress` (string)
- `LastUpdatedTimestamp` (timestamp)
- `TopicDefaultPreferences` (array)
- `TopicPreferences` (array)
- `UnsubscribeAll` (boolean)

### 7. UpdateContact
**Purpose**: Updates a contact's preferences for a list.

**Endpoint**: `PUT /v2/email/contact-lists/{ContactListName}/contacts/{EmailAddress}`

**Required Parameters**:
- `ContactListName` (URI parameter)
- `EmailAddress` (URI parameter)

**Optional Parameters**:
- `AttributesData` (string): Contact attribute data
- `TopicPreferences` (array): Contact's opt-in/opt-out preferences
  - `SubscriptionStatus` (string)
  - `TopicName` (string)
- `UnsubscribeAll` (boolean): Unsubscribe from all topics

**GDPR/Compliance Considerations**:
- **CRITICAL**: Must specify ALL existing topic preferences, not just updates
- Missing preferences will be removed
- Supports granular topic-level subscription management

### 8. DeleteContact
**Purpose**: Removes a contact from a contact list.

**Endpoint**: `DELETE /v2/email/contact-lists/{ContactListName}/contacts/{EmailAddress}`

**Required Parameters**:
- `ContactListName` (URI parameter)
- `EmailAddress` (URI parameter)

**Optional Parameters**: None

**GDPR/Compliance Considerations**:
- Permanently removes contact and all subscription preferences
- Supports right to erasure (GDPR Article 17)

### 9. ListContacts
**Purpose**: Lists the contacts present in a specific contact list.

**Endpoint**: `POST /v2/email/contact-lists/{ContactListName}/contacts/list`

**Required Parameters**:
- `ContactListName` (URI parameter)

**Optional Parameters**:
- `Filter`: Filter contacts by status or topic
  - `FilteredStatus` (string)
  - `TopicFilter`:
    - `TopicName` (string)
    - `UseDefaultIfPreferenceUnavailable` (boolean)
- `NextToken` (string): Pagination token
- `PageSize` (integer): Number of contacts per page

**GDPR/Compliance Considerations**:
- Supports filtering by subscription status
- Can retrieve contacts subscribed/unsubscribed from specific topics

## Subscription Preferences Management

### Key Features:
1. **Topic-Based Subscriptions**: Contacts can opt-in/opt-out of specific topics within a list
2. **Unsubscribe All**: Option to unsubscribe from all topics at once
3. **Default Preferences**: Topics can have default subscription statuses

### Subscription Status Values:
- `OPT_IN`: Contact has explicitly opted into the topic
- `OPT_OUT`: Contact has explicitly opted out of the topic

### Important Note:
While the original query mentioned `PutContactListSubscription`, this functionality is actually handled through the `UpdateContact` operation's `TopicPreferences` parameter rather than a separate endpoint.

## GDPR/Compliance Considerations

### 1. Data Protection
- AWS customers can use all AWS services to process personal data in compliance with GDPR
- Contact lists store minimal PII (email addresses and preferences)
- All data is encrypted in transit and at rest

### 2. Consent Management
- Supports granular consent through topic-based subscriptions
- Tracks opt-in/opt-out status per topic
- Maintains audit trail with timestamps

### 3. Right to Access
- `GetContact` API provides complete access to stored contact data
- `ListContacts` allows bulk retrieval of contact information

### 4. Right to Erasure
- `DeleteContact` permanently removes contacts
- `DeleteContactList` removes entire lists and all contacts

### 5. Automated Unsubscribe Management
- Amazon SES automatically manages unsubscribe requests
- Supports List-Unsubscribe headers for one-click unsubscribe
- Provides hosted unsubscribe pages with preference management

### 6. Compliance Features
- Automatic bounce handling prevents sending to unsubscribed contacts
- Regional data storage (data stays in selected AWS region)
- Integration with AWS Key Management Service for encryption
- Audit logging through AWS CloudTrail

### 7. Bulk Sender Requirements
- Complies with Gmail and Yahoo bulk sender requirements (effective February 2024)
- Supports one-click unsubscribe via List-Unsubscribe-Post header
- Automatically adds required unsubscribe links to emails

## Best Practices

1. **Always include unsubscribe mechanisms**: Use `{{amazonSESUnsubscribeUrl}}` placeholder in emails
2. **Respect preferences immediately**: SES automatically bounces emails to unsubscribed contacts
3. **Use topics for granular control**: Allow subscribers to choose specific content types
4. **Regular list hygiene**: Remove bounced and complained addresses
5. **Document consent**: Store how and when consent was obtained in AttributesData

## Error Handling

Common errors across all endpoints:
- `BadRequestException` (400): Invalid input parameters
- `NotFoundException` (404): Resource doesn't exist
- `TooManyRequestsException` (429): Rate limit exceeded
- `AlreadyExistsException` (400): Resource already exists
- `LimitExceededException` (400): Account limit reached

## SDK Support

All endpoints are supported in:
- AWS CLI
- .NET
- C++
- Go v2
- Java V2
- JavaScript V3
- Kotlin
- PHP V3
- Python (Boto3)
- Ruby V3

## Additional Resources

- [Using list management](https://docs.aws.amazon.com/ses/latest/dg/sending-email-list-management.html)
- [Using subscription management](https://docs.aws.amazon.com/ses/latest/dg/sending-email-subscription-management.html)
- [Amazon SES API v2 Reference](https://docs.aws.amazon.com/ses/latest/APIReference-V2/)
- [GDPR Compliance on AWS](https://aws.amazon.com/compliance/gdpr-center/)