---
title: `Creating traces/spans`
source: https://openai.github.io/openai-agents-python/ref/tracing/create/
---

# `Creating traces/spans`

### trace

```
trace(
    workflow_name: str,
    trace_id: str | None = None,
    group_id: str | None = None,
    metadata: dict[str, Any] | None = None,
    disabled: bool = False,
) -> Trace

```

Create a new trace. The trace will not be started automatically; you should either use
it as a context manager ( `with trace(...):`) or call `trace.start()` \+ `trace.finish()`
manually.

In addition to the workflow name and optional grouping identifier, you can provide
an arbitrary metadata dictionary to attach additional user-defined information to
the trace.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `workflow_name` | `str` | The name of the logical app or workflow. For example, you might provide"code\_bot" for a coding agent, or "customer\_support\_agent" for a customer support agent. | _required_ |
| `trace_id` | `str | None` | The ID of the trace. Optional. If not provided, we will generate an ID. Werecommend using `util.gen_trace_id()` to generate a trace ID, to guarantee that IDs arecorrectly formatted. | `None` |
| `group_id` | `str | None` | Optional grouping identifier to link multiple traces from the same conversationor process. For instance, you might use a chat thread ID. | `None` |
| `metadata` | `dict[str, Any] | None` | Optional dictionary of additional metadata to attach to the trace. | `None` |
| `disabled` | `bool` | If True, we will return a Trace but the Trace will not be recorded. This willnot be checked if there's an existing trace and `even_if_trace_running` is True. | `False` |

Returns:

| Type | Description |
| --- | --- |
| `Trace` | The newly created trace object. |

Source code in `src/agents/tracing/create.py`

|  |  |
| --- | --- |
| ```2829303132333435363738394041424344454647484950515253545556575859606162636465666768697071``` | ```md-code__contentdef trace(    workflow_name: str,    trace_id: str | None = None,    group_id: str | None = None,    metadata: dict[str, Any] | None = None,    disabled: bool = False,) -> Trace:    """    Create a new trace. The trace will not be started automatically; you should either use    it as a context manager (`with trace(...):`) or call `trace.start()` + `trace.finish()`    manually.    In addition to the workflow name and optional grouping identifier, you can provide    an arbitrary metadata dictionary to attach additional user-defined information to    the trace.    Args:        workflow_name: The name of the logical app or workflow. For example, you might provide            "code_bot" for a coding agent, or "customer_support_agent" for a customer support agent.        trace_id: The ID of the trace. Optional. If not provided, we will generate an ID. We            recommend using `util.gen_trace_id()` to generate a trace ID, to guarantee that IDs are            correctly formatted.        group_id: Optional grouping identifier to link multiple traces from the same conversation            or process. For instance, you might use a chat thread ID.        metadata: Optional dictionary of additional metadata to attach to the trace.        disabled: If True, we will return a Trace but the Trace will not be recorded. This will            not be checked if there's an existing trace and `even_if_trace_running` is True.    Returns:        The newly created trace object.    """    current_trace = get_trace_provider().get_current_trace()    if current_trace:        logger.warning(            "Trace already exists. Creating a new trace, but this is probably a mistake."        )    return get_trace_provider().create_trace(        name=workflow_name,        trace_id=trace_id,        group_id=group_id,        metadata=metadata,        disabled=disabled,    )``` |

### get\_current\_trace

```
get_current_trace() -> Trace | None

```

Returns the currently active trace, if present.

Source code in `src/agents/tracing/create.py`

|  |  |
| --- | --- |
| ```747576``` | ```md-code__contentdef get_current_trace() -> Trace | None:    """Returns the currently active trace, if present."""    return get_trace_provider().get_current_trace()``` |

### get\_current\_span

```
get_current_span() -> Span[Any] | None

```

Returns the currently active span, if present.

Source code in `src/agents/tracing/create.py`

|  |  |
| --- | --- |
| ```798081``` | ```md-code__contentdef get_current_span() -> Span[Any] | None:    """Returns the currently active span, if present."""    return get_trace_provider().get_current_span()``` |

