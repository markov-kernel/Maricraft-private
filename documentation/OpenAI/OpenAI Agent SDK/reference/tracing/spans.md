---
title: `Spans`
source: https://openai.github.io/openai-agents-python/ref/tracing/spans/
---

# `Spans`

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

### NoOpSpan

Bases: `Span[TSpanData]`

Source code in `src/agents/tracing/spans.py`

|  |  |
| --- | --- |
| ``` 96 97 98 99100101102103104105106107108109110111112113114115116117118119120121122123124125126127128129130131132133134135136137138139140141142143144145146147148149150151152153154155156``` | ```md-code__contentclass NoOpSpan(Span[TSpanData]):    __slots__ = ("_span_data", "_prev_span_token")    def __init__(self, span_data: TSpanData):        self._span_data = span_data        self._prev_span_token: contextvars.Token[Span[TSpanData] | None] | None = None    @property    def trace_id(self) -> str:        return "no-op"    @property    def span_id(self) -> str:        return "no-op"    @property    def span_data(self) -> TSpanData:        return self._span_data    @property    def parent_id(self) -> str | None:        return None    def start(self, mark_as_current: bool = False):        if mark_as_current:            self._prev_span_token = Scope.set_current_span(self)    def finish(self, reset_current: bool = False) -> None:        if reset_current and self._prev_span_token is not None:            Scope.reset_current_span(self._prev_span_token)            self._prev_span_token = None    def __enter__(self) -> Span[TSpanData]:        self.start(mark_as_current=True)        return self    def __exit__(self, exc_type, exc_val, exc_tb):        reset_current = True        if exc_type is GeneratorExit:            logger.debug("GeneratorExit, skipping span reset")            reset_current = False        self.finish(reset_current=reset_current)    def set_error(self, error: SpanError) -> None:        pass    @property    def error(self) -> SpanError | None:        return None    def export(self) -> dict[str, Any] | None:        return None    @property    def started_at(self) -> str | None:        return None    @property    def ended_at(self) -> str | None:        return None``` |

### SpanImpl

Bases: `Span[TSpanData]`

Source code in `src/agents/tracing/spans.py`

|  |  |
| --- | --- |
| ```159160161162163164165166167168169170171172173174175176177178179180181182183184185186187188189190191192193194195196197198199200201202203204205206207208209210211212213214215216217218219220221222223224225226227228229230231232233234235236237238239240241242243244245246247248249250251252253254255256257258259260261262263264``` | ```md-code__contentclass SpanImpl(Span[TSpanData]):    __slots__ = (        "_trace_id",        "_span_id",        "_parent_id",        "_started_at",        "_ended_at",        "_error",        "_prev_span_token",        "_processor",        "_span_data",    )    def __init__(        self,        trace_id: str,        span_id: str | None,        parent_id: str | None,        processor: TracingProcessor,        span_data: TSpanData,    ):        self._trace_id = trace_id        self._span_id = span_id or util.gen_span_id()        self._parent_id = parent_id        self._started_at: str | None = None        self._ended_at: str | None = None        self._processor = processor        self._error: SpanError | None = None        self._prev_span_token: contextvars.Token[Span[TSpanData] | None] | None = None        self._span_data = span_data    @property    def trace_id(self) -> str:        return self._trace_id    @property    def span_id(self) -> str:        return self._span_id    @property    def span_data(self) -> TSpanData:        return self._span_data    @property    def parent_id(self) -> str | None:        return self._parent_id    def start(self, mark_as_current: bool = False):        if self.started_at is not None:            logger.warning("Span already started")            return        self._started_at = util.time_iso()        self._processor.on_span_start(self)        if mark_as_current:            self._prev_span_token = Scope.set_current_span(self)    def finish(self, reset_current: bool = False) -> None:        if self.ended_at is not None:            logger.warning("Span already finished")            return        self._ended_at = util.time_iso()        self._processor.on_span_end(self)        if reset_current and self._prev_span_token is not None:            Scope.reset_current_span(self._prev_span_token)            self._prev_span_token = None    def __enter__(self) -> Span[TSpanData]:        self.start(mark_as_current=True)        return self    def __exit__(self, exc_type, exc_val, exc_tb):        reset_current = True        if exc_type is GeneratorExit:            logger.debug("GeneratorExit, skipping span reset")            reset_current = False        self.finish(reset_current=reset_current)    def set_error(self, error: SpanError) -> None:        self._error = error    @property    def error(self) -> SpanError | None:        return self._error    @property    def started_at(self) -> str | None:        return self._started_at    @property    def ended_at(self) -> str | None:        return self._ended_at    def export(self) -> dict[str, Any] | None:        return {            "object": "trace.span",            "id": self.span_id,            "trace_id": self.trace_id,            "parent_id": self._parent_id,            "started_at": self._started_at,            "ended_at": self._ended_at,            "span_data": self.span_data.export(),            "error": self._error,        }``` |