---
title: Tracing module
source: https://openai.github.io/openai-agents-python/ref/tracing/
---

# Tracing module

### TracingProcessor

Bases: `ABC`

Interface for processing spans.

Source code in `src/agents/tracing/processor_interface.py`

|  |  |
| --- | --- |
| ``` 91011121314151617181920212223242526272829303132333435363738394041424344454647484950515253545556``` | ```md-code__contentclass TracingProcessor(abc.ABC):    """Interface for processing spans."""    @abc.abstractmethod    def on_trace_start(self, trace: "Trace") -> None:        """Called when a trace is started.        Args:            trace: The trace that started.        """        pass    @abc.abstractmethod    def on_trace_end(self, trace: "Trace") -> None:        """Called when a trace is finished.        Args:            trace: The trace that finished.        """        pass    @abc.abstractmethod    def on_span_start(self, span: "Span[Any]") -> None:        """Called when a span is started.        Args:            span: The span that started.        """        pass    @abc.abstractmethod    def on_span_end(self, span: "Span[Any]") -> None:        """Called when a span is finished. Should not block or raise exceptions.        Args:            span: The span that finished.        """        pass    @abc.abstractmethod    def shutdown(self) -> None:        """Called when the application stops."""        pass    @abc.abstractmethod    def force_flush(self) -> None:        """Forces an immediate flush of all queued spans/traces."""        pass``` |

#### on\_trace\_start`abstractmethod`

```
on_trace_start(trace: Trace) -> None

```

Called when a trace is started.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `trace` | `Trace` | The trace that started. | _required_ |

Source code in `src/agents/tracing/processor_interface.py`

|  |  |
| --- | --- |
| ```1213141516171819``` | ```md-code__content@abc.abstractmethoddef on_trace_start(self, trace: "Trace") -> None:    """Called when a trace is started.    Args:        trace: The trace that started.    """    pass``` |

#### on\_trace\_end`abstractmethod`

```
on_trace_end(trace: Trace) -> None

```

Called when a trace is finished.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `trace` | `Trace` | The trace that finished. | _required_ |

Source code in `src/agents/tracing/processor_interface.py`

|  |  |
| --- | --- |
| ```2122232425262728``` | ```md-code__content@abc.abstractmethoddef on_trace_end(self, trace: "Trace") -> None:    """Called when a trace is finished.    Args:        trace: The trace that finished.    """    pass``` |

#### on\_span\_start`abstractmethod`

```
on_span_start(span: Span[Any]) -> None

```

Called when a span is started.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `span` | `Span[Any]` | The span that started. | _required_ |

Source code in `src/agents/tracing/processor_interface.py`

|  |  |
| --- | --- |
| ```3031323334353637``` | ```md-code__content@abc.abstractmethoddef on_span_start(self, span: "Span[Any]") -> None:    """Called when a span is started.    Args:        span: The span that started.    """    pass``` |

#### on\_span\_end`abstractmethod`

```
on_span_end(span: Span[Any]) -> None

```

Called when a span is finished. Should not block or raise exceptions.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `span` | `Span[Any]` | The span that finished. | _required_ |

Source code in `src/agents/tracing/processor_interface.py`

|  |  |
| --- | --- |
| ```3940414243444546``` | ```md-code__content@abc.abstractmethoddef on_span_end(self, span: "Span[Any]") -> None:    """Called when a span is finished. Should not block or raise exceptions.    Args:        span: The span that finished.    """    pass``` |

#### shutdown`abstractmethod`

```
shutdown() -> None

```

Called when the application stops.

Source code in `src/agents/tracing/processor_interface.py`

|  |  |
| --- | --- |
| ```48495051``` | ```md-code__content@abc.abstractmethoddef shutdown(self) -> None:    """Called when the application stops."""    pass``` |

#### force\_flush`abstractmethod`

```
force_flush() -> None

```

Forces an immediate flush of all queued spans/traces.

Source code in `src/agents/tracing/processor_interface.py`