### agent\_span

```
agent_span(
    name: str,
    handoffs: list[str] | None = None,
    tools: list[str] | None = None,
    output_type: str | None = None,
    span_id: str | None = None,
    parent: Trace | Span[Any] | None = None,
    disabled: bool = False,
) -> Span[AgentSpanData]

```

Create a new agent span. The span will not be started automatically, you should either do
`with agent_span() ...` or call `span.start()` \+ `span.finish()` manually.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `name` | `str` | The name of the agent. | _required_ |
| `handoffs` | `list[str] | None` | Optional list of agent names to which this agent could hand off control. | `None` |
| `tools` | `list[str] | None` | Optional list of tool names available to this agent. | `None` |
| `output_type` | `str | None` | Optional name of the output type produced by the agent. | `None` |
| `span_id` | `str | None` | The ID of the span. Optional. If not provided, we will generate an ID. Werecommend using `util.gen_span_id()` to generate a span ID, to guarantee that IDs arecorrectly formatted. | `None` |
| `parent` | `Trace | Span[Any] | None` | The parent span or trace. If not provided, we will automatically use the currenttrace/span as the parent. | `None` |
| `disabled` | `bool` | If True, we will return a Span but the Span will not be recorded. | `False` |

Returns:

| Type | Description |
| --- | --- |
| `Span[AgentSpanData]` | The newly created agent span. |

Source code in `src/agents/tracing/create.py`

|  |  |
| --- | --- |
| ``` 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99100101102103104105106107108109110111112113114115116``` | ```md-code__contentdef agent_span(    name: str,    handoffs: list[str] | None = None,    tools: list[str] | None = None,    output_type: str | None = None,    span_id: str | None = None,    parent: Trace | Span[Any] | None = None,    disabled: bool = False,) -> Span[AgentSpanData]:    """Create a new agent span. The span will not be started automatically, you should either do    `with agent_span() ...` or call `span.start()` + `span.finish()` manually.    Args:        name: The name of the agent.        handoffs: Optional list of agent names to which this agent could hand off control.        tools: Optional list of tool names available to this agent.        output_type: Optional name of the output type produced by the agent.        span_id: The ID of the span. Optional. If not provided, we will generate an ID. We            recommend using `util.gen_span_id()` to generate a span ID, to guarantee that IDs are            correctly formatted.        parent: The parent span or trace. If not provided, we will automatically use the current            trace/span as the parent.        disabled: If True, we will return a Span but the Span will not be recorded.    Returns:        The newly created agent span.    """    return get_trace_provider().create_span(        span_data=AgentSpanData(name=name, handoffs=handoffs, tools=tools, output_type=output_type),        span_id=span_id,        parent=parent,        disabled=disabled,    )``` |

### function\_span

```
function_span(
    name: str,
    input: str | None = None,
    output: str | None = None,
    span_id: str | None = None,
    parent: Trace | Span[Any] | None = None,
    disabled: bool = False,
) -> Span[FunctionSpanData]

```

Create a new function span. The span will not be started automatically, you should either do
`with function_span() ...` or call `span.start()` \+ `span.finish()` manually.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `name` | `str` | The name of the function. | _required_ |
| `input` | `str | None` | The input to the function. | `None` |
| `output` | `str | None` | The output of the function. | `None` |
| `span_id` | `str | None` | The ID of the span. Optional. If not provided, we will generate an ID. Werecommend using `util.gen_span_id()` to generate a span ID, to guarantee that IDs arecorrectly formatted. | `None` |
| `parent` | `Trace | Span[Any] | None` | The parent span or trace. If not provided, we will automatically use the currenttrace/span as the parent. | `None` |
| `disabled` | `bool` | If True, we will return a Span but the Span will not be recorded. | `False` |

Returns:

| Type | Description |
| --- | --- |
| `Span[FunctionSpanData]` | The newly created function span. |

Source code in `src/agents/tracing/create.py`

