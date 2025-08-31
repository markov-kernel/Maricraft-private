---
title: `Guardrails`
source: https://openai.github.io/openai-agents-python/ref/guardrail/
---

# `Guardrails`

### GuardrailFunctionOutput`dataclass`

The output of a guardrail function.

Source code in `src/agents/guardrail.py`

|  |  |
| --- | --- |
| ```1920212223242526272829303132``` | ```md-code__content@dataclassclass GuardrailFunctionOutput:    """The output of a guardrail function."""    output_info: Any    """    Optional information about the guardrail's output. For example, the guardrail could include    information about the checks it performed and granular results.    """    tripwire_triggered: bool    """    Whether the tripwire was triggered. If triggered, the agent's execution will be halted.    """``` |

#### output\_info`instance-attribute`

```
output_info: Any

```

Optional information about the guardrail's output. For example, the guardrail could include
information about the checks it performed and granular results.

#### tripwire\_triggered`instance-attribute`

```
tripwire_triggered: bool

```

Whether the tripwire was triggered. If triggered, the agent's execution will be halted.

### InputGuardrailResult`dataclass`

The result of a guardrail run.

Source code in `src/agents/guardrail.py`

|  |  |
| --- | --- |
| ```3536373839404142434445``` | ```md-code__content@dataclassclass InputGuardrailResult:    """The result of a guardrail run."""    guardrail: InputGuardrail[Any]    """    The guardrail that was run.    """    output: GuardrailFunctionOutput    """The output of the guardrail function."""``` |

#### guardrail`instance-attribute`

```
guardrail: InputGuardrail[Any]

```

The guardrail that was run.

#### output`instance-attribute`

```
output: GuardrailFunctionOutput

```

The output of the guardrail function.

### OutputGuardrailResult`dataclass`

The result of a guardrail run.

Source code in `src/agents/guardrail.py`

|  |  |
| --- | --- |
| ```484950515253545556575859606162636465666768``` | ```md-code__content@dataclassclass OutputGuardrailResult:    """The result of a guardrail run."""    guardrail: OutputGuardrail[Any]    """    The guardrail that was run.    """    agent_output: Any    """    The output of the agent that was checked by the guardrail.    """    agent: Agent[Any]    """    The agent that was checked by the guardrail.    """    output: GuardrailFunctionOutput    """The output of the guardrail function."""``` |

#### guardrail`instance-attribute`

```
guardrail: OutputGuardrail[Any]

```

The guardrail that was run.

#### agent\_output`instance-attribute`

```
agent_output: Any

```

The output of the agent that was checked by the guardrail.

#### agent`instance-attribute`

```
agent: Agent[Any]

```

The agent that was checked by the guardrail.

#### output`instance-attribute`

```
output: GuardrailFunctionOutput

```

The output of the guardrail function.

### InputGuardrail`dataclass`

Bases: `Generic[TContext]`

Input guardrails are checks that run in parallel to the agent's execution.
They can be used to do things like:
\- Check if input messages are off-topic
\- Take over control of the agent's execution if an unexpected input is detected

You can use the `@input_guardrail()` decorator to turn a function into an `InputGuardrail`, or
create an `InputGuardrail` manually.

Guardrails return a `GuardrailResult`. If `result.tripwire_triggered` is `True`, the agent
execution will immediately stop and a `InputGuardrailTripwireTriggered` exception will be raised

Source code in `src/agents/guardrail.py`

|  |  |
| --- | --- |
| ``` 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99100101102103104105106107108109110111112113114115116117118119120121122123124``` | ```md-code__content@dataclassclass InputGuardrail(Generic[TContext]):    """Input guardrails are checks that run in parallel to the agent's execution.    They can be used to do things like:    - Check if input messages are off-topic    - Take over control of the agent's execution if an unexpected input is detected    You can use the `@input_guardrail()` decorator to turn a function into an `InputGuardrail`, or    create an `InputGuardrail` manually.    Guardrails return a `GuardrailResult`. If `result.tripwire_triggered` is `True`, the agent    execution will immediately stop and a `InputGuardrailTripwireTriggered` exception will be raised    """    guardrail_function: Callable[        [RunContextWrapper[TContext], Agent[Any], str | list[TResponseInputItem]],        MaybeAwaitable[GuardrailFunctionOutput],    ]    """A function that receives the agent input and the context, and returns a     `GuardrailResult`. The result marks whether the tripwire was triggered, and can optionally     include information about the guardrail's output.    """    name: str | None = None    """The name of the guardrail, used for tracing. If not provided, we'll use the guardrail    function's name.    """    def get_name(self) -> str:        if self.name:            return self.name        return self.guardrail_function.__name__    async def run(        self,        agent: Agent[Any],        input: str | list[TResponseInputItem],        context: RunContextWrapper[TContext],    ) -> InputGuardrailResult:        if not callable(self.guardrail_function):            raise UserError(f"Guardrail function must be callable, got {self.guardrail_function}")        output = self.guardrail_function(context, agent, input)        if inspect.isawaitable(output):            return InputGuardrailResult(                guardrail=self,                output=await output,            )        return InputGuardrailResult(            guardrail=self,            output=output,        )``` |