|  |  |
| --- | --- |
| ```53545556``` | ```md-code__content@abc.abstractmethoddef force_flush(self) -> None:    """Forces an immediate flush of all queued spans/traces."""    pass``` |

### TraceProvider

Bases: `ABC`

Interface for creating traces and spans.

Source code in `src/agents/tracing/provider.py`

|  |  |
| --- | --- |
| ``` 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99100101102103104105106107108109110111112113114115116117118119120121122123124125126127128129130131132133134135136137138139140141142143144145146147``` | ```md-code__contentclass TraceProvider(ABC):    """Interface for creating traces and spans."""    @abstractmethod    def register_processor(self, processor: TracingProcessor) -> None:        """Add a processor that will receive all traces and spans."""    @abstractmethod    def set_processors(self, processors: list[TracingProcessor]) -> None:        """Replace the list of processors with ``processors``."""    @abstractmethod    def get_current_trace(self) -> Trace | None:        """Return the currently active trace, if any."""    @abstractmethod    def get_current_span(self) -> Span[Any] | None:        """Return the currently active span, if any."""    @abstractmethod    def set_disabled(self, disabled: bool) -> None:        """Enable or disable tracing globally."""    @abstractmethod    def time_iso(self) -> str:        """Return the current time in ISO 8601 format."""    @abstractmethod    def gen_trace_id(self) -> str:        """Generate a new trace identifier."""    @abstractmethod    def gen_span_id(self) -> str:        """Generate a new span identifier."""    @abstractmethod    def gen_group_id(self) -> str:        """Generate a new group identifier."""    @abstractmethod    def create_trace(        self,        name: str,        trace_id: str | None = None,        group_id: str | None = None,        metadata: dict[str, Any] | None = None,        disabled: bool = False,    ) -> Trace:        """Create a new trace."""    @abstractmethod    def create_span(        self,        span_data: TSpanData,        span_id: str | None = None,        parent: Trace | Span[Any] | None = None,        disabled: bool = False,    ) -> Span[TSpanData]:        """Create a new span."""    @abstractmethod    def shutdown(self) -> None:        """Clean up any resources used by the provider."""``` |

#### register\_processor`abstractmethod`

```
register_processor(processor: TracingProcessor) -> None

```

Add a processor that will receive all traces and spans.

Source code in `src/agents/tracing/provider.py`

|  |  |
| --- | --- |
| ```888990``` | ```md-code__content@abstractmethoddef register_processor(self, processor: TracingProcessor) -> None:    """Add a processor that will receive all traces and spans."""``` |

#### set\_processors`abstractmethod`

```
set_processors(processors: list[TracingProcessor]) -> None

```

Replace the list of processors with `processors`.

Source code in `src/agents/tracing/provider.py`

|  |  |
| --- | --- |
| ```929394``` | ```md-code__content@abstractmethoddef set_processors(self, processors: list[TracingProcessor]) -> None:    """Replace the list of processors with ``processors``."""``` |

#### get\_current\_trace`abstractmethod`

```
get_current_trace() -> Trace | None

```

Return the currently active trace, if any.

Source code in `src/agents/tracing/provider.py`

|  |  |
| --- | --- |
| ```969798``` | ```md-code__content@abstractmethoddef get_current_trace(self) -> Trace | None:    """Return the currently active trace, if any."""``` |

#### get\_current\_span`abstractmethod`

```
get_current_span() -> Span[Any] | None

```

Return the currently active span, if any.

Source code in `src/agents/tracing/provider.py`

|  |  |
| --- | --- |
| ```100101102``` | ```md-code__content@abstractmethoddef get_current_span(self) -> Span[Any] | None:    """Return the currently active span, if any."""``` |

#### set\_disabled`abstractmethod`

```
set_disabled(disabled: bool) -> None

```

Enable or disable tracing globally.

Source code in `src/agents/tracing/provider.py`

|  |  |
| --- | --- |
| ```104105106``` | ```md-code__content@abstractmethoddef set_disabled(self, disabled: bool) -> None:    """Enable or disable tracing globally."""``` |