|  |  |
| --- | --- |
| ```119120121122123124125126127128129130131132133134135136137138139140141142143144145146147148149``` | ```md-code__contentdef function_span(    name: str,    input: str | None = None,    output: str | None = None,    span_id: str | None = None,    parent: Trace | Span[Any] | None = None,    disabled: bool = False,) -> Span[FunctionSpanData]:    """Create a new function span. The span will not be started automatically, you should either do    `with function_span() ...` or call `span.start()` + `span.finish()` manually.    Args:        name: The name of the function.        input: The input to the function.        output: The output of the function.        span_id: The ID of the span. Optional. If not provided, we will generate an ID. We            recommend using `util.gen_span_id()` to generate a span ID, to guarantee that IDs are            correctly formatted.        parent: The parent span or trace. If not provided, we will automatically use the current            trace/span as the parent.        disabled: If True, we will return a Span but the Span will not be recorded.    Returns:        The newly created function span.    """    return get_trace_provider().create_span(        span_data=FunctionSpanData(name=name, input=input, output=output),        span_id=span_id,        parent=parent,        disabled=disabled,    )``` |

### generation\_span

```
generation_span(
    input: Sequence[Mapping[str, Any]] | None = None,
    output: Sequence[Mapping[str, Any]] | None = None,
    model: str | None = None,
    model_config: Mapping[str, Any] | None = None,
    usage: dict[str, Any] | None = None,
    span_id: str | None = None,
    parent: Trace | Span[Any] | None = None,
    disabled: bool = False,
) -> Span[GenerationSpanData]

```

Create a new generation span. The span will not be started automatically, you should either
do `with generation_span() ...` or call `span.start()` \+ `span.finish()` manually.

This span captures the details of a model generation, including the
input message sequence, any generated outputs, the model name and
configuration, and usage data. If you only need to capture a model
response identifier, use `response_span()` instead.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `input` | `Sequence[Mapping[str, Any]] | None` | The sequence of input messages sent to the model. | `None` |
| `output` | `Sequence[Mapping[str, Any]] | None` | The sequence of output messages received from the model. | `None` |
| `model` | `str | None` | The model identifier used for the generation. | `None` |
| `model_config` | `Mapping[str, Any] | None` | The model configuration (hyperparameters) used. | `None` |
| `usage` | `dict[str, Any] | None` | A dictionary of usage information (input tokens, output tokens, etc.). | `None` |
| `span_id` | `str | None` | The ID of the span. Optional. If not provided, we will generate an ID. Werecommend using `util.gen_span_id()` to generate a span ID, to guarantee that IDs arecorrectly formatted. | `None` |
| `parent` | `Trace | Span[Any] | None` | The parent span or trace. If not provided, we will automatically use the currenttrace/span as the parent. | `None` |
| `disabled` | `bool` | If True, we will return a Span but the Span will not be recorded. | `False` |

Returns:

| Type | Description |
| --- | --- |
| `Span[GenerationSpanData]` | The newly created generation span. |

Source code in `src/agents/tracing/create.py`

|  |  |
| --- | --- |
| ```152153154155156157158159160161162163164165166167168169170171172173174175176177178179180181182183184185186187188189190191192193194195196197``` | ```md-code__contentdef generation_span(    input: Sequence[Mapping[str, Any]] | None = None,    output: Sequence[Mapping[str, Any]] | None = None,    model: str | None = None,    model_config: Mapping[str, Any] | None = None,    usage: dict[str, Any] | None = None,    span_id: str | None = None,    parent: Trace | Span[Any] | None = None,    disabled: bool = False,) -> Span[GenerationSpanData]:    """Create a new generation span. The span will not be started automatically, you should either    do `with generation_span() ...` or call `span.start()` + `span.finish()` manually.    This span captures the details of a model generation, including the    input message sequence, any generated outputs, the model name and    configuration, and usage data. If you only need to capture a model    response identifier, use `response_span()` instead.    Args:        input: The sequence of input messages sent to the model.        output: The sequence of output messages received from the model.        model: The model identifier used for the generation.        model_config: The model configuration (hyperparameters) used.        usage: A dictionary of usage information (input tokens, output tokens, etc.).        span_id: The ID of the span. Optional. If not provided, we will generate an ID. We            recommend using `util.gen_span_id()` to generate a span ID, to guarantee that IDs are            correctly formatted.        parent: The parent span or trace. If not provided, we will automatically use the current            trace/span as the parent.        disabled: If True, we will return a Span but the Span will not be recorded.    Returns:        The newly created generation span.    """    return get_trace_provider().create_span(        span_data=GenerationSpanData(            input=input,            output=output,            model=model,            model_config=model_config,            usage=usage,        ),        span_id=span_id,        parent=parent,        disabled=disabled,    )``` |

