---
title: `Model`
source: https://openai.github.io/openai-agents-python/ref/voice/model/
---

# `Model`

### TTSVoice`module-attribute`

```
TTSVoice = Literal[\
    "alloy",\
    "ash",\
    "coral",\
    "echo",\
    "fable",\
    "onyx",\
    "nova",\
    "sage",\
    "shimmer",\
]

```

Exportable type for the TTSModelSettings voice enum

### TTSModelSettings`dataclass`

Settings for a TTS model.

Source code in `src/agents/voice/model.py`

|  |  |
| --- | --- |
| ```2122232425262728293031323334353637383940414243444546474849505152535455565758596061``` | ```md-code__content@dataclassclass TTSModelSettings:    """Settings for a TTS model."""    voice: TTSVoice | None = None    """    The voice to use for the TTS model. If not provided, the default voice for the respective model    will be used.    """    buffer_size: int = 120    """The minimal size of the chunks of audio data that are being streamed out."""    dtype: npt.DTypeLike = np.int16    """The data type for the audio data to be returned in."""    transform_data: (        Callable[[npt.NDArray[np.int16 | np.float32]], npt.NDArray[np.int16 | np.float32]] | None    ) = None    """    A function to transform the data from the TTS model. This is useful if you want the resulting    audio stream to have the data in a specific shape already.    """    instructions: str = (        "You will receive partial sentences. Do not complete the sentence just read out the text."    )    """    The instructions to use for the TTS model. This is useful if you want to control the tone of the    audio output.    """    text_splitter: Callable[[str], tuple[str, str]] = get_sentence_based_splitter()    """    A function to split the text into chunks. This is useful if you want to split the text into    chunks before sending it to the TTS model rather than waiting for the whole text to be    processed.    """    speed: float | None = None    """The speed with which the TTS model will read the text. Between 0.25 and 4.0."""``` |

#### voice`class-attribute``instance-attribute`

```
voice: TTSVoice | None = None

```

The voice to use for the TTS model. If not provided, the default voice for the respective model
will be used.

#### buffer\_size`class-attribute``instance-attribute`

```
buffer_size: int = 120

```

The minimal size of the chunks of audio data that are being streamed out.

#### dtype`class-attribute``instance-attribute`

```
dtype: DTypeLike = int16

```

The data type for the audio data to be returned in.

#### transform\_data`class-attribute``instance-attribute`

```
transform_data: (
    Callable[\
        [NDArray[int16 | float32]], NDArray[int16 | float32]\
    ]
    | None
) = None

```

A function to transform the data from the TTS model. This is useful if you want the resulting
audio stream to have the data in a specific shape already.

#### instructions`class-attribute``instance-attribute`

```
instructions: str = "You will receive partial sentences. Do not complete the sentence just read out the text."

```

The instructions to use for the TTS model. This is useful if you want to control the tone of the
audio output.

#### text\_splitter`class-attribute``instance-attribute`

```
text_splitter: Callable[[str], tuple[str, str]] = (
    get_sentence_based_splitter()
)

```

A function to split the text into chunks. This is useful if you want to split the text into
chunks before sending it to the TTS model rather than waiting for the whole text to be
processed.

#### speed`class-attribute``instance-attribute`

```
speed: float | None = None

```

The speed with which the TTS model will read the text. Between 0.25 and 4.0.

### TTSModel

Bases: `ABC`

A text-to-speech model that can convert text into audio output.

Source code in `src/agents/voice/model.py`

|  |  |
| --- | --- |
| ```6465666768697071727374757677787980818283``` | ```md-code__contentclass TTSModel(abc.ABC):    """A text-to-speech model that can convert text into audio output."""    @property    @abc.abstractmethod    def model_name(self) -> str:        """The name of the TTS model."""        pass    @abc.abstractmethod    def run(self, text: str, settings: TTSModelSettings) -> AsyncIterator[bytes]:        """Given a text string, produces a stream of audio bytes, in PCM format.        Args:            text: The text to convert to audio.        Returns:            An async iterator of audio bytes, in PCM format.        """        pass``` |

#### model\_name`abstractmethod``property`

```
model_name: str

```

The name of the TTS model.

#### run`abstractmethod`

```
run(
    text: str, settings: TTSModelSettings
) -> AsyncIterator[bytes]

```

Given a text string, produces a stream of audio bytes, in PCM format.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `text` | `str` | The text to convert to audio. | _required_ |

Returns:

| Type | Description |
| --- | --- |
| `AsyncIterator[bytes]` | An async iterator of audio bytes, in PCM format. |

Source code in `src/agents/voice/model.py`

|  |  |
| --- | --- |
| ```7374757677787980818283``` | ```md-code__content@abc.abstractmethoddef run(self, text: str, settings: TTSModelSettings) -> AsyncIterator[bytes]:    """Given a text string, produces a stream of audio bytes, in PCM format.    Args:        text: The text to convert to audio.    Returns:        An async iterator of audio bytes, in PCM format.    """    pass``` |

