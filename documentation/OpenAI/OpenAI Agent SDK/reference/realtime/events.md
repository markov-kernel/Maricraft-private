---
title: Realtime Events
source: https://openai.github.io/openai-agents-python/ref/realtime/events/
---

# Realtime Events

## Session Events

An event emitted by the realtime session.

## Event Types

### Agent Events

A new agent has started.

Source code in `src/agents/realtime/events.py`

|  |  |
| --- | --- |
| ```2223242526272829303132``` | ```md-code__content@dataclassclass RealtimeAgentStartEvent:    """A new agent has started."""    agent: RealtimeAgent    """The new agent."""    info: RealtimeEventInfo    """Common info for all events, such as the context."""    type: Literal["agent_start"] = "agent_start"``` |

### agent`instance-attribute`

```
agent: RealtimeAgent

```

The new agent.

### info`instance-attribute`

```
info: RealtimeEventInfo

```

Common info for all events, such as the context.

An agent has ended.

Source code in `src/agents/realtime/events.py`

|  |  |
| --- | --- |
| ```3536373839404142434445``` | ```md-code__content@dataclassclass RealtimeAgentEndEvent:    """An agent has ended."""    agent: RealtimeAgent    """The agent that ended."""    info: RealtimeEventInfo    """Common info for all events, such as the context."""    type: Literal["agent_end"] = "agent_end"``` |

### agent`instance-attribute`

```
agent: RealtimeAgent

```

The agent that ended.

### info`instance-attribute`

```
info: RealtimeEventInfo

```

Common info for all events, such as the context.

### Audio Events

Triggered when the agent generates new audio to be played.

Source code in `src/agents/realtime/events.py`

|  |  |
| --- | --- |
| ```121122123124125126127128129130131``` | ```md-code__content@dataclassclass RealtimeAudio:    """Triggered when the agent generates new audio to be played."""    audio: RealtimeModelAudioEvent    """The audio event from the model layer."""    info: RealtimeEventInfo    """Common info for all events, such as the context."""    type: Literal["audio"] = "audio"``` |

### audio`instance-attribute`

```
audio: RealtimeModelAudioEvent

```

The audio event from the model layer.

### info`instance-attribute`

```
info: RealtimeEventInfo

```

Common info for all events, such as the context.

Triggered when the agent stops generating audio.

Source code in `src/agents/realtime/events.py`

|  |  |
| --- | --- |
| ```111112113114115116117118``` | ```md-code__content@dataclassclass RealtimeAudioEnd:    """Triggered when the agent stops generating audio."""    info: RealtimeEventInfo    """Common info for all events, such as the context."""    type: Literal["audio_end"] = "audio_end"``` |

### info`instance-attribute`

```
info: RealtimeEventInfo

```

Common info for all events, such as the context.

Triggered when the agent is interrupted. Can be listened to by the user to stop audio
playback or give visual indicators to the user.

Source code in `src/agents/realtime/events.py`

|  |  |
| --- | --- |
| ```134135136137138139140141142143``` | ```md-code__content@dataclassclass RealtimeAudioInterrupted:    """Triggered when the agent is interrupted. Can be listened to by the user to stop audio    playback or give visual indicators to the user.    """    info: RealtimeEventInfo    """Common info for all events, such as the context."""    type: Literal["audio_interrupted"] = "audio_interrupted"``` |

### info`instance-attribute`

```
info: RealtimeEventInfo

```

Common info for all events, such as the context.

### Tool Events

An agent is starting a tool call.

Source code in `src/agents/realtime/events.py`

|  |  |
| --- | --- |
| ```64656667686970717273747576``` | ```md-code__content@dataclassclass RealtimeToolStart:    """An agent is starting a tool call."""    agent: RealtimeAgent    """The agent that updated."""    tool: Tool    info: RealtimeEventInfo    """Common info for all events, such as the context."""    type: Literal["tool_start"] = "tool_start"``` |

### agent`instance-attribute`

```
agent: RealtimeAgent

```

The agent that updated.

### info`instance-attribute`

```
info: RealtimeEventInfo

```

Common info for all events, such as the context.

An agent has ended a tool call.

Source code in `src/agents/realtime/events.py`

|  |  |
| --- | --- |
| ```7980818283848586878889909192939495``` | ```md-code__content@dataclassclass RealtimeToolEnd:    """An agent has ended a tool call."""    agent: RealtimeAgent    """The agent that ended the tool call."""    tool: Tool    """The tool that was called."""    output: Any    """The output of the tool call."""    info: RealtimeEventInfo    """Common info for all events, such as the context."""    type: Literal["tool_end"] = "tool_end"``` |

### agent`instance-attribute`

```
agent: RealtimeAgent

```

