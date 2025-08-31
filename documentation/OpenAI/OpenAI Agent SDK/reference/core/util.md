---
title: `MCP Util`
source: https://openai.github.io/openai-agents-python/ref/mcp/util/
---

# `MCP Util`

### ToolFilterCallable`module-attribute`

```
ToolFilterCallable = Callable[\
    ["ToolFilterContext", "MCPTool"], MaybeAwaitable[bool]\
]

```

A function that determines whether a tool should be available.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `context` |  | The context information including run context, agent, and server name. | _required_ |
| `tool` |  | The MCP tool to filter. | _required_ |

Returns:

| Type | Description |
| --- | --- |
|  | Whether the tool should be available (True) or filtered out (False). |

### ToolFilter`module-attribute`

```
ToolFilter = Union[\
    ToolFilterCallable, ToolFilterStatic, None\
]

```

A tool filter that can be either a function, static configuration, or None (no filtering).

### ToolFilterContext`dataclass`

Context information available to tool filter functions.

Source code in `src/agents/mcp/util.py`

|  |  |
| --- | --- |
| ```242526272829303132333435``` | ```md-code__content@dataclassclass ToolFilterContext:    """Context information available to tool filter functions."""    run_context: RunContextWrapper[Any]    """The current run context."""    agent: "AgentBase"    """The agent that is requesting the tool list."""    server_name: str    """The name of the MCP server."""``` |

#### run\_context`instance-attribute`

```
run_context: RunContextWrapper[Any]

```

The current run context.

#### agent`instance-attribute`

```
agent: AgentBase

```

The agent that is requesting the tool list.

#### server\_name`instance-attribute`

```
server_name: str

```

The name of the MCP server.

### ToolFilterStatic

Bases: `TypedDict`

Static tool filter configuration using allowlists and blocklists.

Source code in `src/agents/mcp/util.py`

|  |  |
| --- | --- |
| ```50515253545556575859``` | ```md-code__contentclass ToolFilterStatic(TypedDict):    """Static tool filter configuration using allowlists and blocklists."""    allowed_tool_names: NotRequired[list[str]]    """Optional list of tool names to allow (whitelist).    If set, only these tools will be available."""    blocked_tool_names: NotRequired[list[str]]    """Optional list of tool names to exclude (blacklist).    If set, these tools will be filtered out."""``` |

#### allowed\_tool\_names`instance-attribute`

```
allowed_tool_names: NotRequired[list[str]]

```

Optional list of tool names to allow (whitelist).
If set, only these tools will be available.

#### blocked\_tool\_names`instance-attribute`

```
blocked_tool_names: NotRequired[list[str]]

```

Optional list of tool names to exclude (blacklist).
If set, these tools will be filtered out.

### MCPUtil

Set of utilities for interop between MCP and Agents SDK tools.

Source code in `src/agents/mcp/util.py`

