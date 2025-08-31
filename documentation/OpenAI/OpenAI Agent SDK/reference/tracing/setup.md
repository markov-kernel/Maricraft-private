---
title: `Setup`
source: https://openai.github.io/openai-agents-python/ref/tracing/setup/
---

# `Setup`

### set\_trace\_provider

```
set_trace_provider(provider: TraceProvider) -> None

```

Set the global trace provider used by tracing utilities.

Source code in `src/agents/tracing/setup.py`

|  |  |
| --- | --- |
| ```11121314``` | ```md-code__contentdef set_trace_provider(provider: TraceProvider) -> None:    """Set the global trace provider used by tracing utilities."""    global GLOBAL_TRACE_PROVIDER    GLOBAL_TRACE_PROVIDER = provider``` |

### get\_trace\_provider

```
get_trace_provider() -> TraceProvider

```

Get the global trace provider used by tracing utilities.

Source code in `src/agents/tracing/setup.py`

|  |  |
| --- | --- |
| ```1718192021``` | ```md-code__contentdef get_trace_provider() -> TraceProvider:    """Get the global trace provider used by tracing utilities."""    if GLOBAL_TRACE_PROVIDER is None:        raise RuntimeError("Trace provider not set")    return GLOBAL_TRACE_PROVIDER``` |