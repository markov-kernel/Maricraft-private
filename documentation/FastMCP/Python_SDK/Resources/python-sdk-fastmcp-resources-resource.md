# fastmcp.resources.resource
# fastmcp.resources.resource

> **Category:** fastmcp.resources.resource
> **Source:** gofastmcp.com_python-sdk_fastmcp-resources-resource.json

---

fastmcp.resources

resource

fastmcp.resources.resource

Base classes and interfaces for FastMCP resources.

## Classes

Resource

Base class for all resources.**Methods:**

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
from_function(fn: Callable[..., Any], uri: str | AnyUrl, name: str | None = None, title: str | None = None, description: str | None = None, mime_type: str | None = None, tags: set[str] | None = None, enabled: bool | None = None) -> FunctionResource

```

set_default_mime_type

Copy

```
set_default_mime_type(cls, mime_type: str | None) -> str

```

Set default MIME type if not provided.

set_default_name

Copy

```
set_default_name(self) -> Self

```

Set default name from URI if not provided.

read

Copy

```
read(self) -> str | bytes

```

Read the resource content.

to_mcp_resource

Copy

```
to_mcp_resource(self, **overrides: Any) -> MCPResource

```

Convert the resource to an MCPResource.

key

Copy

```
key(self) -> str

```

The key of the component. This is used for internal bookkeeping
and may reflect e.g. prefixes or other identifiers. You should not depend on
keys having a certain value, as the same tool loaded from different
hierarchies of servers may have different keys.

FunctionResource

A resource that defers data loading by wrapping a function.The function is only called when the resource is read, allowing for lazy loading
of potentially expensive data. This is particularly useful when listing resources,
as the function won’t be called until the resource is actually accessed.The function can return:

- str for text content (default)
- bytes for binary content
- other types will be converted to JSON

**Methods:**

from_function

Copy

```
from_function(cls, fn: Callable[..., Any], uri: str | AnyUrl, name: str | None = None, title: str | None = None, description: str | None = None, mime_type: str | None = None, tags: set[str] | None = None, enabled: bool | None = None) -> FunctionResource

```

Create a FunctionResource from a function.

read

Copy

```
read(self) -> str | bytes

```

Read the resource by calling the wrapped function.

[\_\_init\_\_](https://gofastmcp.com/python-sdk/fastmcp-resources-__init__) [resource\_manager](https://gofastmcp.com/python-sdk/fastmcp-resources-resource_manager)