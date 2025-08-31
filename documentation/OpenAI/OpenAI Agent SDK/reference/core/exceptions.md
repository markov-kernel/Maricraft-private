---
title: `Exceptions`
source: https://openai.github.io/openai-agents-python/ref/exceptions/
---

# `Exceptions`

### RunErrorDetails`dataclass`

Data collected from an agent run when an exception occurs.

Source code in `src/agents/exceptions.py`

|  |  |
| --- | --- |
| ```1516171819202122232425262728``` | ```md-code__content@dataclassclass RunErrorDetails:    """Data collected from an agent run when an exception occurs."""    input: str | list[TResponseInputItem]    new_items: list[RunItem]    raw_responses: list[ModelResponse]    last_agent: Agent[Any]    context_wrapper: RunContextWrapper[Any]    input_guardrail_results: list[InputGuardrailResult]    output_guardrail_results: list[OutputGuardrailResult]    def __str__(self) -> str:        return pretty_print_run_error_details(self)``` |

### AgentsException

Bases: `Exception`

Base class for all exceptions in the Agents SDK.

Source code in `src/agents/exceptions.py`

|  |  |
| --- | --- |
| ```3132333435363738``` | ```md-code__contentclass AgentsException(Exception):    """Base class for all exceptions in the Agents SDK."""    run_data: RunErrorDetails | None    def __init__(self, *args: object) -> None:        super().__init__(*args)        self.run_data = None``` |

### MaxTurnsExceeded

Bases: `AgentsException`

Exception raised when the maximum number of turns is exceeded.

Source code in `src/agents/exceptions.py`

|  |  |
| --- | --- |
| ```4142434445464748``` | ```md-code__contentclass MaxTurnsExceeded(AgentsException):    """Exception raised when the maximum number of turns is exceeded."""    message: str    def __init__(self, message: str):        self.message = message        super().__init__(message)``` |

### ModelBehaviorError

Bases: `AgentsException`

Exception raised when the model does something unexpected, e.g. calling a tool that doesn't
exist, or providing malformed JSON.

Source code in `src/agents/exceptions.py`

|  |  |
| --- | --- |
| ```51525354555657585960``` | ```md-code__contentclass ModelBehaviorError(AgentsException):    """Exception raised when the model does something unexpected, e.g. calling a tool that doesn't    exist, or providing malformed JSON.    """    message: str    def __init__(self, message: str):        self.message = message        super().__init__(message)``` |

### UserError

Bases: `AgentsException`

Exception raised when the user makes an error using the SDK.

Source code in `src/agents/exceptions.py`

|  |  |
| --- | --- |
| ```6364656667686970``` | ```md-code__contentclass UserError(AgentsException):    """Exception raised when the user makes an error using the SDK."""    message: str    def __init__(self, message: str):        self.message = message        super().__init__(message)``` |

### InputGuardrailTripwireTriggered

Bases: `AgentsException`

Exception raised when a guardrail tripwire is triggered.

Source code in `src/agents/exceptions.py`

|  |  |
| --- | --- |
| ```7374757677787980818283``` | ```md-code__contentclass InputGuardrailTripwireTriggered(AgentsException):    """Exception raised when a guardrail tripwire is triggered."""    guardrail_result: InputGuardrailResult    """The result data of the guardrail that was triggered."""    def __init__(self, guardrail_result: InputGuardrailResult):        self.guardrail_result = guardrail_result        super().__init__(            f"Guardrail {guardrail_result.guardrail.__class__.__name__} triggered tripwire"        )``` |

#### guardrail\_result`instance-attribute`

```
guardrail_result: InputGuardrailResult = guardrail_result

```

The result data of the guardrail that was triggered.

### OutputGuardrailTripwireTriggered

Bases: `AgentsException`

Exception raised when a guardrail tripwire is triggered.

Source code in `src/agents/exceptions.py`

|  |  |
| --- | --- |
| ```8687888990919293949596``` | ```md-code__contentclass OutputGuardrailTripwireTriggered(AgentsException):    """Exception raised when a guardrail tripwire is triggered."""    guardrail_result: OutputGuardrailResult    """The result data of the guardrail that was triggered."""    def __init__(self, guardrail_result: OutputGuardrailResult):        self.guardrail_result = guardrail_result        super().__init__(            f"Guardrail {guardrail_result.guardrail.__class__.__name__} triggered tripwire"        )``` |

#### guardrail\_result`instance-attribute`

```
guardrail_result: OutputGuardrailResult = guardrail_result

```

The result data of the guardrail that was triggered.