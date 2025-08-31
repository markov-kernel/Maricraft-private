---
title: `Model settings`
source: https://openai.github.io/openai-agents-python/ref/model_settings/
---

# `Model settings`

### ModelSettings

Settings to use when calling an LLM.

This class holds optional model configuration parameters (e.g. temperature,
top\_p, penalties, truncation, etc.).

Not all models/providers support all of these parameters, so please check the API documentation
for the specific model and provider you are using.

Source code in `src/agents/model_settings.py`

|  |  |
| --- | --- |
| ``` 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99100101102103104105106107108109110111112113114115116117118119120121122123124125126127128129130131132133134135136137138139140141142143144145146147148149150151152153154155156157158159160161162163164165166167168169170``` | ```md-code__content@dataclassclass ModelSettings:    """Settings to use when calling an LLM.    This class holds optional model configuration parameters (e.g. temperature,    top_p, penalties, truncation, etc.).    Not all models/providers support all of these parameters, so please check the API documentation    for the specific model and provider you are using.    """    temperature: float | None = None    """The temperature to use when calling the model."""    top_p: float | None = None    """The top_p to use when calling the model."""    frequency_penalty: float | None = None    """The frequency penalty to use when calling the model."""    presence_penalty: float | None = None    """The presence penalty to use when calling the model."""    tool_choice: ToolChoice | None = None    """The tool choice to use when calling the model."""    parallel_tool_calls: bool | None = None    """Controls whether the model can make multiple parallel tool calls in a single turn.    If not provided (i.e., set to None), this behavior defers to the underlying    model provider's default. For most current providers (e.g., OpenAI), this typically    means parallel tool calls are enabled (True).    Set to True to explicitly enable parallel tool calls, or False to restrict the    model to at most one tool call per turn.    """    truncation: Literal["auto", "disabled"] | None = None    """The truncation strategy to use when calling the model."""    max_tokens: int | None = None    """The maximum number of output tokens to generate."""    reasoning: Reasoning | None = None    """Configuration options for    [reasoning models](https://platform.openai.com/docs/guides/reasoning).    """    metadata: dict[str, str] | None = None    """Metadata to include with the model response call."""    store: bool | None = None    """Whether to store the generated model response for later retrieval.    Defaults to True if not provided."""    include_usage: bool | None = None    """Whether to include usage chunk.    Defaults to True if not provided."""    response_include: list[ResponseIncludable] | None = None    """Additional output data to include in the model response.    [include parameter](https://platform.openai.com/docs/api-reference/responses/create#responses-create-include)"""    extra_query: Query | None = None    """Additional query fields to provide with the request.    Defaults to None if not provided."""    extra_body: Body | None = None    """Additional body fields to provide with the request.    Defaults to None if not provided."""    extra_headers: Headers | None = None    """Additional headers to provide with the request.    Defaults to None if not provided."""    extra_args: dict[str, Any] | None = None    """Arbitrary keyword arguments to pass to the model API call.    These will be passed directly to the underlying model provider's API.    Use with caution as not all models support all parameters."""    def resolve(self, override: ModelSettings | None) -> ModelSettings:        """Produce a new ModelSettings by overlaying any non-None values from the        override on top of this instance."""        if override is None:            return self        changes = {            field.name: getattr(override, field.name)            for field in fields(self)            if getattr(override, field.name) is not None        }        # Handle extra_args merging specially - merge dictionaries instead of replacing        if self.extra_args is not None or override.extra_args is not None:            merged_args = {}            if self.extra_args:                merged_args.update(self.extra_args)            if override.extra_args:                merged_args.update(override.extra_args)            changes["extra_args"] = merged_args if merged_args else None        return replace(self, **changes)    def to_json_dict(self) -> dict[str, Any]:        dataclass_dict = dataclasses.asdict(self)        json_dict: dict[str, Any] = {}        for field_name, value in dataclass_dict.items():            if isinstance(value, BaseModel):                json_dict[field_name] = value.model_dump(mode="json")            else:                json_dict[field_name] = value        return json_dict``` |