#### time\_iso`abstractmethod`

```
time_iso() -> str

```

Return the current time in ISO 8601 format.

Source code in `src/agents/tracing/provider.py`

|  |  |
| --- | --- |
| ```108109110``` | ```md-code__content@abstractmethoddef time_iso(self) -> str:    """Return the current time in ISO 8601 format."""``` |

#### gen\_trace\_id`abstractmethod`

```
gen_trace_id() -> str

```

Generate a new trace identifier.

Source code in `src/agents/tracing/provider.py`

|  |  |
| --- | --- |
| ```112113114``` | ```md-code__content@abstractmethoddef gen_trace_id(self) -> str:    """Generate a new trace identifier."""``` |

#### gen\_span\_id`abstractmethod`

```
gen_span_id() -> str

```

Generate a new span identifier.

Source code in `src/agents/tracing/provider.py`

|  |  |
| --- | --- |
| ```116117118``` | ```md-code__content@abstractmethoddef gen_span_id(self) -> str:    """Generate a new span identifier."""``` |

#### gen\_group\_id`abstractmethod`

```
gen_group_id() -> str

```

Generate a new group identifier.

Source code in `src/agents/tracing/provider.py`

|  |  |
| --- | --- |
| ```120121122``` | ```md-code__content@abstractmethoddef gen_group_id(self) -> str:    """Generate a new group identifier."""``` |

#### create\_trace`abstractmethod`

```
create_trace(
    name: str,
    trace_id: str | None = None,
    group_id: str | None = None,
    metadata: dict[str, Any] | None = None,
    disabled: bool = False,
) -> Trace

```

Create a new trace.

Source code in `src/agents/tracing/provider.py`

|  |  |
| --- | --- |
| ```124125126127128129130131132133``` | ```md-code__content@abstractmethoddef create_trace(    self,    name: str,    trace_id: str | None = None,    group_id: str | None = None,    metadata: dict[str, Any] | None = None,    disabled: bool = False,) -> Trace:    """Create a new trace."""``` |

#### create\_span`abstractmethod`

```
create_span(
    span_data: TSpanData,
    span_id: str | None = None,
    parent: Trace | Span[Any] | None = None,
    disabled: bool = False,
) -> Span[TSpanData]

```

Create a new span.

Source code in `src/agents/tracing/provider.py`

|  |  |
| --- | --- |
| ```135136137138139140141142143``` | ```md-code__content@abstractmethoddef create_span(    self,    span_data: TSpanData,    span_id: str | None = None,    parent: Trace | Span[Any] | None = None,    disabled: bool = False,) -> Span[TSpanData]:    """Create a new span."""``` |

#### shutdown`abstractmethod`

```
shutdown() -> None

```

Clean up any resources used by the provider.

Source code in `src/agents/tracing/provider.py`

|  |  |
| --- | --- |
| ```145146147``` | ```md-code__content@abstractmethoddef shutdown(self) -> None:    """Clean up any resources used by the provider."""``` |

### AgentSpanData

Bases: `SpanData`

Represents an Agent Span in the trace.
Includes name, handoffs, tools, and output type.

Source code in `src/agents/tracing/span_data.py`

|  |  |
| --- | --- |
| ```2829303132333435363738394041424344454647484950515253545556575859``` | ```md-code__contentclass AgentSpanData(SpanData):    """    Represents an Agent Span in the trace.    Includes name, handoffs, tools, and output type.    """    __slots__ = ("name", "handoffs", "tools", "output_type")    def __init__(        self,        name: str,        handoffs: list[str] | None = None,        tools: list[str] | None = None,        output_type: str | None = None,    ):        self.name = name        self.handoffs: list[str] | None = handoffs        self.tools: list[str] | None = tools        self.output_type: str | None = output_type    @property    def type(self) -> str:        return "agent"    def export(self) -> dict[str, Any]:        return {            "type": self.type,            "name": self.name,            "handoffs": self.handoffs,            "tools": self.tools,            "output_type": self.output_type,        }``` |