### StreamedTranscriptionSession

Bases: `ABC`

A streamed transcription of audio input.

Source code in `src/agents/voice/model.py`

|  |  |
| --- | --- |
| ``` 86 87 88 89 90 91 92 93 94 95 96 97 98 99100``` | ```md-code__contentclass StreamedTranscriptionSession(abc.ABC):    """A streamed transcription of audio input."""    @abc.abstractmethod    def transcribe_turns(self) -> AsyncIterator[str]:        """Yields a stream of text transcriptions. Each transcription is a turn in the conversation.        This method is expected to return only after `close()` is called.        """        pass    @abc.abstractmethod    async def close(self) -> None:        """Closes the session."""        pass``` |

#### transcribe\_turns`abstractmethod`

```
transcribe_turns() -> AsyncIterator[str]

```

Yields a stream of text transcriptions. Each transcription is a turn in the conversation.

This method is expected to return only after `close()` is called.

Source code in `src/agents/voice/model.py`

|  |  |
| --- | --- |
| ```89909192939495``` | ```md-code__content@abc.abstractmethoddef transcribe_turns(self) -> AsyncIterator[str]:    """Yields a stream of text transcriptions. Each transcription is a turn in the conversation.    This method is expected to return only after `close()` is called.    """    pass``` |

#### close`abstractmethod``async`

```
close() -> None

```

Closes the session.

Source code in `src/agents/voice/model.py`

|  |  |
| --- | --- |
| ``` 97 98 99100``` | ```md-code__content@abc.abstractmethodasync def close(self) -> None:    """Closes the session."""    pass``` |

### STTModelSettings`dataclass`

Settings for a speech-to-text model.

Source code in `src/agents/voice/model.py`

|  |  |
| --- | --- |
| ```103104105106107108109110111112113114115116117``` | ```md-code__content@dataclassclass STTModelSettings:    """Settings for a speech-to-text model."""    prompt: str | None = None    """Instructions for the model to follow."""    language: str | None = None    """The language of the audio input."""    temperature: float | None = None    """The temperature of the model."""    turn_detection: dict[str, Any] | None = None    """The turn detection settings for the model when using streamed audio input."""``` |

#### prompt`class-attribute``instance-attribute`

```
prompt: str | None = None

```

Instructions for the model to follow.

#### language`class-attribute``instance-attribute`

```
language: str | None = None

```

The language of the audio input.

#### temperature`class-attribute``instance-attribute`

```
temperature: float | None = None

```

The temperature of the model.

#### turn\_detection`class-attribute``instance-attribute`

```
turn_detection: dict[str, Any] | None = None

```

The turn detection settings for the model when using streamed audio input.

### STTModel

Bases: `ABC`

A speech-to-text model that can convert audio input into text.

Source code in `src/agents/voice/model.py`

|  |  |
| --- | --- |
| ```120121122123124125126127128129130131132133134135136137138139140141142143144145146147148149150151152153154155156157158159160161162163164165166167168169170``` | ```md-code__contentclass STTModel(abc.ABC):    """A speech-to-text model that can convert audio input into text."""    @property    @abc.abstractmethod    def model_name(self) -> str:        """The name of the STT model."""        pass    @abc.abstractmethod    async def transcribe(        self,        input: AudioInput,        settings: STTModelSettings,        trace_include_sensitive_data: bool,        trace_include_sensitive_audio_data: bool,    ) -> str:        """Given an audio input, produces a text transcription.        Args:            input: The audio input to transcribe.            settings: The settings to use for the transcription.            trace_include_sensitive_data: Whether to include sensitive data in traces.            trace_include_sensitive_audio_data: Whether to include sensitive audio data in traces.        Returns:            The text transcription of the audio input.        """        pass    @abc.abstractmethod    async def create_session(        self,        input: StreamedAudioInput,        settings: STTModelSettings,        trace_include_sensitive_data: bool,        trace_include_sensitive_audio_data: bool,    ) -> StreamedTranscriptionSession:        """Creates a new transcription session, which you can push audio to, and receive a stream        of text transcriptions.        Args:            input: The audio input to transcribe.            settings: The settings to use for the transcription.            trace_include_sensitive_data: Whether to include sensitive data in traces.            trace_include_sensitive_audio_data: Whether to include sensitive audio data in traces.        Returns:            A new transcription session.        """        pass``` |

#### model\_name`abstractmethod``property`

```
model_name: str

```

The name of the STT model.

#### transcribe`abstractmethod``async`

```
transcribe(
    input: AudioInput,
    settings: STTModelSettings,
    trace_include_sensitive_data: bool,
    trace_include_sensitive_audio_data: bool,
) -> str

```

