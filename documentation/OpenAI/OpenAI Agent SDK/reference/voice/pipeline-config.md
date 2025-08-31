---
title: `Pipeline Config`
source: https://openai.github.io/openai-agents-python/ref/voice/pipeline_config/
---

# `Pipeline Config`

### VoicePipelineConfig`dataclass`

Configuration for a `VoicePipeline`.

Source code in `src/agents/voice/pipeline_config.py`

|  |  |
| --- | --- |
| ```111213141516171819202122232425262728293031323334353637383940414243444546``` | ```md-code__content@dataclassclass VoicePipelineConfig:    """Configuration for a `VoicePipeline`."""    model_provider: VoiceModelProvider = field(default_factory=OpenAIVoiceModelProvider)    """The voice model provider to use for the pipeline. Defaults to OpenAI."""    tracing_disabled: bool = False    """Whether to disable tracing of the pipeline. Defaults to `False`."""    trace_include_sensitive_data: bool = True    """Whether to include sensitive data in traces. Defaults to `True`. This is specifically for the      voice pipeline, and not for anything that goes on inside your Workflow."""    trace_include_sensitive_audio_data: bool = True    """Whether to include audio data in traces. Defaults to `True`."""    workflow_name: str = "Voice Agent"    """The name of the workflow to use for tracing. Defaults to `Voice Agent`."""    group_id: str = field(default_factory=gen_group_id)    """    A grouping identifier to use for tracing, to link multiple traces from the same conversation    or process. If not provided, we will create a random group ID.    """    trace_metadata: dict[str, Any] | None = None    """    An optional dictionary of additional metadata to include with the trace.    """    stt_settings: STTModelSettings = field(default_factory=STTModelSettings)    """The settings to use for the STT model."""    tts_settings: TTSModelSettings = field(default_factory=TTSModelSettings)    """The settings to use for the TTS model."""``` |

#### model\_provider`class-attribute``instance-attribute`

```
model_provider: VoiceModelProvider = field(
    default_factory=OpenAIVoiceModelProvider
)

```

The voice model provider to use for the pipeline. Defaults to OpenAI.

#### tracing\_disabled`class-attribute``instance-attribute`

```
tracing_disabled: bool = False

```

Whether to disable tracing of the pipeline. Defaults to `False`.

#### trace\_include\_sensitive\_data`class-attribute``instance-attribute`

```
trace_include_sensitive_data: bool = True

```

Whether to include sensitive data in traces. Defaults to `True`. This is specifically for the
voice pipeline, and not for anything that goes on inside your Workflow.

#### trace\_include\_sensitive\_audio\_data`class-attribute``instance-attribute`

```
trace_include_sensitive_audio_data: bool = True

```

Whether to include audio data in traces. Defaults to `True`.

#### workflow\_name`class-attribute``instance-attribute`

```
workflow_name: str = 'Voice Agent'

```

The name of the workflow to use for tracing. Defaults to `Voice Agent`.

#### group\_id`class-attribute``instance-attribute`

```
group_id: str = field(default_factory=gen_group_id)

```

A grouping identifier to use for tracing, to link multiple traces from the same conversation
or process. If not provided, we will create a random group ID.

#### trace\_metadata`class-attribute``instance-attribute`

```
trace_metadata: dict[str, Any] | None = None

```

An optional dictionary of additional metadata to include with the trace.

#### stt\_settings`class-attribute``instance-attribute`

```
stt_settings: STTModelSettings = field(
    default_factory=STTModelSettings
)

```

The settings to use for the STT model.

#### tts\_settings`class-attribute``instance-attribute`

```
tts_settings: TTSModelSettings = field(
    default_factory=TTSModelSettings
)

```

The settings to use for the TTS model.