#### guardrail\_function`instance-attribute`

```
guardrail_function: Callable[\
    [\
        RunContextWrapper[TContext],\
        Agent[Any],\
        str | list[TResponseInputItem],\
    ],\
    MaybeAwaitable[GuardrailFunctionOutput],\
]

```

A function that receives the agent input and the context, and returns a
`GuardrailResult`. The result marks whether the tripwire was triggered, and can optionally
include information about the guardrail's output.

#### name`class-attribute``instance-attribute`

```
name: str | None = None

```

The name of the guardrail, used for tracing. If not provided, we'll use the guardrail
function's name.

### OutputGuardrail`dataclass`

Bases: `Generic[TContext]`

Output guardrails are checks that run on the final output of an agent.
They can be used to do check if the output passes certain validation criteria

You can use the `@output_guardrail()` decorator to turn a function into an `OutputGuardrail`,
or create an `OutputGuardrail` manually.

Guardrails return a `GuardrailResult`. If `result.tripwire_triggered` is `True`, a
`OutputGuardrailTripwireTriggered` exception will be raised.

Source code in `src/agents/guardrail.py`

|  |  |
| --- | --- |
| ```127128129130131132133134135136137138139140141142143144145146147148149150151152153154155156157158159160161162163164165166167168169170171172173174175176177178179``` | ```md-code__content@dataclassclass OutputGuardrail(Generic[TContext]):    """Output guardrails are checks that run on the final output of an agent.    They can be used to do check if the output passes certain validation criteria    You can use the `@output_guardrail()` decorator to turn a function into an `OutputGuardrail`,    or create an `OutputGuardrail` manually.    Guardrails return a `GuardrailResult`. If `result.tripwire_triggered` is `True`, a    `OutputGuardrailTripwireTriggered` exception will be raised.    """    guardrail_function: Callable[        [RunContextWrapper[TContext], Agent[Any], Any],        MaybeAwaitable[GuardrailFunctionOutput],    ]    """A function that receives the final agent, its output, and the context, and returns a     `GuardrailResult`. The result marks whether the tripwire was triggered, and can optionally     include information about the guardrail's output.    """    name: str | None = None    """The name of the guardrail, used for tracing. If not provided, we'll use the guardrail    function's name.    """    def get_name(self) -> str:        if self.name:            return self.name        return self.guardrail_function.__name__    async def run(        self, context: RunContextWrapper[TContext], agent: Agent[Any], agent_output: Any    ) -> OutputGuardrailResult:        if not callable(self.guardrail_function):            raise UserError(f"Guardrail function must be callable, got {self.guardrail_function}")        output = self.guardrail_function(context, agent, agent_output)        if inspect.isawaitable(output):            return OutputGuardrailResult(                guardrail=self,                agent=agent,                agent_output=agent_output,                output=await output,            )        return OutputGuardrailResult(            guardrail=self,            agent=agent,            agent_output=agent_output,            output=output,        )``` |

#### guardrail\_function`instance-attribute`

```
guardrail_function: Callable[\
    [RunContextWrapper[TContext], Agent[Any], Any],\
    MaybeAwaitable[GuardrailFunctionOutput],\
]

```

A function that receives the final agent, its output, and the context, and returns a
`GuardrailResult`. The result marks whether the tripwire was triggered, and can optionally
include information about the guardrail's output.

#### name`class-attribute``instance-attribute`

```
name: str | None = None

```

The name of the guardrail, used for tracing. If not provided, we'll use the guardrail
function's name.

### input\_guardrail

```
input_guardrail(
    func: _InputGuardrailFuncSync[TContext_co],
) -> InputGuardrail[TContext_co]

```

```
input_guardrail(
    func: _InputGuardrailFuncAsync[TContext_co],
) -> InputGuardrail[TContext_co]

```

```
input_guardrail(
    *, name: str | None = None
) -> Callable[\
    [\
        _InputGuardrailFuncSync[TContext_co]\
        | _InputGuardrailFuncAsync[TContext_co]\
    ],\
    InputGuardrail[TContext_co],\
]

```

