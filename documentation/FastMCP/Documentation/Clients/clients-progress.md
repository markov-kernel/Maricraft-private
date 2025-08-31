# Override with specific progress handler for this call
# Override with specific progress handler for this call

> **Category:** Clients
> **Source:** gofastmcp.com_clients_progress.json

---

Advanced Features

Progress Monitoring

`New in version: 2.3.5` MCP servers can report progress during long-running operations. The client can receive these updates through a progress handler.

## Progress Handler

Set a progress handler when creating the client:

Copy

```
from fastmcp import Client

async def my_progress_handler(
progress: float,
total: float | None,
message: str | None
) -> None:
if total is not None:
percentage = (progress / total) * 100
print(f"Progress: {percentage:.1f}% - {message or ''}")
else:
print(f"Progress: {progress} - {message or ''}")

client = Client(
"my_mcp_server.py",
progress_handler=my_progress_handler
)

```

### Handler Parameters

The progress handler receives three parameters:

## Progress Handler Parameters

progress

float

Current progress value

total

float \| None

Expected total value (may be None)

message

str \| None

Optional status message (may be None)

## Per-Call Progress Handler

Override the progress handler for specific tool calls:

Copy

```
async with client:
# Override with specific progress handler for this call
result = await client.call_tool(
"long_running_task",
{"param": "value"},
progress_handler=my_progress_handler
)

```

[Logging](https://gofastmcp.com/clients/logging) [Sampling](https://gofastmcp.com/clients/sampling)