### CustomSpanData

Bases: `SpanData`

Represents a Custom Span in the trace.
Includes name and data property bag.

Source code in `src/agents/tracing/span_data.py`

|  |  |
| --- | --- |
| ```192193194195196197198199200201202203204205206207208209210211212213``` | ```md-code__contentclass CustomSpanData(SpanData):    """    Represents a Custom Span in the trace.    Includes name and data property bag.    """    __slots__ = ("name", "data")    def __init__(self, name: str, data: dict[str, Any]):        self.name = name        self.data = data    @property    def type(self) -> str:        return "custom"    def export(self) -> dict[str, Any]:        return {            "type": self.type,            "name": self.name,            "data": self.data,        }``` |

### FunctionSpanData

Bases: `SpanData`

Represents a Function Span in the trace.
Includes input, output and MCP data (if applicable).

Source code in `src/agents/tracing/span_data.py`

|  |  |
| --- | --- |
| ```6263646566676869707172737475767778798081828384858687888990919293``` | ```md-code__contentclass FunctionSpanData(SpanData):    """    Represents a Function Span in the trace.    Includes input, output and MCP data (if applicable).    """    __slots__ = ("name", "input", "output", "mcp_data")    def __init__(        self,        name: str,        input: str | None,        output: Any | None,        mcp_data: dict[str, Any] | None = None,    ):        self.name = name        self.input = input        self.output = output        self.mcp_data = mcp_data    @property    def type(self) -> str:        return "function"    def export(self) -> dict[str, Any]:        return {            "type": self.type,            "name": self.name,            "input": self.input,            "output": str(self.output) if self.output else None,            "mcp_data": self.mcp_data,        }``` |

### GenerationSpanData

Bases: `SpanData`

Represents a Generation Span in the trace.
Includes input, output, model, model configuration, and usage.

Source code in `src/agents/tracing/span_data.py`

|  |  |
| --- | --- |
| ``` 96 97 98 99100101102103104105106107108109110111112113114115116117118119120121122123124125126127128129130131132133134135136``` | ```md-code__contentclass GenerationSpanData(SpanData):    """    Represents a Generation Span in the trace.    Includes input, output, model, model configuration, and usage.    """    __slots__ = (        "input",        "output",        "model",        "model_config",        "usage",    )    def __init__(        self,        input: Sequence[Mapping[str, Any]] | None = None,        output: Sequence[Mapping[str, Any]] | None = None,        model: str | None = None,        model_config: Mapping[str, Any] | None = None,        usage: dict[str, Any] | None = None,    ):        self.input = input        self.output = output        self.model = model        self.model_config = model_config        self.usage = usage    @property    def type(self) -> str:        return "generation"    def export(self) -> dict[str, Any]:        return {            "type": self.type,            "input": self.input,            "output": self.output,            "model": self.model,            "model_config": self.model_config,            "usage": self.usage,        }``` |

### GuardrailSpanData

Bases: `SpanData`

Represents a Guardrail Span in the trace.
Includes name and triggered status.

Source code in `src/agents/tracing/span_data.py`

|  |  |
| --- | --- |
| ```216217218219220221222223224225226227228229230231232233234235236237``` | ```md-code__contentclass GuardrailSpanData(SpanData):    """    Represents a Guardrail Span in the trace.    Includes name and triggered status.    """    __slots__ = ("name", "triggered")    def __init__(self, name: str, triggered: bool = False):        self.name = name        self.triggered = triggered    @property    def type(self) -> str:        return "guardrail"    def export(self) -> dict[str, Any]:        return {            "type": self.type,            "name": self.name,            "triggered": self.triggered,        }``` |

### HandoffSpanData

Bases: `SpanData`

Represents a Handoff Span in the trace.
Includes source and destination agents.

Source code in `src/agents/tracing/span_data.py`

