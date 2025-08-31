---
title: `Agents`
source: https://openai.github.io/openai-agents-python/ref/agent/
---

# `Agents`

### ToolsToFinalOutputFunction`module-attribute`

```
ToolsToFinalOutputFunction: TypeAlias = Callable[\
    [RunContextWrapper[TContext], list[FunctionToolResult]],\
    MaybeAwaitable[ToolsToFinalOutputResult],\
]

```

A function that takes a run context and a list of tool results, and returns a
`ToolsToFinalOutputResult`.

### ToolsToFinalOutputResult`dataclass`

Source code in `src/agents/agent.py`

|  |  |
| --- | --- |
| ```3334353637383940414243``` | ```md-code__content@dataclassclass ToolsToFinalOutputResult:    is_final_output: bool    """Whether this is the final output. If False, the LLM will run again and receive the tool call    output.    """    final_output: Any | None = None    """The final output. Can be None if `is_final_output` is False, otherwise must match the    `output_type` of the agent.    """``` |

#### is\_final\_output`instance-attribute`

```
is_final_output: bool

```

Whether this is the final output. If False, the LLM will run again and receive the tool call
output.

#### final\_output`class-attribute``instance-attribute`

```
final_output: Any | None = None

```

The final output. Can be None if `is_final_output` is False, otherwise must match the
`output_type` of the agent.

### StopAtTools

Bases: `TypedDict`

Source code in `src/agents/agent.py`

|  |  |
| --- | --- |
| ```555657``` | ```md-code__contentclass StopAtTools(TypedDict):    stop_at_tool_names: list[str]    """A list of tool names, any of which will stop the agent from running further."""``` |

#### stop\_at\_tool\_names`instance-attribute`

```
stop_at_tool_names: list[str]

```

A list of tool names, any of which will stop the agent from running further.

### MCPConfig

Bases: `TypedDict`

Configuration for MCP servers.

Source code in `src/agents/agent.py`

|  |  |
| --- | --- |
| ```60616263646566``` | ```md-code__contentclass MCPConfig(TypedDict):    """Configuration for MCP servers."""    convert_schemas_to_strict: NotRequired[bool]    """If True, we will attempt to convert the MCP schemas to strict-mode schemas. This is a    best-effort conversion, so some schemas may not be convertible. Defaults to False.    """``` |

#### convert\_schemas\_to\_strict`instance-attribute`

```
convert_schemas_to_strict: NotRequired[bool]

```

If True, we will attempt to convert the MCP schemas to strict-mode schemas. This is a
best-effort conversion, so some schemas may not be convertible. Defaults to False.

### AgentBase`dataclass`

Bases: `Generic[TContext]`

Base class for `Agent` and `RealtimeAgent`.

Source code in `src/agents/agent.py`

|  |  |
| --- | --- |
| ``` 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99100101102103104105106107108109110111112113114115116117118119120121122``` | ```md-code__content@dataclassclass AgentBase(Generic[TContext]):    """Base class for `Agent` and `RealtimeAgent`."""    name: str    """The name of the agent."""    handoff_description: str | None = None    """A description of the agent. This is used when the agent is used as a handoff, so that an    LLM knows what it does and when to invoke it.    """    tools: list[Tool] = field(default_factory=list)    """A list of tools that the agent can use."""    mcp_servers: list[MCPServer] = field(default_factory=list)    """A list of [Model Context Protocol](https://modelcontextprotocol.io/) servers that    the agent can use. Every time the agent runs, it will include tools from these servers in the    list of available tools.    NOTE: You are expected to manage the lifecycle of these servers. Specifically, you must call    `server.connect()` before passing it to the agent, and `server.cleanup()` when the server is no    longer needed.    """    mcp_config: MCPConfig = field(default_factory=lambda: MCPConfig())    """Configuration for MCP servers."""    async def get_mcp_tools(self, run_context: RunContextWrapper[TContext]) -> list[Tool]:        """Fetches the available tools from the MCP servers."""        convert_schemas_to_strict = self.mcp_config.get("convert_schemas_to_strict", False)        return await MCPUtil.get_all_function_tools(            self.mcp_servers, convert_schemas_to_strict, run_context, self        )    async def get_all_tools(self, run_context: RunContextWrapper[Any]) -> list[Tool]:        """All agent tools, including MCP tools and function tools."""        mcp_tools = await self.get_mcp_tools(run_context)        async def _check_tool_enabled(tool: Tool) -> bool:            if not isinstance(tool, FunctionTool):                return True            attr = tool.is_enabled            if isinstance(attr, bool):                return attr            res = attr(run_context, self)            if inspect.isawaitable(res):                return bool(await res)            return bool(res)        results = await asyncio.gather(*(_check_tool_enabled(t) for t in self.tools))        enabled: list[Tool] = [t for t, ok in zip(self.tools, results) if ok]        return [*mcp_tools, *enabled]``` |