### response\_span

```
response_span(
    response: Response | None = None,
    span_id: str | None = None,
    parent: Trace | Span[Any] | None = None,
    disabled: bool = False,
) -> Span[ResponseSpanData]

```

Create a new response span. The span will not be started automatically, you should either do
`with response_span() ...` or call `span.start()` \+ `span.finish()` manually.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `response` | `Response | None` | The OpenAI Response object. | `None` |
| `span_id` | `str | None` | The ID of the span. Optional. If not provided, we will generate an ID. Werecommend using `util.gen_span_id()` to generate a span ID, to guarantee that IDs arecorrectly formatted. | `None` |
| `parent` | `Trace | Span[Any] | None` | The parent span or trace. If not provided, we will automatically use the currenttrace/span as the parent. | `None` |
| `disabled` | `bool` | If True, we will return a Span but the Span will not be recorded. | `False` |

Source code in `src/agents/tracing/create.py`

|  |  |
| --- | --- |
| ```200201202203204205206207208209210211212213214215216217218219220221222223``` | ```md-code__contentdef response_span(    response: Response | None = None,    span_id: str | None = None,    parent: Trace | Span[Any] | None = None,    disabled: bool = False,) -> Span[ResponseSpanData]:    """Create a new response span. The span will not be started automatically, you should either do    `with response_span() ...` or call `span.start()` + `span.finish()` manually.    Args:        response: The OpenAI Response object.        span_id: The ID of the span. Optional. If not provided, we will generate an ID. We            recommend using `util.gen_span_id()` to generate a span ID, to guarantee that IDs are            correctly formatted.        parent: The parent span or trace. If not provided, we will automatically use the current            trace/span as the parent.        disabled: If True, we will return a Span but the Span will not be recorded.    """    return get_trace_provider().create_span(        span_data=ResponseSpanData(response=response),        span_id=span_id,        parent=parent,        disabled=disabled,    )``` |

### handoff\_span

```
handoff_span(
    from_agent: str | None = None,
    to_agent: str | None = None,
    span_id: str | None = None,
    parent: Trace | Span[Any] | None = None,
    disabled: bool = False,
) -> Span[HandoffSpanData]

```

Create a new handoff span. The span will not be started automatically, you should either do
`with handoff_span() ...` or call `span.start()` \+ `span.finish()` manually.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `from_agent` | `str | None` | The name of the agent that is handing off. | `None` |
| `to_agent` | `str | None` | The name of the agent that is receiving the handoff. | `None` |
| `span_id` | `str | None` | The ID of the span. Optional. If not provided, we will generate an ID. Werecommend using `util.gen_span_id()` to generate a span ID, to guarantee that IDs arecorrectly formatted. | `None` |
| `parent` | `Trace | Span[Any] | None` | The parent span or trace. If not provided, we will automatically use the currenttrace/span as the parent. | `None` |
| `disabled` | `bool` | If True, we will return a Span but the Span will not be recorded. | `False` |

Returns:

| Type | Description |
| --- | --- |
| `Span[HandoffSpanData]` | The newly created handoff span. |

Source code in `src/agents/tracing/create.py`

