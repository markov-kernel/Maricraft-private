---
title: `Tools`
source: https://openai.github.io/openai-agents-python/ref/tool/
---

# `Tools`

### MCPToolApprovalFunction`module-attribute`

```
MCPToolApprovalFunction = Callable[\
    [MCPToolApprovalRequest],\
    MaybeAwaitable[MCPToolApprovalFunctionResult],\
]

```

A function that approves or rejects a tool call.

### LocalShellExecutor`module-attribute`

```
LocalShellExecutor = Callable[\
    [LocalShellCommandRequest], MaybeAwaitable[str]\
]

```

A function that executes a command on a shell.

### Tool`module-attribute`

```
Tool = Union[\
    FunctionTool,\
    FileSearchTool,\
    WebSearchTool,\
    ComputerTool,\
    HostedMCPTool,\
    LocalShellTool,\
    ImageGenerationTool,\
    CodeInterpreterTool,\
]

```

A tool that can be used in an agent.

### FunctionToolResult`dataclass`

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ```49505152535455565758``` | ```md-code__content@dataclassclass FunctionToolResult:    tool: FunctionTool    """The tool that was run."""    output: Any    """The output of the tool."""    run_item: RunItem    """The run item that was produced as a result of the tool call."""``` |

#### tool`instance-attribute`

```
tool: FunctionTool

```

The tool that was run.

#### output`instance-attribute`

```
output: Any

```

The output of the tool.

#### run\_item`instance-attribute`

```
run_item: RunItem

```

The run item that was produced as a result of the tool call.

### FunctionTool`dataclass`

A tool that wraps a function. In most cases, you should use the `function_tool` helpers to
create a FunctionTool, as they let you easily wrap a Python function.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ```6162636465666768697071727374757677787980818283848586878889909192939495969798``` | ```md-code__content@dataclassclass FunctionTool:    """A tool that wraps a function. In most cases, you should use  the `function_tool` helpers to    create a FunctionTool, as they let you easily wrap a Python function.    """    name: str    """The name of the tool, as shown to the LLM. Generally the name of the function."""    description: str    """A description of the tool, as shown to the LLM."""    params_json_schema: dict[str, Any]    """The JSON schema for the tool's parameters."""    on_invoke_tool: Callable[[ToolContext[Any], str], Awaitable[Any]]    """A function that invokes the tool with the given context and parameters. The params passed    are:    1. The tool run context.    2. The arguments from the LLM, as a JSON string.    You must return a string representation of the tool output, or something we can call `str()` on.    In case of errors, you can either raise an Exception (which will cause the run to fail) or    return a string error message (which will be sent back to the LLM).    """    strict_json_schema: bool = True    """Whether the JSON schema is in strict mode. We **strongly** recommend setting this to True,    as it increases the likelihood of correct JSON input."""    is_enabled: bool | Callable[[RunContextWrapper[Any], AgentBase], MaybeAwaitable[bool]] = True    """Whether the tool is enabled. Either a bool or a Callable that takes the run context and agent    and returns whether the tool is enabled. You can use this to dynamically enable/disable a tool    based on your context/state."""    def __post_init__(self):        if self.strict_json_schema:            self.params_json_schema = ensure_strict_json_schema(self.params_json_schema)``` |

#### name`instance-attribute`

```
name: str

```

The name of the tool, as shown to the LLM. Generally the name of the function.

#### description`instance-attribute`

```
description: str

```

A description of the tool, as shown to the LLM.

#### params\_json\_schema`instance-attribute`

```
params_json_schema: dict[str, Any]

```

The JSON schema for the tool's parameters.

#### on\_invoke\_tool`instance-attribute`

```
on_invoke_tool: Callable[\
    [ToolContext[Any], str], Awaitable[Any]\
]

```

A function that invokes the tool with the given context and parameters. The params passed
are:
1\. The tool run context.
2\. The arguments from the LLM, as a JSON string.