|  |  |
| --- | --- |
| ```168169170171172173174175176177178179180181182183184185186187188189``` | ```md-code__contentclass HandoffSpanData(SpanData):    """    Represents a Handoff Span in the trace.    Includes source and destination agents.    """    __slots__ = ("from_agent", "to_agent")    def __init__(self, from_agent: str | None, to_agent: str | None):        self.from_agent = from_agent        self.to_agent = to_agent    @property    def type(self) -> str:        return "handoff"    def export(self) -> dict[str, Any]:        return {            "type": self.type,            "from_agent": self.from_agent,            "to_agent": self.to_agent,        }``` |

### MCPListToolsSpanData

Bases: `SpanData`

Represents an MCP List Tools Span in the trace.
Includes server and result.

Source code in `src/agents/tracing/span_data.py`

|  |  |
| --- | --- |
| ```350351352353354355356357358359360361362363364365366367368369370371372373374``` | ```md-code__contentclass MCPListToolsSpanData(SpanData):    """    Represents an MCP List Tools Span in the trace.    Includes server and result.    """    __slots__ = (        "server",        "result",    )    def __init__(self, server: str | None = None, result: list[str] | None = None):        self.server = server        self.result = result    @property    def type(self) -> str:        return "mcp_tools"    def export(self) -> dict[str, Any]:        return {            "type": self.type,            "server": self.server,            "result": self.result,        }``` |

### ResponseSpanData

Bases: `SpanData`

Represents a Response Span in the trace.
Includes response and input.

Source code in `src/agents/tracing/span_data.py`

|  |  |
| --- | --- |
| ```139140141142143144145146147148149150151152153154155156157158159160161162163164165``` | ```md-code__contentclass ResponseSpanData(SpanData):    """    Represents a Response Span in the trace.    Includes response and input.    """    __slots__ = ("response", "input")    def __init__(        self,        response: Response | None = None,        input: str | list[ResponseInputItemParam] | None = None,    ) -> None:        self.response = response        # This is not used by the OpenAI trace processors, but is useful for other tracing        # processor implementations        self.input = input    @property    def type(self) -> str:        return "response"    def export(self) -> dict[str, Any]:        return {            "type": self.type,            "response_id": self.response.id if self.response else None,        }``` |

### SpanData

Bases: `ABC`

Represents span data in the trace.

Source code in `src/agents/tracing/span_data.py`

|  |  |
| --- | --- |
| ```111213141516171819202122232425``` | ```md-code__contentclass SpanData(abc.ABC):    """    Represents span data in the trace.    """    @abc.abstractmethod    def export(self) -> dict[str, Any]:        """Export the span data as a dictionary."""        pass    @property    @abc.abstractmethod    def type(self) -> str:        """Return the type of the span."""        pass``` |

#### type`abstractmethod``property`

```
type: str

```

Return the type of the span.

#### export`abstractmethod`

```
export() -> dict[str, Any]

```

Export the span data as a dictionary.

Source code in `src/agents/tracing/span_data.py`

|  |  |
| --- | --- |
| ```16171819``` | ```md-code__content@abc.abstractmethoddef export(self) -> dict[str, Any]:    """Export the span data as a dictionary."""    pass``` |

### SpeechGroupSpanData

Bases: `SpanData`

Represents a Speech Group Span in the trace.

Source code in `src/agents/tracing/span_data.py`

|  |  |
| --- | --- |
| ```326327328329330331332333334335336337338339340341342343344345346347``` | ```md-code__contentclass SpeechGroupSpanData(SpanData):    """    Represents a Speech Group Span in the trace.    """    __slots__ = "input"    def __init__(        self,        input: str | None = None,    ):        self.input = input    @property    def type(self) -> str:        return "speech_group"    def export(self) -> dict[str, Any]:        return {            "type": self.type,            "input": self.input,        }``` |

### SpeechSpanData

Bases: `SpanData`

Represents a Speech Span in the trace.
Includes input, output, model, model configuration, and first content timestamp.

Source code in `src/agents/tracing/span_data.py`

