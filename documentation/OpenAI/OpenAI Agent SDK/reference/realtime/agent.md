---
title: `RealtimeAgent`
source: https://openai.github.io/openai-agents-python/ref/realtime/agent/
---

# `RealtimeAgent`

Bases: `AgentBase`, `Generic[TContext]`

A specialized agent instance that is meant to be used within a `RealtimeSession` to build
voice agents. Due to the nature of this agent, some configuration options are not supported
that are supported by regular `Agent` instances. For example:
\- `model` choice is not supported, as all RealtimeAgents will be handled by the same model
within a `RealtimeSession`.
\- `modelSettings` is not supported, as all RealtimeAgents will be handled by the same model
within a `RealtimeSession`.
\- `outputType` is not supported, as RealtimeAgents do not support structured outputs.
\- `toolUseBehavior` is not supported, as all RealtimeAgents will be handled by the same model
within a `RealtimeSession`.
\- `voice` can be configured on an `Agent` level; however, it cannot be changed after the first
agent within a `RealtimeSession` has spoken.

See `AgentBase` for base parameters that are shared with `Agent` s.

Source code in `src/agents/realtime/agent.py`

|  |  |
| --- | --- |
| ```23242526272829303132333435363738394041424344454647484950515253545556575859606162636465666768697071727374757677787980818283848586878889``` | ````md-code__content@dataclassclass RealtimeAgent(AgentBase, Generic[TContext]):    """A specialized agent instance that is meant to be used within a `RealtimeSession` to build    voice agents. Due to the nature of this agent, some configuration options are not supported    that are supported by regular `Agent` instances. For example:    - `model` choice is not supported, as all RealtimeAgents will be handled by the same model      within a `RealtimeSession`.    - `modelSettings` is not supported, as all RealtimeAgents will be handled by the same model      within a `RealtimeSession`.    - `outputType` is not supported, as RealtimeAgents do not support structured outputs.    - `toolUseBehavior` is not supported, as all RealtimeAgents will be handled by the same model      within a `RealtimeSession`.    - `voice` can be configured on an `Agent` level; however, it cannot be changed after the first      agent within a `RealtimeSession` has spoken.    See `AgentBase` for base parameters that are shared with `Agent`s.    """    instructions: (        str | Callable[            [RunContextWrapper[TContext], RealtimeAgent[TContext]],            MaybeAwaitable[str],        ] | None    ) = None    """The instructions for the agent. Will be used as the "system prompt" when this agent is    invoked. Describes what the agent should do, and how it responds.    Can either be a string, or a function that dynamically generates instructions for the agent. If    you provide a function, it will be called with the context and the agent instance. It must    return a string.    """    handoffs: list[RealtimeAgent[Any] | Handoff[TContext, RealtimeAgent[Any]]] = field(        default_factory=list    )    """Handoffs are sub-agents that the agent can delegate to. You can provide a list of handoffs,    and the agent can choose to delegate to them if relevant. Allows for separation of concerns and    modularity.    """    hooks: RealtimeAgentHooks | None = None    """A class that receives callbacks on various lifecycle events for this agent.    """    def clone(self, **kwargs: Any) -> RealtimeAgent[TContext]:        """Make a copy of the agent, with the given arguments changed. For example, you could do:        ```        new_agent = agent.clone(instructions="New instructions")        ```        """        return dataclasses.replace(self, **kwargs)    async def get_system_prompt(self, run_context: RunContextWrapper[TContext]) -> str | None:        """Get the system prompt for the agent."""        if isinstance(self.instructions, str):            return self.instructions        elif callable(self.instructions):            if inspect.iscoroutinefunction(self.instructions):                return await cast(Awaitable[str], self.instructions(run_context, self))            else:                return cast(str, self.instructions(run_context, self))        elif self.instructions is not None:            logger.error(f"Instructions must be a string or a function, got {self.instructions}")        return None```` |

### instructions`class-attribute``instance-attribute`

```
instructions: (
    str
    | Callable[\
        [\
            RunContextWrapper[TContext],\
            RealtimeAgent[TContext],\
        ],\
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

### handoffs`class-attribute``instance-attribute`

```
handoffs: list[\
    RealtimeAgent[Any]\
    | Handoff[TContext, RealtimeAgent[Any]]\
] = field(default_factory=list)

```

Handoffs are sub-agents that the agent can delegate to. You can provide a list of handoffs,
and the agent can choose to delegate to them if relevant. Allows for separation of concerns and
modularity.

### hooks`class-attribute``instance-attribute`

```
hooks: RealtimeAgentHooks | None = None

```

A class that receives callbacks on various lifecycle events for this agent.

### name`instance-attribute`

```
name: str

```

The name of the agent.

### handoff\_description`class-attribute``instance-attribute`

```
handoff_description: str | None = None

```

A description of the agent. This is used when the agent is used as a handoff, so that an
LLM knows what it does and when to invoke it.

### tools`class-attribute``instance-attribute`

```
tools: list[Tool] = field(default_factory=list)

```

A list of tools that the agent can use.

### mcp\_servers`class-attribute``instance-attribute`

```
mcp_servers: list[MCPServer] = field(default_factory=list)

```

A list of [Model Context Protocol](https://modelcontextprotocol.io/) servers that
the agent can use. Every time the agent runs, it will include tools from these servers in the
list of available tools.

NOTE: You are expected to manage the lifecycle of these servers. Specifically, you must call
`server.connect()` before passing it to the agent, and `server.cleanup()` when the server is no
longer needed.

### mcp\_config`class-attribute``instance-attribute`

```
mcp_config: MCPConfig = field(
    default_factory=lambda: MCPConfig()
)

```

Configuration for MCP servers.

### clone

```
clone(**kwargs: Any) -> RealtimeAgent[TContext]

```

Make a copy of the agent, with the given arguments changed. For example, you could do:

```
new_agent = agent.clone(instructions="New instructions")

```

Source code in `src/agents/realtime/agent.py`

|  |  |
| --- | --- |
| ```69707172737475``` | ````md-code__contentdef clone(self, **kwargs: Any) -> RealtimeAgent[TContext]:    """Make a copy of the agent, with the given arguments changed. For example, you could do:    ```    new_agent = agent.clone(instructions="New instructions")    ```    """    return dataclasses.replace(self, **kwargs)```` |

### get\_system\_prompt`async`

```
get_system_prompt(
    run_context: RunContextWrapper[TContext],
) -> str | None

```

Get the system prompt for the agent.

Source code in `src/agents/realtime/agent.py`

|  |  |
| --- | --- |
| ```77787980818283848586878889``` | ```md-code__contentasync def get_system_prompt(self, run_context: RunContextWrapper[TContext]) -> str | None:    """Get the system prompt for the agent."""    if isinstance(self.instructions, str):        return self.instructions    elif callable(self.instructions):        if inspect.iscoroutinefunction(self.instructions):            return await cast(Awaitable[str], self.instructions(run_context, self))        else:            return cast(str, self.instructions(run_context, self))    elif self.instructions is not None:        logger.error(f"Instructions must be a string or a function, got {self.instructions}")    return None``` |

### get\_mcp\_tools`async`

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

### get\_all\_tools`async`

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