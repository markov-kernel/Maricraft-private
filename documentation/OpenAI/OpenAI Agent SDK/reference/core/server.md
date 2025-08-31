---
title: `MCP Servers`
source: https://openai.github.io/openai-agents-python/ref/mcp/server/
---

# `MCP Servers`

### MCPServer

Bases: `ABC`

Base class for Model Context Protocol servers.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ```2829303132333435363738394041424344454647484950515253545556575859606162636465666768697071727374757677787980818283848586878889``` | ```md-code__contentclass MCPServer(abc.ABC):    """Base class for Model Context Protocol servers."""    def __init__(self, use_structured_content: bool = False):        """        Args:            use_structured_content: Whether to use `tool_result.structured_content` when calling an                MCP tool.Defaults to False for backwards compatibility - most MCP servers still                include the structured content in the `tool_result.content`, and using it by                default will cause duplicate content. You can set this to True if you know the                server will not duplicate the structured content in the `tool_result.content`.        """        self.use_structured_content = use_structured_content    @abc.abstractmethod    async def connect(self):        """Connect to the server. For example, this might mean spawning a subprocess or        opening a network connection. The server is expected to remain connected until        `cleanup()` is called.        """        pass    @property    @abc.abstractmethod    def name(self) -> str:        """A readable name for the server."""        pass    @abc.abstractmethod    async def cleanup(self):        """Cleanup the server. For example, this might mean closing a subprocess or        closing a network connection.        """        pass    @abc.abstractmethod    async def list_tools(        self,        run_context: RunContextWrapper[Any] | None = None,        agent: AgentBase | None = None,    ) -> list[MCPTool]:        """List the tools available on the server."""        pass    @abc.abstractmethod    async def call_tool(self, tool_name: str, arguments: dict[str, Any] | None) -> CallToolResult:        """Invoke a tool on the server."""        pass    @abc.abstractmethod    async def list_prompts(        self,    ) -> ListPromptsResult:        """List the prompts available on the server."""        pass    @abc.abstractmethod    async def get_prompt(        self, name: str, arguments: dict[str, Any] | None = None    ) -> GetPromptResult:        """Get a specific prompt from the server."""        pass``` |

#### name`abstractmethod``property`

```
name: str

```

A readable name for the server.

#### \_\_init\_\_

```
__init__(use_structured_content: bool = False)

```

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `use_structured_content` | `bool` | Whether to use `tool_result.structured_content` when calling anMCP tool.Defaults to False for backwards compatibility - most MCP servers stillinclude the structured content in the `tool_result.content`, and using it bydefault will cause duplicate content. You can set this to True if you know theserver will not duplicate the structured content in the `tool_result.content`. | `False` |

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ```31323334353637383940``` | ```md-code__contentdef __init__(self, use_structured_content: bool = False):    """    Args:        use_structured_content: Whether to use `tool_result.structured_content` when calling an            MCP tool.Defaults to False for backwards compatibility - most MCP servers still            include the structured content in the `tool_result.content`, and using it by            default will cause duplicate content. You can set this to True if you know the            server will not duplicate the structured content in the `tool_result.content`.    """    self.use_structured_content = use_structured_content``` |

#### connect`abstractmethod``async`

```
connect()

```

Connect to the server. For example, this might mean spawning a subprocess or
opening a network connection. The server is expected to remain connected until
`cleanup()` is called.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ```42434445464748``` | ```md-code__content@abc.abstractmethodasync def connect(self):    """Connect to the server. For example, this might mean spawning a subprocess or    opening a network connection. The server is expected to remain connected until    `cleanup()` is called.    """    pass``` |

#### cleanup`abstractmethod``async`

```
cleanup()

```

Cleanup the server. For example, this might mean closing a subprocess or
closing a network connection.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ```565758596061``` | ```md-code__content@abc.abstractmethodasync def cleanup(self):    """Cleanup the server. For example, this might mean closing a subprocess or    closing a network connection.    """    pass``` |

#### list\_tools`abstractmethod``async`

```
list_tools(
    run_context: RunContextWrapper[Any] | None = None,
    agent: AgentBase | None = None,
) -> list[Tool]

```

List the tools available on the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ```6364656667686970``` | ```md-code__content@abc.abstractmethodasync def list_tools(    self,    run_context: RunContextWrapper[Any] | None = None,    agent: AgentBase | None = None,) -> list[MCPTool]:    """List the tools available on the server."""    pass``` |

#### call\_tool`abstractmethod``async`

```
call_tool(
    tool_name: str, arguments: dict[str, Any] | None
) -> CallToolResult

```

Invoke a tool on the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ```72737475``` | ```md-code__content@abc.abstractmethodasync def call_tool(self, tool_name: str, arguments: dict[str, Any] | None) -> CallToolResult:    """Invoke a tool on the server."""    pass``` |

#### list\_prompts`abstractmethod``async`

```
list_prompts() -> ListPromptsResult

```

List the prompts available on the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ```777879808182``` | ```md-code__content@abc.abstractmethodasync def list_prompts(    self,) -> ListPromptsResult:    """List the prompts available on the server."""    pass``` |

#### get\_prompt`abstractmethod``async`

```
get_prompt(
    name: str, arguments: dict[str, Any] | None = None
) -> GetPromptResult

```

Get a specific prompt from the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ```848586878889``` | ```md-code__content@abc.abstractmethodasync def get_prompt(    self, name: str, arguments: dict[str, Any] | None = None) -> GetPromptResult:    """Get a specific prompt from the server."""    pass``` |