|  |  |
| --- | --- |
| ``` 93 94 95 96 97 98 99100101102103104105106107108109110111112113114115116117118119120121122123124125126127128129130131132133134135136137138139140141142143144145146147148149150151152153154155156157158159160161162163164165166167168169170171172173174175176177178179180181182183184185186187188189190191192193194195196197198199200201202203204205206207208209210211212213214215216217218219220221222223224225226227``` | ```md-code__contentclass MCPUtil:    """Set of utilities for interop between MCP and Agents SDK tools."""    @classmethod    async def get_all_function_tools(        cls,        servers: list["MCPServer"],        convert_schemas_to_strict: bool,        run_context: RunContextWrapper[Any],        agent: "AgentBase",    ) -> list[Tool]:        """Get all function tools from a list of MCP servers."""        tools = []        tool_names: set[str] = set()        for server in servers:            server_tools = await cls.get_function_tools(                server, convert_schemas_to_strict, run_context, agent            )            server_tool_names = {tool.name for tool in server_tools}            if len(server_tool_names & tool_names) > 0:                raise UserError(                    f"Duplicate tool names found across MCP servers: "                    f"{server_tool_names & tool_names}"                )            tool_names.update(server_tool_names)            tools.extend(server_tools)        return tools    @classmethod    async def get_function_tools(        cls,        server: "MCPServer",        convert_schemas_to_strict: bool,        run_context: RunContextWrapper[Any],        agent: "AgentBase",    ) -> list[Tool]:        """Get all function tools from a single MCP server."""        with mcp_tools_span(server=server.name) as span:            tools = await server.list_tools(run_context, agent)            span.span_data.result = [tool.name for tool in tools]        return [cls.to_function_tool(tool, server, convert_schemas_to_strict) for tool in tools]    @classmethod    def to_function_tool(        cls, tool: "MCPTool", server: "MCPServer", convert_schemas_to_strict: bool    ) -> FunctionTool:        """Convert an MCP tool to an Agents SDK function tool."""        invoke_func = functools.partial(cls.invoke_mcp_tool, server, tool)        schema, is_strict = tool.inputSchema, False        # MCP spec doesn't require the inputSchema to have `properties`, but OpenAI spec does.        if "properties" not in schema:            schema["properties"] = {}        if convert_schemas_to_strict:            try:                schema = ensure_strict_json_schema(schema)                is_strict = True            except Exception as e:                logger.info(f"Error converting MCP schema to strict mode: {e}")        return FunctionTool(            name=tool.name,            description=tool.description or "",            params_json_schema=schema,            on_invoke_tool=invoke_func,            strict_json_schema=is_strict,        )    @classmethod    async def invoke_mcp_tool(        cls, server: "MCPServer", tool: "MCPTool", context: RunContextWrapper[Any], input_json: str    ) -> str:        """Invoke an MCP tool and return the result as a string."""        try:            json_data: dict[str, Any] = json.loads(input_json) if input_json else {}        except Exception as e:            if _debug.DONT_LOG_TOOL_DATA:                logger.debug(f"Invalid JSON input for tool {tool.name}")            else:                logger.debug(f"Invalid JSON input for tool {tool.name}: {input_json}")            raise ModelBehaviorError(                f"Invalid JSON input for tool {tool.name}: {input_json}"            ) from e        if _debug.DONT_LOG_TOOL_DATA:            logger.debug(f"Invoking MCP tool {tool.name}")        else:            logger.debug(f"Invoking MCP tool {tool.name} with input {input_json}")        try:            result = await server.call_tool(tool.name, json_data)        except Exception as e:            logger.error(f"Error invoking MCP tool {tool.name}: {e}")            raise AgentsException(f"Error invoking MCP tool {tool.name}: {e}") from e        if _debug.DONT_LOG_TOOL_DATA:            logger.debug(f"MCP tool {tool.name} completed.")        else:            logger.debug(f"MCP tool {tool.name} returned {result}")        # The MCP tool result is a list of content items, whereas OpenAI tool outputs are a single        # string. We'll try to convert.        if len(result.content) == 1:            tool_output = result.content[0].model_dump_json()            # Append structured content if it exists and we're using it.            if server.use_structured_content and result.structuredContent:                tool_output = f"{tool_output}\n{json.dumps(result.structuredContent)}"        elif len(result.content) > 1:            tool_results = [item.model_dump(mode="json") for item in result.content]            if server.use_structured_content and result.structuredContent:                tool_results.append(result.structuredContent)            tool_output = json.dumps(tool_results)        elif server.use_structured_content and result.structuredContent:            tool_output = json.dumps(result.structuredContent)        else:            # Empty content is a valid result (e.g., "no results found")            tool_output = "[]"        current_span = get_current_span()        if current_span:            if isinstance(current_span.span_data, FunctionSpanData):                current_span.span_data.output = tool_output                current_span.span_data.mcp_data = {                    "server": server.name,                }            else:                logger.warning(                    f"Current span is not a FunctionSpanData, skipping tool output: {current_span}"                )        return tool_output``` |

#### get\_all\_function\_tools`async``classmethod`

