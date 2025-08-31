---
title: `OpenAIVoiceModelProvider`
source: https://openai.github.io/openai-agents-python/ref/voice/models/openai_provider/
---

# `OpenAIVoiceModelProvider`

### OpenAIVoiceModelProvider

Bases: `VoiceModelProvider`

A voice model provider that uses OpenAI models.

Source code in `src/agents/voice/models/openai_model_provider.py`

|  |  |
| --- | --- |
| ```2728293031323334353637383940414243444546474849505152535455565758596061626364656667686970717273747576777879808182838485868788899091929394959697``` | ```md-code__contentclass OpenAIVoiceModelProvider(VoiceModelProvider):    """A voice model provider that uses OpenAI models."""    def __init__(        self,        *,        api_key: str | None = None,        base_url: str | None = None,        openai_client: AsyncOpenAI | None = None,        organization: str | None = None,        project: str | None = None,    ) -> None:        """Create a new OpenAI voice model provider.        Args:            api_key: The API key to use for the OpenAI client. If not provided, we will use the                default API key.            base_url: The base URL to use for the OpenAI client. If not provided, we will use the                default base URL.            openai_client: An optional OpenAI client to use. If not provided, we will create a new                OpenAI client using the api_key and base_url.            organization: The organization to use for the OpenAI client.            project: The project to use for the OpenAI client.        """        if openai_client is not None:            assert api_key is None and base_url is None, (                "Don't provide api_key or base_url if you provide openai_client"            )            self._client: AsyncOpenAI | None = openai_client        else:            self._client = None            self._stored_api_key = api_key            self._stored_base_url = base_url            self._stored_organization = organization            self._stored_project = project    # We lazy load the client in case you never actually use OpenAIProvider(). Otherwise    # AsyncOpenAI() raises an error if you don't have an API key set.    def _get_client(self) -> AsyncOpenAI:        if self._client is None:            self._client = _openai_shared.get_default_openai_client() or AsyncOpenAI(                api_key=self._stored_api_key or _openai_shared.get_default_openai_key(),                base_url=self._stored_base_url,                organization=self._stored_organization,                project=self._stored_project,                http_client=shared_http_client(),            )        return self._client    def get_stt_model(self, model_name: str | None) -> STTModel:        """Get a speech-to-text model by name.        Args:            model_name: The name of the model to get.        Returns:            The speech-to-text model.        """        return OpenAISTTModel(model_name or DEFAULT_STT_MODEL, self._get_client())    def get_tts_model(self, model_name: str | None) -> TTSModel:        """Get a text-to-speech model by name.        Args:            model_name: The name of the model to get.        Returns:            The text-to-speech model.        """        return OpenAITTSModel(model_name or DEFAULT_TTS_MODEL, self._get_client())``` |

#### \_\_init\_\_

```
__init__(
    *,
    api_key: str | None = None,
    base_url: str | None = None,
    openai_client: AsyncOpenAI | None = None,
    organization: str | None = None,
    project: str | None = None,
) -> None

```

Create a new OpenAI voice model provider.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `api_key` | `str | None` | The API key to use for the OpenAI client. If not provided, we will use thedefault API key. | `None` |
| `base_url` | `str | None` | The base URL to use for the OpenAI client. If not provided, we will use thedefault base URL. | `None` |
| `openai_client` | `AsyncOpenAI | None` | An optional OpenAI client to use. If not provided, we will create a newOpenAI client using the api\_key and base\_url. | `None` |
| `organization` | `str | None` | The organization to use for the OpenAI client. | `None` |
| `project` | `str | None` | The project to use for the OpenAI client. | `None` |

Source code in `src/agents/voice/models/openai_model_provider.py`

|  |  |
| --- | --- |
| ```3031323334353637383940414243444546474849505152535455565758596061``` | ```md-code__contentdef __init__(    self,    *,    api_key: str | None = None,    base_url: str | None = None,    openai_client: AsyncOpenAI | None = None,    organization: str | None = None,    project: str | None = None,) -> None:    """Create a new OpenAI voice model provider.    Args:        api_key: The API key to use for the OpenAI client. If not provided, we will use the            default API key.        base_url: The base URL to use for the OpenAI client. If not provided, we will use the            default base URL.        openai_client: An optional OpenAI client to use. If not provided, we will create a new            OpenAI client using the api_key and base_url.        organization: The organization to use for the OpenAI client.        project: The project to use for the OpenAI client.    """    if openai_client is not None:        assert api_key is None and base_url is None, (            "Don't provide api_key or base_url if you provide openai_client"        )        self._client: AsyncOpenAI | None = openai_client    else:        self._client = None        self._stored_api_key = api_key        self._stored_base_url = base_url        self._stored_organization = organization        self._stored_project = project``` |

#### get\_stt\_model

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

Source code in `src/agents/voice/models/openai_model_provider.py`

|  |  |
| --- | --- |
| ```77787980818283848586``` | ```md-code__contentdef get_stt_model(self, model_name: str | None) -> STTModel:    """Get a speech-to-text model by name.    Args:        model_name: The name of the model to get.    Returns:        The speech-to-text model.    """    return OpenAISTTModel(model_name or DEFAULT_STT_MODEL, self._get_client())``` |

#### get\_tts\_model

```
get_tts_model(model_name: str | None) -> TTSModel

```

Get a text-to-speech model by name.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `model_name` | `str | None` | The name of the model to get. | _required_ |

Returns:

| Type | Description |
| --- | --- |
| `TTSModel` | The text-to-speech model. |

Source code in `src/agents/voice/models/openai_model_provider.py`

|  |  |
| --- | --- |
| ```88899091929394959697``` | ```md-code__contentdef get_tts_model(self, model_name: str | None) -> TTSModel:    """Get a text-to-speech model by name.    Args:        model_name: The name of the model to get.    Returns:        The text-to-speech model.    """    return OpenAITTSModel(model_name or DEFAULT_TTS_MODEL, self._get_client())``` |