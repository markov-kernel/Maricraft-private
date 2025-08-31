---
title: `Runner`
source: https://openai.github.io/openai-agents-python/ref/run/
---

# `Runner`

### Runner

Source code in `src/agents/run.py`

|  |  |
| --- | --- |
| ```165166167168169170171172173174175176177178179180181182183184185186187188189190191192193194195196197198199200201202203204205206207208209210211212213214215216217218219220221222223224225226227228229230231232233234235236237238239240241242243244245246247248249250251252253254255256257258259260261262263264265266267268269270271272273274275276277278279280281282283284285286287288289290291292293294295296297298299300301302303304305306307308309310311312313314315316317318319``` | ```md-code__contentclass Runner:    @classmethod    async def run(        cls,        starting_agent: Agent[TContext],        input: str | list[TResponseInputItem],        *,        context: TContext | None = None,        max_turns: int = DEFAULT_MAX_TURNS,        hooks: RunHooks[TContext] | None = None,        run_config: RunConfig | None = None,        previous_response_id: str | None = None,        session: Session | None = None,    ) -> RunResult:        """Run a workflow starting at the given agent. The agent will run in a loop until a final        output is generated. The loop runs like so:        1. The agent is invoked with the given input.        2. If there is a final output (i.e. the agent produces something of type            `agent.output_type`, the loop terminates.        3. If there's a handoff, we run the loop again, with the new agent.        4. Else, we run tool calls (if any), and re-run the loop.        In two cases, the agent may raise an exception:        1. If the max_turns is exceeded, a MaxTurnsExceeded exception is raised.        2. If a guardrail tripwire is triggered, a GuardrailTripwireTriggered exception is raised.        Note that only the first agent's input guardrails are run.        Args:            starting_agent: The starting agent to run.            input: The initial input to the agent. You can pass a single string for a user message,                or a list of input items.            context: The context to run the agent with.            max_turns: The maximum number of turns to run the agent for. A turn is defined as one                AI invocation (including any tool calls that might occur).            hooks: An object that receives callbacks on various lifecycle events.            run_config: Global settings for the entire agent run.            previous_response_id: The ID of the previous response, if using OpenAI models via the                Responses API, this allows you to skip passing in input from the previous turn.        Returns:            A run result containing all the inputs, guardrail results and the output of the last            agent. Agents may perform handoffs, so we don't know the specific type of the output.        """        runner = DEFAULT_AGENT_RUNNER        return await runner.run(            starting_agent,            input,            context=context,            max_turns=max_turns,            hooks=hooks,            run_config=run_config,            previous_response_id=previous_response_id,            session=session,        )    @classmethod    def run_sync(        cls,        starting_agent: Agent[TContext],        input: str | list[TResponseInputItem],        *,        context: TContext | None = None,        max_turns: int = DEFAULT_MAX_TURNS,        hooks: RunHooks[TContext] | None = None,        run_config: RunConfig | None = None,        previous_response_id: str | None = None,        session: Session | None = None,    ) -> RunResult:        """Run a workflow synchronously, starting at the given agent. Note that this just wraps the        `run` method, so it will not work if there's already an event loop (e.g. inside an async        function, or in a Jupyter notebook or async context like FastAPI). For those cases, use        the `run` method instead.        The agent will run in a loop until a final output is generated. The loop runs like so:        1. The agent is invoked with the given input.        2. If there is a final output (i.e. the agent produces something of type            `agent.output_type`, the loop terminates.        3. If there's a handoff, we run the loop again, with the new agent.        4. Else, we run tool calls (if any), and re-run the loop.        In two cases, the agent may raise an exception:        1. If the max_turns is exceeded, a MaxTurnsExceeded exception is raised.        2. If a guardrail tripwire is triggered, a GuardrailTripwireTriggered exception is raised.        Note that only the first agent's input guardrails are run.        Args:            starting_agent: The starting agent to run.            input: The initial input to the agent. You can pass a single string for a user message,                or a list of input items.            context: The context to run the agent with.            max_turns: The maximum number of turns to run the agent for. A turn is defined as one                AI invocation (including any tool calls that might occur).            hooks: An object that receives callbacks on various lifecycle events.            run_config: Global settings for the entire agent run.            previous_response_id: The ID of the previous response, if using OpenAI models via the                Responses API, this allows you to skip passing in input from the previous turn.        Returns:            A run result containing all the inputs, guardrail results and the output of the last            agent. Agents may perform handoffs, so we don't know the specific type of the output.        """        runner = DEFAULT_AGENT_RUNNER        return runner.run_sync(            starting_agent,            input,            context=context,            max_turns=max_turns,            hooks=hooks,            run_config=run_config,            previous_response_id=previous_response_id,            session=session,        )    @classmethod    def run_streamed(        cls,        starting_agent: Agent[TContext],        input: str | list[TResponseInputItem],        context: TContext | None = None,        max_turns: int = DEFAULT_MAX_TURNS,        hooks: RunHooks[TContext] | None = None,        run_config: RunConfig | None = None,        previous_response_id: str | None = None,        session: Session | None = None,    ) -> RunResultStreaming:        """Run a workflow starting at the given agent in streaming mode. The returned result object        contains a method you can use to stream semantic events as they are generated.        The agent will run in a loop until a final output is generated. The loop runs like so:        1. The agent is invoked with the given input.        2. If there is a final output (i.e. the agent produces something of type            `agent.output_type`, the loop terminates.        3. If there's a handoff, we run the loop again, with the new agent.        4. Else, we run tool calls (if any), and re-run the loop.        In two cases, the agent may raise an exception:        1. If the max_turns is exceeded, a MaxTurnsExceeded exception is raised.        2. If a guardrail tripwire is triggered, a GuardrailTripwireTriggered exception is raised.        Note that only the first agent's input guardrails are run.        Args:            starting_agent: The starting agent to run.            input: The initial input to the agent. You can pass a single string for a user message,                or a list of input items.            context: The context to run the agent with.            max_turns: The maximum number of turns to run the agent for. A turn is defined as one                AI invocation (including any tool calls that might occur).            hooks: An object that receives callbacks on various lifecycle events.            run_config: Global settings for the entire agent run.            previous_response_id: The ID of the previous response, if using OpenAI models via the                Responses API, this allows you to skip passing in input from the previous turn.        Returns:            A result object that contains data about the run, as well as a method to stream events.        """        runner = DEFAULT_AGENT_RUNNER        return runner.run_streamed(            starting_agent,            input,            context=context,            max_turns=max_turns,            hooks=hooks,            run_config=run_config,            previous_response_id=previous_response_id,            session=session,        )``` |

