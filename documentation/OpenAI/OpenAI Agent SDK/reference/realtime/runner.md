---
title: `RealtimeRunner`
source: https://openai.github.io/openai-agents-python/ref/realtime/runner/
---

# `RealtimeRunner`

A `RealtimeRunner` is the equivalent of `Runner` for realtime agents. It automatically
handles multiple turns by maintaining a persistent connection with the underlying model
layer.

The session manages the local history copy, executes tools, runs guardrails and facilitates
handoffs between agents.

Since this code runs on your server, it uses WebSockets by default. You can optionally create
your own custom model layer by implementing the `RealtimeModel` interface.

Source code in `src/agents/realtime/runner.py`

|  |  |
| --- | --- |
| ```1819202122232425262728293031323334353637383940414243444546474849505152535455565758596061626364656667686970717273747576``` | ````md-code__contentclass RealtimeRunner:    """A `RealtimeRunner` is the equivalent of `Runner` for realtime agents. It automatically    handles multiple turns by maintaining a persistent connection with the underlying model    layer.    The session manages the local history copy, executes tools, runs guardrails and facilitates    handoffs between agents.    Since this code runs on your server, it uses WebSockets by default. You can optionally create    your own custom model layer by implementing the `RealtimeModel` interface.    """    def __init__(        self,        starting_agent: RealtimeAgent,        *,        model: RealtimeModel | None = None,        config: RealtimeRunConfig | None = None,    ) -> None:        """Initialize the realtime runner.        Args:            starting_agent: The agent to start the session with.            context: The context to use for the session.            model: The model to use. If not provided, will use a default OpenAI realtime model.            config: Override parameters to use for the entire run.        """        self._starting_agent = starting_agent        self._config = config        self._model = model or OpenAIRealtimeWebSocketModel()    async def run(        self, *, context: TContext | None = None, model_config: RealtimeModelConfig | None = None    ) -> RealtimeSession:        """Start and returns a realtime session.        Returns:            RealtimeSession: A session object that allows bidirectional communication with the            realtime model.        Example:            ```python            runner = RealtimeRunner(agent)            async with await runner.run() as session:                await session.send_message("Hello")                async for event in session:                    print(event)            ```        """        # Create and return the connection        session = RealtimeSession(            model=self._model,            agent=self._starting_agent,            context=context,            model_config=model_config,            run_config=self._config,        )        return session```` |

### \_\_init\_\_

```
__init__(
    starting_agent: RealtimeAgent,
    *,
    model: RealtimeModel | None = None,
    config: RealtimeRunConfig | None = None,
) -> None

```

Initialize the realtime runner.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `starting_agent` | `RealtimeAgent` | The agent to start the session with. | _required_ |
| `context` |  | The context to use for the session. | _required_ |
| `model` | `RealtimeModel | None` | The model to use. If not provided, will use a default OpenAI realtime model. | `None` |
| `config` | `RealtimeRunConfig | None` | Override parameters to use for the entire run. | `None` |

Source code in `src/agents/realtime/runner.py`

|  |  |
| --- | --- |
| ```303132333435363738394041424344454647``` | ```md-code__contentdef __init__(    self,    starting_agent: RealtimeAgent,    *,    model: RealtimeModel | None = None,    config: RealtimeRunConfig | None = None,) -> None:    """Initialize the realtime runner.    Args:        starting_agent: The agent to start the session with.        context: The context to use for the session.        model: The model to use. If not provided, will use a default OpenAI realtime model.        config: Override parameters to use for the entire run.    """    self._starting_agent = starting_agent    self._config = config    self._model = model or OpenAIRealtimeWebSocketModel()``` |

### run`async`

```
run(
    *,
    context: TContext | None = None,
    model_config: RealtimeModelConfig | None = None,
) -> RealtimeSession

```

Start and returns a realtime session.

Returns:

| Name | Type | Description |
| --- | --- | --- |
| `RealtimeSession` | `RealtimeSession` | A session object that allows bidirectional communication with the |
|  | `RealtimeSession` | realtime model. |

Example

```
runner = RealtimeRunner(agent)
async with await runner.run() as session:
    await session.send_message("Hello")
    async for event in session:
        print(event)

```

Source code in `src/agents/realtime/runner.py`

|  |  |
| --- | --- |
| ```49505152535455565758596061626364656667686970717273747576``` | ````md-code__contentasync def run(    self, *, context: TContext | None = None, model_config: RealtimeModelConfig | None = None) -> RealtimeSession:    """Start and returns a realtime session.    Returns:        RealtimeSession: A session object that allows bidirectional communication with the        realtime model.    Example:        ```python        runner = RealtimeRunner(agent)        async with await runner.run() as session:            await session.send_message("Hello")            async for event in session:                print(event)        ```    """    # Create and return the connection    session = RealtimeSession(        model=self._model,        agent=self._starting_agent,        context=context,        model_config=model_config,        run_config=self._config,    )    return session```` |