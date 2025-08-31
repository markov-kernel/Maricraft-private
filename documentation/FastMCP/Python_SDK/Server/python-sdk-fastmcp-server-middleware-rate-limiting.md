# fastmcp.server.middleware.rate_limiting
# fastmcp.server.middleware.rate_limiting

> **Category:** fastmcp.server.middleware.rate/limiting
> **Source:** gofastmcp.com_python-sdk_fastmcp-server-middleware-rate_limiting.json

---

middleware

rate\_limiting

fastmcp.server.middleware.rate_limiting

Rate limiting middleware for protecting FastMCP servers from abuse.

## Classes

RateLimitError

Error raised when rate limit is exceeded.

TokenBucketRateLimiter

Token bucket implementation for rate limiting.**Methods:**

consume

Copy

```
consume(self, tokens: int = 1) -> bool

```

Try to consume tokens from the bucket.**Args:**

- `tokens`: Number of tokens to consume

**Returns:**

- True if tokens were available and consumed, False otherwise

SlidingWindowRateLimiter

Sliding window rate limiter implementation.**Methods:**

is_allowed

Copy

```
is_allowed(self) -> bool

```

Check if a request is allowed.

RateLimitingMiddleware

Middleware that implements rate limiting to prevent server abuse.Uses a token bucket algorithm by default, allowing for burst traffic
while maintaining a sustainable long-term rate.**Methods:**

on_request

Copy

```
on_request(self, context: MiddlewareContext, call_next: CallNext) -> Any

```

Apply rate limiting to requests.

SlidingWindowRateLimitingMiddleware

Middleware that implements sliding window rate limiting.Uses a sliding window approach which provides more precise rate limiting
but uses more memory to track individual request timestamps.**Methods:**

on_request

Copy

```
on_request(self, context: MiddlewareContext, call_next: CallNext) -> Any

```

Apply sliding window rate limiting to requests.

[middleware](https://gofastmcp.com/python-sdk/fastmcp-server-middleware-middleware) [timing](https://gofastmcp.com/python-sdk/fastmcp-server-middleware-timing)