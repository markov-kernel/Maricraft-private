# fastmcp.server.middleware.middleware
# fastmcp.server.middleware.middleware

> **Category:** fastmcp.server.middleware.middleware
> **Source:** gofastmcp.com_python-sdk_fastmcp-server-middleware-middleware.json

---

middleware

middleware

fastmcp.server.middleware.middleware

## Functions

make_middleware_wrapper

Copy

```
make_middleware_wrapper(middleware: Middleware, call_next: CallNext[T, R]) -> CallNext[T, R]

```

Create a wrapper that applies a single middleware to a context. The
closure bakes in the middleware and call\_next function, so it can be
passed to other functions that expect a call\_next function.

## Classes

CallNext

ServerResultProtocol

MiddlewareContext

Unified context for all middleware operations.**Methods:**

copy

Copy

```
copy(self, **kwargs: Any) -> MiddlewareContext[T]

```

Middleware

Base class for FastMCP middleware with dispatching hooks.**Methods:**

on_message

Copy

```
on_message(self, context: MiddlewareContext[Any], call_next: CallNext[Any, Any]) -> Any

```

on_request

Copy

```
on_request(self, context: MiddlewareContext[mt.Request], call_next: CallNext[mt.Request, Any]) -> Any

```

on_notification

Copy

```
on_notification(self, context: MiddlewareContext[mt.Notification], call_next: CallNext[mt.Notification, Any]) -> Any

```

on_call_tool

Copy

```
on_call_tool(self, context: MiddlewareContext[mt.CallToolRequestParams], call_next: CallNext[mt.CallToolRequestParams, mt.CallToolResult]) -> mt.CallToolResult

```

on_read_resource

Copy

```
on_read_resource(self, context: MiddlewareContext[mt.ReadResourceRequestParams], call_next: CallNext[mt.ReadResourceRequestParams, mt.ReadResourceResult]) -> mt.ReadResourceResult

```

on_get_prompt

Copy

```
on_get_prompt(self, context: MiddlewareContext[mt.GetPromptRequestParams], call_next: CallNext[mt.GetPromptRequestParams, mt.GetPromptResult]) -> mt.GetPromptResult

```

on_list_tools

Copy

```
on_list_tools(self, context: MiddlewareContext[mt.ListToolsRequest], call_next: CallNext[mt.ListToolsRequest, list[Tool]]) -> list[Tool]

```

on_list_resources

Copy

```
on_list_resources(self, context: MiddlewareContext[mt.ListResourcesRequest], call_next: CallNext[mt.ListResourcesRequest, list[Resource]]) -> list[Resource]

```

on_list_resource_templates

Copy

```
on_list_resource_templates(self, context: MiddlewareContext[mt.ListResourceTemplatesRequest], call_next: CallNext[mt.ListResourceTemplatesRequest, list[ResourceTemplate]]) -> list[ResourceTemplate]

```

on_list_prompts

Copy

```
on_list_prompts(self, context: MiddlewareContext[mt.ListPromptsRequest], call_next: CallNext[mt.ListPromptsRequest, list[Prompt]]) -> list[Prompt]

```

[logging](https://gofastmcp.com/python-sdk/fastmcp-server-middleware-logging) [rate\_limiting](https://gofastmcp.com/python-sdk/fastmcp-server-middleware-rate_limiting)