# fastmcp.tools.tool
# fastmcp.tools.tool

> **Category:** fastmcp.tools.tool
> **Source:** gofastmcp.com_python-sdk_fastmcp-tools-tool.json

---

fastmcp.tools

tool

fastmcp.tools.tool

## Functions

default_serializer

Copy

```
default_serializer(data: Any) -> str

```

## Classes

ToolResult

**Methods:**

to_mcp_result

Copy

```
to_mcp_result(self) -> list[ContentBlock] | tuple[list[ContentBlock], dict[str, Any]]

```

Tool

Internal tool registration info.**Methods:**

enable

Copy

```
enable(self) -> None

```

disable

Copy

```
disable(self) -> None

```

to_mcp_tool

Copy

```
to_mcp_tool(self, **overrides: Any) -> MCPTool

```

from_function

Copy

```
from_function(fn: Callable[..., Any], name: str | None = None, title: str | None = None, description: str | None = None, tags: set[str] | None = None, annotations: ToolAnnotations | None = None, exclude_args: list[str] | None = None, output_schema: dict[str, Any] | None | NotSetT | Literal[False] = NotSet, serializer: Callable[[Any], str] | None = None, enabled: bool | None = None) -> FunctionTool

```

Create a Tool from a function.

run

Copy

```
run(self, arguments: dict[str, Any]) -> ToolResult

```

Run the tool with arguments.This method is not implemented in the base Tool class and must be
implemented by subclasses.`run()` can EITHER return a list of ContentBlocks, or a tuple of
(list of ContentBlocks, dict of structured output).

from_tool

Copy

```
from_tool(cls, tool: Tool, transform_fn: Callable[..., Any] | None = None, name: str | None = None, title: str | None | NotSetT = NotSet, transform_args: dict[str, ArgTransform] | None = None, description: str | None | NotSetT = NotSet, tags: set[str] | None = None, annotations: ToolAnnotations | None = None, output_schema: dict[str, Any] | None | Literal[False] = None, serializer: Callable[[Any], str] | None = None, enabled: bool | None = None) -> TransformedTool

```

FunctionTool

**Methods:**

from_function

Copy

```
from_function(cls, fn: Callable[..., Any], name: str | None = None, title: str | None = None, description: str | None = None, tags: set[str] | None = None, annotations: ToolAnnotations | None = None, exclude_args: list[str] | None = None, output_schema: dict[str, Any] | None | NotSetT | Literal[False] = NotSet, serializer: Callable[[Any], str] | None = None, enabled: bool | None = None) -> FunctionTool

```

Create a Tool from a function.

run

Copy

```
run(self, arguments: dict[str, Any]) -> ToolResult

```

Run the tool with arguments.

ParsedFunction

**Methods:**

from_function

Copy

```
from_function(cls, fn: Callable[..., Any], exclude_args: list[str] | None = None, validate: bool = True, wrap_non_object_output_schema: bool = True) -> ParsedFunction

```

[\_\_init\_\_](https://gofastmcp.com/python-sdk/fastmcp-tools-__init__) [tool\_manager](https://gofastmcp.com/python-sdk/fastmcp-tools-tool_manager)