#### name`instance-attribute`

```
name: str

```

The name of the agent.

#### handoff\_description`class-attribute``instance-attribute`

```
handoff_description: str | None = None

```

A description of the agent. This is used when the agent is used as a handoff, so that an
LLM knows what it does and when to invoke it.

#### tools`class-attribute``instance-attribute`

```
tools: list[Tool] = field(default_factory=list)

```

A list of tools that the agent can use.

#### mcp\_servers`class-attribute``instance-attribute`

```
mcp_servers: list[MCPServer] = field(default_factory=list)

```

A list of [Model Context Protocol](https://modelcontextprotocol.io/) servers that
the agent can use. Every time the agent runs, it will include tools from these servers in the
list of available tools.

NOTE: You are expected to manage the lifecycle of these servers. Specifically, you must call
`server.connect()` before passing it to the agent, and `server.cleanup()` when the server is no
longer needed.

#### mcp\_config`class-attribute``instance-attribute`

```
mcp_config: MCPConfig = field(
    default_factory=lambda: MCPConfig()
)

```

Configuration for MCP servers.

#### get\_mcp\_tools`async`

```
get_mcp_tools(
    run_context: RunContextWrapper[TContext],
) -> list[Tool]

```

Fetches the available tools from the MCP servers.

Source code in `src/agents/agent.py`

|  |  |
| --- | --- |
| ``` 97 98 99100101102``` | ```md-code__contentasync def get_mcp_tools(self, run_context: RunContextWrapper[TContext]) -> list[Tool]:    """Fetches the available tools from the MCP servers."""    convert_schemas_to_strict = self.mcp_config.get("convert_schemas_to_strict", False)    return await MCPUtil.get_all_function_tools(        self.mcp_servers, convert_schemas_to_strict, run_context, self    )``` |

#### get\_all\_tools`async`

```
get_all_tools(
    run_context: RunContextWrapper[Any],
) -> list[Tool]

```

All agent tools, including MCP tools and function tools.

Source code in `src/agents/agent.py`

|  |  |
| --- | --- |
| ```104105106107108109110111112113114115116117118119120121122``` | ```md-code__contentasync def get_all_tools(self, run_context: RunContextWrapper[Any]) -> list[Tool]:    """All agent tools, including MCP tools and function tools."""    mcp_tools = await self.get_mcp_tools(run_context)    async def _check_tool_enabled(tool: Tool) -> bool:        if not isinstance(tool, FunctionTool):            return True        attr = tool.is_enabled        if isinstance(attr, bool):            return attr        res = attr(run_context, self)        if inspect.isawaitable(res):            return bool(await res)        return bool(res)    results = await asyncio.gather(*(_check_tool_enabled(t) for t in self.tools))    enabled: list[Tool] = [t for t, ok in zip(self.tools, results) if ok]    return [*mcp_tools, *enabled]``` |

### Agent`dataclass`

Bases: `AgentBase`, `Generic[TContext]`

An agent is an AI model configured with instructions, tools, guardrails, handoffs and more.

We strongly recommend passing `instructions`, which is the "system prompt" for the agent. In
addition, you can pass `handoff_description`, which is a human-readable description of the
agent, used when the agent is used inside tools/handoffs.

Agents are generic on the context type. The context is a (mutable) object you create. It is
passed to tool functions, handoffs, guardrails, etc.

See `AgentBase` for base parameters that are shared with `RealtimeAgent` s.

Source code in `src/agents/agent.py`

|  |  |
| --- | --- |
| ```125126127128129130131132133134135136137138139140141142143144145146147148149150151152153154155156157158159160161162163164165166167168169170171172173174175176177178179180181182183184185186187188189190191192193194195196197198199200201202203204205206207208209210211212213214215216217218219220221222223224225226227228229230231232233234235236237238239240241242243244245246247248249250251252253254255256257258259260261262263264265266267268269270271272273274275276277278279280281282283284285286287288289290291292293294295296297298299300301302303304305306307308309310311312313314315316317318``` | ````md-code__content@dataclassclass Agent(AgentBase, Generic[TContext]):    """An agent is an AI model configured with instructions, tools, guardrails, handoffs and more.    We strongly recommend passing `instructions`, which is the "system prompt" for the agent. In    addition, you can pass `handoff_description`, which is a human-readable description of the    agent, used when the agent is used inside tools/handoffs.    Agents are generic on the context type. The context is a (mutable) object you create. It is    passed to tool functions, handoffs, guardrails, etc.    See `AgentBase` for base parameters that are shared with `RealtimeAgent`s.    """    instructions: (        str | Callable[            [RunContextWrapper[TContext], Agent[TContext]],            MaybeAwaitable[str],        ] | None    ) = None    """The instructions for the agent. Will be used as the "system prompt" when this agent is    invoked. Describes what the agent should do, and how it responds.    Can either be a string, or a function that dynamically generates instructions for the agent. If    you provide a function, it will be called with the context and the agent instance. It must    return a string.    """    prompt: Prompt | DynamicPromptFunction | None = None    """A prompt object (or a function that returns a Prompt). Prompts allow you to dynamically    configure the instructions, tools and other config for an agent outside of your code. Only    usable with OpenAI models, using the Responses API.    """    handoffs: list[Agent[Any] | Handoff[TContext, Any]] = field(default_factory=list)    """Handoffs are sub-agents that the agent can delegate to. You can provide a list of handoffs,    and the agent can choose to delegate to them if relevant. Allows for separation of concerns and    modularity.    """    model: str | Model | None = None    """The model implementation to use when invoking the LLM.    By default, if not set, the agent will use the default model configured in    `openai_provider.DEFAULT_MODEL` (currently "gpt-4o").    """    model_settings: ModelSettings = field(default_factory=ModelSettings)    """Configures model-specific tuning parameters (e.g. temperature, top_p).    """    input_guardrails: list[InputGuardrail[TContext]] = field(default_factory=list)    """A list of checks that run in parallel to the agent's execution, before generating a    response. Runs only if the agent is the first agent in the chain.    """    output_guardrails: list[OutputGuardrail[TContext]] = field(default_factory=list)    """A list of checks that run on the final output of the agent, after generating a response.    Runs only if the agent produces a final output.    """    output_type: type[Any] | AgentOutputSchemaBase | None = None    """The type of the output object. If not provided, the output will be `str`. In most cases,    you should pass a regular Python type (e.g. a dataclass, Pydantic model, TypedDict, etc).    You can customize this in two ways:    1. If you want non-strict schemas, pass `AgentOutputSchema(MyClass, strict_json_schema=False)`.    2. If you want to use a custom JSON schema (i.e. without using the SDK's automatic schema)       creation, subclass and pass an `AgentOutputSchemaBase` subclass.    """    hooks: AgentHooks[TContext] | None = None    """A class that receives callbacks on various lifecycle events for this agent.    """    tool_use_behavior: (        Literal["run_llm_again", "stop_on_first_tool"] | StopAtTools | ToolsToFinalOutputFunction    ) = "run_llm_again"    """This lets you configure how tool use is handled.    - "run_llm_again": The default behavior. Tools are run, and then the LLM receives the results        and gets to respond.    - "stop_on_first_tool": The output of the first tool call is used as the final output. This        means that the LLM does not process the result of the tool call.    - A list of tool names: The agent will stop running if any of the tools in the list are called.        The final output will be the output of the first matching tool call. The LLM does not        process the result of the tool call.    - A function: If you pass a function, it will be called with the run context and the list of      tool results. It must return a `ToolsToFinalOutputResult`, which determines whether the tool      calls result in a final output.      NOTE: This configuration is specific to FunctionTools. Hosted tools, such as file search,      web search, etc are always processed by the LLM.    """    reset_tool_choice: bool = True    """Whether to reset the tool choice to the default value after a tool has been called. Defaults    to True. This ensures that the agent doesn't enter an infinite loop of tool usage."""    def clone(self, **kwargs: Any) -> Agent[TContext]:        """Make a copy of the agent, with the given arguments changed. For example, you could do:        ```        new_agent = agent.clone(instructions="New instructions")        ```        """        return dataclasses.replace(self, **kwargs)    def as_tool(        self,        tool_name: str | None,        tool_description: str | None,        custom_output_extractor: Callable[[RunResult], Awaitable[str]] | None = None,    ) -> Tool:        """Transform this agent into a tool, callable by other agents.        This is different from handoffs in two ways:        1. In handoffs, the new agent receives the conversation history. In this tool, the new agent           receives generated input.        2. In handoffs, the new agent takes over the conversation. In this tool, the new agent is           called as a tool, and the conversation is continued by the original agent.        Args:            tool_name: The name of the tool. If not provided, the agent's name will be used.            tool_description: The description of the tool, which should indicate what it does and                when to use it.            custom_output_extractor: A function that extracts the output from the agent. If not                provided, the last message from the agent will be used.        """        @function_tool(            name_override=tool_name or _transforms.transform_string_function_style(self.name),            description_override=tool_description or "",        )        async def run_agent(context: RunContextWrapper, input: str) -> str:            from .run import Runner            output = await Runner.run(                starting_agent=self,                input=input,                context=context.context,            )            if custom_output_extractor:                return await custom_output_extractor(output)            return ItemHelpers.text_message_outputs(output.new_items)        return run_agent    async def get_system_prompt(self, run_context: RunContextWrapper[TContext]) -> str | None:        """Get the system prompt for the agent."""        if isinstance(self.instructions, str):            return self.instructions        elif callable(self.instructions):            if inspect.iscoroutinefunction(self.instructions):                return await cast(Awaitable[str], self.instructions(run_context, self))            else:                return cast(str, self.instructions(run_context, self))        elif self.instructions is not None:            logger.error(f"Instructions must be a string or a function, got {self.instructions}")        return None    async def get_prompt(        self, run_context: RunContextWrapper[TContext]    ) -> ResponsePromptParam | None:        """Get the prompt for the agent."""        return await PromptUtil.to_model_input(self.prompt, run_context, self)    async def get_mcp_tools(self, run_context: RunContextWrapper[TContext]) -> list[Tool]:        """Fetches the available tools from the MCP servers."""        convert_schemas_to_strict = self.mcp_config.get("convert_schemas_to_strict", False)        return await MCPUtil.get_all_function_tools(            self.mcp_servers, convert_schemas_to_strict, run_context, self        )    async def get_all_tools(self, run_context: RunContextWrapper[Any]) -> list[Tool]:        """All agent tools, including MCP tools and function tools."""        mcp_tools = await self.get_mcp_tools(run_context)        async def _check_tool_enabled(tool: Tool) -> bool:            if not isinstance(tool, FunctionTool):                return True            attr = tool.is_enabled            if isinstance(attr, bool):                return attr            res = attr(run_context, self)            if inspect.isawaitable(res):                return bool(await res)            return bool(res)        results = await asyncio.gather(*(_check_tool_enabled(t) for t in self.tools))        enabled: list[Tool] = [t for t, ok in zip(self.tools, results) if ok]        return [*mcp_tools, *enabled]```` |

#### instructions`class-attribute``instance-attribute`

```
instructions: (
    str
    | Callable[\
        [RunContextWrapper[TContext], Agent[TContext]],\
        MaybeAwaitable[str],\
    ]
    | None
) = None

```

The instructions for the agent. Will be used as the "system prompt" when this agent is
invoked. Describes what the agent should do, and how it responds.

Can either be a string, or a function that dynamically generates instructions for the agent. If
you provide a function, it will be called with the context and the agent instance. It must
return a string.

#### prompt`class-attribute``instance-attribute`

```
prompt: Prompt | DynamicPromptFunction | None = None

```

A prompt object (or a function that returns a Prompt). Prompts allow you to dynamically
configure the instructions, tools and other config for an agent outside of your code. Only
usable with OpenAI models, using the Responses API.

#### handoffs`class-attribute``instance-attribute`

```
handoffs: list[Agent[Any] | Handoff[TContext, Any]] = field(
    default_factory=list
)

```

Handoffs are sub-agents that the agent can delegate to. You can provide a list of handoffs,
and the agent can choose to delegate to them if relevant. Allows for separation of concerns and
modularity.

#### model`class-attribute``instance-attribute`

```
model: str | Model | None = None

```

The model implementation to use when invoking the LLM.

By default, if not set, the agent will use the default model configured in
`openai_provider.DEFAULT_MODEL` (currently "gpt-4o").

#### model\_settings`class-attribute``instance-attribute`

```
model_settings: ModelSettings = field(
    default_factory=ModelSettings
)

```

Configures model-specific tuning parameters (e.g. temperature, top\_p).

#### input\_guardrails`class-attribute``instance-attribute`

```
input_guardrails: list[InputGuardrail[TContext]] = field(
    default_factory=list
)

```

A list of checks that run in parallel to the agent's execution, before generating a
response. Runs only if the agent is the first agent in the chain.

#### output\_guardrails`class-attribute``instance-attribute`

```
output_guardrails: list[OutputGuardrail[TContext]] = field(
    default_factory=list
)

```

A list of checks that run on the final output of the agent, after generating a response.
Runs only if the agent produces a final output.

#### output\_type`class-attribute``instance-attribute`

```
output_type: type[Any] | AgentOutputSchemaBase | None = None

```

The type of the output object. If not provided, the output will be `str`. In most cases,
you should pass a regular Python type (e.g. a dataclass, Pydantic model, TypedDict, etc).
You can customize this in two ways:
1\. If you want non-strict schemas, pass `AgentOutputSchema(MyClass, strict_json_schema=False)`.
2\. If you want to use a custom JSON schema (i.e. without using the SDK's automatic schema)
creation, subclass and pass an `AgentOutputSchemaBase` subclass.

#### hooks`class-attribute``instance-attribute`

```
hooks: AgentHooks[TContext] | None = None

```

A class that receives callbacks on various lifecycle events for this agent.

#### tool\_use\_behavior`class-attribute``instance-attribute`

```
tool_use_behavior: (
    Literal["run_llm_again", "stop_on_first_tool"]
    | StopAtTools
    | ToolsToFinalOutputFunction
) = "run_llm_again"

```

This lets you configure how tool use is handled.
\- "run\_llm\_again": The default behavior. Tools are run, and then the LLM receives the results
and gets to respond.
\- "stop\_on\_first\_tool": The output of the first tool call is used as the final output. This
means that the LLM does not process the result of the tool call.
\- A list of tool names: The agent will stop running if any of the tools in the list are called.
The final output will be the output of the first matching tool call. The LLM does not
process the result of the tool call.
\- A function: If you pass a function, it will be called with the run context and the list of
tool results. It must return a `ToolsToFinalOutputResult`, which determines whether the tool
calls result in a final output.

NOTE: This configuration is specific to FunctionTools. Hosted tools, such as file search,
web search, etc are always processed by the LLM.

#### reset\_tool\_choice`class-attribute``instance-attribute`

```
reset_tool_choice: bool = True

```

Whether to reset the tool choice to the default value after a tool has been called. Defaults
to True. This ensures that the agent doesn't enter an infinite loop of tool usage.

#### name`instance-attribute`

```
name: str

```

The name of the agent.

#### handoff\_description`class-attribute``instance-attribute`

```
handoff_description: str | None = None

```

A description of the agent. This is used when the agent is used as a handoff, so that an
LLM knows what it does and when to invoke it.

#### tools`class-attribute``instance-attribute`

```
tools: list[Tool] = field(default_factory=list)

```

A list of tools that the agent can use.

#### mcp\_servers`class-attribute``instance-attribute`

```
mcp_servers: list[MCPServer] = field(default_factory=list)

```

A list of [Model Context Protocol](https://modelcontextprotocol.io/) servers that
the agent can use. Every time the agent runs, it will include tools from these servers in the
list of available tools.

NOTE: You are expected to manage the lifecycle of these servers. Specifically, you must call
`server.connect()` before passing it to the agent, and `server.cleanup()` when the server is no
longer needed.

#### mcp\_config`class-attribute``instance-attribute`

```
mcp_config: MCPConfig = field(
    default_factory=lambda: MCPConfig()
)

```

Configuration for MCP servers.

#### clone

```
clone(**kwargs: Any) -> Agent[TContext]

```

Make a copy of the agent, with the given arguments changed. For example, you could do:

```
new_agent = agent.clone(instructions="New instructions")

```

Source code in `src/agents/agent.py`

|  |  |
| --- | --- |
| ```224225226227228229230``` | ````md-code__contentdef clone(self, **kwargs: Any) -> Agent[TContext]:    """Make a copy of the agent, with the given arguments changed. For example, you could do:    ```    new_agent = agent.clone(instructions="New instructions")    ```    """    return dataclasses.replace(self, **kwargs)```` |

#### as\_tool

```
as_tool(
    tool_name: str | None,
    tool_description: str | None,
    custom_output_extractor: Callable[\
        [RunResult], Awaitable[str]\
    ]
    | None = None,
) -> Tool

```

Transform this agent into a tool, callable by other agents.

This is different from handoffs in two ways:
1\. In handoffs, the new agent receives the conversation history. In this tool, the new agent
receives generated input.
2\. In handoffs, the new agent takes over the conversation. In this tool, the new agent is
called as a tool, and the conversation is continued by the original agent.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `tool_name` | `str | None` | The name of the tool. If not provided, the agent's name will be used. | _required_ |
| `tool_description` | `str | None` | The description of the tool, which should indicate what it does andwhen to use it. | _required_ |
| `custom_output_extractor` | `Callable[[RunResult], Awaitable[str]] | None` | A function that extracts the output from the agent. If notprovided, the last message from the agent will be used. | `None` |

Source code in `src/agents/agent.py`

|  |  |
| --- | --- |
| ```232233234235236237238239240241242243244245246247248249250251252253254255256257258259260261262263264265266267268269270271``` | ```md-code__contentdef as_tool(    self,    tool_name: str | None,    tool_description: str | None,    custom_output_extractor: Callable[[RunResult], Awaitable[str]] | None = None,) -> Tool:    """Transform this agent into a tool, callable by other agents.    This is different from handoffs in two ways:    1. In handoffs, the new agent receives the conversation history. In this tool, the new agent       receives generated input.    2. In handoffs, the new agent takes over the conversation. In this tool, the new agent is       called as a tool, and the conversation is continued by the original agent.    Args:        tool_name: The name of the tool. If not provided, the agent's name will be used.        tool_description: The description of the tool, which should indicate what it does and            when to use it.        custom_output_extractor: A function that extracts the output from the agent. If not            provided, the last message from the agent will be used.    """    @function_tool(        name_override=tool_name or _transforms.transform_string_function_style(self.name),        description_override=tool_description or "",    )    async def run_agent(context: RunContextWrapper, input: str) -> str:        from .run import Runner        output = await Runner.run(            starting_agent=self,            input=input,            context=context.context,        )        if custom_output_extractor:            return await custom_output_extractor(output)        return ItemHelpers.text_message_outputs(output.new_items)    return run_agent``` |

#### get\_system\_prompt`async`

```
get_system_prompt(
    run_context: RunContextWrapper[TContext],
) -> str | None

```

Get the system prompt for the agent.

Source code in `src/agents/agent.py`

|  |  |
| --- | --- |
| ```273274275276277278279280281282283284285``` | ```md-code__contentasync def get_system_prompt(self, run_context: RunContextWrapper[TContext]) -> str | None:    """Get the system prompt for the agent."""    if isinstance(self.instructions, str):        return self.instructions    elif callable(self.instructions):        if inspect.iscoroutinefunction(self.instructions):            return await cast(Awaitable[str], self.instructions(run_context, self))        else:            return cast(str, self.instructions(run_context, self))    elif self.instructions is not None:        logger.error(f"Instructions must be a string or a function, got {self.instructions}")    return None``` |

#### get\_prompt`async`

```
get_prompt(
    run_context: RunContextWrapper[TContext],
) -> ResponsePromptParam | None

```

Get the prompt for the agent.

Source code in `src/agents/agent.py`

|  |  |
| --- | --- |
| ```287288289290291``` | ```md-code__contentasync def get_prompt(    self, run_context: RunContextWrapper[TContext]) -> ResponsePromptParam | None:    """Get the prompt for the agent."""    return await PromptUtil.to_model_input(self.prompt, run_context, self)``` |

#### get\_mcp\_tools`async`

```
get_mcp_tools(
    run_context: RunContextWrapper[TContext],
) -> list[Tool]

```

Fetches the available tools from the MCP servers.

Source code in `src/agents/agent.py`

|  |  |
| --- | --- |
| ```293294295296297298``` | ```md-code__contentasync def get_mcp_tools(self, run_context: RunContextWrapper[TContext]) -> list[Tool]:    """Fetches the available tools from the MCP servers."""    convert_schemas_to_strict = self.mcp_config.get("convert_schemas_to_strict", False)    return await MCPUtil.get_all_function_tools(        self.mcp_servers, convert_schemas_to_strict, run_context, self    )``` |

#### get\_all\_tools`async`

```
get_all_tools(
    run_context: RunContextWrapper[Any],
) -> list[Tool]

```

All agent tools, including MCP tools and function tools.

Source code in `src/agents/agent.py`

|  |  |
| --- | --- |
| ```300301302303304305306307308309310311312313314315316317318``` | ```md-code__contentasync def get_all_tools(self, run_context: RunContextWrapper[Any]) -> list[Tool]:    """All agent tools, including MCP tools and function tools."""    mcp_tools = await self.get_mcp_tools(run_context)    async def _check_tool_enabled(tool: Tool) -> bool:        if not isinstance(tool, FunctionTool):            return True        attr = tool.is_enabled        if isinstance(attr, bool):            return attr        res = attr(run_context, self)        if inspect.isawaitable(res):            return bool(await res)        return bool(res)    results = await asyncio.gather(*(_check_tool_enabled(t) for t in self.tools))    enabled: list[Tool] = [t for t, ok in zip(self.tools, results) if ok]    return [*mcp_tools, *enabled]``` |