#### run`async``classmethod`

```
run(
    starting_agent: Agent[TContext],
    input: str | list[TResponseInputItem],
    *,
    context: TContext | None = None,
    max_turns: int = DEFAULT_MAX_TURNS,
    hooks: RunHooks[TContext] | None = None,
    run_config: RunConfig | None = None,
    previous_response_id: str | None = None,
    session: Session | None = None,
) -> RunResult

```

Run a workflow starting at the given agent. The agent will run in a loop until a final
output is generated. The loop runs like so:
1\. The agent is invoked with the given input.
2\. If there is a final output (i.e. the agent produces something of type
`agent.output_type`, the loop terminates.
3\. If there's a handoff, we run the loop again, with the new agent.
4\. Else, we run tool calls (if any), and re-run the loop.
In two cases, the agent may raise an exception:
1\. If the max\_turns is exceeded, a MaxTurnsExceeded exception is raised.
2\. If a guardrail tripwire is triggered, a GuardrailTripwireTriggered exception is raised.
Note that only the first agent's input guardrails are run.
Args:
starting\_agent: The starting agent to run.
input: The initial input to the agent. You can pass a single string for a user message,
or a list of input items.
context: The context to run the agent with.
max\_turns: The maximum number of turns to run the agent for. A turn is defined as one
AI invocation (including any tool calls that might occur).
hooks: An object that receives callbacks on various lifecycle events.
run\_config: Global settings for the entire agent run.
previous\_response\_id: The ID of the previous response, if using OpenAI models via the
Responses API, this allows you to skip passing in input from the previous turn.
Returns:
A run result containing all the inputs, guardrail results and the output of the last
agent. Agents may perform handoffs, so we don't know the specific type of the output.

Source code in `src/agents/run.py`

|  |  |
| --- | --- |
| ```166167168169170171172173174175176177178179180181182183184185186187188189190191192193194195196197198199200201202203204205206207208209210211212213214215``` | ```md-code__content@classmethodasync def run(    cls,    starting_agent: Agent[TContext],    input: str | list[TResponseInputItem],    *,    context: TContext | None = None,    max_turns: int = DEFAULT_MAX_TURNS,    hooks: RunHooks[TContext] | None = None,    run_config: RunConfig | None = None,    previous_response_id: str | None = None,    session: Session | None = None,) -> RunResult:    """Run a workflow starting at the given agent. The agent will run in a loop until a final    output is generated. The loop runs like so:    1. The agent is invoked with the given input.    2. If there is a final output (i.e. the agent produces something of type        `agent.output_type`, the loop terminates.    3. If there's a handoff, we run the loop again, with the new agent.    4. Else, we run tool calls (if any), and re-run the loop.    In two cases, the agent may raise an exception:    1. If the max_turns is exceeded, a MaxTurnsExceeded exception is raised.    2. If a guardrail tripwire is triggered, a GuardrailTripwireTriggered exception is raised.    Note that only the first agent's input guardrails are run.    Args:        starting_agent: The starting agent to run.        input: The initial input to the agent. You can pass a single string for a user message,            or a list of input items.        context: The context to run the agent with.        max_turns: The maximum number of turns to run the agent for. A turn is defined as one            AI invocation (including any tool calls that might occur).        hooks: An object that receives callbacks on various lifecycle events.        run_config: Global settings for the entire agent run.        previous_response_id: The ID of the previous response, if using OpenAI models via the            Responses API, this allows you to skip passing in input from the previous turn.    Returns:        A run result containing all the inputs, guardrail results and the output of the last        agent. Agents may perform handoffs, so we don't know the specific type of the output.    """    runner = DEFAULT_AGENT_RUNNER    return await runner.run(        starting_agent,        input,        context=context,        max_turns=max_turns,        hooks=hooks,        run_config=run_config,        previous_response_id=previous_response_id,        session=session,    )``` |

#### run\_sync`classmethod`

```
run_sync(
    starting_agent: Agent[TContext],
    input: str | list[TResponseInputItem],
    *,
    context: TContext | None = None,
    max_turns: int = DEFAULT_MAX_TURNS,
    hooks: RunHooks[TContext] | None = None,
    run_config: RunConfig | None = None,
    previous_response_id: str | None = None,
    session: Session | None = None,
) -> RunResult

```

Run a workflow synchronously, starting at the given agent. Note that this just wraps the
`run` method, so it will not work if there's already an event loop (e.g. inside an async
function, or in a Jupyter notebook or async context like FastAPI). For those cases, use
the `run` method instead.
The agent will run in a loop until a final output is generated. The loop runs like so:
1\. The agent is invoked with the given input.
2\. If there is a final output (i.e. the agent produces something of type
`agent.output_type`, the loop terminates.
3\. If there's a handoff, we run the loop again, with the new agent.
4\. Else, we run tool calls (if any), and re-run the loop.
In two cases, the agent may raise an exception:
1\. If the max\_turns is exceeded, a MaxTurnsExceeded exception is raised.
2\. If a guardrail tripwire is triggered, a GuardrailTripwireTriggered exception is raised.
Note that only the first agent's input guardrails are run.
Args:
starting\_agent: The starting agent to run.
input: The initial input to the agent. You can pass a single string for a user message,
or a list of input items.
context: The context to run the agent with.
max\_turns: The maximum number of turns to run the agent for. A turn is defined as one
AI invocation (including any tool calls that might occur).
hooks: An object that receives callbacks on various lifecycle events.
run\_config: Global settings for the entire agent run.
previous\_response\_id: The ID of the previous response, if using OpenAI models via the
Responses API, this allows you to skip passing in input from the previous turn.
Returns:
A run result containing all the inputs, guardrail results and the output of the last
agent. Agents may perform handoffs, so we don't know the specific type of the output.

Source code in `src/agents/run.py`

|  |  |
| --- | --- |
| ```217218219220221222223224225226227228229230231232233234235236237238239240241242243244245246247248249250251252253254255256257258259260261262263264265266267268269``` | ```md-code__content@classmethoddef run_sync(    cls,    starting_agent: Agent[TContext],    input: str | list[TResponseInputItem],    *,    context: TContext | None = None,    max_turns: int = DEFAULT_MAX_TURNS,    hooks: RunHooks[TContext] | None = None,    run_config: RunConfig | None = None,    previous_response_id: str | None = None,    session: Session | None = None,) -> RunResult:    """Run a workflow synchronously, starting at the given agent. Note that this just wraps the    `run` method, so it will not work if there's already an event loop (e.g. inside an async    function, or in a Jupyter notebook or async context like FastAPI). For those cases, use    the `run` method instead.    The agent will run in a loop until a final output is generated. The loop runs like so:    1. The agent is invoked with the given input.    2. If there is a final output (i.e. the agent produces something of type        `agent.output_type`, the loop terminates.    3. If there's a handoff, we run the loop again, with the new agent.    4. Else, we run tool calls (if any), and re-run the loop.    In two cases, the agent may raise an exception:    1. If the max_turns is exceeded, a MaxTurnsExceeded exception is raised.    2. If a guardrail tripwire is triggered, a GuardrailTripwireTriggered exception is raised.    Note that only the first agent's input guardrails are run.    Args:        starting_agent: The starting agent to run.        input: The initial input to the agent. You can pass a single string for a user message,            or a list of input items.        context: The context to run the agent with.        max_turns: The maximum number of turns to run the agent for. A turn is defined as one            AI invocation (including any tool calls that might occur).        hooks: An object that receives callbacks on various lifecycle events.        run_config: Global settings for the entire agent run.        previous_response_id: The ID of the previous response, if using OpenAI models via the            Responses API, this allows you to skip passing in input from the previous turn.    Returns:        A run result containing all the inputs, guardrail results and the output of the last        agent. Agents may perform handoffs, so we don't know the specific type of the output.    """    runner = DEFAULT_AGENT_RUNNER    return runner.run_sync(        starting_agent,        input,        context=context,        max_turns=max_turns,        hooks=hooks,        run_config=run_config,        previous_response_id=previous_response_id,        session=session,    )``` |

#### run\_streamed`classmethod`

```
run_streamed(
    starting_agent: Agent[TContext],
    input: str | list[TResponseInputItem],
    context: TContext | None = None,
    max_turns: int = DEFAULT_MAX_TURNS,
    hooks: RunHooks[TContext] | None = None,
    run_config: RunConfig | None = None,
    previous_response_id: str | None = None,
    session: Session | None = None,
) -> RunResultStreaming

```

Run a workflow starting at the given agent in streaming mode. The returned result object
contains a method you can use to stream semantic events as they are generated.
The agent will run in a loop until a final output is generated. The loop runs like so:
1\. The agent is invoked with the given input.
2\. If there is a final output (i.e. the agent produces something of type
`agent.output_type`, the loop terminates.
3\. If there's a handoff, we run the loop again, with the new agent.
4\. Else, we run tool calls (if any), and re-run the loop.
In two cases, the agent may raise an exception:
1\. If the max\_turns is exceeded, a MaxTurnsExceeded exception is raised.
2\. If a guardrail tripwire is triggered, a GuardrailTripwireTriggered exception is raised.
Note that only the first agent's input guardrails are run.
Args:
starting\_agent: The starting agent to run.
input: The initial input to the agent. You can pass a single string for a user message,
or a list of input items.
context: The context to run the agent with.
max\_turns: The maximum number of turns to run the agent for. A turn is defined as one
AI invocation (including any tool calls that might occur).
hooks: An object that receives callbacks on various lifecycle events.
run\_config: Global settings for the entire agent run.
previous\_response\_id: The ID of the previous response, if using OpenAI models via the
Responses API, this allows you to skip passing in input from the previous turn.
Returns:
A result object that contains data about the run, as well as a method to stream events.

Source code in `src/agents/run.py`

|  |  |
| --- | --- |
| ```271272273274275276277278279280281282283284285286287288289290291292293294295296297298299300301302303304305306307308309310311312313314315316317318319``` | ```md-code__content@classmethoddef run_streamed(    cls,    starting_agent: Agent[TContext],    input: str | list[TResponseInputItem],    context: TContext | None = None,    max_turns: int = DEFAULT_MAX_TURNS,    hooks: RunHooks[TContext] | None = None,    run_config: RunConfig | None = None,    previous_response_id: str | None = None,    session: Session | None = None,) -> RunResultStreaming:    """Run a workflow starting at the given agent in streaming mode. The returned result object    contains a method you can use to stream semantic events as they are generated.    The agent will run in a loop until a final output is generated. The loop runs like so:    1. The agent is invoked with the given input.    2. If there is a final output (i.e. the agent produces something of type        `agent.output_type`, the loop terminates.    3. If there's a handoff, we run the loop again, with the new agent.    4. Else, we run tool calls (if any), and re-run the loop.    In two cases, the agent may raise an exception:    1. If the max_turns is exceeded, a MaxTurnsExceeded exception is raised.    2. If a guardrail tripwire is triggered, a GuardrailTripwireTriggered exception is raised.    Note that only the first agent's input guardrails are run.    Args:        starting_agent: The starting agent to run.        input: The initial input to the agent. You can pass a single string for a user message,            or a list of input items.        context: The context to run the agent with.        max_turns: The maximum number of turns to run the agent for. A turn is defined as one            AI invocation (including any tool calls that might occur).        hooks: An object that receives callbacks on various lifecycle events.        run_config: Global settings for the entire agent run.        previous_response_id: The ID of the previous response, if using OpenAI models via the            Responses API, this allows you to skip passing in input from the previous turn.    Returns:        A result object that contains data about the run, as well as a method to stream events.    """    runner = DEFAULT_AGENT_RUNNER    return runner.run_streamed(        starting_agent,        input,        context=context,        max_turns=max_turns,        hooks=hooks,        run_config=run_config,        previous_response_id=previous_response_id,        session=session,    )``` |

### RunConfig`dataclass`

Configures settings for the entire agent run.

Source code in `src/agents/run.py`

|  |  |
| --- | --- |
| ``` 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99100101102103104105106107108109110111112113114115116117118119120121122123124125126127128129130131132133134135136137138139140``` | ```md-code__content@dataclassclass RunConfig:    """Configures settings for the entire agent run."""    model: str | Model | None = None    """The model to use for the entire agent run. If set, will override the model set on every    agent. The model_provider passed in below must be able to resolve this model name.    """    model_provider: ModelProvider = field(default_factory=MultiProvider)    """The model provider to use when looking up string model names. Defaults to OpenAI."""    model_settings: ModelSettings | None = None    """Configure global model settings. Any non-null values will override the agent-specific model    settings.    """    handoff_input_filter: HandoffInputFilter | None = None    """A global input filter to apply to all handoffs. If `Handoff.input_filter` is set, then that    will take precedence. The input filter allows you to edit the inputs that are sent to the new    agent. See the documentation in `Handoff.input_filter` for more details.    """    input_guardrails: list[InputGuardrail[Any]] | None = None    """A list of input guardrails to run on the initial run input."""    output_guardrails: list[OutputGuardrail[Any]] | None = None    """A list of output guardrails to run on the final output of the run."""    tracing_disabled: bool = False    """Whether tracing is disabled for the agent run. If disabled, we will not trace the agent run.    """    trace_include_sensitive_data: bool = True    """Whether we include potentially sensitive data (for example: inputs/outputs of tool calls or    LLM generations) in traces. If False, we'll still create spans for these events, but the    sensitive data will not be included.    """    workflow_name: str = "Agent workflow"    """The name of the run, used for tracing. Should be a logical name for the run, like    "Code generation workflow" or "Customer support agent".    """    trace_id: str | None = None    """A custom trace ID to use for tracing. If not provided, we will generate a new trace ID."""    group_id: str | None = None    """    A grouping identifier to use for tracing, to link multiple traces from the same conversation    or process. For example, you might use a chat thread ID.    """    trace_metadata: dict[str, Any] | None = None    """    An optional dictionary of additional metadata to include with the trace.    """``` |

#### model`class-attribute``instance-attribute`

```
model: str | Model | None = None

```

The model to use for the entire agent run. If set, will override the model set on every
agent. The model\_provider passed in below must be able to resolve this model name.

#### model\_provider`class-attribute``instance-attribute`

```
model_provider: ModelProvider = field(
    default_factory=MultiProvider
)

```

The model provider to use when looking up string model names. Defaults to OpenAI.

#### model\_settings`class-attribute``instance-attribute`

```
model_settings: ModelSettings | None = None

```

Configure global model settings. Any non-null values will override the agent-specific model
settings.

#### handoff\_input\_filter`class-attribute``instance-attribute`

```
handoff_input_filter: HandoffInputFilter | None = None

```

A global input filter to apply to all handoffs. If `Handoff.input_filter` is set, then that
will take precedence. The input filter allows you to edit the inputs that are sent to the new
agent. See the documentation in `Handoff.input_filter` for more details.

#### input\_guardrails`class-attribute``instance-attribute`

```
input_guardrails: list[InputGuardrail[Any]] | None = None

```

A list of input guardrails to run on the initial run input.

#### output\_guardrails`class-attribute``instance-attribute`

```
output_guardrails: list[OutputGuardrail[Any]] | None = None

```

A list of output guardrails to run on the final output of the run.

#### tracing\_disabled`class-attribute``instance-attribute`

```
tracing_disabled: bool = False

```

Whether tracing is disabled for the agent run. If disabled, we will not trace the agent run.

#### trace\_include\_sensitive\_data`class-attribute``instance-attribute`

```
trace_include_sensitive_data: bool = True

```

Whether we include potentially sensitive data (for example: inputs/outputs of tool calls or
LLM generations) in traces. If False, we'll still create spans for these events, but the
sensitive data will not be included.

#### workflow\_name`class-attribute``instance-attribute`

```
workflow_name: str = 'Agent workflow'

```

The name of the run, used for tracing. Should be a logical name for the run, like
"Code generation workflow" or "Customer support agent".

#### trace\_id`class-attribute``instance-attribute`

```
trace_id: str | None = None

```

A custom trace ID to use for tracing. If not provided, we will generate a new trace ID.

#### group\_id`class-attribute``instance-attribute`

```
group_id: str | None = None

```

A grouping identifier to use for tracing, to link multiple traces from the same conversation
or process. For example, you might use a chat thread ID.

#### trace\_metadata`class-attribute``instance-attribute`

```
trace_metadata: dict[str, Any] | None = None

```

An optional dictionary of additional metadata to include with the trace.