### MCPServerStdioParams

Bases: `TypedDict`

Mirrors `mcp.client.stdio.StdioServerParameters`, but lets you pass params without another
import.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ```325326327328329330331332333334335336337338339340341342343344345346347348349350351``` | ```md-code__contentclass MCPServerStdioParams(TypedDict):    """Mirrors `mcp.client.stdio.StdioServerParameters`, but lets you pass params without another    import.    """    command: str    """The executable to run to start the server. For example, `python` or `node`."""    args: NotRequired[list[str]]    """Command line args to pass to the `command` executable. For example, `['foo.py']` or    `['server.js', '--port', '8080']`."""    env: NotRequired[dict[str, str]]    """The environment variables to set for the server. ."""    cwd: NotRequired[str | Path]    """The working directory to use when spawning the process."""    encoding: NotRequired[str]    """The text encoding used when sending/receiving messages to the server. Defaults to `utf-8`."""    encoding_error_handler: NotRequired[Literal["strict", "ignore", "replace"]]    """The text encoding error handler. Defaults to `strict`.    See https://docs.python.org/3/library/codecs.html#codec-base-classes for    explanations of possible values.    """``` |

#### command`instance-attribute`

```
command: str

```

The executable to run to start the server. For example, `python` or `node`.

#### args`instance-attribute`

```
args: NotRequired[list[str]]

```

Command line args to pass to the `command` executable. For example, `['foo.py']` or
`['server.js', '--port', '8080']`.

#### env`instance-attribute`

```
env: NotRequired[dict[str, str]]

```

The environment variables to set for the server. .

#### cwd`instance-attribute`

```
cwd: NotRequired[str | Path]

```

The working directory to use when spawning the process.

#### encoding`instance-attribute`

```
encoding: NotRequired[str]

```

The text encoding used when sending/receiving messages to the server. Defaults to `utf-8`.

#### encoding\_error\_handler`instance-attribute`

```
encoding_error_handler: NotRequired[\
    Literal["strict", "ignore", "replace"]\
]

```

The text encoding error handler. Defaults to `strict`.

See https://docs.python.org/3/library/codecs.html#codec-base-classes for
explanations of possible values.

### MCPServerStdio

Bases: `_MCPServerWithClientSession`

