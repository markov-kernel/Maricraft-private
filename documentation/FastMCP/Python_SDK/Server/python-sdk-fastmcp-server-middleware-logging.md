# fastmcp.server.middleware.logging
# fastmcp.server.middleware.logging

> **Category:** fastmcp.server.middleware.logging
> **Source:** gofastmcp.com_python-sdk_fastmcp-server-middleware-logging.json

---

middleware

logging

fastmcp.server.middleware.logging

Comprehensive logging middleware for FastMCP servers.

## Classes

LoggingMiddleware

Middleware that provides comprehensive request and response logging.Logs all MCP messages with configurable detail levels. Useful for debugging,
monitoring, and understanding server usage patterns.**Methods:**

on_message

Copy

```
on_message(self, context: MiddlewareContext, call_next: CallNext) -> Any

```

Log all messages.

StructuredLoggingMiddleware

Middleware that provides structured JSON logging for better log analysis.Outputs structured logs that are easier to parse and analyze with log
aggregation tools like ELK stack, Splunk, or cloud logging services.**Methods:**

on_message

Copy

```
on_message(self, context: MiddlewareContext, call_next: CallNext) -> Any

```

Log structured message information.

[error\_handling](https://gofastmcp.com/python-sdk/fastmcp-server-middleware-error_handling) [middleware](https://gofastmcp.com/python-sdk/fastmcp-server-middleware-middleware)