```
get_all_function_tools(
    servers: list[MCPServer],
    convert_schemas_to_strict: bool,
    run_context: RunContextWrapper[Any],
    agent: AgentBase,
) -> list[Tool]

```

Get all function tools from a list of MCP servers.

Source code in `src/agents/mcp/util.py`

|  |  |
| --- | --- |
| ``` 96 97 98 99100101102103104105106107108109110111112113114115116117118119120``` | ```md-code__content@classmethodasync def get_all_function_tools(    cls,    servers: list["MCPServer"],    convert_schemas_to_strict: bool,    run_context: RunContextWrapper[Any],    agent: "AgentBase",) -> list[Tool]:    """Get all function tools from a list of MCP servers."""    tools = []    tool_names: set[str] = set()    for server in servers:        server_tools = await cls.get_function_tools(            server, convert_schemas_to_strict, run_context, agent        )        server_tool_names = {tool.name for tool in server_tools}        if len(server_tool_names & tool_names) > 0:            raise UserError(                f"Duplicate tool names found across MCP servers: "                f"{server_tool_names & tool_names}"            )        tool_names.update(server_tool_names)        tools.extend(server_tools)    return tools``` |

#### get\_function\_tools`async``classmethod`

```
get_function_tools(
    server: MCPServer,
    convert_schemas_to_strict: bool,
    run_context: RunContextWrapper[Any],
    agent: AgentBase,
) -> list[Tool]

```

Get all function tools from a single MCP server.

Source code in `src/agents/mcp/util.py`

|  |  |
| --- | --- |
| ```122123124125126127128129130131132133134135136``` | ```md-code__content@classmethodasync def get_function_tools(    cls,    server: "MCPServer",    convert_schemas_to_strict: bool,    run_context: RunContextWrapper[Any],    agent: "AgentBase",) -> list[Tool]:    """Get all function tools from a single MCP server."""    with mcp_tools_span(server=server.name) as span:        tools = await server.list_tools(run_context, agent)        span.span_data.result = [tool.name for tool in tools]    return [cls.to_function_tool(tool, server, convert_schemas_to_strict) for tool in tools]``` |

#### to\_function\_tool`classmethod`

```
to_function_tool(
    tool: Tool,
    server: MCPServer,
    convert_schemas_to_strict: bool,
) -> FunctionTool

```

Convert an MCP tool to an Agents SDK function tool.

Source code in `src/agents/mcp/util.py`

|  |  |
| --- | --- |
| ```138139140141142143144145146147148149150151152153154155156157158159160161162163``` | ```md-code__content@classmethoddef to_function_tool(    cls, tool: "MCPTool", server: "MCPServer", convert_schemas_to_strict: bool) -> FunctionTool:    """Convert an MCP tool to an Agents SDK function tool."""    invoke_func = functools.partial(cls.invoke_mcp_tool, server, tool)    schema, is_strict = tool.inputSchema, False    # MCP spec doesn't require the inputSchema to have `properties`, but OpenAI spec does.    if "properties" not in schema:        schema["properties"] = {}    if convert_schemas_to_strict:        try:            schema = ensure_strict_json_schema(schema)            is_strict = True        except Exception as e:            logger.info(f"Error converting MCP schema to strict mode: {e}")    return FunctionTool(        name=tool.name,        description=tool.description or "",        params_json_schema=schema,        on_invoke_tool=invoke_func,        strict_json_schema=is_strict,    )``` |

#### invoke\_mcp\_tool`async``classmethod`

```
invoke_mcp_tool(
    server: MCPServer,
    tool: Tool,
    context: RunContextWrapper[Any],
    input_json: str,
) -> str

```

Invoke an MCP tool and return the result as a string.

Source code in `src/agents/mcp/util.py`