|  |  |
| --- | --- |
| ```284285286287288289290291292293294295296297298299300301302303304305306307308309310311312313314315316317318319320321322323``` | ```md-code__contentclass SpeechSpanData(SpanData):    """    Represents a Speech Span in the trace.    Includes input, output, model, model configuration, and first content timestamp.    """    __slots__ = ("input", "output", "model", "model_config", "first_content_at")    def __init__(        self,        input: str | None = None,        output: str | None = None,        output_format: str | None = "pcm",        model: str | None = None,        model_config: Mapping[str, Any] | None = None,        first_content_at: str | None = None,    ):        self.input = input        self.output = output        self.output_format = output_format        self.model = model        self.model_config = model_config        self.first_content_at = first_content_at    @property    def type(self) -> str:        return "speech"    def export(self) -> dict[str, Any]:        return {            "type": self.type,            "input": self.input,            "output": {                "data": self.output or "",                "format": self.output_format,            },            "model": self.model,            "model_config": self.model_config,            "first_content_at": self.first_content_at,        }``` |

### TranscriptionSpanData

Bases: `SpanData`

Represents a Transcription Span in the trace.
Includes input, output, model, and model configuration.

Source code in `src/agents/tracing/span_data.py`

|  |  |
| --- | --- |
| ```240241242243244245246247248249250251252253254255256257258259260261262263264265266267268269270271272273274275276277278279280281``` | ```md-code__contentclass TranscriptionSpanData(SpanData):    """    Represents a Transcription Span in the trace.    Includes input, output, model, and model configuration.    """    __slots__ = (        "input",        "output",        "model",        "model_config",    )    def __init__(        self,        input: str | None = None,        input_format: str | None = "pcm",        output: str | None = None,        model: str | None = None,        model_config: Mapping[str, Any] | None = None,    ):        self.input = input        self.input_format = input_format        self.output = output        self.model = model        self.model_config = model_config    @property    def type(self) -> str:        return "transcription"    def export(self) -> dict[str, Any]:        return {            "type": self.type,            "input": {                "data": self.input or "",                "format": self.input_format,            },            "output": self.output,            "model": self.model,            "model_config": self.model_config,        }``` |

### Span

Bases: `ABC`, `Generic[TSpanData]`

Source code in `src/agents/tracing/spans.py`

|  |  |
| --- | --- |
| ```2324252627282930313233343536373839404142434445464748495051525354555657585960616263646566676869707172737475767778798081828384858687888990919293``` | ```md-code__contentclass Span(abc.ABC, Generic[TSpanData]):    @property    @abc.abstractmethod    def trace_id(self) -> str:        pass    @property    @abc.abstractmethod    def span_id(self) -> str:        pass    @property    @abc.abstractmethod    def span_data(self) -> TSpanData:        pass    @abc.abstractmethod    def start(self, mark_as_current: bool = False):        """        Start the span.        Args:            mark_as_current: If true, the span will be marked as the current span.        """        pass    @abc.abstractmethod    def finish(self, reset_current: bool = False) -> None:        """        Finish the span.        Args:            reset_current: If true, the span will be reset as the current span.        """        pass    @abc.abstractmethod    def __enter__(self) -> Span[TSpanData]:        pass    @abc.abstractmethod    def __exit__(self, exc_type, exc_val, exc_tb):        pass    @property    @abc.abstractmethod    def parent_id(self) -> str | None:        pass    @abc.abstractmethod    def set_error(self, error: SpanError) -> None:        pass    @property    @abc.abstractmethod    def error(self) -> SpanError | None:        pass    @abc.abstractmethod    def export(self) -> dict[str, Any] | None:        pass    @property    @abc.abstractmethod    def started_at(self) -> str | None:        pass    @property    @abc.abstractmethod    def ended_at(self) -> str | None:        pass``` |

#### start`abstractmethod`

```
start(mark_as_current: bool = False)

```

Start the span.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `mark_as_current` | `bool` | If true, the span will be marked as the current span. | `False` |

