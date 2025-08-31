---
title: Realtime Configuration
source: https://openai.github.io/openai-agents-python/ref/realtime/config/
---

# Realtime Configuration

## Run Configuration

Bases: `TypedDict`

Configuration for running a realtime agent session.

Source code in `src/agents/realtime/config.py`

|  |  |
| --- | --- |
| ```146147148149150151152153154155156157158159``` | ```md-code__contentclass RealtimeRunConfig(TypedDict):    """Configuration for running a realtime agent session."""    model_settings: NotRequired[RealtimeSessionModelSettings]    """Settings for the realtime model session."""    output_guardrails: NotRequired[list[OutputGuardrail[Any]]]    """List of output guardrails to run on the agent's responses."""    guardrails_settings: NotRequired[RealtimeGuardrailsSettings]    """Settings for guardrail execution."""    tracing_disabled: NotRequired[bool]    """Whether tracing is disabled for this run."""``` |

### model\_settings`instance-attribute`

```
model_settings: NotRequired[RealtimeSessionModelSettings]

```

Settings for the realtime model session.

### output\_guardrails`instance-attribute`

```
output_guardrails: NotRequired[list[OutputGuardrail[Any]]]

```

List of output guardrails to run on the agent's responses.

### guardrails\_settings`instance-attribute`

```
guardrails_settings: NotRequired[RealtimeGuardrailsSettings]

```

Settings for guardrail execution.

### tracing\_disabled`instance-attribute`

```
tracing_disabled: NotRequired[bool]

```

Whether tracing is disabled for this run.

## Model Settings

Bases: `TypedDict`

Model settings for a realtime model session.

Source code in `src/agents/realtime/config.py`

|  |  |
| --- | --- |
| ``` 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99100101102103104105106107108109110111112113114115116117118119``` | ```md-code__contentclass RealtimeSessionModelSettings(TypedDict):    """Model settings for a realtime model session."""    model_name: NotRequired[RealtimeModelName]    """The name of the realtime model to use."""    instructions: NotRequired[str]    """System instructions for the model."""    modalities: NotRequired[list[Literal["text", "audio"]]]    """The modalities the model should support."""    voice: NotRequired[str]    """The voice to use for audio output."""    input_audio_format: NotRequired[RealtimeAudioFormat]    """The format for input audio streams."""    output_audio_format: NotRequired[RealtimeAudioFormat]    """The format for output audio streams."""    input_audio_transcription: NotRequired[RealtimeInputAudioTranscriptionConfig]    """Configuration for transcribing input audio."""    turn_detection: NotRequired[RealtimeTurnDetectionConfig]    """Configuration for detecting conversation turns."""    tool_choice: NotRequired[ToolChoice]    """How the model should choose which tools to call."""    tools: NotRequired[list[Tool]]    """List of tools available to the model."""    handoffs: NotRequired[list[Handoff]]    """List of handoff configurations."""    tracing: NotRequired[RealtimeModelTracingConfig | None]    """Configuration for request tracing."""``` |

### model\_name`instance-attribute`

```
model_name: NotRequired[RealtimeModelName]

```

The name of the realtime model to use.

### instructions`instance-attribute`

```
instructions: NotRequired[str]

```

System instructions for the model.

### modalities`instance-attribute`

```
modalities: NotRequired[list[Literal['text', 'audio']]]

```

The modalities the model should support.

### voice`instance-attribute`

```
voice: NotRequired[str]

```

The voice to use for audio output.

### input\_audio\_format`instance-attribute`

```
input_audio_format: NotRequired[RealtimeAudioFormat]

```

The format for input audio streams.

### output\_audio\_format`instance-attribute`

```
output_audio_format: NotRequired[RealtimeAudioFormat]

```

The format for output audio streams.

### input\_audio\_transcription`instance-attribute`

```
input_audio_transcription: NotRequired[\
    RealtimeInputAudioTranscriptionConfig\
]

```

Configuration for transcribing input audio.

### turn\_detection`instance-attribute`

```
turn_detection: NotRequired[RealtimeTurnDetectionConfig]

```

Configuration for detecting conversation turns.

### tool\_choice`instance-attribute`

```
tool_choice: NotRequired[ToolChoice]

```

How the model should choose which tools to call.

### tools`instance-attribute`

```
tools: NotRequired[list[Tool]]

```

List of tools available to the model.

### handoffs`instance-attribute`

```
handoffs: NotRequired[list[Handoff]]

```

