# Server logs will be emitted at DEBUG level automatically
# Server logs will be emitted at DEBUG level automatically

> **Category:** Clients
> **Source:** gofastmcp.com_clients_logging.json

---

Advanced Features

Server Logging

`New in version: 2.0.0` MCP servers can emit log messages to clients. The client can handle these logs through a log handler callback.

## Log Handler

Provide a `log_handler` function when creating the client:

Copy

```
from fastmcp import Client
from fastmcp.client.logging import LogMessage

async def log_handler(message: LogMessage):
level = message.level.upper()
logger = message.logger or 'server'
data = message.data
print(f"[{level}] {logger}: {data}")

client = Client(
"my_mcp_server.py",
log_handler=log_handler,
)

```

### Handler Parameters

The `log_handler` is called every time a log message is received. It receives a `LogMessage` object:

## Log Handler Parameters

LogMessage

Log Message Object

Show attributes

level

Literal\["debug", "info", "notice", "warning", "error", "critical", "alert", "emergency"\]

The log level

logger

str \| None

The logger name (optional, may be None)

data

Any

The actual log message content

Copy

```
async def detailed_log_handler(message: LogMessage):
if message.level == "error":
print(f"ERROR: {message.data}")
elif message.level == "warning":
print(f"WARNING: {message.data}")
else:
print(f"{message.level.upper()}: {message.data}")

```

## Default Log Handling

If you don’t provide a custom `log_handler`, FastMCP uses a default handler that emits a DEBUG-level FastMCP log for every log message received from the server, which is useful for visibility without polluting your own logs.

Copy

```
client = Client("my_mcp_server.py")

async with client:
# Server logs will be emitted at DEBUG level automatically
await client.call_tool("some_tool")

```

[Elicitation](https://gofastmcp.com/clients/elicitation) [Progress](https://gofastmcp.com/clients/progress)