You must return a string representation of the tool output, or something we can call `str()` on.
In case of errors, you can either raise an Exception (which will cause the run to fail) or
return a string error message (which will be sent back to the LLM).

#### strict\_json\_schema`class-attribute``instance-attribute`

```
strict_json_schema: bool = True

```

Whether the JSON schema is in strict mode. We **strongly** recommend setting this to True,
as it increases the likelihood of correct JSON input.

#### is\_enabled`class-attribute``instance-attribute`

```
is_enabled: (
    bool
    | Callable[\
        [RunContextWrapper[Any], AgentBase],\
        MaybeAwaitable[bool],\
    ]
) = True

```

Whether the tool is enabled. Either a bool or a Callable that takes the run context and agent
and returns whether the tool is enabled. You can use this to dynamically enable/disable a tool
based on your context/state.

### FileSearchTool`dataclass`

A hosted tool that lets the LLM search through a vector store. Currently only supported with
OpenAI models, using the Responses API.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ```101102103104105106107108109110111112113114115116117118119120121122123124``` | ```md-code__content@dataclassclass FileSearchTool:    """A hosted tool that lets the LLM search through a vector store. Currently only supported with    OpenAI models, using the Responses API.    """    vector_store_ids: list[str]    """The IDs of the vector stores to search."""    max_num_results: int | None = None    """The maximum number of results to return."""    include_search_results: bool = False    """Whether to include the search results in the output produced by the LLM."""    ranking_options: RankingOptions | None = None    """Ranking options for search."""    filters: Filters | None = None    """A filter to apply based on file attributes."""    @property    def name(self):        return "file_search"``` |

#### vector\_store\_ids`instance-attribute`

```
vector_store_ids: list[str]

```

The IDs of the vector stores to search.

#### max\_num\_results`class-attribute``instance-attribute`

```
max_num_results: int | None = None

```

The maximum number of results to return.

#### include\_search\_results`class-attribute``instance-attribute`

```
include_search_results: bool = False

```

Whether to include the search results in the output produced by the LLM.

#### ranking\_options`class-attribute``instance-attribute`

```
ranking_options: RankingOptions | None = None

```

Ranking options for search.

#### filters`class-attribute``instance-attribute`

```
filters: Filters | None = None

```

A filter to apply based on file attributes.

### WebSearchTool`dataclass`

A hosted tool that lets the LLM search the web. Currently only supported with OpenAI models,
using the Responses API.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ```127128129130131132133134135136137138139140141``` | ```md-code__content@dataclassclass WebSearchTool:    """A hosted tool that lets the LLM search the web. Currently only supported with OpenAI models,    using the Responses API.    """    user_location: UserLocation | None = None    """Optional location for the search. Lets you customize results to be relevant to a location."""    search_context_size: Literal["low", "medium", "high"] = "medium"    """The amount of context to use for the search."""    @property    def name(self):        return "web_search_preview"``` |

#### user\_location`class-attribute``instance-attribute`

```
user_location: UserLocation | None = None

```

Optional location for the search. Lets you customize results to be relevant to a location.

#### search\_context\_size`class-attribute``instance-attribute`

```
search_context_size: Literal["low", "medium", "high"] = (
    "medium"
)

```

The amount of context to use for the search.

### ComputerTool`dataclass`

A hosted tool that lets the LLM control a computer.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ```144145146147148149150151152153154155156157158``` | ```md-code__content@dataclassclass ComputerTool:    """A hosted tool that lets the LLM control a computer."""    computer: Computer | AsyncComputer    """The computer implementation, which describes the environment and dimensions of the computer,    as well as implements the computer actions like click, screenshot, etc.    """    on_safety_check: Callable[[ComputerToolSafetyCheckData], MaybeAwaitable[bool]] | None = None    """Optional callback to acknowledge computer tool safety checks."""    @property    def name(self):        return "computer_use_preview"``` |

#### computer`instance-attribute`

```
computer: Computer | AsyncComputer

```