|  |  |
| --- | --- |
| ```226227228229230231232233234235236237238239240241242243244245246247248249250251252253254``` | ```md-code__contentdef handoff_span(    from_agent: str | None = None,    to_agent: str | None = None,    span_id: str | None = None,    parent: Trace | Span[Any] | None = None,    disabled: bool = False,) -> Span[HandoffSpanData]:    """Create a new handoff span. The span will not be started automatically, you should either do    `with handoff_span() ...` or call `span.start()` + `span.finish()` manually.    Args:        from_agent: The name of the agent that is handing off.        to_agent: The name of the agent that is receiving the handoff.        span_id: The ID of the span. Optional. If not provided, we will generate an ID. We            recommend using `util.gen_span_id()` to generate a span ID, to guarantee that IDs are            correctly formatted.        parent: The parent span or trace. If not provided, we will automatically use the current            trace/span as the parent.        disabled: If True, we will return a Span but the Span will not be recorded.    Returns:        The newly created handoff span.    """    return get_trace_provider().create_span(        span_data=HandoffSpanData(from_agent=from_agent, to_agent=to_agent),        span_id=span_id,        parent=parent,        disabled=disabled,    )``` |

### custom\_span

```
custom_span(
    name: str,
    data: dict[str, Any] | None = None,
    span_id: str | None = None,
    parent: Trace | Span[Any] | None = None,
    disabled: bool = False,
) -> Span[CustomSpanData]

```

Create a new custom span, to which you can add your own metadata. The span will not be
started automatically, you should either do `with custom_span() ...` or call
`span.start()` \+ `span.finish()` manually.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `name` | `str` | The name of the custom span. | _required_ |
| `data` | `dict[str, Any] | None` | Arbitrary structured data to associate with the span. | `None` |
| `span_id` | `str | None` | The ID of the span. Optional. If not provided, we will generate an ID. Werecommend using `util.gen_span_id()` to generate a span ID, to guarantee that IDs arecorrectly formatted. | `None` |
| `parent` | `Trace | Span[Any] | None` | The parent span or trace. If not provided, we will automatically use the currenttrace/span as the parent. | `None` |
| `disabled` | `bool` | If True, we will return a Span but the Span will not be recorded. | `False` |

Returns:

| Type | Description |
| --- | --- |
| `Span[CustomSpanData]` | The newly created custom span. |

Source code in `src/agents/tracing/create.py`

|  |  |
| --- | --- |
| ```257258259260261262263264265266267268269270271272273274275276277278279280281282283284285286``` | ```md-code__contentdef custom_span(    name: str,    data: dict[str, Any] | None = None,    span_id: str | None = None,    parent: Trace | Span[Any] | None = None,    disabled: bool = False,) -> Span[CustomSpanData]:    """Create a new custom span, to which you can add your own metadata. The span will not be    started automatically, you should either do `with custom_span() ...` or call    `span.start()` + `span.finish()` manually.    Args:        name: The name of the custom span.        data: Arbitrary structured data to associate with the span.        span_id: The ID of the span. Optional. If not provided, we will generate an ID. We            recommend using `util.gen_span_id()` to generate a span ID, to guarantee that IDs are            correctly formatted.        parent: The parent span or trace. If not provided, we will automatically use the current            trace/span as the parent.        disabled: If True, we will return a Span but the Span will not be recorded.    Returns:        The newly created custom span.    """    return get_trace_provider().create_span(        span_data=CustomSpanData(name=name, data=data or {}),        span_id=span_id,        parent=parent,        disabled=disabled,    )``` |

### guardrail\_span

```
guardrail_span(
    name: str,
    triggered: bool = False,
    span_id: str | None = None,
    parent: Trace | Span[Any] | None = None,
    disabled: bool = False,
) -> Span[GuardrailSpanData]

```

Create a new guardrail span. The span will not be started automatically, you should either
do `with guardrail_span() ...` or call `span.start()` \+ `span.finish()` manually.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `name` | `str` | The name of the guardrail. | _required_ |
| `triggered` | `bool` | Whether the guardrail was triggered. | `False` |
| `span_id` | `str | None` | The ID of the span. Optional. If not provided, we will generate an ID. Werecommend using `util.gen_span_id()` to generate a span ID, to guarantee that IDs arecorrectly formatted. | `None` |
| `parent` | `Trace | Span[Any] | None` | The parent span or trace. If not provided, we will automatically use the currenttrace/span as the parent. | `None` |
| `disabled` | `bool` | If True, we will return a Span but the Span will not be recorded. | `False` |

