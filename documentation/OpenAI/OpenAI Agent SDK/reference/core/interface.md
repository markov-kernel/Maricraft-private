---
title: `Model interface`
source: https://openai.github.io/openai-agents-python/ref/models/interface/
---

# `Model interface`

### ModelTracing

Bases: `Enum`

Source code in `src/agents/models/interface.py`

|  |  |
| --- | --- |
| ```192021222324252627282930313233``` | ```md-code__contentclass ModelTracing(enum.Enum):    DISABLED = 0    """Tracing is disabled entirely."""    ENABLED = 1    """Tracing is enabled, and all data is included."""    ENABLED_WITHOUT_DATA = 2    """Tracing is enabled, but inputs/outputs are not included."""    def is_disabled(self) -> bool:        return self == ModelTracing.DISABLED    def include_data(self) -> bool:        return self == ModelTracing.ENABLED``` |

#### DISABLED`class-attribute``instance-attribute`

```
DISABLED = 0

```

Tracing is disabled entirely.

#### ENABLED`class-attribute``instance-attribute`

```
ENABLED = 1

```

Tracing is enabled, and all data is included.

#### ENABLED\_WITHOUT\_DATA`class-attribute``instance-attribute`

```
ENABLED_WITHOUT_DATA = 2

```

Tracing is enabled, but inputs/outputs are not included.

### Model

Bases: `ABC`

The base interface for calling an LLM.

Source code in `src/agents/models/interface.py`

|  |  |
| --- | --- |
| ``` 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99100101102103``` | ```md-code__contentclass Model(abc.ABC):    """The base interface for calling an LLM."""    @abc.abstractmethod    async def get_response(        self,        system_instructions: str | None,        input: str | list[TResponseInputItem],        model_settings: ModelSettings,        tools: list[Tool],        output_schema: AgentOutputSchemaBase | None,        handoffs: list[Handoff],        tracing: ModelTracing,        *,        previous_response_id: str | None,        prompt: ResponsePromptParam | None,    ) -> ModelResponse:        """Get a response from the model.        Args:            system_instructions: The system instructions to use.            input: The input items to the model, in OpenAI Responses format.            model_settings: The model settings to use.            tools: The tools available to the model.            output_schema: The output schema to use.            handoffs: The handoffs available to the model.            tracing: Tracing configuration.            previous_response_id: the ID of the previous response. Generally not used by the model,                except for the OpenAI Responses API.            prompt: The prompt config to use for the model.        Returns:            The full model response.        """        pass    @abc.abstractmethod    def stream_response(        self,        system_instructions: str | None,        input: str | list[TResponseInputItem],        model_settings: ModelSettings,        tools: list[Tool],        output_schema: AgentOutputSchemaBase | None,        handoffs: list[Handoff],        tracing: ModelTracing,        *,        previous_response_id: str | None,        prompt: ResponsePromptParam | None,    ) -> AsyncIterator[TResponseStreamEvent]:        """Stream a response from the model.        Args:            system_instructions: The system instructions to use.            input: The input items to the model, in OpenAI Responses format.            model_settings: The model settings to use.            tools: The tools available to the model.            output_schema: The output schema to use.            handoffs: The handoffs available to the model.            tracing: Tracing configuration.            previous_response_id: the ID of the previous response. Generally not used by the model,                except for the OpenAI Responses API.            prompt: The prompt config to use for the model.        Returns:            An iterator of response stream events, in OpenAI Responses format.        """        pass``` |

#### get\_response`abstractmethod``async`

```
get_response(
    system_instructions: str | None,
    input: str | list[TResponseInputItem],
    model_settings: ModelSettings,
    tools: list[Tool],
    output_schema: AgentOutputSchemaBase | None,
    handoffs: list[Handoff],
    tracing: ModelTracing,
    *,
    previous_response_id: str | None,
    prompt: ResponsePromptParam | None,
) -> ModelResponse

```

Get a response from the model.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `system_instructions` | `str | None` | The system instructions to use. | _required_ |
| `input` | `str | list[TResponseInputItem]` | The input items to the model, in OpenAI Responses format. | _required_ |
| `model_settings` | `ModelSettings` | The model settings to use. | _required_ |
| `tools` | `list[Tool]` | The tools available to the model. | _required_ |
| `output_schema` | `AgentOutputSchemaBase | None` | The output schema to use. | _required_ |
| `handoffs` | `list[Handoff]` | The handoffs available to the model. | _required_ |
| `tracing` | `ModelTracing` | Tracing configuration. | _required_ |
| `previous_response_id` | `str | None` | the ID of the previous response. Generally not used by the model,except for the OpenAI Responses API. | _required_ |
| `prompt` | `ResponsePromptParam | None` | The prompt config to use for the model. | _required_ |

Returns:

| Type | Description |
| --- | --- |
| `ModelResponse` | The full model response. |

