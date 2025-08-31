# fastmcp.resources.template
# fastmcp.resources.template

> **Category:** fastmcp.resources.template
> **Source:** gofastmcp.com_python-sdk_fastmcp-resources-template.json

---

fastmcp.resources

template

fastmcp.resources.template

Resource template functionality.

## Functions

build_regex

Copy

```
build_regex(template: str) -> re.Pattern

```

match_uri_template

Copy

```
match_uri_template(uri: str, uri_template: str) -> dict[str, str] | None

```

## Classes

ResourceTemplate

A template for dynamically creating resources.**Methods:**

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

from_function

Copy

```
from_function(fn: Callable[..., Any], uri_template: str, name: str | None = None, title: str | None = None, description: str | None = None, mime_type: str | None = None, tags: set[str] | None = None, enabled: bool | None = None) -> FunctionResourceTemplate

```

set_default_mime_type

Copy

```
set_default_mime_type(cls, mime_type: str | None) -> str

```

Set default MIME type if not provided.

matches

Copy

```
matches(self, uri: str) -> dict[str, Any] | None

```

Check if URI matches template and extract parameters.

read

Copy

```
read(self, arguments: dict[str, Any]) -> str | bytes

```

Read the resource content.

create_resource

Copy

```
create_resource(self, uri: str, params: dict[str, Any]) -> Resource

```

Create a resource from the template with the given parameters.

to_mcp_template

Copy

```
to_mcp_template(self, **overrides: Any) -> MCPResourceTemplate

```

Convert the resource template to an MCPResourceTemplate.

from_mcp_template

Copy

```
from_mcp_template(cls, mcp_template: MCPResourceTemplate) -> ResourceTemplate

```

Creates a FastMCP ResourceTemplate from a raw MCP ResourceTemplate object.

key

Copy

```
key(self) -> str

```

The key of the component. This is used for internal bookkeeping
and may reflect e.g. prefixes or other identifiers. You should not depend on
keys having a certain value, as the same tool loaded from different
hierarchies of servers may have different keys.

FunctionResourceTemplate

A template for dynamically creating resources.**Methods:**

read

Copy

```
read(self, arguments: dict[str, Any]) -> str | bytes

```

Read the resource content.

from_function

Copy

```
from_function(cls, fn: Callable[..., Any], uri_template: str, name: str | None = None, title: str | None = None, description: str | None = None, mime_type: str | None = None, tags: set[str] | None = None, enabled: bool | None = None) -> FunctionResourceTemplate

```

Create a template from a function.

[resource\_manager](https://gofastmcp.com/python-sdk/fastmcp-resources-resource_manager) [types](https://gofastmcp.com/python-sdk/fastmcp-resources-types)