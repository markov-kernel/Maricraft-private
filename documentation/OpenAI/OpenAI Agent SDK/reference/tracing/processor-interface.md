---
title: `Processor interface`
source: https://openai.github.io/openai-agents-python/ref/tracing/processor_interface/
---

# `Processor interface`

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

### TracingExporter

Bases: `ABC`

Exports traces and spans. For example, could log them or send them to a backend.

Source code in `src/agents/tracing/processor_interface.py`

|  |  |
| --- | --- |
| ```5960616263646566676869``` | ```md-code__contentclass TracingExporter(abc.ABC):    """Exports traces and spans. For example, could log them or send them to a backend."""    @abc.abstractmethod    def export(self, items: list["Trace | Span[Any]"]) -> None:        """Exports a list of traces and spans.        Args:            items: The items to export.        """        pass``` |

#### export`abstractmethod`

```
export(items: list[Trace | Span[Any]]) -> None

```

Exports a list of traces and spans.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `items` | `list[Trace | Span[Any]]` | The items to export. | _required_ |

Source code in `src/agents/tracing/processor_interface.py`

|  |  |
| --- | --- |
| ```6263646566676869``` | ```md-code__content@abc.abstractmethoddef export(self, items: list["Trace | Span[Any]"]) -> None:    """Exports a list of traces and spans.    Args:        items: The items to export.    """    pass``` |