# Generate a new key pair
# Generate a new key pair

> **Category:** General
> **Source:** gofastmcp.com_servers_auth_verifiers.json

---

Authentication

Token Verification

`New in version: 2.11.0`

Authentication and authorization are only relevant for HTTP-based transports.

Bearer Token authentication is a common way to secure HTTP-based APIs. In this model, the client sends a token (usually a JSON Web Token or JWT) in the `Authorization` header with the “Bearer” scheme. The server then validates this token to grant or deny access.FastMCP supports Bearer Token authentication for its HTTP-based transports ( `http` and `sse`), allowing you to protect your server from unauthorized access.

## Authentication Strategy

FastMCP uses **asymmetric encryption** for token validation, which provides a clean security separation between token issuers and FastMCP servers. This approach means:

- **No shared secrets**: Your FastMCP server never needs access to private keys or client secrets
- **Public key verification**: The server only needs a public key (or JWKS endpoint) to verify token signatures
- **Secure token issuance**: Tokens are signed by an external service using a private key that never leaves the issuer
- **Scalable architecture**: Multiple FastMCP servers can validate tokens without coordinating secrets

This design allows you to integrate FastMCP servers into existing authentication infrastructures without compromising security boundaries.

## Token Verification Approaches

FastMCP provides three token verification approaches:

### JWTVerifier

Validates JWT tokens using public key cryptography. Use when you have JWT tokens issued by an external identity provider (Auth0, Okta, Keycloak, etc.) and want self-contained validation without network calls.

### IntrospectionTokenVerifier

Validates tokens by calling a remote OAuth 2.0 authorization server’s introspection endpoint (RFC 7662). Use when your authorization server is separate from your FastMCP server, you’re using opaque tokens, or you need real-time token revocation.

### StaticTokenVerifier

Validates tokens against a predefined dictionary. Use for development and testing only - never in production.

These verifiers validate tokens; they do **not** issue them (or implement any part of an OAuth flow). You’ll need to generate tokens separately, either using FastMCP utilities or an external Identity Provider (IdP) or OAuth 2.1 Authorization Server.

### Configuration Parameters

- JWTVerifier
- IntrospectionTokenVerifier
- StaticTokenVerifier

## JWTVerifier Configuration

public\_key

str

RSA public key in PEM format for static key validation. Required if `jwks_uri` is not provided

jwks\_uri

str

URL for JSON Web Key Set endpoint. Required if `public_key` is not provided

issuer

str \| None

Expected JWT `iss` claim value

algorithm

str \| None

Algorithm for decoding JWT token. Defaults to ‘RS256’

audience

str \| None

Expected JWT `aud` claim value

required\_scopes

list\[str\] \| None

Global scopes required for all requests

## JWT Verification

The `JWTVerifier` validates JWT tokens using public key cryptography. Use this when you have JWT tokens issued by an external identity provider and want self-contained validation without network calls.

Copy

```
from fastmcp import FastMCP
from fastmcp.server.auth.verifiers import JWTVerifier

verifier = JWTVerifier(
jwks_uri="https://my-identity-provider.com/.well-known/jwks.json",
issuer="https://my-identity-provider.com/",
audience="my-mcp-server"
)

mcp = FastMCP(name="My MCP Server", auth=verifier)

```

### Public Key Configuration

#### Using a Static Public Key

If you have a public key in PEM format, you can provide it to the `JWTVerifier` as a string.

Copy

```
from fastmcp.server.auth.verifiers import JWTVerifier
import inspect

public_key_pem = inspect.cleandoc(
"""
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAy...
-----END PUBLIC KEY-----
"""
)

auth = JWTVerifier(public_key=public_key_pem)

```

#### Using JWKS URI

Copy

```
verifier = JWTVerifier(
jwks_uri="https://idp.example.com/.well-known/jwks.json"
)

```

JWKS is recommended for production as it supports automatic key rotation and multiple signing keys.

## OAuth 2.0 Token Introspection

The `IntrospectionTokenVerifier` validates tokens by calling an OAuth 2.0 authorization server’s introspection endpoint (RFC 7662). This is useful when your authorization server is separate from your FastMCP server, you’re using opaque tokens, or you need real-time token validation with immediate revocation support.

