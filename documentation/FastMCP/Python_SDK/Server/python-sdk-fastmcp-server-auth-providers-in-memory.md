# fastmcp.server.auth.providers.in_memory
# fastmcp.server.auth.providers.in_memory

> **Category:** fastmcp.server.auth.providers.in/memory
> **Source:** gofastmcp.com_python-sdk_fastmcp-server-auth-providers-in_memory.json

---

providers

in\_memory

fastmcp.server.auth.providers.in_memory

## Classes

InMemoryOAuthProvider

An in-memory OAuth provider for testing purposes.
It simulates the OAuth 2.1 flow locally without external calls.**Methods:**

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

Simulates user authorization and generates an authorization code.
Returns a redirect URI with the code and state.

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

load_access_token

Copy

```
load_access_token(self, token: str) -> AccessToken | None

```

verify_token

Copy

```
verify_token(self, token: str) -> AccessToken | None

```

Verify a bearer token and return access info if valid.This method implements the TokenVerifier protocol by delegating
to our existing load\_access\_token method.**Args:**

- `token`: The token string to validate

**Returns:**

- AccessToken object if valid, None if invalid or expired

revoke_token

Copy

```
revoke_token(self, token: AccessToken | RefreshToken) -> None

```

Revokes an access or refresh token and its counterpart.

[bearer\_env](https://gofastmcp.com/python-sdk/fastmcp-server-auth-providers-bearer_env) [context](https://gofastmcp.com/python-sdk/fastmcp-server-context)