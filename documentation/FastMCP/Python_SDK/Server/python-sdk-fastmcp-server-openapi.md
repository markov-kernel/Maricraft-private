# fastmcp.server.openapi
# fastmcp.server.openapi

> **Category:** fastmcp.server.openapi
> **Source:** gofastmcp.com_python-sdk_fastmcp-server-openapi.json

---

openapi

fastmcp.server.openapi

FastMCP server implementation for OpenAPI integration.

## Classes

MCPType

Type of FastMCP component to create from a route.

RouteType

Deprecated: Use MCPType instead.This enum is kept for backward compatibility and will be removed in a future version.

RouteMap

Mapping configuration for HTTP routes to FastMCP component types.

OpenAPITool

Tool implementation for OpenAPI endpoints.**Methods:**

run

Copy

```
run(self, arguments: dict[str, Any]) -> ToolResult

```

Execute the HTTP request based on the route configuration.

OpenAPIResource

Resource implementation for OpenAPI endpoints.**Methods:**

read

Copy

```
read(self) -> str | bytes

```

Fetch the resource data by making an HTTP request.

OpenAPIResourceTemplate

Resource template implementation for OpenAPI endpoints.**Methods:**

create_resource

Copy

```
create_resource(self, uri: str, params: dict[str, Any], context: Context | None = None) -> Resource

```

Create a resource with the given parameters.

FastMCPOpenAPI

FastMCP server implementation that creates components from an OpenAPI schema.This class parses an OpenAPI specification and creates appropriate FastMCP components
(Tools, Resources, ResourceTemplates) based on route mappings.

[timing](https://gofastmcp.com/python-sdk/fastmcp-server-middleware-timing) [proxy](https://gofastmcp.com/python-sdk/fastmcp-server-proxy)