MCP server implementation that uses the stdio transport. See the \[spec\]
(https://spec.modelcontextprotocol.io/specification/2024-11-05/basic/transports/#stdio) for
details.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ```354355356357358359360361362363364365366367368369370371372373374375376377378379380381382383384385386387388389390391392393394395396397398399400401402403404405406407408409410411412413414415416417418419420421422423424425``` | ```md-code__contentclass MCPServerStdio(_MCPServerWithClientSession):    """MCP server implementation that uses the stdio transport. See the [spec]    (https://spec.modelcontextprotocol.io/specification/2024-11-05/basic/transports/#stdio) for    details.    """    def __init__(        self,        params: MCPServerStdioParams,        cache_tools_list: bool = False,        name: str | None = None,        client_session_timeout_seconds: float | None = 5,        tool_filter: ToolFilter = None,        use_structured_content: bool = False,    ):        """Create a new MCP server based on the stdio transport.        Args:            params: The params that configure the server. This includes the command to run to                start the server, the args to pass to the command, the environment variables to                set for the server, the working directory to use when spawning the process, and                the text encoding used when sending/receiving messages to the server.            cache_tools_list: Whether to cache the tools list. If `True`, the tools list will be                cached and only fetched from the server once. If `False`, the tools list will be                fetched from the server on each call to `list_tools()`. The cache can be                invalidated by calling `invalidate_tools_cache()`. You should set this to `True`                if you know the server will not change its tools list, because it can drastically                improve latency (by avoiding a round-trip to the server every time).            name: A readable name for the server. If not provided, we'll create one from the                command.            client_session_timeout_seconds: the read timeout passed to the MCP ClientSession.            tool_filter: The tool filter to use for filtering tools.            use_structured_content: Whether to use `tool_result.structured_content` when calling an                MCP tool. Defaults to False for backwards compatibility - most MCP servers still                include the structured content in the `tool_result.content`, and using it by                default will cause duplicate content. You can set this to True if you know the                server will not duplicate the structured content in the `tool_result.content`.        """        super().__init__(            cache_tools_list,            client_session_timeout_seconds,            tool_filter,            use_structured_content,        )        self.params = StdioServerParameters(            command=params["command"],            args=params.get("args", []),            env=params.get("env"),            cwd=params.get("cwd"),            encoding=params.get("encoding", "utf-8"),            encoding_error_handler=params.get("encoding_error_handler", "strict"),        )        self._name = name or f"stdio: {self.params.command}"    def create_streams(        self,    ) -> AbstractAsyncContextManager[        tuple[            MemoryObjectReceiveStream[SessionMessage | Exception],            MemoryObjectSendStream[SessionMessage],            GetSessionIdCallback | None,        ]    ]:        """Create the streams for the server."""        return stdio_client(self.params)    @property    def name(self) -> str:        """A readable name for the server."""        return self._name``` |

#### name`property`

```
name: str

```

A readable name for the server.

#### \_\_init\_\_

```
__init__(
    params: MCPServerStdioParams,
    cache_tools_list: bool = False,
    name: str | None = None,
    client_session_timeout_seconds: float | None = 5,
    tool_filter: ToolFilter = None,
    use_structured_content: bool = False,
)

```

Create a new MCP server based on the stdio transport.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `params` | `MCPServerStdioParams` | The params that configure the server. This includes the command to run tostart the server, the args to pass to the command, the environment variables toset for the server, the working directory to use when spawning the process, andthe text encoding used when sending/receiving messages to the server. | _required_ |
| `cache_tools_list` | `bool` | Whether to cache the tools list. If `True`, the tools list will becached and only fetched from the server once. If `False`, the tools list will befetched from the server on each call to `list_tools()`. The cache can beinvalidated by calling `invalidate_tools_cache()`. You should set this to `True`if you know the server will not change its tools list, because it can drasticallyimprove latency (by avoiding a round-trip to the server every time). | `False` |
| `name` | `str | None` | A readable name for the server. If not provided, we'll create one from thecommand. | `None` |
| `client_session_timeout_seconds` | `float | None` | the read timeout passed to the MCP ClientSession. | `5` |
| `tool_filter` | `ToolFilter` | The tool filter to use for filtering tools. | `None` |
| `use_structured_content` | `bool` | Whether to use `tool_result.structured_content` when calling anMCP tool. Defaults to False for backwards compatibility - most MCP servers stillinclude the structured content in the `tool_result.content`, and using it bydefault will cause duplicate content. You can set this to True if you know theserver will not duplicate the structured content in the `tool_result.content`. | `False` |

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ```360361362363364365366367368369370371372373374375376377378379380381382383384385386387388389390391392393394395396397398399400401402403404405406407408``` | ```md-code__contentdef __init__(    self,    params: MCPServerStdioParams,    cache_tools_list: bool = False,    name: str | None = None,    client_session_timeout_seconds: float | None = 5,    tool_filter: ToolFilter = None,    use_structured_content: bool = False,):    """Create a new MCP server based on the stdio transport.    Args:        params: The params that configure the server. This includes the command to run to            start the server, the args to pass to the command, the environment variables to            set for the server, the working directory to use when spawning the process, and            the text encoding used when sending/receiving messages to the server.        cache_tools_list: Whether to cache the tools list. If `True`, the tools list will be            cached and only fetched from the server once. If `False`, the tools list will be            fetched from the server on each call to `list_tools()`. The cache can be            invalidated by calling `invalidate_tools_cache()`. You should set this to `True`            if you know the server will not change its tools list, because it can drastically            improve latency (by avoiding a round-trip to the server every time).        name: A readable name for the server. If not provided, we'll create one from the            command.        client_session_timeout_seconds: the read timeout passed to the MCP ClientSession.        tool_filter: The tool filter to use for filtering tools.        use_structured_content: Whether to use `tool_result.structured_content` when calling an            MCP tool. Defaults to False for backwards compatibility - most MCP servers still            include the structured content in the `tool_result.content`, and using it by            default will cause duplicate content. You can set this to True if you know the            server will not duplicate the structured content in the `tool_result.content`.    """    super().__init__(        cache_tools_list,        client_session_timeout_seconds,        tool_filter,        use_structured_content,    )    self.params = StdioServerParameters(        command=params["command"],        args=params.get("args", []),        env=params.get("env"),        cwd=params.get("cwd"),        encoding=params.get("encoding", "utf-8"),        encoding_error_handler=params.get("encoding_error_handler", "strict"),    )    self._name = name or f"stdio: {self.params.command}"``` |

#### create\_streams

```
create_streams() -> AbstractAsyncContextManager[\
    tuple[\
        MemoryObjectReceiveStream[\
            SessionMessage | Exception\
        ],\
        MemoryObjectSendStream[SessionMessage],\
        GetSessionIdCallback | None,\
    ]\
]

```

Create the streams for the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ```410411412413414415416417418419420``` | ```md-code__contentdef create_streams(    self,) -> AbstractAsyncContextManager[    tuple[        MemoryObjectReceiveStream[SessionMessage | Exception],        MemoryObjectSendStream[SessionMessage],        GetSessionIdCallback | None,    ]]:    """Create the streams for the server."""    return stdio_client(self.params)``` |

#### connect`async`

```
connect()

```

Connect to the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ```236237238239240241242243244245246247248249250251252253254255256257258259260``` | ```md-code__contentasync def connect(self):    """Connect to the server."""    try:        transport = await self.exit_stack.enter_async_context(self.create_streams())        # streamablehttp_client returns (read, write, get_session_id)        # sse_client returns (read, write)        read, write, *_ = transport        session = await self.exit_stack.enter_async_context(            ClientSession(                read,                write,                timedelta(seconds=self.client_session_timeout_seconds)                if self.client_session_timeout_seconds                else None,            )        )        server_result = await session.initialize()        self.server_initialize_result = server_result        self.session = session    except Exception as e:        logger.error(f"Error initializing MCP server: {e}")        await self.cleanup()        raise``` |

#### cleanup`async`

```
cleanup()

```

Cleanup the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ```314315316317318319320321322``` | ```md-code__contentasync def cleanup(self):    """Cleanup the server."""    async with self._cleanup_lock:        try:            await self.exit_stack.aclose()        except Exception as e:            logger.error(f"Error cleaning up server: {e}")        finally:            self.session = None``` |

#### list\_tools`async`

```
list_tools(
    run_context: RunContextWrapper[Any] | None = None,
    agent: AgentBase | None = None,
) -> list[Tool]

```

List the tools available on the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ```262263264265266267268269270271272273274275276277278279280281282283284285286287``` | ```md-code__contentasync def list_tools(    self,    run_context: RunContextWrapper[Any] | None = None,    agent: AgentBase | None = None,) -> list[MCPTool]:    """List the tools available on the server."""    if not self.session:        raise UserError("Server not initialized. Make sure you call `connect()` first.")    # Return from cache if caching is enabled, we have tools, and the cache is not dirty    if self.cache_tools_list and not self._cache_dirty and self._tools_list:        tools = self._tools_list    else:        # Reset the cache dirty to False        self._cache_dirty = False        # Fetch the tools from the server        self._tools_list = (await self.session.list_tools()).tools        tools = self._tools_list    # Filter tools based on tool_filter    filtered_tools = tools    if self.tool_filter is not None:        if run_context is None or agent is None:            raise UserError("run_context and agent are required for dynamic tool filtering")        filtered_tools = await self._apply_tool_filter(filtered_tools, run_context, agent)    return filtered_tools``` |

#### call\_tool`async`

```
call_tool(
    tool_name: str, arguments: dict[str, Any] | None
) -> CallToolResult

```

Invoke a tool on the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ```289290291292293294``` | ```md-code__contentasync def call_tool(self, tool_name: str, arguments: dict[str, Any] | None) -> CallToolResult:    """Invoke a tool on the server."""    if not self.session:        raise UserError("Server not initialized. Make sure you call `connect()` first.")    return await self.session.call_tool(tool_name, arguments)``` |

#### list\_prompts`async`

```
list_prompts() -> ListPromptsResult

```

List the prompts available on the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ```296297298299300301302303``` | ```md-code__contentasync def list_prompts(    self,) -> ListPromptsResult:    """List the prompts available on the server."""    if not self.session:        raise UserError("Server not initialized. Make sure you call `connect()` first.")    return await self.session.list_prompts()``` |

#### get\_prompt`async`

```
get_prompt(
    name: str, arguments: dict[str, Any] | None = None
) -> GetPromptResult

```

Get a specific prompt from the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ```305306307308309310311312``` | ```md-code__contentasync def get_prompt(    self, name: str, arguments: dict[str, Any] | None = None) -> GetPromptResult:    """Get a specific prompt from the server."""    if not self.session:        raise UserError("Server not initialized. Make sure you call `connect()` first.")    return await self.session.get_prompt(name, arguments)``` |

#### invalidate\_tools\_cache

```
invalidate_tools_cache()

```

Invalidate the tools cache.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ```232233234``` | ```md-code__contentdef invalidate_tools_cache(self):    """Invalidate the tools cache."""    self._cache_dirty = True``` |

### MCPServerSseParams

Bases: `TypedDict`

Mirrors the params in `mcp.client.sse.sse_client`.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ```428429430431432433434435436437438439440441``` | ```md-code__contentclass MCPServerSseParams(TypedDict):    """Mirrors the params in`mcp.client.sse.sse_client`."""    url: str    """The URL of the server."""    headers: NotRequired[dict[str, str]]    """The headers to send to the server."""    timeout: NotRequired[float]    """The timeout for the HTTP request. Defaults to 5 seconds."""    sse_read_timeout: NotRequired[float]    """The timeout for the SSE connection, in seconds. Defaults to 5 minutes."""``` |

#### url`instance-attribute`

```
url: str

```

The URL of the server.

#### headers`instance-attribute`

```
headers: NotRequired[dict[str, str]]

```

The headers to send to the server.

#### timeout`instance-attribute`

```
timeout: NotRequired[float]

```

The timeout for the HTTP request. Defaults to 5 seconds.

#### sse\_read\_timeout`instance-attribute`

```
sse_read_timeout: NotRequired[float]

```

The timeout for the SSE connection, in seconds. Defaults to 5 minutes.

### MCPServerSse

Bases: `_MCPServerWithClientSession`

MCP server implementation that uses the HTTP with SSE transport. See the \[spec\]
(https://spec.modelcontextprotocol.io/specification/2024-11-05/basic/transports/#http-with-sse)
for details.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ```444445446447448449450451452453454455456457458459460461462463464465466467468469470471472473474475476477478479480481482483484485486487488489490491492493494495496497498499500501502503504505506507508509510511512513514``` | ```md-code__contentclass MCPServerSse(_MCPServerWithClientSession):    """MCP server implementation that uses the HTTP with SSE transport. See the [spec]    (https://spec.modelcontextprotocol.io/specification/2024-11-05/basic/transports/#http-with-sse)    for details.    """    def __init__(        self,        params: MCPServerSseParams,        cache_tools_list: bool = False,        name: str | None = None,        client_session_timeout_seconds: float | None = 5,        tool_filter: ToolFilter = None,        use_structured_content: bool = False,    ):        """Create a new MCP server based on the HTTP with SSE transport.        Args:            params: The params that configure the server. This includes the URL of the server,                the headers to send to the server, the timeout for the HTTP request, and the                timeout for the SSE connection.            cache_tools_list: Whether to cache the tools list. If `True`, the tools list will be                cached and only fetched from the server once. If `False`, the tools list will be                fetched from the server on each call to `list_tools()`. The cache can be                invalidated by calling `invalidate_tools_cache()`. You should set this to `True`                if you know the server will not change its tools list, because it can drastically                improve latency (by avoiding a round-trip to the server every time).            name: A readable name for the server. If not provided, we'll create one from the                URL.            client_session_timeout_seconds: the read timeout passed to the MCP ClientSession.            tool_filter: The tool filter to use for filtering tools.            use_structured_content: Whether to use `tool_result.structured_content` when calling an                MCP tool. Defaults to False for backwards compatibility - most MCP servers still                include the structured content in the `tool_result.content`, and using it by                default will cause duplicate content. You can set this to True if you know the                server will not duplicate the structured content in the `tool_result.content`.        """        super().__init__(            cache_tools_list,            client_session_timeout_seconds,            tool_filter,            use_structured_content,        )        self.params = params        self._name = name or f"sse: {self.params['url']}"    def create_streams(        self,    ) -> AbstractAsyncContextManager[        tuple[            MemoryObjectReceiveStream[SessionMessage | Exception],            MemoryObjectSendStream[SessionMessage],            GetSessionIdCallback | None,        ]    ]:        """Create the streams for the server."""        return sse_client(            url=self.params["url"],            headers=self.params.get("headers", None),            timeout=self.params.get("timeout", 5),            sse_read_timeout=self.params.get("sse_read_timeout", 60 * 5),        )    @property    def name(self) -> str:        """A readable name for the server."""        return self._name``` |

#### name`property`

```
name: str

```

A readable name for the server.

#### \_\_init\_\_

```
__init__(
    params: MCPServerSseParams,
    cache_tools_list: bool = False,
    name: str | None = None,
    client_session_timeout_seconds: float | None = 5,
    tool_filter: ToolFilter = None,
    use_structured_content: bool = False,
)

```

Create a new MCP server based on the HTTP with SSE transport.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `params` | `MCPServerSseParams` | The params that configure the server. This includes the URL of the server,the headers to send to the server, the timeout for the HTTP request, and thetimeout for the SSE connection. | _required_ |
| `cache_tools_list` | `bool` | Whether to cache the tools list. If `True`, the tools list will becached and only fetched from the server once. If `False`, the tools list will befetched from the server on each call to `list_tools()`. The cache can beinvalidated by calling `invalidate_tools_cache()`. You should set this to `True`if you know the server will not change its tools list, because it can drasticallyimprove latency (by avoiding a round-trip to the server every time). | `False` |
| `name` | `str | None` | A readable name for the server. If not provided, we'll create one from theURL. | `None` |
| `client_session_timeout_seconds` | `float | None` | the read timeout passed to the MCP ClientSession. | `5` |
| `tool_filter` | `ToolFilter` | The tool filter to use for filtering tools. | `None` |
| `use_structured_content` | `bool` | Whether to use `tool_result.structured_content` when calling anMCP tool. Defaults to False for backwards compatibility - most MCP servers stillinclude the structured content in the `tool_result.content`, and using it bydefault will cause duplicate content. You can set this to True if you know theserver will not duplicate the structured content in the `tool_result.content`. | `False` |

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ```450451452453454455456457458459460461462463464465466467468469470471472473474475476477478479480481482483484485486487488489490491492``` | ```md-code__contentdef __init__(    self,    params: MCPServerSseParams,    cache_tools_list: bool = False,    name: str | None = None,    client_session_timeout_seconds: float | None = 5,    tool_filter: ToolFilter = None,    use_structured_content: bool = False,):    """Create a new MCP server based on the HTTP with SSE transport.    Args:        params: The params that configure the server. This includes the URL of the server,            the headers to send to the server, the timeout for the HTTP request, and the            timeout for the SSE connection.        cache_tools_list: Whether to cache the tools list. If `True`, the tools list will be            cached and only fetched from the server once. If `False`, the tools list will be            fetched from the server on each call to `list_tools()`. The cache can be            invalidated by calling `invalidate_tools_cache()`. You should set this to `True`            if you know the server will not change its tools list, because it can drastically            improve latency (by avoiding a round-trip to the server every time).        name: A readable name for the server. If not provided, we'll create one from the            URL.        client_session_timeout_seconds: the read timeout passed to the MCP ClientSession.        tool_filter: The tool filter to use for filtering tools.        use_structured_content: Whether to use `tool_result.structured_content` when calling an            MCP tool. Defaults to False for backwards compatibility - most MCP servers still            include the structured content in the `tool_result.content`, and using it by            default will cause duplicate content. You can set this to True if you know the            server will not duplicate the structured content in the `tool_result.content`.    """    super().__init__(        cache_tools_list,        client_session_timeout_seconds,        tool_filter,        use_structured_content,    )    self.params = params    self._name = name or f"sse: {self.params['url']}"``` |

#### create\_streams

```
create_streams() -> AbstractAsyncContextManager[\
    tuple[\
        MemoryObjectReceiveStream[\
            SessionMessage | Exception\
        ],\
        MemoryObjectSendStream[SessionMessage],\
        GetSessionIdCallback | None,\
    ]\
]

```

Create the streams for the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ```494495496497498499500501502503504505506507508509``` | ```md-code__contentdef create_streams(    self,) -> AbstractAsyncContextManager[    tuple[        MemoryObjectReceiveStream[SessionMessage | Exception],        MemoryObjectSendStream[SessionMessage],        GetSessionIdCallback | None,    ]]:    """Create the streams for the server."""    return sse_client(        url=self.params["url"],        headers=self.params.get("headers", None),        timeout=self.params.get("timeout", 5),        sse_read_timeout=self.params.get("sse_read_timeout", 60 * 5),    )``` |

#### connect`async`

```
connect()

```

Connect to the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ```236237238239240241242243244245246247248249250251252253254255256257258259260``` | ```md-code__contentasync def connect(self):    """Connect to the server."""    try:        transport = await self.exit_stack.enter_async_context(self.create_streams())        # streamablehttp_client returns (read, write, get_session_id)        # sse_client returns (read, write)        read, write, *_ = transport        session = await self.exit_stack.enter_async_context(            ClientSession(                read,                write,                timedelta(seconds=self.client_session_timeout_seconds)                if self.client_session_timeout_seconds                else None,            )        )        server_result = await session.initialize()        self.server_initialize_result = server_result        self.session = session    except Exception as e:        logger.error(f"Error initializing MCP server: {e}")        await self.cleanup()        raise``` |

#### cleanup`async`

```
cleanup()

```

Cleanup the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ```314315316317318319320321322``` | ```md-code__contentasync def cleanup(self):    """Cleanup the server."""    async with self._cleanup_lock:        try:            await self.exit_stack.aclose()        except Exception as e:            logger.error(f"Error cleaning up server: {e}")        finally:            self.session = None``` |

#### list\_tools`async`

```
list_tools(
    run_context: RunContextWrapper[Any] | None = None,
    agent: AgentBase | None = None,
) -> list[Tool]

```

List the tools available on the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ```262263264265266267268269270271272273274275276277278279280281282283284285286287``` | ```md-code__contentasync def list_tools(    self,    run_context: RunContextWrapper[Any] | None = None,    agent: AgentBase | None = None,) -> list[MCPTool]:    """List the tools available on the server."""    if not self.session:        raise UserError("Server not initialized. Make sure you call `connect()` first.")    # Return from cache if caching is enabled, we have tools, and the cache is not dirty    if self.cache_tools_list and not self._cache_dirty and self._tools_list:        tools = self._tools_list    else:        # Reset the cache dirty to False        self._cache_dirty = False        # Fetch the tools from the server        self._tools_list = (await self.session.list_tools()).tools        tools = self._tools_list    # Filter tools based on tool_filter    filtered_tools = tools    if self.tool_filter is not None:        if run_context is None or agent is None:            raise UserError("run_context and agent are required for dynamic tool filtering")        filtered_tools = await self._apply_tool_filter(filtered_tools, run_context, agent)    return filtered_tools``` |

#### call\_tool`async`

```
call_tool(
    tool_name: str, arguments: dict[str, Any] | None
) -> CallToolResult

```

Invoke a tool on the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ```289290291292293294``` | ```md-code__contentasync def call_tool(self, tool_name: str, arguments: dict[str, Any] | None) -> CallToolResult:    """Invoke a tool on the server."""    if not self.session:        raise UserError("Server not initialized. Make sure you call `connect()` first.")    return await self.session.call_tool(tool_name, arguments)``` |

#### list\_prompts`async`

```
list_prompts() -> ListPromptsResult

```

List the prompts available on the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ```296297298299300301302303``` | ```md-code__contentasync def list_prompts(    self,) -> ListPromptsResult:    """List the prompts available on the server."""    if not self.session:        raise UserError("Server not initialized. Make sure you call `connect()` first.")    return await self.session.list_prompts()``` |

#### get\_prompt`async`

```
get_prompt(
    name: str, arguments: dict[str, Any] | None = None
) -> GetPromptResult

```

Get a specific prompt from the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ```305306307308309310311312``` | ```md-code__contentasync def get_prompt(    self, name: str, arguments: dict[str, Any] | None = None) -> GetPromptResult:    """Get a specific prompt from the server."""    if not self.session:        raise UserError("Server not initialized. Make sure you call `connect()` first.")    return await self.session.get_prompt(name, arguments)``` |

#### invalidate\_tools\_cache

```
invalidate_tools_cache()

```

Invalidate the tools cache.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ```232233234``` | ```md-code__contentdef invalidate_tools_cache(self):    """Invalidate the tools cache."""    self._cache_dirty = True``` |

### MCPServerStreamableHttpParams

Bases: `TypedDict`

Mirrors the params in `mcp.client.streamable_http.streamablehttp_client`.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ```517518519520521522523524525526527528529530531532533``` | ```md-code__contentclass MCPServerStreamableHttpParams(TypedDict):    """Mirrors the params in`mcp.client.streamable_http.streamablehttp_client`."""    url: str    """The URL of the server."""    headers: NotRequired[dict[str, str]]    """The headers to send to the server."""    timeout: NotRequired[timedelta | float]    """The timeout for the HTTP request. Defaults to 5 seconds."""    sse_read_timeout: NotRequired[timedelta | float]    """The timeout for the SSE connection, in seconds. Defaults to 5 minutes."""    terminate_on_close: NotRequired[bool]    """Terminate on close"""``` |

#### url`instance-attribute`

```
url: str

```

The URL of the server.

#### headers`instance-attribute`

```
headers: NotRequired[dict[str, str]]

```

The headers to send to the server.

#### timeout`instance-attribute`

```
timeout: NotRequired[timedelta | float]

```

The timeout for the HTTP request. Defaults to 5 seconds.

#### sse\_read\_timeout`instance-attribute`

```
sse_read_timeout: NotRequired[timedelta | float]

```

The timeout for the SSE connection, in seconds. Defaults to 5 minutes.

#### terminate\_on\_close`instance-attribute`

```
terminate_on_close: NotRequired[bool]

```

Terminate on close

### MCPServerStreamableHttp

Bases: `_MCPServerWithClientSession`

MCP server implementation that uses the Streamable HTTP transport. See the \[spec\]
(https://modelcontextprotocol.io/specification/2025-03-26/basic/transports#streamable-http)
for details.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ```536537538539540541542543544545546547548549550551552553554555556557558559560561562563564565566567568569570571572573574575576577578579580581582583584585586587588589590591592593594595596597598599600601602603604605606607608``` | ```md-code__contentclass MCPServerStreamableHttp(_MCPServerWithClientSession):    """MCP server implementation that uses the Streamable HTTP transport. See the [spec]    (https://modelcontextprotocol.io/specification/2025-03-26/basic/transports#streamable-http)    for details.    """    def __init__(        self,        params: MCPServerStreamableHttpParams,        cache_tools_list: bool = False,        name: str | None = None,        client_session_timeout_seconds: float | None = 5,        tool_filter: ToolFilter = None,        use_structured_content: bool = False,    ):        """Create a new MCP server based on the Streamable HTTP transport.        Args:            params: The params that configure the server. This includes the URL of the server,                the headers to send to the server, the timeout for the HTTP request, and the                timeout for the Streamable HTTP connection and whether we need to                terminate on close.            cache_tools_list: Whether to cache the tools list. If `True`, the tools list will be                cached and only fetched from the server once. If `False`, the tools list will be                fetched from the server on each call to `list_tools()`. The cache can be                invalidated by calling `invalidate_tools_cache()`. You should set this to `True`                if you know the server will not change its tools list, because it can drastically                improve latency (by avoiding a round-trip to the server every time).            name: A readable name for the server. If not provided, we'll create one from the                URL.            client_session_timeout_seconds: the read timeout passed to the MCP ClientSession.            tool_filter: The tool filter to use for filtering tools.            use_structured_content: Whether to use `tool_result.structured_content` when calling an                MCP tool. Defaults to False for backwards compatibility - most MCP servers still                include the structured content in the `tool_result.content`, and using it by                default will cause duplicate content. You can set this to True if you know the                server will not duplicate the structured content in the `tool_result.content`.        """        super().__init__(            cache_tools_list,            client_session_timeout_seconds,            tool_filter,            use_structured_content,        )        self.params = params        self._name = name or f"streamable_http: {self.params['url']}"    def create_streams(        self,    ) -> AbstractAsyncContextManager[        tuple[            MemoryObjectReceiveStream[SessionMessage | Exception],            MemoryObjectSendStream[SessionMessage],            GetSessionIdCallback | None,        ]    ]:        """Create the streams for the server."""        return streamablehttp_client(            url=self.params["url"],            headers=self.params.get("headers", None),            timeout=self.params.get("timeout", 5),            sse_read_timeout=self.params.get("sse_read_timeout", 60 * 5),            terminate_on_close=self.params.get("terminate_on_close", True),        )    @property    def name(self) -> str:        """A readable name for the server."""        return self._name``` |

#### name`property`

```
name: str

```

A readable name for the server.

#### \_\_init\_\_

```
__init__(
    params: MCPServerStreamableHttpParams,
    cache_tools_list: bool = False,
    name: str | None = None,
    client_session_timeout_seconds: float | None = 5,
    tool_filter: ToolFilter = None,
    use_structured_content: bool = False,
)

```

Create a new MCP server based on the Streamable HTTP transport.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `params` | `MCPServerStreamableHttpParams` | The params that configure the server. This includes the URL of the server,the headers to send to the server, the timeout for the HTTP request, and thetimeout for the Streamable HTTP connection and whether we need toterminate on close. | _required_ |
| `cache_tools_list` | `bool` | Whether to cache the tools list. If `True`, the tools list will becached and only fetched from the server once. If `False`, the tools list will befetched from the server on each call to `list_tools()`. The cache can beinvalidated by calling `invalidate_tools_cache()`. You should set this to `True`if you know the server will not change its tools list, because it can drasticallyimprove latency (by avoiding a round-trip to the server every time). | `False` |
| `name` | `str | None` | A readable name for the server. If not provided, we'll create one from theURL. | `None` |
| `client_session_timeout_seconds` | `float | None` | the read timeout passed to the MCP ClientSession. | `5` |
| `tool_filter` | `ToolFilter` | The tool filter to use for filtering tools. | `None` |
| `use_structured_content` | `bool` | Whether to use `tool_result.structured_content` when calling anMCP tool. Defaults to False for backwards compatibility - most MCP servers stillinclude the structured content in the `tool_result.content`, and using it bydefault will cause duplicate content. You can set this to True if you know theserver will not duplicate the structured content in the `tool_result.content`. | `False` |

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ```542543544545546547548549550551552553554555556557558559560561562563564565566567568569570571572573574575576577578579580581582583584585``` | ```md-code__contentdef __init__(    self,    params: MCPServerStreamableHttpParams,    cache_tools_list: bool = False,    name: str | None = None,    client_session_timeout_seconds: float | None = 5,    tool_filter: ToolFilter = None,    use_structured_content: bool = False,):    """Create a new MCP server based on the Streamable HTTP transport.    Args:        params: The params that configure the server. This includes the URL of the server,            the headers to send to the server, the timeout for the HTTP request, and the            timeout for the Streamable HTTP connection and whether we need to            terminate on close.        cache_tools_list: Whether to cache the tools list. If `True`, the tools list will be            cached and only fetched from the server once. If `False`, the tools list will be            fetched from the server on each call to `list_tools()`. The cache can be            invalidated by calling `invalidate_tools_cache()`. You should set this to `True`            if you know the server will not change its tools list, because it can drastically            improve latency (by avoiding a round-trip to the server every time).        name: A readable name for the server. If not provided, we'll create one from the            URL.        client_session_timeout_seconds: the read timeout passed to the MCP ClientSession.        tool_filter: The tool filter to use for filtering tools.        use_structured_content: Whether to use `tool_result.structured_content` when calling an            MCP tool. Defaults to False for backwards compatibility - most MCP servers still            include the structured content in the `tool_result.content`, and using it by            default will cause duplicate content. You can set this to True if you know the            server will not duplicate the structured content in the `tool_result.content`.    """    super().__init__(        cache_tools_list,        client_session_timeout_seconds,        tool_filter,        use_structured_content,    )    self.params = params    self._name = name or f"streamable_http: {self.params['url']}"``` |

#### create\_streams

```
create_streams() -> AbstractAsyncContextManager[\
    tuple[\
        MemoryObjectReceiveStream[\
            SessionMessage | Exception\
        ],\
        MemoryObjectSendStream[SessionMessage],\
        GetSessionIdCallback | None,\
    ]\
]

```

Create the streams for the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ```587588589590591592593594595596597598599600601602603``` | ```md-code__contentdef create_streams(    self,) -> AbstractAsyncContextManager[    tuple[        MemoryObjectReceiveStream[SessionMessage | Exception],        MemoryObjectSendStream[SessionMessage],        GetSessionIdCallback | None,    ]]:    """Create the streams for the server."""    return streamablehttp_client(        url=self.params["url"],        headers=self.params.get("headers", None),        timeout=self.params.get("timeout", 5),        sse_read_timeout=self.params.get("sse_read_timeout", 60 * 5),        terminate_on_close=self.params.get("terminate_on_close", True),    )``` |

#### connect`async`

```
connect()

```

Connect to the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ```236237238239240241242243244245246247248249250251252253254255256257258259260``` | ```md-code__contentasync def connect(self):    """Connect to the server."""    try:        transport = await self.exit_stack.enter_async_context(self.create_streams())        # streamablehttp_client returns (read, write, get_session_id)        # sse_client returns (read, write)        read, write, *_ = transport        session = await self.exit_stack.enter_async_context(            ClientSession(                read,                write,                timedelta(seconds=self.client_session_timeout_seconds)                if self.client_session_timeout_seconds                else None,            )        )        server_result = await session.initialize()        self.server_initialize_result = server_result        self.session = session    except Exception as e:        logger.error(f"Error initializing MCP server: {e}")        await self.cleanup()        raise``` |

#### cleanup`async`

```
cleanup()

```

Cleanup the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ```314315316317318319320321322``` | ```md-code__contentasync def cleanup(self):    """Cleanup the server."""    async with self._cleanup_lock:        try:            await self.exit_stack.aclose()        except Exception as e:            logger.error(f"Error cleaning up server: {e}")        finally:            self.session = None``` |

#### list\_tools`async`

```
list_tools(
    run_context: RunContextWrapper[Any] | None = None,
    agent: AgentBase | None = None,
) -> list[Tool]

```

List the tools available on the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ```262263264265266267268269270271272273274275276277278279280281282283284285286287``` | ```md-code__contentasync def list_tools(    self,    run_context: RunContextWrapper[Any] | None = None,    agent: AgentBase | None = None,) -> list[MCPTool]:    """List the tools available on the server."""    if not self.session:        raise UserError("Server not initialized. Make sure you call `connect()` first.")    # Return from cache if caching is enabled, we have tools, and the cache is not dirty    if self.cache_tools_list and not self._cache_dirty and self._tools_list:        tools = self._tools_list    else:        # Reset the cache dirty to False        self._cache_dirty = False        # Fetch the tools from the server        self._tools_list = (await self.session.list_tools()).tools        tools = self._tools_list    # Filter tools based on tool_filter    filtered_tools = tools    if self.tool_filter is not None:        if run_context is None or agent is None:            raise UserError("run_context and agent are required for dynamic tool filtering")        filtered_tools = await self._apply_tool_filter(filtered_tools, run_context, agent)    return filtered_tools``` |

#### call\_tool`async`

```
call_tool(
    tool_name: str, arguments: dict[str, Any] | None
) -> CallToolResult

```

Invoke a tool on the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ```289290291292293294``` | ```md-code__contentasync def call_tool(self, tool_name: str, arguments: dict[str, Any] | None) -> CallToolResult:    """Invoke a tool on the server."""    if not self.session:        raise UserError("Server not initialized. Make sure you call `connect()` first.")    return await self.session.call_tool(tool_name, arguments)``` |

#### list\_prompts`async`

```
list_prompts() -> ListPromptsResult

```

List the prompts available on the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ```296297298299300301302303``` | ```md-code__contentasync def list_prompts(    self,) -> ListPromptsResult:    """List the prompts available on the server."""    if not self.session:        raise UserError("Server not initialized. Make sure you call `connect()` first.")    return await self.session.list_prompts()``` |

#### get\_prompt`async`

```
get_prompt(
    name: str, arguments: dict[str, Any] | None = None
) -> GetPromptResult

```

Get a specific prompt from the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ```305306307308309310311312``` | ```md-code__contentasync def get_prompt(    self, name: str, arguments: dict[str, Any] | None = None) -> GetPromptResult:    """Get a specific prompt from the server."""    if not self.session:        raise UserError("Server not initialized. Make sure you call `connect()` first.")    return await self.session.get_prompt(name, arguments)``` |

#### invalidate\_tools\_cache

```
invalidate_tools_cache()

```

Invalidate the tools cache.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ```232233234``` | ```md-code__contentdef invalidate_tools_cache(self):    """Invalidate the tools cache."""    self._cache_dirty = True``` |