Source code in `src/agents/tracing/create.py`

|  |  |
| --- | --- |
| ```289290291292293294295296297298299300301302303304305306307308309310311312313314``` | ```md-code__contentdef guardrail_span(    name: str,    triggered: bool = False,    span_id: str | None = None,    parent: Trace | Span[Any] | None = None,    disabled: bool = False,) -> Span[GuardrailSpanData]:    """Create a new guardrail span. The span will not be started automatically, you should either    do `with guardrail_span() ...` or call `span.start()` + `span.finish()` manually.    Args:        name: The name of the guardrail.        triggered: Whether the guardrail was triggered.        span_id: The ID of the span. Optional. If not provided, we will generate an ID. We            recommend using `util.gen_span_id()` to generate a span ID, to guarantee that IDs are            correctly formatted.        parent: The parent span or trace. If not provided, we will automatically use the current            trace/span as the parent.        disabled: If True, we will return a Span but the Span will not be recorded.    """    return get_trace_provider().create_span(        span_data=GuardrailSpanData(name=name, triggered=triggered),        span_id=span_id,        parent=parent,        disabled=disabled,    )``` |

### transcription\_span

```
transcription_span(
    model: str | None = None,
    input: str | None = None,
    input_format: str | None = "pcm",
    output: str | None = None,
    model_config: Mapping[str, Any] | None = None,
    span_id: str | None = None,
    parent: Trace | Span[Any] | None = None,
    disabled: bool = False,
) -> Span[TranscriptionSpanData]

```

Create a new transcription span. The span will not be started automatically, you should
either do `with transcription_span() ...` or call `span.start()` \+ `span.finish()` manually.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `model` | `str | None` | The name of the model used for the speech-to-text. | `None` |
| `input` | `str | None` | The audio input of the speech-to-text transcription, as a base64 encoded string ofaudio bytes. | `None` |
| `input_format` | `str | None` | The format of the audio input (defaults to "pcm"). | `'pcm'` |
| `output` | `str | None` | The output of the speech-to-text transcription. | `None` |
| `model_config` | `Mapping[str, Any] | None` | The model configuration (hyperparameters) used. | `None` |
| `span_id` | `str | None` | The ID of the span. Optional. If not provided, we will generate an ID. Werecommend using `util.gen_span_id()` to generate a span ID, to guarantee that IDs arecorrectly formatted. | `None` |
| `parent` | `Trace | Span[Any] | None` | The parent span or trace. If not provided, we will automatically use the currenttrace/span as the parent. | `None` |
| `disabled` | `bool` | If True, we will return a Span but the Span will not be recorded. | `False` |

Returns:

| Type | Description |
| --- | --- |
| `Span[TranscriptionSpanData]` | The newly created speech-to-text span. |

Source code in `src/agents/tracing/create.py`

|  |  |
| --- | --- |
| ```317318319320321322323324325326327328329330331332333334335336337338339340341342343344345346347348349350351352353354355356357358``` | ```md-code__contentdef transcription_span(    model: str | None = None,    input: str | None = None,    input_format: str | None = "pcm",    output: str | None = None,    model_config: Mapping[str, Any] | None = None,    span_id: str | None = None,    parent: Trace | Span[Any] | None = None,    disabled: bool = False,) -> Span[TranscriptionSpanData]:    """Create a new transcription span. The span will not be started automatically, you should    either do `with transcription_span() ...` or call `span.start()` + `span.finish()` manually.    Args:        model: The name of the model used for the speech-to-text.        input: The audio input of the speech-to-text transcription, as a base64 encoded string of            audio bytes.        input_format: The format of the audio input (defaults to "pcm").        output: The output of the speech-to-text transcription.        model_config: The model configuration (hyperparameters) used.        span_id: The ID of the span. Optional. If not provided, we will generate an ID. We            recommend using `util.gen_span_id()` to generate a span ID, to guarantee that IDs are            correctly formatted.        parent: The parent span or trace. If not provided, we will automatically use the current            trace/span as the parent.        disabled: If True, we will return a Span but the Span will not be recorded.    Returns:        The newly created speech-to-text span.    """    return get_trace_provider().create_span(        span_data=TranscriptionSpanData(            input=input,            input_format=input_format,            output=output,            model=model,            model_config=model_config,        ),        span_id=span_id,        parent=parent,        disabled=disabled,    )``` |