Source code in `src/agents/tracing/spans.py`

|  |  |
| --- | --- |
| ```394041424344454647``` | ```md-code__content@abc.abstractmethoddef start(self, mark_as_current: bool = False):    """    Start the span.    Args:        mark_as_current: If true, the span will be marked as the current span.    """    pass``` |

#### finish`abstractmethod`

```
finish(reset_current: bool = False) -> None

```

Finish the span.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `reset_current` | `bool` | If true, the span will be reset as the current span. | `False` |

Source code in `src/agents/tracing/spans.py`

|  |  |
| --- | --- |
| ```495051525354555657``` | ```md-code__content@abc.abstractmethoddef finish(self, reset_current: bool = False) -> None:    """    Finish the span.    Args:        reset_current: If true, the span will be reset as the current span.    """    pass``` |

### Trace

A trace is the root level object that tracing creates. It represents a logical "workflow".

Source code in `src/agents/tracing/traces.py`

|  |  |
| --- | --- |
| ```13141516171819202122232425262728293031323334353637383940414243444546474849505152535455565758596061626364656667``` | ```md-code__contentclass Trace:    """    A trace is the root level object that tracing creates. It represents a logical "workflow".    """    @abc.abstractmethod    def __enter__(self) -> Trace:        pass    @abc.abstractmethod    def __exit__(self, exc_type, exc_val, exc_tb):        pass    @abc.abstractmethod    def start(self, mark_as_current: bool = False):        """        Start the trace.        Args:            mark_as_current: If true, the trace will be marked as the current trace.        """        pass    @abc.abstractmethod    def finish(self, reset_current: bool = False):        """        Finish the trace.        Args:            reset_current: If true, the trace will be reset as the current trace.        """        pass    @property    @abc.abstractmethod    def trace_id(self) -> str:        """        The trace ID.        """        pass    @property    @abc.abstractmethod    def name(self) -> str:        """        The name of the workflow being traced.        """        pass    @abc.abstractmethod    def export(self) -> dict[str, Any] | None:        """        Export the trace as a dictionary.        """        pass``` |

#### trace\_id`abstractmethod``property`

```
trace_id: str

```

The trace ID.

#### name`abstractmethod``property`

```
name: str

```

The name of the workflow being traced.

#### start`abstractmethod`

```
start(mark_as_current: bool = False)

```

Start the trace.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `mark_as_current` | `bool` | If true, the trace will be marked as the current trace. | `False` |

Source code in `src/agents/tracing/traces.py`

|  |  |
| --- | --- |
| ```262728293031323334``` | ```md-code__content@abc.abstractmethoddef start(self, mark_as_current: bool = False):    """    Start the trace.    Args:        mark_as_current: If true, the trace will be marked as the current trace.    """    pass``` |

#### finish`abstractmethod`

```
finish(reset_current: bool = False)

```

Finish the trace.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `reset_current` | `bool` | If true, the trace will be reset as the current trace. | `False` |

Source code in `src/agents/tracing/traces.py`

|  |  |
| --- | --- |
| ```363738394041424344``` | ```md-code__content@abc.abstractmethoddef finish(self, reset_current: bool = False):    """    Finish the trace.    Args:        reset_current: If true, the trace will be reset as the current trace.    """    pass``` |

#### export`abstractmethod`

```
export() -> dict[str, Any] | None

```

Export the trace as a dictionary.

Source code in `src/agents/tracing/traces.py`

|  |  |
| --- | --- |
| ```626364656667``` | ```md-code__content@abc.abstractmethoddef export(self) -> dict[str, Any] | None:    """    Export the trace as a dictionary.    """    pass``` |

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

### get\_current\_span

```
get_current_span() -> Span[Any] | None

```

Returns the currently active span, if present.

Source code in `src/agents/tracing/create.py`

|  |  |
| --- | --- |
| ```798081``` | ```md-code__contentdef get_current_span() -> Span[Any] | None:    """Returns the currently active span, if present."""    return get_trace_provider().get_current_span()``` |

