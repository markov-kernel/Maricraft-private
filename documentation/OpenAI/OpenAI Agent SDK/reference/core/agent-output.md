---
title: `Agent output`
source: https://openai.github.io/openai-agents-python/ref/agent_output/
---

# `Agent output`

### AgentOutputSchemaBase

Bases: `ABC`

An object that captures the JSON schema of the output, as well as validating/parsing JSON
produced by the LLM into the output type.

Source code in `src/agents/agent_output.py`

|  |  |
| --- | --- |
| ```161718192021222324252627282930313233343536373839404142434445464748495051``` | ```md-code__contentclass AgentOutputSchemaBase(abc.ABC):    """An object that captures the JSON schema of the output, as well as validating/parsing JSON    produced by the LLM into the output type.    """    @abc.abstractmethod    def is_plain_text(self) -> bool:        """Whether the output type is plain text (versus a JSON object)."""        pass    @abc.abstractmethod    def name(self) -> str:        """The name of the output type."""        pass    @abc.abstractmethod    def json_schema(self) -> dict[str, Any]:        """Returns the JSON schema of the output. Will only be called if the output type is not        plain text.        """        pass    @abc.abstractmethod    def is_strict_json_schema(self) -> bool:        """Whether the JSON schema is in strict mode. Strict mode constrains the JSON schema        features, but guarantees valid JSON. See here for details:        https://platform.openai.com/docs/guides/structured-outputs#supported-schemas        """        pass    @abc.abstractmethod    def validate_json(self, json_str: str) -> Any:        """Validate a JSON string against the output type. You must return the validated object,        or raise a `ModelBehaviorError` if the JSON is invalid.        """        pass``` |

#### is\_plain\_text`abstractmethod`

```
is_plain_text() -> bool

```

Whether the output type is plain text (versus a JSON object).

Source code in `src/agents/agent_output.py`

|  |  |
| --- | --- |
| ```21222324``` | ```md-code__content@abc.abstractmethoddef is_plain_text(self) -> bool:    """Whether the output type is plain text (versus a JSON object)."""    pass``` |

#### name`abstractmethod`

```
name() -> str

```

The name of the output type.

Source code in `src/agents/agent_output.py`

|  |  |
| --- | --- |
| ```26272829``` | ```md-code__content@abc.abstractmethoddef name(self) -> str:    """The name of the output type."""    pass``` |

#### json\_schema`abstractmethod`

```
json_schema() -> dict[str, Any]

```

Returns the JSON schema of the output. Will only be called if the output type is not
plain text.

Source code in `src/agents/agent_output.py`

|  |  |
| --- | --- |
| ```313233343536``` | ```md-code__content@abc.abstractmethoddef json_schema(self) -> dict[str, Any]:    """Returns the JSON schema of the output. Will only be called if the output type is not    plain text.    """    pass``` |

#### is\_strict\_json\_schema`abstractmethod`

```
is_strict_json_schema() -> bool

```

Whether the JSON schema is in strict mode. Strict mode constrains the JSON schema
features, but guarantees valid JSON. See here for details:
https://platform.openai.com/docs/guides/structured-outputs#supported-schemas

Source code in `src/agents/agent_output.py`

|  |  |
| --- | --- |
| ```38394041424344``` | ```md-code__content@abc.abstractmethoddef is_strict_json_schema(self) -> bool:    """Whether the JSON schema is in strict mode. Strict mode constrains the JSON schema    features, but guarantees valid JSON. See here for details:    https://platform.openai.com/docs/guides/structured-outputs#supported-schemas    """    pass``` |

#### validate\_json`abstractmethod`

```
validate_json(json_str: str) -> Any

```

Validate a JSON string against the output type. You must return the validated object,
or raise a `ModelBehaviorError` if the JSON is invalid.

Source code in `src/agents/agent_output.py`

|  |  |
| --- | --- |
| ```464748495051``` | ```md-code__content@abc.abstractmethoddef validate_json(self, json_str: str) -> Any:    """Validate a JSON string against the output type. You must return the validated object,    or raise a `ModelBehaviorError` if the JSON is invalid.    """    pass``` |

### AgentOutputSchema`dataclass`

Bases: `AgentOutputSchemaBase`

An object that captures the JSON schema of the output, as well as validating/parsing JSON
produced by the LLM into the output type.

Source code in `src/agents/agent_output.py`

