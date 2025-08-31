---
title: Agents module
source: https://openai.github.io/openai-agents-python/ref/
---

# Agents module

### set\_default\_openai\_key

```
set_default_openai_key(
    key: str, use_for_tracing: bool = True
) -> None

```

Set the default OpenAI API key to use for LLM requests (and optionally tracing(). This is
only necessary if the OPENAI\_API\_KEY environment variable is not already set.

If provided, this key will be used instead of the OPENAI\_API\_KEY environment variable.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `key` | `str` | The OpenAI key to use. | _required_ |
| `use_for_tracing` | `bool` | Whether to also use this key to send traces to OpenAI. Defaults to TrueIf False, you'll either need to set the OPENAI\_API\_KEY environment variable or callset\_tracing\_export\_api\_key() with the API key you want to use for tracing. | `True` |

Source code in `src/agents/__init__.py`

|  |  |
| --- | --- |
| ```120121122123124125126127128129130131132``` | ```md-code__contentdef set_default_openai_key(key: str, use_for_tracing: bool = True) -> None:    """Set the default OpenAI API key to use for LLM requests (and optionally tracing(). This is    only necessary if the OPENAI_API_KEY environment variable is not already set.    If provided, this key will be used instead of the OPENAI_API_KEY environment variable.    Args:        key: The OpenAI key to use.        use_for_tracing: Whether to also use this key to send traces to OpenAI. Defaults to True            If False, you'll either need to set the OPENAI_API_KEY environment variable or call            set_tracing_export_api_key() with the API key you want to use for tracing.    """    _config.set_default_openai_key(key, use_for_tracing)``` |

### set\_default\_openai\_client

```
set_default_openai_client(
    client: AsyncOpenAI, use_for_tracing: bool = True
) -> None

```

Set the default OpenAI client to use for LLM requests and/or tracing. If provided, this
client will be used instead of the default OpenAI client.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `client` | `AsyncOpenAI` | The OpenAI client to use. | _required_ |
| `use_for_tracing` | `bool` | Whether to use the API key from this client for uploading traces. If False,you'll either need to set the OPENAI\_API\_KEY environment variable or callset\_tracing\_export\_api\_key() with the API key you want to use for tracing. | `True` |

Source code in `src/agents/__init__.py`

|  |  |
| --- | --- |
| ```135136137138139140141142143144145``` | ```md-code__contentdef set_default_openai_client(client: AsyncOpenAI, use_for_tracing: bool = True) -> None:    """Set the default OpenAI client to use for LLM requests and/or tracing. If provided, this    client will be used instead of the default OpenAI client.    Args:        client: The OpenAI client to use.        use_for_tracing: Whether to use the API key from this client for uploading traces. If False,            you'll either need to set the OPENAI_API_KEY environment variable or call            set_tracing_export_api_key() with the API key you want to use for tracing.    """    _config.set_default_openai_client(client, use_for_tracing)``` |

### set\_default\_openai\_api

```
set_default_openai_api(
    api: Literal["chat_completions", "responses"],
) -> None

```

Set the default API to use for OpenAI LLM requests. By default, we will use the responses API
but you can set this to use the chat completions API instead.

Source code in `src/agents/__init__.py`

|  |  |
| --- | --- |
| ```148149150151152``` | ```md-code__contentdef set_default_openai_api(api: Literal["chat_completions", "responses"]) -> None:    """Set the default API to use for OpenAI LLM requests. By default, we will use the responses API    but you can set this to use the chat completions API instead.    """    _config.set_default_openai_api(api)``` |

### set\_tracing\_export\_api\_key

```
set_tracing_export_api_key(api_key: str) -> None

```

Set the OpenAI API key for the backend exporter.

Source code in `src/agents/tracing/__init__.py`

|  |  |
| --- | --- |
| ```104105106107108``` | ```md-code__contentdef set_tracing_export_api_key(api_key: str) -> None:    """    Set the OpenAI API key for the backend exporter.    """    default_exporter().set_api_key(api_key)``` |

### set\_tracing\_disabled

```
set_tracing_disabled(disabled: bool) -> None

```

Set whether tracing is globally disabled.

Source code in `src/agents/tracing/__init__.py`

|  |  |
| --- | --- |
| ``` 97 98 99100101``` | ```md-code__contentdef set_tracing_disabled(disabled: bool) -> None:    """    Set whether tracing is globally disabled.    """    get_trace_provider().set_disabled(disabled)``` |

### set\_trace\_processors

```
set_trace_processors(
    processors: list[TracingProcessor],
) -> None

```

Set the list of trace processors. This will replace the current list of processors.

Source code in `src/agents/tracing/__init__.py`

|  |  |
| --- | --- |
| ```9091929394``` | ```md-code__contentdef set_trace_processors(processors: list[TracingProcessor]) -> None:    """    Set the list of trace processors. This will replace the current list of processors.    """    get_trace_provider().set_processors(processors)``` |

### enable\_verbose\_stdout\_logging

```
enable_verbose_stdout_logging()

```

Enables verbose logging to stdout. This is useful for debugging.

Source code in `src/agents/__init__.py`

|  |  |
| --- | --- |
| ```155156157158159``` | ```md-code__contentdef enable_verbose_stdout_logging():    """Enables verbose logging to stdout. This is useful for debugging."""    logger = logging.getLogger("openai.agents")    logger.setLevel(logging.DEBUG)    logger.addHandler(logging.StreamHandler(sys.stdout))``` |