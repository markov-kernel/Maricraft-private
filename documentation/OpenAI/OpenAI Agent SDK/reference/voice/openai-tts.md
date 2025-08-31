---
title: `OpenAI TTS`
source: https://openai.github.io/openai-agents-python/ref/voice/models/openai_tts/
---

# `OpenAI TTS`

### OpenAITTSModel

Bases: `TTSModel`

A text-to-speech model for OpenAI.

Source code in `src/agents/voice/models/openai_tts.py`

|  |  |
| --- | --- |
| ```1112131415161718192021222324252627282930313233343536373839404142434445464748495051525354``` | ```md-code__contentclass OpenAITTSModel(TTSModel):    """A text-to-speech model for OpenAI."""    def __init__(        self,        model: str,        openai_client: AsyncOpenAI,    ):        """Create a new OpenAI text-to-speech model.        Args:            model: The name of the model to use.            openai_client: The OpenAI client to use.        """        self.model = model        self._client = openai_client    @property    def model_name(self) -> str:        return self.model    async def run(self, text: str, settings: TTSModelSettings) -> AsyncIterator[bytes]:        """Run the text-to-speech model.        Args:            text: The text to convert to speech.            settings: The settings to use for the text-to-speech model.        Returns:            An iterator of audio chunks.        """        response = self._client.audio.speech.with_streaming_response.create(            model=self.model,            voice=settings.voice or DEFAULT_VOICE,            input=text,            response_format="pcm",            extra_body={                "instructions": settings.instructions,            },        )        async with response as stream:            async for chunk in stream.iter_bytes(chunk_size=1024):                yield chunk``` |

#### \_\_init\_\_

```
__init__(model: str, openai_client: AsyncOpenAI)

```

Create a new OpenAI text-to-speech model.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `model` | `str` | The name of the model to use. | _required_ |
| `openai_client` | `AsyncOpenAI` | The OpenAI client to use. | _required_ |

Source code in `src/agents/voice/models/openai_tts.py`

|  |  |
| --- | --- |
| ```14151617181920212223242526``` | ```md-code__contentdef __init__(    self,    model: str,    openai_client: AsyncOpenAI,):    """Create a new OpenAI text-to-speech model.    Args:        model: The name of the model to use.        openai_client: The OpenAI client to use.    """    self.model = model    self._client = openai_client``` |

#### run`async`

```
run(
    text: str, settings: TTSModelSettings
) -> AsyncIterator[bytes]

```

Run the text-to-speech model.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `text` | `str` | The text to convert to speech. | _required_ |
| `settings` | `TTSModelSettings` | The settings to use for the text-to-speech model. | _required_ |

Returns:

| Type | Description |
| --- | --- |
| `AsyncIterator[bytes]` | An iterator of audio chunks. |

Source code in `src/agents/voice/models/openai_tts.py`

|  |  |
| --- | --- |
| ```3233343536373839404142434445464748495051525354``` | ```md-code__contentasync def run(self, text: str, settings: TTSModelSettings) -> AsyncIterator[bytes]:    """Run the text-to-speech model.    Args:        text: The text to convert to speech.        settings: The settings to use for the text-to-speech model.    Returns:        An iterator of audio chunks.    """    response = self._client.audio.speech.with_streaming_response.create(        model=self.model,        voice=settings.voice or DEFAULT_VOICE,        input=text,        response_format="pcm",        extra_body={            "instructions": settings.instructions,        },    )    async with response as stream:        async for chunk in stream.iter_bytes(chunk_size=1024):            yield chunk``` |