# fastmcp.client.auth.oauth
# fastmcp.client.auth.oauth

> **Category:** fastmcp.client.auth.oauth
> **Source:** gofastmcp.com_python-sdk_fastmcp-client-auth-oauth.json

---

auth

oauth

fastmcp.client.auth.oauth

## Functions

default_cache_dir

Copy

```
default_cache_dir() -> Path

```

discover_oauth_metadata

Copy

```
discover_oauth_metadata(server_base_url: str, httpx_kwargs: dict[str, Any] | None = None) -> OAuthMetadata | None

```

Discover OAuth metadata from the server using RFC 8414 well-known endpoint.**Args:**

- `server_base_url`: Base URL of the OAuth server (e.g., “ [https://example.com](https://example.com/)”)
- `httpx_kwargs`: Additional kwargs for httpx client

**Returns:**

- OAuth metadata if found, None otherwise

check_if_auth_required

Copy

```
check_if_auth_required(mcp_url: str, httpx_kwargs: dict[str, Any] | None = None) -> bool

```

Check if the MCP endpoint requires authentication by making a test request.**Returns:**

- True if auth appears to be required, False otherwise

OAuth

Copy

```
OAuth(mcp_url: str, scopes: str | list[str] | None = None, client_name: str = 'FastMCP Client', token_storage_cache_dir: Path | None = None, additional_client_metadata: dict[str, Any] | None = None) -> OAuthClientProvider

```

Create an OAuthClientProvider for an MCP server.This is intended to be provided to the `auth` parameter of an
httpx.AsyncClient (or appropriate FastMCP client/transport instance)**Args:**

- `mcp_url`: Full URL to the MCP endpoint (e.g. “http://host/mcp/sse/”)
- `scopes`: OAuth scopes to request. Can be a
- `client_name`: Name for this client during registration
- `token_storage_cache_dir`: Directory for FileTokenStorage
- `additional_client_metadata`: Extra fields for OAuthClientMetadata

**Returns:**

- OAuthClientProvider

## Classes

FileTokenStorage

File-based token storage implementation for OAuth credentials and tokens.
Implements the mcp.client.auth.TokenStorage protocol.Each instance is tied to a specific server URL for proper token isolation.**Methods:**

get_base_url

Copy

```
get_base_url(url: str) -> str

```

Extract the base URL (scheme + host) from a URL.

get_cache_key

Copy

```
get_cache_key(self) -> str

```

Generate a safe filesystem key from the server’s base URL.

get_tokens

Copy

```
get_tokens(self) -> OAuthToken | None

```

Load tokens from file storage.

set_tokens

Copy

```
set_tokens(self, tokens: OAuthToken) -> None

```

Save tokens to file storage.

get_client_info

Copy

```
get_client_info(self) -> OAuthClientInformationFull | None

```

Load client information from file storage.

set_client_info

Copy

```
set_client_info(self, client_info: OAuthClientInformationFull) -> None

```

Save client information to file storage.

clear

Copy

```
clear(self) -> None

```

Clear all cached data for this server.

clear_all

Copy

```
clear_all(cls, cache_dir: Path | None = None) -> None

```

Clear all cached data for all servers.

[bearer](https://gofastmcp.com/python-sdk/fastmcp-client-auth-bearer) [client](https://gofastmcp.com/python-sdk/fastmcp-client-client)