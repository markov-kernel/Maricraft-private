# fastmcp.server.middleware.timing
# fastmcp.server.middleware.timing

> **Category:** fastmcp.server.middleware.timing
> **Source:** gofastmcp.com_python-sdk_fastmcp-server-middleware-timing.json

---

middleware

timing

fastmcp.server.middleware.timing

Timing middleware for measuring and logging request performance.

## Classes

TimingMiddleware

Middleware that logs the execution time of requests.Only measures and logs timing for request messages (not notifications).
Provides insights into performance characteristics of your MCP server.**Methods:**

on_request

Copy

```
on_request(self, context: MiddlewareContext, call_next: CallNext) -> Any

```

Time request execution and log the results.

DetailedTimingMiddleware

Enhanced timing middleware with per-operation breakdowns.Provides detailed timing information for different types of MCP operations,
allowing you to identify performance bottlenecks in specific operations.**Methods:**

on_call_tool

Copy

```
on_call_tool(self, context: MiddlewareContext, call_next: CallNext) -> Any

```

Time tool execution.

on_read_resource

Copy

```
on_read_resource(self, context: MiddlewareContext, call_next: CallNext) -> Any

```

Time resource reading.

on_get_prompt

Copy

```
on_get_prompt(self, context: MiddlewareContext, call_next: CallNext) -> Any

```

Time prompt retrieval.

on_list_tools

Copy

```
on_list_tools(self, context: MiddlewareContext, call_next: CallNext) -> Any

```

Time tool listing.

on_list_resources

Copy

```
on_list_resources(self, context: MiddlewareContext, call_next: CallNext) -> Any

```

Time resource listing.

on_list_resource_templates

Copy

```
on_list_resource_templates(self, context: MiddlewareContext, call_next: CallNext) -> Any

```

Time resource template listing.

on_list_prompts

Copy

```
on_list_prompts(self, context: MiddlewareContext, call_next: CallNext) -> Any

```

Time prompt listing.

[rate\_limiting](https://gofastmcp.com/python-sdk/fastmcp-server-middleware-rate_limiting) [openapi](https://gofastmcp.com/python-sdk/fastmcp-server-openapi)