Copy

```
from fastmcp.server.auth.verifiers import IntrospectionTokenVerifier

verifier = IntrospectionTokenVerifier(
introspection_endpoint="https://auth.company.com/oauth/introspect",
server_url="https://mcp.company.com", # This server's URL
client_id="mcp-resource-server",
client_secret="your-secret",
required_scopes=["mcp:access"]
)

mcp = FastMCP(name="MCP Server", auth=verifier)

```

For each request, the verifier makes an HTTP call to the introspection endpoint to check if the token is valid and active. This provides real-time validation but requires network connectivity.

## Static Token Verification

The `StaticTokenVerifier` validates tokens against a predefined dictionary of token strings and claims. Use this for development and testing when you need predictable tokens without setting up a real OAuth server.

Copy

```
from fastmcp.server.auth.verifiers import StaticTokenVerifier

verifier = StaticTokenVerifier(
tokens={
"dev-token-123": {
"client_id": "dev-user",
"scopes": ["read", "write"],
"sub": "developer@example.com"
},
"readonly-token": {
"client_id": "readonly-user",
"scopes": ["read"],
"expires_at": 1735689600 # Optional expiration
}
},
required_scopes=["read"]
)

mcp = FastMCP(name="Development Server", auth=verifier)

```

Token claims can include `client_id` (required), `scopes`, `sub`, `expires_at`, and any custom metadata your application needs.

Never use StaticTokenVerifier in production - tokens are stored in plain text.

## Generating Tokens

For development and testing, FastMCP provides the `RSAKeyPair` utility class to generate tokens without needing an external OAuth provider.

The `RSAKeyPair` utility is intended for development and testing only. For production, use a proper OAuth 2.1 Authorization Server or Identity Provider.

### Basic Token Generation

Copy

```
from fastmcp import FastMCP
from fastmcp.server.auth.verifiers import JWTVerifier, RSAKeyPair

# Generate a new key pair
key_pair = RSAKeyPair.generate()

# Configure the auth verifier with the public key
auth = JWTVerifier(
public_key=key_pair.public_key,
issuer="https://dev.example.com",
audience="my-dev-server"
)

mcp = FastMCP(name="Development Server", auth=auth)

# Generate a token for testing
token = key_pair.create_token(
subject="dev-user",
issuer="https://dev.example.com",
audience="my-dev-server",
scopes=["read", "write"]
)

print(f"Test token: {token}")

```

### Token Creation Parameters

The `create_token()` method accepts these parameters:

## create\_token() Parameters

subject

str

default:"fastmcp-user"

JWT subject claim (usually user ID)

issuer

str

default:"https://fastmcp.example.com"

JWT issuer claim

audience

str \| None

JWT audience claim

scopes

list\[str\] \| None

OAuth scopes to include

expires\_in\_seconds

int

default:"3600"

Token expiration time in seconds

additional\_claims

dict \| None

Extra claims to include in the token

kid

str \| None

Key ID for JWKS lookup

## Accessing Token Claims

Once authenticated, your tools, resources, or prompts can access token information using the `get_access_token()` dependency function:

Copy

```
from fastmcp import FastMCP, Context, ToolError
from fastmcp.server.dependencies import get_access_token, AccessToken

@mcp.tool
async def get_my_data(ctx: Context) -> dict:
access_token: AccessToken = get_access_token()

user_id = access_token.client_id # From JWT 'sub' or 'client_id' claim
user_scopes = access_token.scopes

if "data:read_sensitive" not in user_scopes:
raise ToolError("Insufficient permissions: 'data:read_sensitive' scope required.")

return {
"user": user_id,
"sensitive_data": f"Private data for {user_id}",
"granted_scopes": user_scopes
}

```

### AccessToken Properties

## AccessToken Properties

token

str

The raw JWT string

client\_id

str

Authenticated principal identifier

scopes

list\[str\]

Granted scopes

expires\_at

datetime \| None

Token expiration timestamp

[Middleware](https://gofastmcp.com/servers/middleware) [Overview](https://gofastmcp.com/clients/client)