### get\_current\_trace

```
get_current_trace() -> Trace | None

```

Returns the currently active trace, if present.

Source code in `src/agents/tracing/create.py`

|  |  |
| --- | --- |
| ```747576``` | ```md-code__contentdef get_current_trace() -> Trace | None:    """Returns the currently active trace, if present."""    return get_trace_provider().get_current_trace()``` |

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

### get\_trace\_provider

```
get_trace_provider() -> TraceProvider

```

Get the global trace provider used by tracing utilities.

Source code in `src/agents/tracing/setup.py`

|  |  |
| --- | --- |
| ```1718192021``` | ```md-code__contentdef get_trace_provider() -> TraceProvider:    """Get the global trace provider used by tracing utilities."""    if GLOBAL_TRACE_PROVIDER is None:        raise RuntimeError("Trace provider not set")    return GLOBAL_TRACE_PROVIDER``` |

### set\_trace\_provider

```
set_trace_provider(provider: TraceProvider) -> None

```

Set the global trace provider used by tracing utilities.

Source code in `src/agents/tracing/setup.py`

|  |  |
| --- | --- |
| ```11121314``` | ```md-code__contentdef set_trace_provider(provider: TraceProvider) -> None:    """Set the global trace provider used by tracing utilities."""    global GLOBAL_TRACE_PROVIDER    GLOBAL_TRACE_PROVIDER = provider``` |

### gen\_span\_id

```
gen_span_id() -> str

```

Generate a new span ID.

Source code in `src/agents/tracing/util.py`

|  |  |
| --- | --- |
| ```141516``` | ```md-code__contentdef gen_span_id() -> str:    """Generate a new span ID."""    return get_trace_provider().gen_span_id()``` |

### gen\_trace\_id

```
gen_trace_id() -> str

```

Generate a new trace ID.

Source code in `src/agents/tracing/util.py`

|  |  |
| --- | --- |
| ``` 91011``` | ```md-code__contentdef gen_trace_id() -> str:    """Generate a new trace ID."""    return get_trace_provider().gen_trace_id()``` |

### add\_trace\_processor

```
add_trace_processor(
    span_processor: TracingProcessor,
) -> None

```

Adds a new trace processor. This processor will receive all traces/spans.

Source code in `src/agents/tracing/__init__.py`

|  |  |
| --- | --- |
| ```8384858687``` | ```md-code__contentdef add_trace_processor(span_processor: TracingProcessor) -> None:    """    Adds a new trace processor. This processor will receive all traces/spans.    """    get_trace_provider().register_processor(span_processor)``` |

### set\_trace\_processors

```
set_trace_processors(
    processors: list[TracingProcessor],
) -> None

```

Set the list of trace processors. This will replace the current list of processors.

Source code in `src/agents/tracing/__init__.py`

|  |  |
| --- | --- |
| ```9091929394``` | ```md-code__contentdef set_trace_processors(processors: list[TracingProcessor]) -> None:    """    Set the list of trace processors. This will replace the current list of processors.    """    get_trace_provider().set_processors(processors)``` |

### set\_tracing\_disabled

```
set_tracing_disabled(disabled: bool) -> None

```

Set whether tracing is globally disabled.

Source code in `src/agents/tracing/__init__.py`

|  |  |
| --- | --- |
| ``` 97 98 99100101``` | ```md-code__contentdef set_tracing_disabled(disabled: bool) -> None:    """    Set whether tracing is globally disabled.    """    get_trace_provider().set_disabled(disabled)``` |

### set\_tracing\_export\_api\_key

```
set_tracing_export_api_key(api_key: str) -> None

```

Set the OpenAI API key for the backend exporter.

Source code in `src/agents/tracing/__init__.py`

|  |  |
| --- | --- |
| ```104105106107108``` | ```md-code__contentdef set_tracing_export_api_key(api_key: str) -> None:    """    Set the OpenAI API key for the backend exporter.    """    default_exporter().set_api_key(api_key)``` |