Given an audio input, produces a text transcription.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `input` | `AudioInput` | The audio input to transcribe. | _required_ |
| `settings` | `STTModelSettings` | The settings to use for the transcription. | _required_ |
| `trace_include_sensitive_data` | `bool` | Whether to include sensitive data in traces. | _required_ |
| `trace_include_sensitive_audio_data` | `bool` | Whether to include sensitive audio data in traces. | _required_ |

Returns:

| Type | Description |
| --- | --- |
| `str` | The text transcription of the audio input. |

Source code in `src/agents/voice/model.py`

|  |  |
| --- | --- |
| ```129130131132133134135136137138139140141142143144145146147148``` | ```md-code__content@abc.abstractmethodasync def transcribe(    self,    input: AudioInput,    settings: STTModelSettings,    trace_include_sensitive_data: bool,    trace_include_sensitive_audio_data: bool,) -> str:    """Given an audio input, produces a text transcription.    Args:        input: The audio input to transcribe.        settings: The settings to use for the transcription.        trace_include_sensitive_data: Whether to include sensitive data in traces.        trace_include_sensitive_audio_data: Whether to include sensitive audio data in traces.    Returns:        The text transcription of the audio input.    """    pass``` |

#### create\_session`abstractmethod``async`

```
create_session(
    input: StreamedAudioInput,
    settings: STTModelSettings,
    trace_include_sensitive_data: bool,
    trace_include_sensitive_audio_data: bool,
) -> StreamedTranscriptionSession

```

Creates a new transcription session, which you can push audio to, and receive a stream
of text transcriptions.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `input` | `StreamedAudioInput` | The audio input to transcribe. | _required_ |
| `settings` | `STTModelSettings` | The settings to use for the transcription. | _required_ |
| `trace_include_sensitive_data` | `bool` | Whether to include sensitive data in traces. | _required_ |
| `trace_include_sensitive_audio_data` | `bool` | Whether to include sensitive audio data in traces. | _required_ |

Returns:

| Type | Description |
| --- | --- |
| `StreamedTranscriptionSession` | A new transcription session. |

Source code in `src/agents/voice/model.py`

|  |  |
| --- | --- |
| ```150151152153154155156157158159160161162163164165166167168169170``` | ```md-code__content@abc.abstractmethodasync def create_session(    self,    input: StreamedAudioInput,    settings: STTModelSettings,    trace_include_sensitive_data: bool,    trace_include_sensitive_audio_data: bool,) -> StreamedTranscriptionSession:    """Creates a new transcription session, which you can push audio to, and receive a stream    of text transcriptions.    Args:        input: The audio input to transcribe.        settings: The settings to use for the transcription.        trace_include_sensitive_data: Whether to include sensitive data in traces.        trace_include_sensitive_audio_data: Whether to include sensitive audio data in traces.    Returns:        A new transcription session.    """    pass``` |

### VoiceModelProvider

Bases: `ABC`

The base interface for a voice model provider.

A model provider is responsible for creating speech-to-text and text-to-speech models, given a
name.

Source code in `src/agents/voice/model.py`

|  |  |
| --- | --- |
| ```173174175176177178179180181182183184185186187188189190191192193194``` | ```md-code__contentclass VoiceModelProvider(abc.ABC):    """The base interface for a voice model provider.    A model provider is responsible for creating speech-to-text and text-to-speech models, given a    name.    """    @abc.abstractmethod    def get_stt_model(self, model_name: str | None) -> STTModel:        """Get a speech-to-text model by name.        Args:            model_name: The name of the model to get.        Returns:            The speech-to-text model.        """        pass    @abc.abstractmethod    def get_tts_model(self, model_name: str | None) -> TTSModel:        """Get a text-to-speech model by name."""``` |

#### get\_stt\_model`abstractmethod`

```
get_stt_model(model_name: str | None) -> STTModel

```

Get a speech-to-text model by name.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `model_name` | `str | None` | The name of the model to get. | _required_ |

Returns:

| Type | Description |
| --- | --- |
| `STTModel` | The speech-to-text model. |

Source code in `src/agents/voice/model.py`

|  |  |
| --- | --- |
| ```180181182183184185186187188189190``` | ```md-code__content@abc.abstractmethoddef get_stt_model(self, model_name: str | None) -> STTModel:    """Get a speech-to-text model by name.    Args:        model_name: The name of the model to get.    Returns:        The speech-to-text model.    """    pass``` |

#### get\_tts\_model`abstractmethod`

```
get_tts_model(model_name: str | None) -> TTSModel

```

Get a text-to-speech model by name.

Source code in `src/agents/voice/model.py`

|  |  |
| --- | --- |
| ```192193194``` | ```md-code__content@abc.abstractmethoddef get_tts_model(self, model_name: str | None) -> TTSModel:    """Get a text-to-speech model by name."""``` |