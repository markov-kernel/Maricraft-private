---
title: `Span data`
source: https://openai.github.io/openai-agents-python/ref/tracing/span_data/
---

# `Span data`

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

### AgentSpanData

Bases: `SpanData`

Represents an Agent Span in the trace.
Includes name, handoffs, tools, and output type.

Source code in `src/agents/tracing/span_data.py`

|  |  |
| --- | --- |
| ```2829303132333435363738394041424344454647484950515253545556575859``` | ```md-code__contentclass AgentSpanData(SpanData):    """    Represents an Agent Span in the trace.    Includes name, handoffs, tools, and output type.    """    __slots__ = ("name", "handoffs", "tools", "output_type")    def __init__(        self,        name: str,        handoffs: list[str] | None = None,        tools: list[str] | None = None,        output_type: str | None = None,    ):        self.name = name        self.handoffs: list[str] | None = handoffs        self.tools: list[str] | None = tools        self.output_type: str | None = output_type    @property    def type(self) -> str:        return "agent"    def export(self) -> dict[str, Any]:        return {            "type": self.type,            "name": self.name,            "handoffs": self.handoffs,            "tools": self.tools,            "output_type": self.output_type,        }``` |

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

### ResponseSpanData

Bases: `SpanData`

Represents a Response Span in the trace.
Includes response and input.

Source code in `src/agents/tracing/span_data.py`

|  |  |
| --- | --- |
| ```139140141142143144145146147148149150151152153154155156157158159160161162163164165``` | ```md-code__contentclass ResponseSpanData(SpanData):    """    Represents a Response Span in the trace.    Includes response and input.    """    __slots__ = ("response", "input")    def __init__(        self,        response: Response | None = None,        input: str | list[ResponseInputItemParam] | None = None,    ) -> None:        self.response = response        # This is not used by the OpenAI trace processors, but is useful for other tracing        # processor implementations        self.input = input    @property    def type(self) -> str:        return "response"    def export(self) -> dict[str, Any]:        return {            "type": self.type,            "response_id": self.response.id if self.response else None,        }``` |

### HandoffSpanData

Bases: `SpanData`

Represents a Handoff Span in the trace.
Includes source and destination agents.

Source code in `src/agents/tracing/span_data.py`

|  |  |
| --- | --- |
| ```168169170171172173174175176177178179180181182183184185186187188189``` | ```md-code__contentclass HandoffSpanData(SpanData):    """    Represents a Handoff Span in the trace.    Includes source and destination agents.    """    __slots__ = ("from_agent", "to_agent")    def __init__(self, from_agent: str | None, to_agent: str | None):        self.from_agent = from_agent        self.to_agent = to_agent    @property    def type(self) -> str:        return "handoff"    def export(self) -> dict[str, Any]:        return {            "type": self.type,            "from_agent": self.from_agent,            "to_agent": self.to_agent,        }``` |

### CustomSpanData

Bases: `SpanData`

Represents a Custom Span in the trace.
Includes name and data property bag.

Source code in `src/agents/tracing/span_data.py`

|  |  |
| --- | --- |
| ```192193194195196197198199200201202203204205206207208209210211212213``` | ```md-code__contentclass CustomSpanData(SpanData):    """    Represents a Custom Span in the trace.    Includes name and data property bag.    """    __slots__ = ("name", "data")    def __init__(self, name: str, data: dict[str, Any]):        self.name = name        self.data = data    @property    def type(self) -> str:        return "custom"    def export(self) -> dict[str, Any]:        return {            "type": self.type,            "name": self.name,            "data": self.data,        }``` |

### GuardrailSpanData

Bases: `SpanData`

Represents a Guardrail Span in the trace.
Includes name and triggered status.

Source code in `src/agents/tracing/span_data.py`

|  |  |
| --- | --- |
| ```216217218219220221222223224225226227228229230231232233234235236237``` | ```md-code__contentclass GuardrailSpanData(SpanData):    """    Represents a Guardrail Span in the trace.    Includes name and triggered status.    """    __slots__ = ("name", "triggered")    def __init__(self, name: str, triggered: bool = False):        self.name = name        self.triggered = triggered    @property    def type(self) -> str:        return "guardrail"    def export(self) -> dict[str, Any]:        return {            "type": self.type,            "name": self.name,            "triggered": self.triggered,        }``` |

