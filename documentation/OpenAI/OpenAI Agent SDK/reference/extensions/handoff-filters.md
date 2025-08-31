---
title: `Handoff filters`
source: https://openai.github.io/openai-agents-python/ref/extensions/handoff_filters/
---

# `Handoff filters`

### remove\_all\_tools

```
remove_all_tools(
    handoff_input_data: HandoffInputData,
) -> HandoffInputData

```

Filters out all tool items: file search, web search and function calls+output.

Source code in `src/agents/extensions/handoff_filters.py`

|  |  |
| --- | --- |
| ```1617181920212223242526272829303132``` | ```md-code__contentdef remove_all_tools(handoff_input_data: HandoffInputData) -> HandoffInputData:    """Filters out all tool items: file search, web search and function calls+output."""    history = handoff_input_data.input_history    new_items = handoff_input_data.new_items    filtered_history = (        _remove_tool_types_from_input(history) if isinstance(history, tuple) else history    )    filtered_pre_handoff_items = _remove_tools_from_items(handoff_input_data.pre_handoff_items)    filtered_new_items = _remove_tools_from_items(new_items)    return HandoffInputData(        input_history=filtered_history,        pre_handoff_items=filtered_pre_handoff_items,        new_items=filtered_new_items,    )``` |