|  |  |
| --- | --- |
| ``` 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99100101102103104105106107108109110111112113114115116117118119120121122123124125126127128129130131132133134135136137138139140141142143144145146147148149150151152153154155156157158159160161162163164165166167168``` | ```md-code__content@dataclass(init=False)class AgentOutputSchema(AgentOutputSchemaBase):    """An object that captures the JSON schema of the output, as well as validating/parsing JSON    produced by the LLM into the output type.    """    output_type: type[Any]    """The type of the output."""    _type_adapter: TypeAdapter[Any]    """A type adapter that wraps the output type, so that we can validate JSON."""    _is_wrapped: bool    """Whether the output type is wrapped in a dictionary. This is generally done if the base    output type cannot be represented as a JSON Schema object.    """    _output_schema: dict[str, Any]    """The JSON schema of the output."""    _strict_json_schema: bool    """Whether the JSON schema is in strict mode. We **strongly** recommend setting this to True,    as it increases the likelihood of correct JSON input.    """    def __init__(self, output_type: type[Any], strict_json_schema: bool = True):        """        Args:            output_type: The type of the output.            strict_json_schema: Whether the JSON schema is in strict mode. We **strongly** recommend                setting this to True, as it increases the likelihood of correct JSON input.        """        self.output_type = output_type        self._strict_json_schema = strict_json_schema        if output_type is None or output_type is str:            self._is_wrapped = False            self._type_adapter = TypeAdapter(output_type)            self._output_schema = self._type_adapter.json_schema()            return        # We should wrap for things that are not plain text, and for things that would definitely        # not be a JSON Schema object.        self._is_wrapped = not _is_subclass_of_base_model_or_dict(output_type)        if self._is_wrapped:            OutputType = TypedDict(                "OutputType",                {                    _WRAPPER_DICT_KEY: output_type,  # type: ignore                },            )            self._type_adapter = TypeAdapter(OutputType)            self._output_schema = self._type_adapter.json_schema()        else:            self._type_adapter = TypeAdapter(output_type)            self._output_schema = self._type_adapter.json_schema()        if self._strict_json_schema:            try:                self._output_schema = ensure_strict_json_schema(self._output_schema)            except UserError as e:                raise UserError(                    "Strict JSON schema is enabled, but the output type is not valid. "                    "Either make the output type strict, "                    "or wrap your type with AgentOutputSchema(your_type, strict_json_schema=False)"                ) from e    def is_plain_text(self) -> bool:        """Whether the output type is plain text (versus a JSON object)."""        return self.output_type is None or self.output_type is str    def is_strict_json_schema(self) -> bool:        """Whether the JSON schema is in strict mode."""        return self._strict_json_schema    def json_schema(self) -> dict[str, Any]:        """The JSON schema of the output type."""        if self.is_plain_text():            raise UserError("Output type is plain text, so no JSON schema is available")        return self._output_schema    def validate_json(self, json_str: str) -> Any:        """Validate a JSON string against the output type. Returns the validated object, or raises        a `ModelBehaviorError` if the JSON is invalid.        """        validated = _json.validate_json(json_str, self._type_adapter, partial=False)        if self._is_wrapped:            if not isinstance(validated, dict):                _error_tracing.attach_error_to_current_span(                    SpanError(                        message="Invalid JSON",                        data={"details": f"Expected a dict, got {type(validated)}"},                    )                )                raise ModelBehaviorError(                    f"Expected a dict, got {type(validated)} for JSON: {json_str}"                )            if _WRAPPER_DICT_KEY not in validated:                _error_tracing.attach_error_to_current_span(                    SpanError(                        message="Invalid JSON",                        data={"details": f"Could not find key {_WRAPPER_DICT_KEY} in JSON"},                    )                )                raise ModelBehaviorError(                    f"Could not find key {_WRAPPER_DICT_KEY} in JSON: {json_str}"                )            return validated[_WRAPPER_DICT_KEY]        return validated    def name(self) -> str:        """The name of the output type."""        return _type_to_str(self.output_type)``` |

#### output\_type`instance-attribute`

```
output_type: type[Any] = output_type

```

The type of the output.

#### \_\_init\_\_

```
__init__(
    output_type: type[Any], strict_json_schema: bool = True
)

```

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `output_type` | `type[Any]` | The type of the output. | _required_ |
| `strict_json_schema` | `bool` | Whether the JSON schema is in strict mode. We **strongly** recommendsetting this to True, as it increases the likelihood of correct JSON input. | `True` |

Source code in `src/agents/agent_output.py`