The computer implementation, which describes the environment and dimensions of the computer,
as well as implements the computer actions like click, screenshot, etc.

#### on\_safety\_check`class-attribute``instance-attribute`

```
on_safety_check: (
    Callable[\
        [ComputerToolSafetyCheckData], MaybeAwaitable[bool]\
    ]
    | None
) = None

```

Optional callback to acknowledge computer tool safety checks.

### ComputerToolSafetyCheckData`dataclass`

Information about a computer tool safety check.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ```161162163164165166167168169170171172173174175``` | ```md-code__content@dataclassclass ComputerToolSafetyCheckData:    """Information about a computer tool safety check."""    ctx_wrapper: RunContextWrapper[Any]    """The run context."""    agent: Agent[Any]    """The agent performing the computer action."""    tool_call: ResponseComputerToolCall    """The computer tool call."""    safety_check: PendingSafetyCheck    """The pending safety check to acknowledge."""``` |

#### ctx\_wrapper`instance-attribute`

```
ctx_wrapper: RunContextWrapper[Any]

```

The run context.

#### agent`instance-attribute`

```
agent: Agent[Any]

```

The agent performing the computer action.

#### tool\_call`instance-attribute`

```
tool_call: ResponseComputerToolCall

```

The computer tool call.

#### safety\_check`instance-attribute`

```
safety_check: PendingSafetyCheck

```

The pending safety check to acknowledge.

### MCPToolApprovalRequest`dataclass`

A request to approve a tool call.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ```178179180181182183184185186``` | ```md-code__content@dataclassclass MCPToolApprovalRequest:    """A request to approve a tool call."""    ctx_wrapper: RunContextWrapper[Any]    """The run context."""    data: McpApprovalRequest    """The data from the MCP tool approval request."""``` |

#### ctx\_wrapper`instance-attribute`

```
ctx_wrapper: RunContextWrapper[Any]

```

The run context.

#### data`instance-attribute`

```
data: McpApprovalRequest

```

The data from the MCP tool approval request.

### MCPToolApprovalFunctionResult

Bases: `TypedDict`

The result of an MCP tool approval function.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ```189190191192193194195196``` | ```md-code__contentclass MCPToolApprovalFunctionResult(TypedDict):    """The result of an MCP tool approval function."""    approve: bool    """Whether to approve the tool call."""    reason: NotRequired[str]    """An optional reason, if rejected."""``` |

#### approve`instance-attribute`

```
approve: bool

```

Whether to approve the tool call.

#### reason`instance-attribute`

```
reason: NotRequired[str]

```

An optional reason, if rejected.

### HostedMCPTool`dataclass`

A tool that allows the LLM to use a remote MCP server. The LLM will automatically list and
call tools, without requiring a round trip back to your code.
If you want to run MCP servers locally via stdio, in a VPC or other non-publicly-accessible
environment, or you just prefer to run tool calls locally, then you can instead use the servers
in `agents.mcp` and pass `Agent(mcp_servers=[...])` to the agent.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ```205206207208209210211212213214215216217218219220221222223``` | ```md-code__content@dataclassclass HostedMCPTool:    """A tool that allows the LLM to use a remote MCP server. The LLM will automatically list and    call tools, without requiring a round trip back to your code.    If you want to run MCP servers locally via stdio, in a VPC or other non-publicly-accessible    environment, or you just prefer to run tool calls locally, then you can instead use the servers    in `agents.mcp` and pass `Agent(mcp_servers=[...])` to the agent."""    tool_config: Mcp    """The MCP tool config, which includes the server URL and other settings."""    on_approval_request: MCPToolApprovalFunction | None = None    """An optional function that will be called if approval is requested for an MCP tool. If not    provided, you will need to manually add approvals/rejections to the input and call    `Runner.run(...)` again."""    @property    def name(self):        return "hosted_mcp"``` |

#### tool\_config`instance-attribute`

```
tool_config: Mcp

```

The MCP tool config, which includes the server URL and other settings.

