# fastmcp.server.context
# fastmcp.server.context

> **Category:** fastmcp.server.context
> **Source:** gofastmcp.com_python-sdk_fastmcp-server-context.json

---

context

fastmcp.server.context

## Functions

set_context

Copy

```
set_context(context: Context) -> Generator[Context, None, None]

```

## Classes

Context

Context object providing access to MCP capabilities.This provides a cleaner interface to MCP’s RequestContext functionality.
It gets injected into tool and resource functions that request it via type hints.To use context in a tool function, add a parameter with the Context type annotation:

Copy

```
@server.tool
def my_tool(x: int, ctx: Context) -> str:
# Log messages to the client
ctx.info(f"Processing {x}")
ctx.debug("Debug info")
ctx.warning("Warning message")
ctx.error("Error message")

# Report progress
ctx.report_progress(50, 100, "Processing")

# Access resources
data = ctx.read_resource("resource://data")

# Get request info
request_id = ctx.request_id
client_id = ctx.client_id

# Manage state across the request
ctx.set_state_value("key", "value")
value = ctx.get_state_value("key")

return str(x)

```

State Management:
Context objects maintain a state dictionary that can be used to store and share
data across middleware and tool calls within a request. When a new context
is created (nested contexts), it inherits a copy of its parent’s state, ensuring
that modifications in child contexts don’t affect parent contexts.The context parameter name can be anything as long as it’s annotated with Context.
The context is optional - tools that don’t need it can omit the parameter.**Methods:**

request_context

Copy

```
request_context(self) -> RequestContext

```

Access to the underlying request context.If called outside of a request context, this will raise a ValueError.

report_progress

Copy

```
report_progress(self, progress: float, total: float | None = None, message: str | None = None) -> None

```

Report progress for the current operation.**Args:**

- `progress`: Current progress value e.g. 24
- `total`: Optional total value e.g. 100

read_resource

Copy

```
read_resource(self, uri: str | AnyUrl) -> list[ReadResourceContents]

```

Read a resource by URI.**Args:**

- `uri`: Resource URI to read

**Returns:**

- The resource content as either text or bytes

log

Copy

```
log(self, message: str, level: LoggingLevel | None = None, logger_name: str | None = None) -> None

```

Send a log message to the client.**Args:**

- `message`: Log message
- `level`: Optional log level. One of “debug”, “info”, “notice”, “warning”, “error”, “critical”,
“alert”, or “emergency”. Default is “info”.
- `logger_name`: Optional logger name

client_id

Copy

```
client_id(self) -> str | None

```

Get the client ID if available.

request_id

Copy

```
request_id(self) -> str

```

Get the unique ID for this request.

session_id

Copy

```
session_id(self) -> str | None

```

Get the MCP session ID for HTTP transports.Returns the session ID that can be used as a key for session-based
data storage (e.g., Redis) to share data between tool calls within
the same client session.**Returns:**

- The session ID for HTTP transports (SSE, StreamableHTTP), or None
- for stdio and in-memory transports which don’t use session IDs.

session

Copy

```
session(self) -> ServerSession

```

Access to the underlying session for advanced usage.

debug

Copy

```
debug(self, message: str, logger_name: str | None = None) -> None

```

Send a debug log message.

info

Copy

```
info(self, message: str, logger_name: str | None = None) -> None

```

Send an info log message.

warning

Copy

```
warning(self, message: str, logger_name: str | None = None) -> None

```

Send a warning log message.

error

Copy

```
error(self, message: str, logger_name: str | None = None) -> None

```

Send an error log message.

list_roots

Copy

```
list_roots(self) -> list[Root]

```

List the roots available to the server, as indicated by the client.

send_tool_list_changed

Copy

```
send_tool_list_changed(self) -> None

```

Send a tool list changed notification to the client.

send_resource_list_changed

Copy

```
send_resource_list_changed(self) -> None

```

Send a resource list changed notification to the client.

send_prompt_list_changed

Copy

```
send_prompt_list_changed(self) -> None

```

Send a prompt list changed notification to the client.

sample

Copy

```
sample(self, messages: str | list[str | SamplingMessage], system_prompt: str | None = None, include_context: IncludeContext | None = None, temperature: float | None = None, max_tokens: int | None = None, model_preferences: ModelPreferences | str | list[str] | None = None) -> ContentBlock

```

Send a sampling request to the client and await the response.Call this method at any time to have the server request an LLM
completion from the client. The client must be appropriately configured,
or the request will error.

elicit

Copy

```
elicit(self, message: str, response_type: None) -> AcceptedElicitation[dict[str, Any]] | DeclinedElicitation | CancelledElicitation

```

elicit

Copy

```
elicit(self, message: str, response_type: type[T]) -> AcceptedElicitation[T] | DeclinedElicitation | CancelledElicitation

```

elicit

Copy

```
elicit(self, message: str, response_type: list[str]) -> AcceptedElicitation[str] | DeclinedElicitation | CancelledElicitation

```

elicit

Copy

```
elicit(self, message: str, response_type: type[T] | list[str] | None = None) -> AcceptedElicitation[T] | AcceptedElicitation[dict[str, Any]] | AcceptedElicitation[str] | DeclinedElicitation | CancelledElicitation

```

Send an elicitation request to the client and await the response.Call this method at any time to request additional information from
the user through the client. The client must support elicitation,
or the request will error.Note that the MCP protocol only supports simple object schemas with
primitive types. You can provide a dataclass, TypedDict, or BaseModel to
comply. If you provide a primitive type, an object schema with a single
“value” field will be generated for the MCP interaction and
automatically deconstructed into the primitive type upon response.If the response\_type is None, the generated schema will be that of an
empty object in order to comply with the MCP protocol requirements.
Clients must send an empty object ("")in response.**Args:**

- `message`: A human-readable message explaining what information is needed
- `response_type`: The type of the response, which should be a primitive
type or dataclass or BaseModel. If it is a primitive type, an
object schema with a single “value” field will be generated.

get_http_request

Copy

```
get_http_request(self) -> Request

```

Get the active starlette request.

set_state

Copy

```
set_state(self, key: str, value: Any) -> None

```

Set a value in the context state.

get_state

Copy

```
get_state(self, key: str) -> Any

```

Get a value from the context state. Returns None if the key is not found.

[in\_memory](https://gofastmcp.com/python-sdk/fastmcp-server-auth-providers-in_memory) [dependencies](https://gofastmcp.com/python-sdk/fastmcp-server-dependencies)