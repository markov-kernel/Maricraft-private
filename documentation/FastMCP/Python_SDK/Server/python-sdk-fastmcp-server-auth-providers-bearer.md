# fastmcp.server.auth.providers.bearer
# fastmcp.server.auth.providers.bearer

> **Category:** fastmcp.server.auth.providers.bearer
> **Source:** gofastmcp.com_python-sdk_fastmcp-server-auth-providers-bearer.json

---

providers

bearer

fastmcp.server.auth.providers.bearer

## Classes

JWKData

JSON Web Key data structure.

JWKSData

JSON Web Key Set data structure.

RSAKeyPair

**Methods:**

generate

Copy

```
generate(cls) -> 'RSAKeyPair'

```

Generate an RSA key pair for testing.**Returns:**

- (private\_key\_pem, public\_key\_pem)

create_token

Copy

```
create_token(self, subject: str = 'fastmcp-user', issuer: str = 'https://fastmcp.example.com', audience: str | list[str] | None = None, scopes: list[str] | None = None, expires_in_seconds: int = 3600, additional_claims: dict[str, Any] | None = None, kid: str | None = None) -> str

```

Generate a test JWT token for testing purposes.**Args:**

- `private_key_pem`: RSA private key in PEM format
- `subject`: Subject claim (usually user ID)
- `issuer`: Issuer claim
- `audience`: Audience claim - can be a string or list of strings (optional)
- `scopes`: List of scopes to include
- `expires_in_seconds`: Token expiration time in seconds
- `additional_claims`: Any additional claims to include
- `kid`: Key ID for JWKS lookup (optional)

**Returns:**

- Signed JWT token string

BearerAuthProvider

Simple JWT Bearer Token validator for hosted MCP servers.
Uses RS256 asymmetric encryption by default but supports all JWA algorithms. Supports either static public key
or JWKS URI for key rotation.Note that this provider DOES NOT permit client registration or revocation, or any OAuth flows.
It is intended to be used with a control plane that manages clients and tokens.**Methods:**

load_access_token

Copy

```
load_access_token(self, token: str) -> AccessToken | None

```

Validates the provided JWT bearer token.**Args:**

- `token`: The JWT token string to validate

**Returns:**

- AccessToken object if valid, None if invalid or expired

verify_token

Copy

```
verify_token(self, token: str) -> AccessToken | None

```

Verify a bearer token and return access info if valid.This method implements the TokenVerifier protocol by delegating
to our existing load\_access\_token method.**Args:**

- `token`: The JWT token string to validate

**Returns:**

- AccessToken object if valid, None if invalid or expired

get_client

Copy

```
get_client(self, client_id: str) -> OAuthClientInformationFull | None

```

register_client

Copy

```
register_client(self, client_info: OAuthClientInformationFull) -> None

```

authorize

Copy

```
authorize(self, client: OAuthClientInformationFull, params: AuthorizationParams) -> str

```

load_authorization_code

Copy

```
load_authorization_code(self, client: OAuthClientInformationFull, authorization_code: str) -> AuthorizationCode | None

```

exchange_authorization_code

Copy

```
exchange_authorization_code(self, client: OAuthClientInformationFull, authorization_code: AuthorizationCode) -> OAuthToken

```

load_refresh_token

Copy

```
load_refresh_token(self, client: OAuthClientInformationFull, refresh_token: str) -> RefreshToken | None

```

exchange_refresh_token

Copy

```
exchange_refresh_token(self, client: OAuthClientInformationFull, refresh_token: RefreshToken, scopes: list[str]) -> OAuthToken

```

revoke_token

Copy

```
revoke_token(self, token: AccessToken | RefreshToken) -> None

```

[\_\_init\_\_](https://gofastmcp.com/python-sdk/fastmcp-server-auth-providers-__init__) [bearer\_env](https://gofastmcp.com/python-sdk/fastmcp-server-auth-providers-bearer_env)