#### on\_approval\_request`class-attribute``instance-attribute`

```
on_approval_request: MCPToolApprovalFunction | None = None

```

An optional function that will be called if approval is requested for an MCP tool. If not
provided, you will need to manually add approvals/rejections to the input and call
`Runner.run(...)` again.

### CodeInterpreterTool`dataclass`

A tool that allows the LLM to execute code in a sandboxed environment.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ```226227228229230231232233234235``` | ```md-code__content@dataclassclass CodeInterpreterTool:    """A tool that allows the LLM to execute code in a sandboxed environment."""    tool_config: CodeInterpreter    """The tool config, which includes the container and other settings."""    @property    def name(self):        return "code_interpreter"``` |

#### tool\_config`instance-attribute`

```
tool_config: CodeInterpreter

```

The tool config, which includes the container and other settings.

### ImageGenerationTool`dataclass`

A tool that allows the LLM to generate images.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ```238239240241242243244245246247``` | ```md-code__content@dataclassclass ImageGenerationTool:    """A tool that allows the LLM to generate images."""    tool_config: ImageGeneration    """The tool config, which image generation settings."""    @property    def name(self):        return "image_generation"``` |

#### tool\_config`instance-attribute`

```
tool_config: ImageGeneration

```

The tool config, which image generation settings.

### LocalShellCommandRequest`dataclass`

A request to execute a command on a shell.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ```250251252253254255256257258``` | ```md-code__content@dataclassclass LocalShellCommandRequest:    """A request to execute a command on a shell."""    ctx_wrapper: RunContextWrapper[Any]    """The run context."""    data: LocalShellCall    """The data from the local shell tool call."""``` |

#### ctx\_wrapper`instance-attribute`

```
ctx_wrapper: RunContextWrapper[Any]

```

The run context.

#### data`instance-attribute`

```
data: LocalShellCall

```

The data from the local shell tool call.

### LocalShellTool`dataclass`

A tool that allows the LLM to execute commands on a shell.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ```265266267268269270271272273274``` | ```md-code__content@dataclassclass LocalShellTool:    """A tool that allows the LLM to execute commands on a shell."""    executor: LocalShellExecutor    """A function that executes a command on a shell."""    @property    def name(self):        return "local_shell"``` |

#### executor`instance-attribute`

```
executor: LocalShellExecutor

```

A function that executes a command on a shell.

### default\_tool\_error\_function

```
default_tool_error_function(
    ctx: RunContextWrapper[Any], error: Exception
) -> str

```

The default tool error function, which just returns a generic error message.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ```290291292``` | ```md-code__contentdef default_tool_error_function(ctx: RunContextWrapper[Any], error: Exception) -> str:    """The default tool error function, which just returns a generic error message."""    return f"An error occurred while running the tool. Please try again. Error: {str(error)}"``` |

### function\_tool

```
function_tool(
    func: ToolFunction[...],
    *,
    name_override: str | None = None,
    description_override: str | None = None,
    docstring_style: DocstringStyle | None = None,
    use_docstring_info: bool = True,
    failure_error_function: ToolErrorFunction | None = None,
    strict_mode: bool = True,
    is_enabled: bool
    | Callable[\
        [RunContextWrapper[Any], AgentBase],\
        MaybeAwaitable[bool],\
    ] = True,
) -> FunctionTool

```

```
function_tool(
    *,
    name_override: str | None = None,
    description_override: str | None = None,
    docstring_style: DocstringStyle | None = None,
    use_docstring_info: bool = True,
    failure_error_function: ToolErrorFunction | None = None,
    strict_mode: bool = True,
    is_enabled: bool
    | Callable[\
        [RunContextWrapper[Any], AgentBase],\
        MaybeAwaitable[bool],\
    ] = True,
) -> Callable[[ToolFunction[...]], FunctionTool]

```