```
input_guardrail(
    func: _InputGuardrailFuncSync[TContext_co]
    | _InputGuardrailFuncAsync[TContext_co]
    | None = None,
    *,
    name: str | None = None,
) -> (
    InputGuardrail[TContext_co]
    | Callable[\
        [\
            _InputGuardrailFuncSync[TContext_co]\
            | _InputGuardrailFuncAsync[TContext_co]\
        ],\
        InputGuardrail[TContext_co],\
    ]
)

```

Decorator that transforms a sync or async function into an `InputGuardrail`.
It can be used directly (no parentheses) or with keyword args, e.g.:

```
@input_guardrail
def my_sync_guardrail(...): ...

@input_guardrail(name="guardrail_name")
async def my_async_guardrail(...): ...

```

Source code in `src/agents/guardrail.py`

|  |  |
| --- | --- |
| ```217218219220221222223224225226227228229230231232233234235236237238239240241242243244245246247248249250251252253254255``` | ```md-code__contentdef input_guardrail(    func: _InputGuardrailFuncSync[TContext_co] | _InputGuardrailFuncAsync[TContext_co] | None = None,    *,    name: str | None = None,) -> (    InputGuardrail[TContext_co] | Callable[        [_InputGuardrailFuncSync[TContext_co] | _InputGuardrailFuncAsync[TContext_co]],        InputGuardrail[TContext_co],    ]):    """    Decorator that transforms a sync or async function into an `InputGuardrail`.    It can be used directly (no parentheses) or with keyword args, e.g.:        @input_guardrail        def my_sync_guardrail(...): ...        @input_guardrail(name="guardrail_name")        async def my_async_guardrail(...): ...    """    def decorator(        f: _InputGuardrailFuncSync[TContext_co] | _InputGuardrailFuncAsync[TContext_co],    ) -> InputGuardrail[TContext_co]:        return InputGuardrail(            guardrail_function=f,            # If not set, guardrail name uses the function’s name by default.            name=name if name else f.__name__,        )    if func is not None:        # Decorator was used without parentheses        return decorator(func)    # Decorator used with keyword arguments    return decorator``` |

### output\_guardrail

```
output_guardrail(
    func: _OutputGuardrailFuncSync[TContext_co],
) -> OutputGuardrail[TContext_co]

```

```
output_guardrail(
    func: _OutputGuardrailFuncAsync[TContext_co],
) -> OutputGuardrail[TContext_co]

```

```
output_guardrail(
    *, name: str | None = None
) -> Callable[\
    [\
        _OutputGuardrailFuncSync[TContext_co]\
        | _OutputGuardrailFuncAsync[TContext_co]\
    ],\
    OutputGuardrail[TContext_co],\
]

```

```
output_guardrail(
    func: _OutputGuardrailFuncSync[TContext_co]
    | _OutputGuardrailFuncAsync[TContext_co]
    | None = None,
    *,
    name: str | None = None,
) -> (
    OutputGuardrail[TContext_co]
    | Callable[\
        [\
            _OutputGuardrailFuncSync[TContext_co]\
            | _OutputGuardrailFuncAsync[TContext_co]\
        ],\
        OutputGuardrail[TContext_co],\
    ]
)

```

Decorator that transforms a sync or async function into an `OutputGuardrail`.
It can be used directly (no parentheses) or with keyword args, e.g.:

```
@output_guardrail
def my_sync_guardrail(...): ...

@output_guardrail(name="guardrail_name")
async def my_async_guardrail(...): ...

```

Source code in `src/agents/guardrail.py`

|  |  |
| --- | --- |
| ```290291292293294295296297298299300301302303304305306307308309310311312313314315316317318319320321322323324325326327328``` | ```md-code__contentdef output_guardrail(    func: _OutputGuardrailFuncSync[TContext_co] | _OutputGuardrailFuncAsync[TContext_co] | None = None,    *,    name: str | None = None,) -> (    OutputGuardrail[TContext_co] | Callable[        [_OutputGuardrailFuncSync[TContext_co] | _OutputGuardrailFuncAsync[TContext_co]],        OutputGuardrail[TContext_co],    ]):    """    Decorator that transforms a sync or async function into an `OutputGuardrail`.    It can be used directly (no parentheses) or with keyword args, e.g.:        @output_guardrail        def my_sync_guardrail(...): ...        @output_guardrail(name="guardrail_name")        async def my_async_guardrail(...): ...    """    def decorator(        f: _OutputGuardrailFuncSync[TContext_co] | _OutputGuardrailFuncAsync[TContext_co],    ) -> OutputGuardrail[TContext_co]:        return OutputGuardrail(            guardrail_function=f,            # Guardrail name defaults to function name when not specified (None).            name=name if name else f.__name__,        )    if func is not None:        # Decorator was used without parentheses        return decorator(func)    # Decorator used with keyword arguments    return decorator``` |