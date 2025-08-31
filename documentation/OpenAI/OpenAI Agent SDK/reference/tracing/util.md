---
title: `Util`
source: https://openai.github.io/openai-agents-python/ref/tracing/util/
---

# `Util`

### time\_iso

```
time_iso() -> str

```

Return the current time in ISO 8601 format.

Source code in `src/agents/tracing/util.py`

|  |  |
| --- | --- |
| ```456``` | ```md-code__contentdef time_iso() -> str:    """Return the current time in ISO 8601 format."""    return get_trace_provider().time_iso()``` |

### gen\_trace\_id

```
gen_trace_id() -> str

```

Generate a new trace ID.

Source code in `src/agents/tracing/util.py`

|  |  |
| --- | --- |
| ``` 91011``` | ```md-code__contentdef gen_trace_id() -> str:    """Generate a new trace ID."""    return get_trace_provider().gen_trace_id()``` |

### gen\_span\_id

```
gen_span_id() -> str

```

Generate a new span ID.

Source code in `src/agents/tracing/util.py`

|  |  |
| --- | --- |
| ```141516``` | ```md-code__contentdef gen_span_id() -> str:    """Generate a new span ID."""    return get_trace_provider().gen_span_id()``` |

### gen\_group\_id

```
gen_group_id() -> str

```

Generate a new group ID.

Source code in `src/agents/tracing/util.py`

|  |  |
| --- | --- |
| ```192021``` | ```md-code__contentdef gen_group_id() -> str:    """Generate a new group ID."""    return get_trace_provider().gen_group_id()``` |