# fastmcp.server.proxy
# fastmcp.server.proxy

> **Category:** fastmcp.server.proxy
> **Source:** gofastmcp.com_python-sdk_fastmcp-server-proxy.json

---

proxy

fastmcp.server.proxy

## Functions

default_proxy_roots_handler

Copy

```
default_proxy_roots_handler(context: RequestContext[ClientSession, LifespanContextT]) -> RootsList

```

A handler that forwards the list roots request from the remote server to the proxy’s connected clients and relays the response back to the remote server.

## Classes

ProxyToolManager

A ToolManager that sources its tools from a remote client in addition to local and mounted tools.**Methods:**

get_tools

Copy

```
get_tools(self) -> dict[str, Tool]

```

Gets the unfiltered tool inventory including local, mounted, and proxy tools.

list_tools

Copy

```
list_tools(self) -> list[Tool]

```

Gets the filtered list of tools including local, mounted, and proxy tools.

call_tool

Copy

```
call_tool(self, key: str, arguments: dict[str, Any]) -> ToolResult

```

Calls a tool, trying local/mounted first, then proxy if not found.

ProxyResourceManager

A ResourceManager that sources its resources from a remote client in addition to local and mounted resources.**Methods:**

get_resources

Copy

```
get_resources(self) -> dict[str, Resource]

```

Gets the unfiltered resource inventory including local, mounted, and proxy resources.

get_resource_templates

Copy

```
get_resource_templates(self) -> dict[str, ResourceTemplate]

```

Gets the unfiltered template inventory including local, mounted, and proxy templates.

list_resources

Copy

```
list_resources(self) -> list[Resource]

```

Gets the filtered list of resources including local, mounted, and proxy resources.

list_resource_templates

Copy

```
list_resource_templates(self) -> list[ResourceTemplate]

```

Gets the filtered list of templates including local, mounted, and proxy templates.

read_resource

Copy

```
read_resource(self, uri: AnyUrl | str) -> str | bytes

```

Reads a resource, trying local/mounted first, then proxy if not found.

ProxyPromptManager

A PromptManager that sources its prompts from a remote client in addition to local and mounted prompts.**Methods:**

get_prompts

Copy

```
get_prompts(self) -> dict[str, Prompt]

```

Gets the unfiltered prompt inventory including local, mounted, and proxy prompts.

list_prompts

Copy

```
list_prompts(self) -> list[Prompt]

```

Gets the filtered list of prompts including local, mounted, and proxy prompts.

render_prompt

Copy

```
render_prompt(self, name: str, arguments: dict[str, Any] | None = None) -> GetPromptResult

```

Renders a prompt, trying local/mounted first, then proxy if not found.

ProxyTool

A Tool that represents and executes a tool on a remote server.**Methods:**

from_mcp_tool

Copy

```
from_mcp_tool(cls, client: Client, mcp_tool: mcp.types.Tool) -> ProxyTool

```

Factory method to create a ProxyTool from a raw MCP tool schema.

run

Copy

```
run(self, arguments: dict[str, Any], context: Context | None = None) -> ToolResult

```

Executes the tool by making a call through the client.

ProxyResource

A Resource that represents and reads a resource from a remote server.**Methods:**

from_mcp_resource

Copy

```
from_mcp_resource(cls, client: Client, mcp_resource: mcp.types.Resource) -> ProxyResource

```

Factory method to create a ProxyResource from a raw MCP resource schema.

read

Copy

```
read(self) -> str | bytes

```

Read the resource content from the remote server.

ProxyTemplate

A ResourceTemplate that represents and creates resources from a remote server template.**Methods:**

from_mcp_template

Copy

```
from_mcp_template(cls, client: Client, mcp_template: mcp.types.ResourceTemplate) -> ProxyTemplate

```

Factory method to create a ProxyTemplate from a raw MCP template schema.

create_resource

Copy

```
create_resource(self, uri: str, params: dict[str, Any], context: Context | None = None) -> ProxyResource

```

Create a resource from the template by calling the remote server.

ProxyPrompt

A Prompt that represents and renders a prompt from a remote server.**Methods:**

from_mcp_prompt

Copy

```
from_mcp_prompt(cls, client: Client, mcp_prompt: mcp.types.Prompt) -> ProxyPrompt

```

Factory method to create a ProxyPrompt from a raw MCP prompt schema.

render

Copy

```
render(self, arguments: dict[str, Any]) -> list[PromptMessage]

```

Render the prompt by making a call through the client.

FastMCPProxy

A FastMCP server that acts as a proxy to a remote MCP-compliant server.
It uses specialized managers that fulfill requests via a client factory.

ProxyClient

A proxy client that forwards advanced interactions between a remote MCP server and the proxy’s connected clients.
Supports forwarding roots, sampling, elicitation, logging, and progress.**Methods:**

default_sampling_handler

Copy

```
default_sampling_handler(cls, messages: list[mcp.types.SamplingMessage], params: mcp.types.CreateMessageRequestParams, context: RequestContext[ClientSession, LifespanContextT]) -> mcp.types.CreateMessageResult

```

A handler that forwards the sampling request from the remote server to the proxy’s connected clients and relays the response back to the remote server.

default_elicitation_handler

Copy

```
default_elicitation_handler(cls, message: str, response_type: type, params: mcp.types.ElicitRequestParams, context: RequestContext[ClientSession, LifespanContextT]) -> ElicitResult

```

A handler that forwards the elicitation request from the remote server to the proxy’s connected clients and relays the response back to the remote server.

default_log_handler

Copy

```
default_log_handler(cls, message: LogMessage) -> None

```

A handler that forwards the log notification from the remote server to the proxy’s connected clients.

default_progress_handler

Copy

```
default_progress_handler(cls, progress: float, total: float | None, message: str | None) -> None

```

A handler that forwards the progress notification from the remote server to the proxy’s connected clients.

StatefulProxyClient

A proxy client that provides a stateful client factory for the proxy server.The stateful proxy client bound its copy to the server session.
And it will be disconnected when the session is exited.This is useful to proxy a stateful mcp server such as the Playwright MCP server.
Note that it is essential to ensure that the proxy server itself is also stateful.**Methods:**

new_stateful

Copy

```
new_stateful(self) -> Client[ClientTransportT]

```

Create a new stateful proxy client instance with the same configuration.Use this method as the client factory for stateful proxy server.

[openapi](https://gofastmcp.com/python-sdk/fastmcp-server-openapi) [server](https://gofastmcp.com/python-sdk/fastmcp-server-server)