|  |  |
| --- | --- |
| ```165166167168169170171172173174175176177178179180181182183184185186187188189190191192193194195196197198199200201202203204205206207208209210211212213214215216217218219220221222223224225226227``` | ```md-code__content@classmethodasync def invoke_mcp_tool(    cls, server: "MCPServer", tool: "MCPTool", context: RunContextWrapper[Any], input_json: str) -> str:    """Invoke an MCP tool and return the result as a string."""    try:        json_data: dict[str, Any] = json.loads(input_json) if input_json else {}    except Exception as e:        if _debug.DONT_LOG_TOOL_DATA:            logger.debug(f"Invalid JSON input for tool {tool.name}")        else:            logger.debug(f"Invalid JSON input for tool {tool.name}: {input_json}")        raise ModelBehaviorError(            f"Invalid JSON input for tool {tool.name}: {input_json}"        ) from e    if _debug.DONT_LOG_TOOL_DATA:        logger.debug(f"Invoking MCP tool {tool.name}")    else:        logger.debug(f"Invoking MCP tool {tool.name} with input {input_json}")    try:        result = await server.call_tool(tool.name, json_data)    except Exception as e:        logger.error(f"Error invoking MCP tool {tool.name}: {e}")        raise AgentsException(f"Error invoking MCP tool {tool.name}: {e}") from e    if _debug.DONT_LOG_TOOL_DATA:        logger.debug(f"MCP tool {tool.name} completed.")    else:        logger.debug(f"MCP tool {tool.name} returned {result}")    # The MCP tool result is a list of content items, whereas OpenAI tool outputs are a single    # string. We'll try to convert.    if len(result.content) == 1:        tool_output = result.content[0].model_dump_json()        # Append structured content if it exists and we're using it.        if server.use_structured_content and result.structuredContent:            tool_output = f"{tool_output}\n{json.dumps(result.structuredContent)}"    elif len(result.content) > 1:        tool_results = [item.model_dump(mode="json") for item in result.content]        if server.use_structured_content and result.structuredContent:            tool_results.append(result.structuredContent)        tool_output = json.dumps(tool_results)    elif server.use_structured_content and result.structuredContent:        tool_output = json.dumps(result.structuredContent)    else:        # Empty content is a valid result (e.g., "no results found")        tool_output = "[]"    current_span = get_current_span()    if current_span:        if isinstance(current_span.span_data, FunctionSpanData):            current_span.span_data.output = tool_output            current_span.span_data.mcp_data = {                "server": server.name,            }        else:            logger.warning(                f"Current span is not a FunctionSpanData, skipping tool output: {current_span}"            )    return tool_output``` |

### create\_static\_tool\_filter

```
create_static_tool_filter(
    allowed_tool_names: Optional[list[str]] = None,
    blocked_tool_names: Optional[list[str]] = None,
) -> Optional[ToolFilterStatic]

```

Create a static tool filter from allowlist and blocklist parameters.

This is a convenience function for creating a ToolFilterStatic.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `allowed_tool_names` | `Optional[list[str]]` | Optional list of tool names to allow (whitelist). | `None` |
| `blocked_tool_names` | `Optional[list[str]]` | Optional list of tool names to exclude (blacklist). | `None` |

Returns:

| Type | Description |
| --- | --- |
| `Optional[ToolFilterStatic]` | A ToolFilterStatic if any filtering is specified, None otherwise. |

Source code in `src/agents/mcp/util.py`

|  |  |
| --- | --- |
| ```66676869707172737475767778798081828384858687888990``` | ```md-code__contentdef create_static_tool_filter(    allowed_tool_names: Optional[list[str]] = None,    blocked_tool_names: Optional[list[str]] = None,) -> Optional[ToolFilterStatic]:    """Create a static tool filter from allowlist and blocklist parameters.    This is a convenience function for creating a ToolFilterStatic.    Args:        allowed_tool_names: Optional list of tool names to allow (whitelist).        blocked_tool_names: Optional list of tool names to exclude (blacklist).    Returns:        A ToolFilterStatic if any filtering is specified, None otherwise.    """    if allowed_tool_names is None and blocked_tool_names is None:        return None    filter_dict: ToolFilterStatic = {}    if allowed_tool_names is not None:        filter_dict["allowed_tool_names"] = allowed_tool_names    if blocked_tool_names is not None:        filter_dict["blocked_tool_names"] = blocked_tool_names    return filter_dict``` |