```
function_tool(
    func: ToolFunction[...] | None = None,
    *,
    name_override: str | None = None,
    description_override: str | None = None,
    docstring_style: DocstringStyle | None = None,
    use_docstring_info: bool = True,
    failure_error_function: ToolErrorFunction
    | None = default_tool_error_function,
    strict_mode: bool = True,
    is_enabled: bool
    | Callable[\
        [RunContextWrapper[Any], AgentBase],\
        MaybeAwaitable[bool],\
    ] = True,
) -> (
    FunctionTool
    | Callable[[ToolFunction[...]], FunctionTool]
)

```

Decorator to create a FunctionTool from a function. By default, we will:
1\. Parse the function signature to create a JSON schema for the tool's parameters.
2\. Use the function's docstring to populate the tool's description.
3\. Use the function's docstring to populate argument descriptions.
The docstring style is detected automatically, but you can override it.

If the function takes a `RunContextWrapper` as the first argument, it _must_ match the
context type of the agent that uses the tool.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `func` | `ToolFunction[...] | None` | The function to wrap. | `None` |
| `name_override` | `str | None` | If provided, use this name for the tool instead of the function's name. | `None` |
| `description_override` | `str | None` | If provided, use this description for the tool instead of thefunction's docstring. | `None` |
| `docstring_style` | `DocstringStyle | None` | If provided, use this style for the tool's docstring. If not provided,we will attempt to auto-detect the style. | `None` |
| `use_docstring_info` | `bool` | If True, use the function's docstring to populate the tool'sdescription and argument descriptions. | `True` |
| `failure_error_function` | `ToolErrorFunction | None` | If provided, use this function to generate an error message whenthe tool call fails. The error message is sent to the LLM. If you pass None, then noerror message will be sent and instead an Exception will be raised. | `default_tool_error_function` |
| `strict_mode` | `bool` | Whether to enable strict mode for the tool's JSON schema. We _strongly_recommend setting this to True, as it increases the likelihood of correct JSON input.If False, it allows non-strict JSON schemas. For example, if a parameter has a defaultvalue, it will be optional, additional properties are allowed, etc. See here for more:https://platform.openai.com/docs/guides/structured-outputs?api-mode=responses#supported-schemas | `True` |
| `is_enabled` | `bool | Callable[[RunContextWrapper[Any], AgentBase], MaybeAwaitable[bool]]` | Whether the tool is enabled. Can be a bool or a callable that takes the runcontext and agent and returns whether the tool is enabled. Disabled tools are hiddenfrom the LLM at runtime. | `True` |

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ```329330331332333334335336337338339340341342343344345346347348349350351352353354355356357358359360361362363364365366367368369370371372373374375376377378379380381382383384385386387388389390391392393394395396397398399400401402403404405406407408409410411412413414415416417418419420421422423424425426427428429430431432433434435436437438439440441442443444445446447448449450451452453454455456457458459460461462463464465466467468469470``` | ```md-code__contentdef function_tool(    func: ToolFunction[...] | None = None,    *,    name_override: str | None = None,    description_override: str | None = None,    docstring_style: DocstringStyle | None = None,    use_docstring_info: bool = True,    failure_error_function: ToolErrorFunction | None = default_tool_error_function,    strict_mode: bool = True,    is_enabled: bool | Callable[[RunContextWrapper[Any], AgentBase], MaybeAwaitable[bool]] = True,) -> FunctionTool | Callable[[ToolFunction[...]], FunctionTool]:    """    Decorator to create a FunctionTool from a function. By default, we will:    1. Parse the function signature to create a JSON schema for the tool's parameters.    2. Use the function's docstring to populate the tool's description.    3. Use the function's docstring to populate argument descriptions.    The docstring style is detected automatically, but you can override it.    If the function takes a `RunContextWrapper` as the first argument, it *must* match the    context type of the agent that uses the tool.    Args:        func: The function to wrap.        name_override: If provided, use this name for the tool instead of the function's name.        description_override: If provided, use this description for the tool instead of the            function's docstring.        docstring_style: If provided, use this style for the tool's docstring. If not provided,            we will attempt to auto-detect the style.        use_docstring_info: If True, use the function's docstring to populate the tool's            description and argument descriptions.        failure_error_function: If provided, use this function to generate an error message when            the tool call fails. The error message is sent to the LLM. If you pass None, then no            error message will be sent and instead an Exception will be raised.        strict_mode: Whether to enable strict mode for the tool's JSON schema. We *strongly*            recommend setting this to True, as it increases the likelihood of correct JSON input.            If False, it allows non-strict JSON schemas. For example, if a parameter has a default            value, it will be optional, additional properties are allowed, etc. See here for more:            https://platform.openai.com/docs/guides/structured-outputs?api-mode=responses#supported-schemas        is_enabled: Whether the tool is enabled. Can be a bool or a callable that takes the run            context and agent and returns whether the tool is enabled. Disabled tools are hidden            from the LLM at runtime.    """    def _create_function_tool(the_func: ToolFunction[...]) -> FunctionTool:        schema = function_schema(            func=the_func,            name_override=name_override,            description_override=description_override,            docstring_style=docstring_style,            use_docstring_info=use_docstring_info,            strict_json_schema=strict_mode,        )        async def _on_invoke_tool_impl(ctx: ToolContext[Any], input: str) -> Any:            try:                json_data: dict[str, Any] = json.loads(input) if input else {}            except Exception as e:                if _debug.DONT_LOG_TOOL_DATA:                    logger.debug(f"Invalid JSON input for tool {schema.name}")                else:                    logger.debug(f"Invalid JSON input for tool {schema.name}: {input}")                raise ModelBehaviorError(                    f"Invalid JSON input for tool {schema.name}: {input}"                ) from e            if _debug.DONT_LOG_TOOL_DATA:                logger.debug(f"Invoking tool {schema.name}")            else:                logger.debug(f"Invoking tool {schema.name} with input {input}")            try:                parsed = (                    schema.params_pydantic_model(**json_data)                    if json_data                    else schema.params_pydantic_model()                )            except ValidationError as e:                raise ModelBehaviorError(f"Invalid JSON input for tool {schema.name}: {e}") from e            args, kwargs_dict = schema.to_call_args(parsed)            if not _debug.DONT_LOG_TOOL_DATA:                logger.debug(f"Tool call args: {args}, kwargs: {kwargs_dict}")            if inspect.iscoroutinefunction(the_func):                if schema.takes_context:                    result = await the_func(ctx, *args, **kwargs_dict)                else:                    result = await the_func(*args, **kwargs_dict)            else:                if schema.takes_context:                    result = the_func(ctx, *args, **kwargs_dict)                else:                    result = the_func(*args, **kwargs_dict)            if _debug.DONT_LOG_TOOL_DATA:                logger.debug(f"Tool {schema.name} completed.")            else:                logger.debug(f"Tool {schema.name} returned {result}")            return result        async def _on_invoke_tool(ctx: ToolContext[Any], input: str) -> Any:            try:                return await _on_invoke_tool_impl(ctx, input)            except Exception as e:                if failure_error_function is None:                    raise                result = failure_error_function(ctx, e)                if inspect.isawaitable(result):                    return await result                _error_tracing.attach_error_to_current_span(                    SpanError(                        message="Error running tool (non-fatal)",                        data={                            "tool_name": schema.name,                            "error": str(e),                        },                    )                )                return result        return FunctionTool(            name=schema.name,            description=schema.description or "",            params_json_schema=schema.params_json_schema,            on_invoke_tool=_on_invoke_tool,            strict_json_schema=strict_mode,            is_enabled=is_enabled,        )    # If func is actually a callable, we were used as @function_tool with no parentheses    if callable(func):        return _create_function_tool(func)    # Otherwise, we were used as @function_tool(...), so return a decorator    def decorator(real_func: ToolFunction[...]) -> FunctionTool:        return _create_function_tool(real_func)    return decorator``` |