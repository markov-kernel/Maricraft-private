# fastmcp.server.middleware.error_handling
# fastmcp.server.middleware.error_handling

> **Category:** fastmcp.server.middleware.error/handling
> **Source:** gofastmcp.com_python-sdk_fastmcp-server-middleware-error_handling.json

---

middleware

error\_handling

fastmcp.server.middleware.error_handling

Error handling middleware for consistent error responses and tracking.

## Classes

ErrorHandlingMiddleware

Middleware that provides consistent error handling and logging.Catches exceptions, logs them appropriately, and converts them to
proper MCP error responses. Also tracks error patterns for monitoring.**Methods:**

on_message

Copy

```
on_message(self, context: MiddlewareContext, call_next: CallNext) -> Any

```

Handle errors for all messages.

get_error_stats

Copy

```
get_error_stats(self) -> dict[str, int]

```

Get error statistics for monitoring.

RetryMiddleware

Middleware that implements automatic retry logic for failed requests.Retries requests that fail with transient errors, using exponential
backoff to avoid overwhelming the server or external dependencies.**Methods:**

on_request

Copy

```
on_request(self, context: MiddlewareContext, call_next: CallNext) -> Any

```

Implement retry logic for requests.

[\_\_init\_\_](https://gofastmcp.com/python-sdk/fastmcp-server-middleware-__init__) [logging](https://gofastmcp.com/python-sdk/fastmcp-server-middleware-logging)