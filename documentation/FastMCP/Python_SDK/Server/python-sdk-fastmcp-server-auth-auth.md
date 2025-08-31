# fastmcp.server.auth.auth
# fastmcp.server.auth.auth

> **Category:** fastmcp.server.auth.auth
> **Source:** gofastmcp.com_python-sdk_fastmcp-server-auth-auth.json

---

auth

auth

fastmcp.server.auth.auth

## Classes

OAuthProvider

**Methods:**

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

[\_\_init\_\_](https://gofastmcp.com/python-sdk/fastmcp-server-auth-__init__) [\_\_init\_\_](https://gofastmcp.com/python-sdk/fastmcp-server-auth-providers-__init__)