List of handoff configurations.

### tracing`instance-attribute`

```
tracing: NotRequired[RealtimeModelTracingConfig | None]

```

Configuration for request tracing.

## Audio Configuration

Bases: `TypedDict`

Configuration for audio transcription in realtime sessions.

Source code in `src/agents/realtime/config.py`

|  |  |
| --- | --- |
| ```4445464748495051525354``` | ```md-code__contentclass RealtimeInputAudioTranscriptionConfig(TypedDict):    """Configuration for audio transcription in realtime sessions."""    language: NotRequired[str]    """The language code for transcription."""    model: NotRequired[Literal["gpt-4o-transcribe", "gpt-4o-mini-transcribe", "whisper-1"] | str]    """The transcription model to use."""    prompt: NotRequired[str]    """An optional prompt to guide transcription."""``` |

### language`instance-attribute`

```
language: NotRequired[str]

```

The language code for transcription.

### model`instance-attribute`

```
model: NotRequired[\
    Literal[\
        "gpt-4o-transcribe",\
        "gpt-4o-mini-transcribe",\
        "whisper-1",\
    ]\
    | str\
]

```

The transcription model to use.

### prompt`instance-attribute`

```
prompt: NotRequired[str]

```

An optional prompt to guide transcription.

Bases: `TypedDict`

Turn detection config. Allows extra vendor keys if needed.

Source code in `src/agents/realtime/config.py`

|  |  |
| --- | --- |
| ```5758596061626364656667686970717273747576777879``` | ```md-code__contentclass RealtimeTurnDetectionConfig(TypedDict):    """Turn detection config. Allows extra vendor keys if needed."""    type: NotRequired[Literal["semantic_vad", "server_vad"]]    """The type of voice activity detection to use."""    create_response: NotRequired[bool]    """Whether to create a response when a turn is detected."""    eagerness: NotRequired[Literal["auto", "low", "medium", "high"]]    """How eagerly to detect turn boundaries."""    interrupt_response: NotRequired[bool]    """Whether to allow interrupting the assistant's response."""    prefix_padding_ms: NotRequired[int]    """Padding time in milliseconds before turn detection."""    silence_duration_ms: NotRequired[int]    """Duration of silence in milliseconds to trigger turn detection."""    threshold: NotRequired[float]    """The threshold for voice activity detection."""``` |

### type`instance-attribute`

```
type: NotRequired[Literal['semantic_vad', 'server_vad']]

```

The type of voice activity detection to use.

### create\_response`instance-attribute`

```
create_response: NotRequired[bool]

```

Whether to create a response when a turn is detected.

### eagerness`instance-attribute`

```
eagerness: NotRequired[\
    Literal["auto", "low", "medium", "high"]\
]

```

How eagerly to detect turn boundaries.

### interrupt\_response`instance-attribute`

```
interrupt_response: NotRequired[bool]

```

Whether to allow interrupting the assistant's response.

### prefix\_padding\_ms`instance-attribute`

```
prefix_padding_ms: NotRequired[int]

```

Padding time in milliseconds before turn detection.

### silence\_duration\_ms`instance-attribute`

```
silence_duration_ms: NotRequired[int]

```

Duration of silence in milliseconds to trigger turn detection.

### threshold`instance-attribute`

```
threshold: NotRequired[float]

```

The threshold for voice activity detection.

## Guardrails Settings

Bases: `TypedDict`

Settings for output guardrails in realtime sessions.

Source code in `src/agents/realtime/config.py`

|  |  |
| --- | --- |
| ```122123124125126127128129130``` | ```md-code__contentclass RealtimeGuardrailsSettings(TypedDict):    """Settings for output guardrails in realtime sessions."""    debounce_text_length: NotRequired[int]    """    The minimum number of characters to accumulate before running guardrails on transcript    deltas. Defaults to 100. Guardrails run every time the accumulated text reaches    1x, 2x, 3x, etc. times this threshold.    """``` |

### debounce\_text\_length`instance-attribute`

```
debounce_text_length: NotRequired[int]

```

The minimum number of characters to accumulate before running guardrails on transcript
deltas. Defaults to 100. Guardrails run every time the accumulated text reaches
1x, 2x, 3x, etc. times this threshold.

## Model Configuration

Bases: `TypedDict`

Options for connecting to a realtime model.

Source code in `src/agents/realtime/model.py`

