# Amazon SES Email/Domain Verification API Documentation

## Overview
Amazon Simple Email Service (SES) provides several API endpoints for verifying email addresses and domains before sending emails. This document covers all verification-related API endpoints.

## API Endpoints

### 1. VerifyEmailIdentity

**Purpose/Description:**
Adds an email address to the list of identities for your Amazon SES account in the current AWS Region and attempts to verify it. A verification email is sent to the specified address.

**Required Parameters:**
- `EmailAddress` (string): The email address to be verified

**Optional Parameters:**
None

**Verification Process Details:**
1. After calling VerifyEmailIdentity, a verification email is sent from `no-reply-aws@amazon.com`
2. The recipient must click the link in the email within 24 hours
3. Once clicked, the identity status changes to "Verified"
4. If not clicked within 24 hours, status changes to "Failed"

**Example (AWS CLI):**
```bash
aws ses verify-email-identity --email-address user@example.com
```

---

### 2. VerifyEmailAddress (DEPRECATED)

**Purpose/Description:**
This API is deprecated. Use VerifyEmailIdentity instead.

**Status:** ⚠️ DEPRECATED
**Replacement:** Use `VerifyEmailIdentity` for email verification

---

### 3. VerifyDomainIdentity

**Purpose/Description:**
Adds a domain to the list of identities for your Amazon SES account in the current AWS Region and attempts to verify it. Returns a verification token that must be added as a TXT record in the domain's DNS configuration.

**Required Parameters:**
- `Domain` (string): The domain to be verified

**Optional Parameters:**
None

**Verification Process Details:**
1. Returns a verification token
2. Create a TXT record in your domain's DNS with the token
3. Amazon SES checks for the record (can take up to 72 hours)
4. Once detected, domain status changes to "Success"
5. If not detected within 72 hours, status changes to "Failed"

**Example (Python Boto3):**
```python
import boto3

ses = boto3.client('ses')
response = ses.verify_domain_identity(Domain='example.com')
verification_token = response['VerificationToken']
```

---

### 4. VerifyDomainDkim

**Purpose/Description:**
Returns a set of DKIM tokens for a domain identity. These tokens are used to enable Easy DKIM signing for the domain, providing email authentication.

**Required Parameters:**
- `Domain` (string): The domain for which to enable DKIM signing

**Optional Parameters:**
None

**Verification Process Details:**
1. Returns multiple DKIM tokens (typically 3)
2. Create CNAME records in your DNS for each token
3. Records should point to Amazon SES DKIM public keys
4. Amazon SES detects the records (can take up to 72 hours)
5. Once verified, SES can DKIM-sign emails from that domain

**Example Response:**
```json
{
    "DkimTokens": [
        "EXAMPLEq76owjnks3lnluwg65scbemvw",
        "EXAMPLEi3dnsj67hstzaj673klariwx2",
        "EXAMPLEwfbtcukvimehexktmdtaz6naj"
    ]
}
```

---

### 5. GetIdentityVerificationAttributes

**Purpose/Description:**
Given a list of identities (email addresses and/or domains), returns the verification status and (for domain identities) the verification token for each identity.

**Required Parameters:**
- `Identities` (list of strings): List of identities to check (max 100)

**Optional Parameters:**
None

**Verification Process Details:**
- Returns verification status for each identity
- Possible statuses: "Pending", "Success", "Failed", "TemporaryFailure", "NotStarted"
- For domains, also returns the verification token
- Throttled at one request per second

**Example (AWS CLI):**
```bash
aws ses get-identity-verification-attributes \
    --identities "user1@example.com" "example.com"
```

---

### 6. ListIdentities

**Purpose/Description:**
Returns a list containing all of the identities (email addresses and domains) for your AWS account in the current AWS Region, regardless of verification status.

**Required Parameters:**
None

**Optional Parameters:**
- `IdentityType` (string): Type of identities to list - "EmailAddress", "Domain", or omit for both
- `MaxItems` (integer): Maximum number of identities to return
- `NextToken` (string): Token for pagination

**Verification Process Details:**
- Lists all identities regardless of verification status
- Can filter by identity type
- Supports pagination for large lists
- Throttled at one request per second

**Example (AWS CLI):**
```bash
aws ses list-identities --identity-type Domain --max-items 10
```

---

### 7. DeleteIdentity

**Purpose/Description:**
Deletes the specified identity (an email address or a domain) from the list of verified identities.

**Required Parameters:**
- `Identity` (string): The identity to be removed (email address or domain)

**Optional Parameters:**
None

**Verification Process Details:**
- Permanently removes the identity from your SES account
- Works for both email addresses and domains
- Throttled at one request per second
- No confirmation required - deletion is immediate

**Example (Python Boto3):**
```python
ses = boto3.client('ses')
ses.delete_identity(Identity='user@example.com')
```

---

### 8. GetIdentityDkimAttributes

**Purpose/Description:**
Returns the current status of Easy DKIM signing for an entity. For domain identities, also returns the DKIM tokens required for Easy DKIM signing.

**Required Parameters:**
- `Identities` (list of strings): List of verified identities

**Optional Parameters:**
None

**Verification Process Details:**
- Returns DKIM enablement status
- For domains, returns DKIM tokens if DKIM is enabled
- Shows whether DKIM verification is complete
- Useful for checking DKIM configuration status

**Example Response:**
```json
{
    "DkimAttributes": {
        "example.com": {
            "DkimEnabled": true,
            "DkimVerificationStatus": "Success",
            "DkimTokens": [
                "EXAMPLEq76owjnks3lnluwg65scbemvw",
                "EXAMPLEi3dnsj67hstzaj673klariwx2",
                "EXAMPLEwfbtcukvimehexktmdtaz6naj"
            ]
        }
    }
}
```

---

## Important Notes

1. **Rate Limits**: Most verification APIs are throttled at one request per second

2. **Verification Time Limits**:
   - Email verification links expire after 24 hours
   - Domain verification must be completed within 72 hours

3. **Regional**: Identities are verified per AWS Region - verification in one region doesn't apply to others

4. **SES API v2**: There's a newer API version (SES API v2) with `CreateEmailIdentity` that combines creation and configuration

5. **Required for Sending**: SES can only send emails from verified email addresses or domains

6. **Domain vs Email**: Verifying a domain allows sending from any address on that domain

## Best Practices

1. Always check verification status before attempting to send emails
2. Implement proper error handling for verification failures
3. For production use, verify domains rather than individual email addresses
4. Monitor verification status changes using GetIdentityVerificationAttributes
5. Keep track of verification tokens for domain verification troubleshooting