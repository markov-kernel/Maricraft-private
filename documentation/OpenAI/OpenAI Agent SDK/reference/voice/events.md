---
title: `Events`
source: https://openai.github.io/openai-agents-python/ref/voice/events/
---

# `Events`

### VoiceStreamEvent`module-attribute`

```
VoiceStreamEvent: TypeAlias = Union[\
    VoiceStreamEventAudio,\
    VoiceStreamEventLifecycle,\
    VoiceStreamEventError,\
]

```

An event from the `VoicePipeline`, streamed via `StreamedAudioResult.stream()`.

### VoiceStreamEventAudio`dataclass`

Streaming event from the VoicePipeline

Source code in `src/agents/voice/events.py`

|  |  |
| --- | --- |
| ```111213141516171819``` | ```md-code__content@dataclassclass VoiceStreamEventAudio:    """Streaming event from the VoicePipeline"""    data: npt.NDArray[np.int16 | np.float32] | None    """The audio data."""    type: Literal["voice_stream_event_audio"] = "voice_stream_event_audio"    """The type of event."""``` |

#### data`instance-attribute`

```
data: NDArray[int16 | float32] | None

```

The audio data.

#### type`class-attribute``instance-attribute`

```
type: Literal["voice_stream_event_audio"] = (
    "voice_stream_event_audio"
)

```

The type of event.

### VoiceStreamEventLifecycle`dataclass`

Streaming event from the VoicePipeline

Source code in `src/agents/voice/events.py`

|  |  |
| --- | --- |
| ```222324252627282930``` | ```md-code__content@dataclassclass VoiceStreamEventLifecycle:    """Streaming event from the VoicePipeline"""    event: Literal["turn_started", "turn_ended", "session_ended"]    """The event that occurred."""    type: Literal["voice_stream_event_lifecycle"] = "voice_stream_event_lifecycle"    """The type of event."""``` |

#### event`instance-attribute`

```
event: Literal[\
    "turn_started", "turn_ended", "session_ended"\
]

```

The event that occurred.

#### type`class-attribute``instance-attribute`

```
type: Literal["voice_stream_event_lifecycle"] = (
    "voice_stream_event_lifecycle"
)

```

The type of event.

### VoiceStreamEventError`dataclass`

Streaming event from the VoicePipeline

Source code in `src/agents/voice/events.py`

|  |  |
| --- | --- |
| ```333435363738394041``` | ```md-code__content@dataclassclass VoiceStreamEventError:    """Streaming event from the VoicePipeline"""    error: Exception    """The error that occurred."""    type: Literal["voice_stream_event_error"] = "voice_stream_event_error"    """The type of event."""``` |

#### error`instance-attribute`

```
error: Exception

```

The error that occurred.

#### type`class-attribute``instance-attribute`

```
type: Literal["voice_stream_event_error"] = (
    "voice_stream_event_error"
)

```

The type of event.