---
title: `Scope`
source: https://openai.github.io/openai-agents-python/ref/tracing/scope/
---

# `Scope`

### Scope

Manages the current span and trace in the context.

Source code in `src/agents/tracing/scope.py`

|  |  |
| --- | --- |
| ```202122232425262728293031323334353637383940414243444546474849``` | ```md-code__contentclass Scope:    """    Manages the current span and trace in the context.    """    @classmethod    def get_current_span(cls) -> "Span[Any] | None":        return _current_span.get()    @classmethod    def set_current_span(cls, span: "Span[Any] | None") -> "contextvars.Token[Span[Any] | None]":        return _current_span.set(span)    @classmethod    def reset_current_span(cls, token: "contextvars.Token[Span[Any] | None]") -> None:        _current_span.reset(token)    @classmethod    def get_current_trace(cls) -> "Trace | None":        return _current_trace.get()    @classmethod    def set_current_trace(cls, trace: "Trace | None") -> "contextvars.Token[Trace | None]":        logger.debug(f"Setting current trace: {trace.trace_id if trace else None}")        return _current_trace.set(trace)    @classmethod    def reset_current_trace(cls, token: "contextvars.Token[Trace | None]") -> None:        logger.debug("Resetting current trace")        _current_trace.reset(token)``` |