|  |  |
| --- | --- |
| ```25262728293031323334353637383940``` | ```md-code__contentclass RealtimeModelConfig(TypedDict):    """Options for connecting to a realtime model."""    api_key: NotRequired[str | Callable[[], MaybeAwaitable[str]]]    """The API key (or function that returns a key) to use when connecting. If unset, the model will    try to use a sane default. For example, the OpenAI Realtime model will try to use the    `OPENAI_API_KEY`  environment variable.    """    url: NotRequired[str]    """The URL to use when connecting. If unset, the model will use a sane default. For example,    the OpenAI Realtime model will use the default OpenAI WebSocket URL.    """    initial_model_settings: NotRequired[RealtimeSessionModelSettings]    """The initial model settings to use when connecting."""``` |

### api\_key`instance-attribute`

```
api_key: NotRequired[\
    str | Callable[[], MaybeAwaitable[str]]\
]

```

The API key (or function that returns a key) to use when connecting. If unset, the model will
try to use a sane default. For example, the OpenAI Realtime model will try to use the
`OPENAI_API_KEY` environment variable.

### url`instance-attribute`

```
url: NotRequired[str]

```

The URL to use when connecting. If unset, the model will use a sane default. For example,
the OpenAI Realtime model will use the default OpenAI WebSocket URL.

### initial\_model\_settings`instance-attribute`

```
initial_model_settings: NotRequired[\
    RealtimeSessionModelSettings\
]

```

The initial model settings to use when connecting.

## Tracing Configuration

Bases: `TypedDict`

Configuration for tracing in realtime model sessions.

Source code in `src/agents/realtime/config.py`

|  |  |
| --- | --- |
| ```133134135136137138139140141142143``` | ```md-code__contentclass RealtimeModelTracingConfig(TypedDict):    """Configuration for tracing in realtime model sessions."""    workflow_name: NotRequired[str]    """The workflow name to use for tracing."""    group_id: NotRequired[str]    """A group identifier to use for tracing, to link multiple traces together."""    metadata: NotRequired[dict[str, Any]]    """Additional metadata to include with the trace."""``` |

### workflow\_name`instance-attribute`

```
workflow_name: NotRequired[str]

```

The workflow name to use for tracing.

### group\_id`instance-attribute`

```
group_id: NotRequired[str]

```

A group identifier to use for tracing, to link multiple traces together.

### metadata`instance-attribute`

```
metadata: NotRequired[dict[str, Any]]

```

Additional metadata to include with the trace.

## User Input Types

User input that can be a string or structured message.

Bases: `TypedDict`

A text input from the user.

Source code in `src/agents/realtime/config.py`

|  |  |
| --- | --- |
| ```164165166167168169170171``` | ```md-code__contentclass RealtimeUserInputText(TypedDict):    """A text input from the user."""    type: Literal["input_text"]    """The type identifier for text input."""    text: str    """The text content from the user."""``` |

### type`instance-attribute`

```
type: Literal['input_text']

```

The type identifier for text input.

### text`instance-attribute`

```
text: str

```

The text content from the user.

Bases: `TypedDict`

A message input from the user.

Source code in `src/agents/realtime/config.py`

|  |  |
| --- | --- |
| ```174175176177178179180181182183184``` | ```md-code__contentclass RealtimeUserInputMessage(TypedDict):    """A message input from the user."""    type: Literal["message"]    """The type identifier for message inputs."""    role: Literal["user"]    """The role identifier for user messages."""    content: list[RealtimeUserInputText]    """List of text content items in the message."""``` |

### type`instance-attribute`

```
type: Literal['message']

```

The type identifier for message inputs.

### role`instance-attribute`

```
role: Literal['user']

```

The role identifier for user messages.

### content`instance-attribute`

```
content: list[RealtimeUserInputText]

```

List of text content items in the message.

## Client Messages

Bases: `TypedDict`

A raw message to be sent to the model.

Source code in `src/agents/realtime/config.py`

|  |  |
| --- | --- |
| ```3435363738394041``` | ```md-code__contentclass RealtimeClientMessage(TypedDict):    """A raw message to be sent to the model."""    type: str  # explicitly required    """The type of the message."""    other_data: NotRequired[dict[str, Any]]    """Merged into the message body."""``` |

### type`instance-attribute`

```
type: str

```

The type of the message.

### other\_data`instance-attribute`

```
other_data: NotRequired[dict[str, Any]]

```

Merged into the message body.

## Type Aliases

The name of a realtime model.

The audio format for realtime audio streams.