### TranscriptionSpanData

Bases: `SpanData`

Represents a Transcription Span in the trace.
Includes input, output, model, and model configuration.

Source code in `src/agents/tracing/span_data.py`

|  |  |
| --- | --- |
| ```240241242243244245246247248249250251252253254255256257258259260261262263264265266267268269270271272273274275276277278279280281``` | ```md-code__contentclass TranscriptionSpanData(SpanData):    """    Represents a Transcription Span in the trace.    Includes input, output, model, and model configuration.    """    __slots__ = (        "input",        "output",        "model",        "model_config",    )    def __init__(        self,        input: str | None = None,        input_format: str | None = "pcm",        output: str | None = None,        model: str | None = None,        model_config: Mapping[str, Any] | None = None,    ):        self.input = input        self.input_format = input_format        self.output = output        self.model = model        self.model_config = model_config    @property    def type(self) -> str:        return "transcription"    def export(self) -> dict[str, Any]:        return {            "type": self.type,            "input": {                "data": self.input or "",                "format": self.input_format,            },            "output": self.output,            "model": self.model,            "model_config": self.model_config,        }``` |

### SpeechSpanData

Bases: `SpanData`

Represents a Speech Span in the trace.
Includes input, output, model, model configuration, and first content timestamp.

Source code in `src/agents/tracing/span_data.py`

|  |  |
| --- | --- |
| ```284285286287288289290291292293294295296297298299300301302303304305306307308309310311312313314315316317318319320321322323``` | ```md-code__contentclass SpeechSpanData(SpanData):    """    Represents a Speech Span in the trace.    Includes input, output, model, model configuration, and first content timestamp.    """    __slots__ = ("input", "output", "model", "model_config", "first_content_at")    def __init__(        self,        input: str | None = None,        output: str | None = None,        output_format: str | None = "pcm",        model: str | None = None,        model_config: Mapping[str, Any] | None = None,        first_content_at: str | None = None,    ):        self.input = input        self.output = output        self.output_format = output_format        self.model = model        self.model_config = model_config        self.first_content_at = first_content_at    @property    def type(self) -> str:        return "speech"    def export(self) -> dict[str, Any]:        return {            "type": self.type,            "input": self.input,            "output": {                "data": self.output or "",                "format": self.output_format,            },            "model": self.model,            "model_config": self.model_config,            "first_content_at": self.first_content_at,        }``` |

### SpeechGroupSpanData

Bases: `SpanData`

Represents a Speech Group Span in the trace.

Source code in `src/agents/tracing/span_data.py`

|  |  |
| --- | --- |
| ```326327328329330331332333334335336337338339340341342343344345346347``` | ```md-code__contentclass SpeechGroupSpanData(SpanData):    """    Represents a Speech Group Span in the trace.    """    __slots__ = "input"    def __init__(        self,        input: str | None = None,    ):        self.input = input    @property    def type(self) -> str:        return "speech_group"    def export(self) -> dict[str, Any]:        return {            "type": self.type,            "input": self.input,        }``` |

### MCPListToolsSpanData

Bases: `SpanData`

Represents an MCP List Tools Span in the trace.
Includes server and result.

Source code in `src/agents/tracing/span_data.py`

|  |  |
| --- | --- |
| ```350351352353354355356357358359360361362363364365366367368369370371372373374``` | ```md-code__contentclass MCPListToolsSpanData(SpanData):    """    Represents an MCP List Tools Span in the trace.    Includes server and result.    """    __slots__ = (        "server",        "result",    )    def __init__(self, server: str | None = None, result: list[str] | None = None):        self.server = server        self.result = result    @property    def type(self) -> str:        return "mcp_tools"    def export(self) -> dict[str, Any]:        return {            "type": self.type,            "server": self.server,            "result": self.result,        }``` |