The agent that ended the tool call.

### tool`instance-attribute`

```
tool: Tool

```

The tool that was called.

### output`instance-attribute`

```
output: Any

```

The output of the tool call.

### info`instance-attribute`

```
info: RealtimeEventInfo

```

Common info for all events, such as the context.

### Handoff Events

An agent has handed off to another agent.

Source code in `src/agents/realtime/events.py`

|  |  |
| --- | --- |
| ```4849505152535455565758596061``` | ```md-code__content@dataclassclass RealtimeHandoffEvent:    """An agent has handed off to another agent."""    from_agent: RealtimeAgent    """The agent that handed off."""    to_agent: RealtimeAgent    """The agent that was handed off to."""    info: RealtimeEventInfo    """Common info for all events, such as the context."""    type: Literal["handoff"] = "handoff"``` |

### from\_agent`instance-attribute`

```
from_agent: RealtimeAgent

```

The agent that handed off.

### to\_agent`instance-attribute`

```
to_agent: RealtimeAgent

```

The agent that was handed off to.

### info`instance-attribute`

```
info: RealtimeEventInfo

```

Common info for all events, such as the context.

### Guardrail Events

A guardrail has been tripped and the agent has been interrupted.

Source code in `src/agents/realtime/events.py`

|  |  |
| --- | --- |
| ```185186187188189190191192193194195196197198``` | ```md-code__content@dataclassclass RealtimeGuardrailTripped:    """A guardrail has been tripped and the agent has been interrupted."""    guardrail_results: list[OutputGuardrailResult]    """The results from all triggered guardrails."""    message: str    """The message that was being generated when the guardrail was triggered."""    info: RealtimeEventInfo    """Common info for all events, such as the context."""    type: Literal["guardrail_tripped"] = "guardrail_tripped"``` |

### guardrail\_results`instance-attribute`

```
guardrail_results: list[OutputGuardrailResult]

```

The results from all triggered guardrails.

### message`instance-attribute`

```
message: str

```

The message that was being generated when the guardrail was triggered.

### info`instance-attribute`

```
info: RealtimeEventInfo

```

Common info for all events, such as the context.

### History Events

A new item has been added to the history.

Source code in `src/agents/realtime/events.py`

|  |  |
| --- | --- |
| ```172173174175176177178179180181182``` | ```md-code__content@dataclassclass RealtimeHistoryAdded:    """A new item has been added to the history."""    item: RealtimeItem    """The new item that was added to the history."""    info: RealtimeEventInfo    """Common info for all events, such as the context."""    type: Literal["history_added"] = "history_added"``` |

### item`instance-attribute`

```
item: RealtimeItem

```

The new item that was added to the history.

### info`instance-attribute`

```
info: RealtimeEventInfo

```

Common info for all events, such as the context.

The history has been updated. Contains the full history of the session.

Source code in `src/agents/realtime/events.py`

|  |  |
| --- | --- |
| ```159160161162163164165166167168169``` | ```md-code__content@dataclassclass RealtimeHistoryUpdated:    """The history has been updated. Contains the full history of the session."""    history: list[RealtimeItem]    """The full history of the session."""    info: RealtimeEventInfo    """Common info for all events, such as the context."""    type: Literal["history_updated"] = "history_updated"``` |

### history`instance-attribute`

```
history: list[RealtimeItem]

```

The full history of the session.

### info`instance-attribute`

```
info: RealtimeEventInfo

```

Common info for all events, such as the context.

### Error Events

An error has occurred.

Source code in `src/agents/realtime/events.py`

|  |  |
| --- | --- |
| ```146147148149150151152153154155156``` | ```md-code__content@dataclassclass RealtimeError:    """An error has occurred."""    error: Any    """The error that occurred."""    info: RealtimeEventInfo    """Common info for all events, such as the context."""    type: Literal["error"] = "error"``` |

### error`instance-attribute`

```
error: Any

```

The error that occurred.

### info`instance-attribute`

```
info: RealtimeEventInfo

```

Common info for all events, such as the context.

### Raw Model Events

Forwards raw events from the model layer.

Source code in `src/agents/realtime/events.py`

|  |  |
| --- | --- |
| ``` 98 99100101102103104105106107108``` | ```md-code__content@dataclassclass RealtimeRawModelEvent:    """Forwards raw events from the model layer."""    data: RealtimeModelEvent    """The raw data from the model layer."""    info: RealtimeEventInfo    """Common info for all events, such as the context."""    type: Literal["raw_model_event"] = "raw_model_event"``` |

### data`instance-attribute`

```
data: RealtimeModelEvent

```

The raw data from the model layer.

### info`instance-attribute`

```
info: RealtimeEventInfo

```

Common info for all events, such as the context.