Source code in `src/agents/models/interface.py`

|  |  |
| --- | --- |
| ```3940414243444546474849505152535455565758596061626364656667686970``` | ```md-code__content@abc.abstractmethodasync def get_response(    self,    system_instructions: str | None,    input: str | list[TResponseInputItem],    model_settings: ModelSettings,    tools: list[Tool],    output_schema: AgentOutputSchemaBase | None,    handoffs: list[Handoff],    tracing: ModelTracing,    *,    previous_response_id: str | None,    prompt: ResponsePromptParam | None,) -> ModelResponse:    """Get a response from the model.    Args:        system_instructions: The system instructions to use.        input: The input items to the model, in OpenAI Responses format.        model_settings: The model settings to use.        tools: The tools available to the model.        output_schema: The output schema to use.        handoffs: The handoffs available to the model.        tracing: Tracing configuration.        previous_response_id: the ID of the previous response. Generally not used by the model,            except for the OpenAI Responses API.        prompt: The prompt config to use for the model.    Returns:        The full model response.    """    pass``` |

#### stream\_response`abstractmethod`

```
stream_response(
    system_instructions: str | None,
    input: str | list[TResponseInputItem],
    model_settings: ModelSettings,
    tools: list[Tool],
    output_schema: AgentOutputSchemaBase | None,
    handoffs: list[Handoff],
    tracing: ModelTracing,
    *,
    previous_response_id: str | None,
    prompt: ResponsePromptParam | None,
) -> AsyncIterator[TResponseStreamEvent]

```

Stream a response from the model.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `system_instructions` | `str | None` | The system instructions to use. | _required_ |
| `input` | `str | list[TResponseInputItem]` | The input items to the model, in OpenAI Responses format. | _required_ |
| `model_settings` | `ModelSettings` | The model settings to use. | _required_ |
| `tools` | `list[Tool]` | The tools available to the model. | _required_ |
| `output_schema` | `AgentOutputSchemaBase | None` | The output schema to use. | _required_ |
| `handoffs` | `list[Handoff]` | The handoffs available to the model. | _required_ |
| `tracing` | `ModelTracing` | Tracing configuration. | _required_ |
| `previous_response_id` | `str | None` | the ID of the previous response. Generally not used by the model,except for the OpenAI Responses API. | _required_ |
| `prompt` | `ResponsePromptParam | None` | The prompt config to use for the model. | _required_ |

Returns:

| Type | Description |
| --- | --- |
| `AsyncIterator[TResponseStreamEvent]` | An iterator of response stream events, in OpenAI Responses format. |

Source code in `src/agents/models/interface.py`

|  |  |
| --- | --- |
| ``` 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99100101102103``` | ```md-code__content@abc.abstractmethoddef stream_response(    self,    system_instructions: str | None,    input: str | list[TResponseInputItem],    model_settings: ModelSettings,    tools: list[Tool],    output_schema: AgentOutputSchemaBase | None,    handoffs: list[Handoff],    tracing: ModelTracing,    *,    previous_response_id: str | None,    prompt: ResponsePromptParam | None,) -> AsyncIterator[TResponseStreamEvent]:    """Stream a response from the model.    Args:        system_instructions: The system instructions to use.        input: The input items to the model, in OpenAI Responses format.        model_settings: The model settings to use.        tools: The tools available to the model.        output_schema: The output schema to use.        handoffs: The handoffs available to the model.        tracing: Tracing configuration.        previous_response_id: the ID of the previous response. Generally not used by the model,            except for the OpenAI Responses API.        prompt: The prompt config to use for the model.    Returns:        An iterator of response stream events, in OpenAI Responses format.    """    pass``` |

### ModelProvider

Bases: `ABC`

The base interface for a model provider.

Model provider is responsible for looking up Models by name.

Source code in `src/agents/models/interface.py`

|  |  |
| --- | --- |
| ```106107108109110111112113114115116117118119120121``` | ```md-code__contentclass ModelProvider(abc.ABC):    """The base interface for a model provider.    Model provider is responsible for looking up Models by name.    """    @abc.abstractmethod    def get_model(self, model_name: str | None) -> Model:        """Get a model by name.        Args:            model_name: The name of the model to get.        Returns:            The model.        """``` |

#### get\_model`abstractmethod`

```
get_model(model_name: str | None) -> Model

```

Get a model by name.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `model_name` | `str | None` | The name of the model to get. | _required_ |

Returns:

| Type | Description |
| --- | --- |
| `Model` | The model. |

Source code in `src/agents/models/interface.py`

|  |  |
| --- | --- |
| ```112113114115116117118119120121``` | ```md-code__content@abc.abstractmethoddef get_model(self, model_name: str | None) -> Model:    """Get a model by name.    Args:        model_name: The name of the model to get.    Returns:        The model.    """``` |