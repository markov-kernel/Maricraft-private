# fastmcp.tools.tool_manager
# fastmcp.tools.tool_manager

> **Category:** fastmcp.tools.tool/manager
> **Source:** gofastmcp.com_python-sdk_fastmcp-tools-tool_manager.json

---

fastmcp.tools

tool\_manager

fastmcp.tools.tool_manager

## Classes

ToolManager

Manages FastMCP tools.**Methods:**

mount

Copy

```
mount(self, server: MountedServer) -> None

```

Adds a mounted server as a source for tools.

has_tool

Copy

```
has_tool(self, key: str) -> bool

```

Check if a tool exists.

get_tool

Copy

```
get_tool(self, key: str) -> Tool

```

Get tool by key.

get_tools

Copy

```
get_tools(self) -> dict[str, Tool]

```

Gets the complete, unfiltered inventory of all tools.

list_tools

Copy

```
list_tools(self) -> list[Tool]

```

Lists all tools, applying protocol filtering.

add_tool_from_fn

Copy

```
add_tool_from_fn(self, fn: Callable[..., Any], name: str | None = None, description: str | None = None, tags: set[str] | None = None, annotations: ToolAnnotations | None = None, serializer: Callable[[Any], str] | None = None, exclude_args: list[str] | None = None) -> Tool

```

Add a tool to the server.

add_tool

Copy

```
add_tool(self, tool: Tool) -> Tool

```

Register a tool with the server.

add_tool_transformation

Copy

```
add_tool_transformation(self, tool_name: str, transformation: ToolTransformConfig) -> None

```

Add a tool transformation.

get_tool_transformation

Copy

```
get_tool_transformation(self, tool_name: str) -> ToolTransformConfig | None

```

Get a tool transformation.

remove_tool_transformation

Copy

```
remove_tool_transformation(self, tool_name: str) -> None

```

Remove a tool transformation.

remove_tool

Copy

```
remove_tool(self, key: str) -> None

```

Remove a tool from the server.**Args:**

- `key`: The key of the tool to remove

**Raises:**

- `NotFoundError`: If the tool is not found

call_tool

Copy

```
call_tool(self, key: str, arguments: dict[str, Any]) -> ToolResult

```

Internal API for servers: Finds and calls a tool, respecting the
filtered protocol path.

[tool](https://gofastmcp.com/python-sdk/fastmcp-tools-tool) [tool\_transform](https://gofastmcp.com/python-sdk/fastmcp-tools-tool_transform)