|  |  |
| --- | --- |
| ``` 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99100101102103104105106107108109110111112113114115116117118119120``` | ```md-code__contentdef __init__(self, output_type: type[Any], strict_json_schema: bool = True):    """    Args:        output_type: The type of the output.        strict_json_schema: Whether the JSON schema is in strict mode. We **strongly** recommend            setting this to True, as it increases the likelihood of correct JSON input.    """    self.output_type = output_type    self._strict_json_schema = strict_json_schema    if output_type is None or output_type is str:        self._is_wrapped = False        self._type_adapter = TypeAdapter(output_type)        self._output_schema = self._type_adapter.json_schema()        return    # We should wrap for things that are not plain text, and for things that would definitely    # not be a JSON Schema object.    self._is_wrapped = not _is_subclass_of_base_model_or_dict(output_type)    if self._is_wrapped:        OutputType = TypedDict(            "OutputType",            {                _WRAPPER_DICT_KEY: output_type,  # type: ignore            },        )        self._type_adapter = TypeAdapter(OutputType)        self._output_schema = self._type_adapter.json_schema()    else:        self._type_adapter = TypeAdapter(output_type)        self._output_schema = self._type_adapter.json_schema()    if self._strict_json_schema:        try:            self._output_schema = ensure_strict_json_schema(self._output_schema)        except UserError as e:            raise UserError(                "Strict JSON schema is enabled, but the output type is not valid. "                "Either make the output type strict, "                "or wrap your type with AgentOutputSchema(your_type, strict_json_schema=False)"            ) from e``` |

#### is\_plain\_text

```
is_plain_text() -> bool

```

Whether the output type is plain text (versus a JSON object).

Source code in `src/agents/agent_output.py`

|  |  |
| --- | --- |
| ```122123124``` | ```md-code__contentdef is_plain_text(self) -> bool:    """Whether the output type is plain text (versus a JSON object)."""    return self.output_type is None or self.output_type is str``` |

#### is\_strict\_json\_schema

```
is_strict_json_schema() -> bool

```

Whether the JSON schema is in strict mode.

Source code in `src/agents/agent_output.py`

|  |  |
| --- | --- |
| ```126127128``` | ```md-code__contentdef is_strict_json_schema(self) -> bool:    """Whether the JSON schema is in strict mode."""    return self._strict_json_schema``` |

#### json\_schema

```
json_schema() -> dict[str, Any]

```

The JSON schema of the output type.

Source code in `src/agents/agent_output.py`

|  |  |
| --- | --- |
| ```130131132133134``` | ```md-code__contentdef json_schema(self) -> dict[str, Any]:    """The JSON schema of the output type."""    if self.is_plain_text():        raise UserError("Output type is plain text, so no JSON schema is available")    return self._output_schema``` |

#### validate\_json

```
validate_json(json_str: str) -> Any

```

Validate a JSON string against the output type. Returns the validated object, or raises
a `ModelBehaviorError` if the JSON is invalid.

Source code in `src/agents/agent_output.py`

|  |  |
| --- | --- |
| ```136137138139140141142143144145146147148149150151152153154155156157158159160161162163164``` | ```md-code__contentdef validate_json(self, json_str: str) -> Any:    """Validate a JSON string against the output type. Returns the validated object, or raises    a `ModelBehaviorError` if the JSON is invalid.    """    validated = _json.validate_json(json_str, self._type_adapter, partial=False)    if self._is_wrapped:        if not isinstance(validated, dict):            _error_tracing.attach_error_to_current_span(                SpanError(                    message="Invalid JSON",                    data={"details": f"Expected a dict, got {type(validated)}"},                )            )            raise ModelBehaviorError(                f"Expected a dict, got {type(validated)} for JSON: {json_str}"            )        if _WRAPPER_DICT_KEY not in validated:            _error_tracing.attach_error_to_current_span(                SpanError(                    message="Invalid JSON",                    data={"details": f"Could not find key {_WRAPPER_DICT_KEY} in JSON"},                )            )            raise ModelBehaviorError(                f"Could not find key {_WRAPPER_DICT_KEY} in JSON: {json_str}"            )        return validated[_WRAPPER_DICT_KEY]    return validated``` |

#### name

```
name() -> str

```

The name of the output type.

Source code in `src/agents/agent_output.py`

|  |  |
| --- | --- |
| ```166167168``` | ```md-code__contentdef name(self) -> str:    """The name of the output type."""    return _type_to_str(self.output_type)``` |