# Clients Roots
# Clients Roots

> **Category:** Clients
> **Source:** gofastmcp.com_clients_roots.json

---

Advanced Features

Client Roots

`New in version: 2.0.0` Roots are a way for clients to inform servers about the resources they have access to. Servers can use this information to adjust behavior or provide more relevant responses.

## Setting Static Roots

Provide a list of roots when creating the client:

Static Roots

Dynamic Roots Callback

Copy

```
from fastmcp import Client

client = Client(
"my_mcp_server.py",
roots=["/path/to/root1", "/path/to/root2"]
)

```

[Messages](https://gofastmcp.com/clients/messages) [OAuth](https://gofastmcp.com/clients/auth/oauth)