### speech\_span

```
speech_span(
    model: str | None = None,
    input: str | None = None,
    output: str | None = None,
    output_format: str | None = "pcm",
    model_config: Mapping[str, Any] | None = None,
    first_content_at: str | None = None,
    span_id: str | None = None,
    parent: Trace | Span[Any] | None = None,
    disabled: bool = False,
) -> Span[SpeechSpanData]

```

Create a new speech span. The span will not be started automatically, you should either do
`with speech_span() ...` or call `span.start()` \+ `span.finish()` manually.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `model` | `str | None` | The name of the model used for the text-to-speech. | `None` |
| `input` | `str | None` | The text input of the text-to-speech. | `None` |
| `output` | `str | None` | The audio output of the text-to-speech as base64 encoded string of PCM audio bytes. | `None` |
| `output_format` | `str | None` | The format of the audio output (defaults to "pcm"). | `'pcm'` |
| `model_config` | `Mapping[str, Any] | None` | The model configuration (hyperparameters) used. | `None` |
| `first_content_at` | `str | None` | The time of the first byte of the audio output. | `None` |
| `span_id` | `str | None` | The ID of the span. Optional. If not provided, we will generate an ID. Werecommend using `util.gen_span_id()` to generate a span ID, to guarantee that IDs arecorrectly formatted. | `None` |
| `parent` | `Trace | Span[Any] | None` | The parent span or trace. If not provided, we will automatically use the currenttrace/span as the parent. | `None` |
| `disabled` | `bool` | If True, we will return a Span but the Span will not be recorded. | `False` |

Source code in `src/agents/tracing/create.py`

|  |  |
| --- | --- |
| ```361362363364365366367368369370371372373374375376377378379380381382383384385386387388389390391392393394395396397398399400401``` | ```md-code__contentdef speech_span(    model: str | None = None,    input: str | None = None,    output: str | None = None,    output_format: str | None = "pcm",    model_config: Mapping[str, Any] | None = None,    first_content_at: str | None = None,    span_id: str | None = None,    parent: Trace | Span[Any] | None = None,    disabled: bool = False,) -> Span[SpeechSpanData]:    """Create a new speech span. The span will not be started automatically, you should either do    `with speech_span() ...` or call `span.start()` + `span.finish()` manually.    Args:        model: The name of the model used for the text-to-speech.        input: The text input of the text-to-speech.        output: The audio output of the text-to-speech as base64 encoded string of PCM audio bytes.        output_format: The format of the audio output (defaults to "pcm").        model_config: The model configuration (hyperparameters) used.        first_content_at: The time of the first byte of the audio output.        span_id: The ID of the span. Optional. If not provided, we will generate an ID. We            recommend using `util.gen_span_id()` to generate a span ID, to guarantee that IDs are            correctly formatted.        parent: The parent span or trace. If not provided, we will automatically use the current            trace/span as the parent.        disabled: If True, we will return a Span but the Span will not be recorded.    """    return get_trace_provider().create_span(        span_data=SpeechSpanData(            model=model,            input=input,            output=output,            output_format=output_format,            model_config=model_config,            first_content_at=first_content_at,        ),        span_id=span_id,        parent=parent,        disabled=disabled,    )``` |

### speech\_group\_span

```
speech_group_span(
    input: str | None = None,
    span_id: str | None = None,
    parent: Trace | Span[Any] | None = None,
    disabled: bool = False,
) -> Span[SpeechGroupSpanData]

```