#### temperature`class-attribute``instance-attribute`

```
temperature: float | None = None

```

The temperature to use when calling the model.

#### top\_p`class-attribute``instance-attribute`

```
top_p: float | None = None

```

The top\_p to use when calling the model.

#### frequency\_penalty`class-attribute``instance-attribute`

```
frequency_penalty: float | None = None

```

The frequency penalty to use when calling the model.

#### presence\_penalty`class-attribute``instance-attribute`

```
presence_penalty: float | None = None

```

The presence penalty to use when calling the model.

#### tool\_choice`class-attribute``instance-attribute`

```
tool_choice: ToolChoice | None = None

```

The tool choice to use when calling the model.

#### parallel\_tool\_calls`class-attribute``instance-attribute`

```
parallel_tool_calls: bool | None = None

```

Controls whether the model can make multiple parallel tool calls in a single turn.
If not provided (i.e., set to None), this behavior defers to the underlying
model provider's default. For most current providers (e.g., OpenAI), this typically
means parallel tool calls are enabled (True).
Set to True to explicitly enable parallel tool calls, or False to restrict the
model to at most one tool call per turn.

#### truncation`class-attribute``instance-attribute`

```
truncation: Literal['auto', 'disabled'] | None = None

```

The truncation strategy to use when calling the model.

#### max\_tokens`class-attribute``instance-attribute`

```
max_tokens: int | None = None

```

The maximum number of output tokens to generate.

#### reasoning`class-attribute``instance-attribute`

```
reasoning: Reasoning | None = None

```

Configuration options for
[reasoning models](https://platform.openai.com/docs/guides/reasoning).

#### metadata`class-attribute``instance-attribute`

```
metadata: dict[str, str] | None = None

```

Metadata to include with the model response call.

#### store`class-attribute``instance-attribute`

```
store: bool | None = None

```

Whether to store the generated model response for later retrieval.
Defaults to True if not provided.

#### include\_usage`class-attribute``instance-attribute`

```
include_usage: bool | None = None

```

Whether to include usage chunk.
Defaults to True if not provided.

#### response\_include`class-attribute``instance-attribute`

```
response_include: list[ResponseIncludable] | None = None

```

Additional output data to include in the model response.
[include parameter](https://platform.openai.com/docs/api-reference/responses/create#responses-create-include)

#### extra\_query`class-attribute``instance-attribute`

```
extra_query: Query | None = None

```

Additional query fields to provide with the request.
Defaults to None if not provided.

#### extra\_body`class-attribute``instance-attribute`

```
extra_body: Body | None = None

```

Additional body fields to provide with the request.
Defaults to None if not provided.

#### extra\_headers`class-attribute``instance-attribute`

```
extra_headers: Headers | None = None

```

Additional headers to provide with the request.
Defaults to None if not provided.

#### extra\_args`class-attribute``instance-attribute`

```
extra_args: dict[str, Any] | None = None

```

Arbitrary keyword arguments to pass to the model API call.
These will be passed directly to the underlying model provider's API.
Use with caution as not all models support all parameters.

#### resolve

```
resolve(override: ModelSettings | None) -> ModelSettings

```

Produce a new ModelSettings by overlaying any non-None values from the
override on top of this instance.

Source code in `src/agents/model_settings.py`

|  |  |
| --- | --- |
| ```136137138139140141142143144145146147148149150151152153154155156157``` | ```md-code__contentdef resolve(self, override: ModelSettings | None) -> ModelSettings:    """Produce a new ModelSettings by overlaying any non-None values from the    override on top of this instance."""    if override is None:        return self    changes = {        field.name: getattr(override, field.name)        for field in fields(self)        if getattr(override, field.name) is not None    }    # Handle extra_args merging specially - merge dictionaries instead of replacing    if self.extra_args is not None or override.extra_args is not None:        merged_args = {}        if self.extra_args:            merged_args.update(self.extra_args)        if override.extra_args:            merged_args.update(override.extra_args)        changes["extra_args"] = merged_args if merged_args else None    return replace(self, **changes)``` |