Create a new speech group span. The span will not be started automatically, you should
either do `with speech_group_span() ...` or call `span.start()` \+ `span.finish()` manually.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `input` | `str | None` | The input text used for the speech request. | `None` |
| `span_id` | `str | None` | The ID of the span. Optional. If not provided, we will generate an ID. Werecommend using `util.gen_span_id()` to generate a span ID, to guarantee that IDs arecorrectly formatted. | `None` |
| `parent` | `Trace | Span[Any] | None` | The parent span or trace. If not provided, we will automatically use the currenttrace/span as the parent. | `None` |
| `disabled` | `bool` | If True, we will return a Span but the Span will not be recorded. | `False` |

Source code in `src/agents/tracing/create.py`

|  |  |
| --- | --- |
| ```404405406407408409410411412413414415416417418419420421422423424425426427``` | ```md-code__contentdef speech_group_span(    input: str | None = None,    span_id: str | None = None,    parent: Trace | Span[Any] | None = None,    disabled: bool = False,) -> Span[SpeechGroupSpanData]:    """Create a new speech group span. The span will not be started automatically, you should    either do `with speech_group_span() ...` or call `span.start()` + `span.finish()` manually.    Args:        input: The input text used for the speech request.        span_id: The ID of the span. Optional. If not provided, we will generate an ID. We            recommend using `util.gen_span_id()` to generate a span ID, to guarantee that IDs are            correctly formatted.        parent: The parent span or trace. If not provided, we will automatically use the current            trace/span as the parent.        disabled: If True, we will return a Span but the Span will not be recorded.    """    return get_trace_provider().create_span(        span_data=SpeechGroupSpanData(input=input),        span_id=span_id,        parent=parent,        disabled=disabled,    )``` |

### mcp\_tools\_span

```
mcp_tools_span(
    server: str | None = None,
    result: list[str] | None = None,
    span_id: str | None = None,
    parent: Trace | Span[Any] | None = None,
    disabled: bool = False,
) -> Span[MCPListToolsSpanData]

```

Create a new MCP list tools span. The span will not be started automatically, you should
either do `with mcp_tools_span() ...` or call `span.start()` \+ `span.finish()` manually.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `server` | `str | None` | The name of the MCP server. | `None` |
| `result` | `list[str] | None` | The result of the MCP list tools call. | `None` |
| `span_id` | `str | None` | The ID of the span. Optional. If not provided, we will generate an ID. Werecommend using `util.gen_span_id()` to generate a span ID, to guarantee that IDs arecorrectly formatted. | `None` |
| `parent` | `Trace | Span[Any] | None` | The parent span or trace. If not provided, we will automatically use the currenttrace/span as the parent. | `None` |
| `disabled` | `bool` | If True, we will return a Span but the Span will not be recorded. | `False` |

Source code in `src/agents/tracing/create.py`

|  |  |
| --- | --- |
| ```430431432433434435436437438439440441442443444445446447448449450451452453454455``` | ```md-code__contentdef mcp_tools_span(    server: str | None = None,    result: list[str] | None = None,    span_id: str | None = None,    parent: Trace | Span[Any] | None = None,    disabled: bool = False,) -> Span[MCPListToolsSpanData]:    """Create a new MCP list tools span. The span will not be started automatically, you should    either do `with mcp_tools_span() ...` or call `span.start()` + `span.finish()` manually.    Args:        server: The name of the MCP server.        result: The result of the MCP list tools call.        span_id: The ID of the span. Optional. If not provided, we will generate an ID. We            recommend using `util.gen_span_id()` to generate a span ID, to guarantee that IDs are            correctly formatted.        parent: The parent span or trace. If not provided, we will automatically use the current            trace/span as the parent.        disabled: If True, we will return a Span but the Span will not be recorded.    """    return get_trace_provider().create_span(        span_data=MCPListToolsSpanData(server=server, result=result),        span_id=span_id,        parent=parent,        disabled=disabled,    )``` |