---
title: `Workflow`
source: https://openai.github.io/openai-agents-python/ref/voice/workflow/
---

# `Workflow`

### VoiceWorkflowBase

Bases: `ABC`

A base class for a voice workflow. You must implement the `run` method. A "workflow" is any
code you want, that receives a transcription and yields text that will be turned into speech
by a text-to-speech model.
In most cases, you'll create `Agent` s and use `Runner.run_streamed()` to run them, returning
some or all of the text events from the stream. You can use the `VoiceWorkflowHelper` class to
help with extracting text events from the stream.
If you have a simple workflow that has a single starting agent and no custom logic, you can
use `SingleAgentVoiceWorkflow` directly.

Source code in `src/agents/voice/workflow.py`

|  |  |
| --- | --- |
| ```1314151617181920212223242526272829303132333435363738394041``` | ```md-code__contentclass VoiceWorkflowBase(abc.ABC):    """    A base class for a voice workflow. You must implement the `run` method. A "workflow" is any    code you want, that receives a transcription and yields text that will be turned into speech    by a text-to-speech model.    In most cases, you'll create `Agent`s and use `Runner.run_streamed()` to run them, returning    some or all of the text events from the stream. You can use the `VoiceWorkflowHelper` class to    help with extracting text events from the stream.    If you have a simple workflow that has a single starting agent and no custom logic, you can    use `SingleAgentVoiceWorkflow` directly.    """    @abc.abstractmethod    def run(self, transcription: str) -> AsyncIterator[str]:        """        Run the voice workflow. You will receive an input transcription, and must yield text that        will be spoken to the user. You can run whatever logic you want here. In most cases, the        final logic will involve calling `Runner.run_streamed()` and yielding any text events from        the stream.        """        pass    async def on_start(self) -> AsyncIterator[str]:        """        Optional method that runs before any user input is received. Can be used        to deliver a greeting or instruction via TTS. Defaults to doing nothing.        """        return        yield``` |

#### run`abstractmethod`

```
run(transcription: str) -> AsyncIterator[str]

```

Run the voice workflow. You will receive an input transcription, and must yield text that
will be spoken to the user. You can run whatever logic you want here. In most cases, the
final logic will involve calling `Runner.run_streamed()` and yielding any text events from
the stream.

Source code in `src/agents/voice/workflow.py`

|  |  |
| --- | --- |
| ```252627282930313233``` | ```md-code__content@abc.abstractmethoddef run(self, transcription: str) -> AsyncIterator[str]:    """    Run the voice workflow. You will receive an input transcription, and must yield text that    will be spoken to the user. You can run whatever logic you want here. In most cases, the    final logic will involve calling `Runner.run_streamed()` and yielding any text events from    the stream.    """    pass``` |

#### on\_start`async`

```
on_start() -> AsyncIterator[str]

```

Optional method that runs before any user input is received. Can be used
to deliver a greeting or instruction via TTS. Defaults to doing nothing.

Source code in `src/agents/voice/workflow.py`

|  |  |
| --- | --- |
| ```35363738394041``` | ```md-code__contentasync def on_start(self) -> AsyncIterator[str]:    """    Optional method that runs before any user input is received. Can be used    to deliver a greeting or instruction via TTS. Defaults to doing nothing.    """    return    yield``` |

### VoiceWorkflowHelper

Source code in `src/agents/voice/workflow.py`

|  |  |
| --- | --- |
| ```44454647484950515253``` | ```md-code__contentclass VoiceWorkflowHelper:    @classmethod    async def stream_text_from(cls, result: RunResultStreaming) -> AsyncIterator[str]:        """Wraps a `RunResultStreaming` object and yields text events from the stream."""        async for event in result.stream_events():            if (                event.type == "raw_response_event"                and event.data.type == "response.output_text.delta"            ):                yield event.data.delta``` |

#### stream\_text\_from`async``classmethod`

```
stream_text_from(
    result: RunResultStreaming,
) -> AsyncIterator[str]

```

Wraps a `RunResultStreaming` object and yields text events from the stream.

Source code in `src/agents/voice/workflow.py`

|  |  |
| --- | --- |
| ```454647484950515253``` | ```md-code__content@classmethodasync def stream_text_from(cls, result: RunResultStreaming) -> AsyncIterator[str]:    """Wraps a `RunResultStreaming` object and yields text events from the stream."""    async for event in result.stream_events():        if (            event.type == "raw_response_event"            and event.data.type == "response.output_text.delta"        ):            yield event.data.delta``` |

### SingleAgentWorkflowCallbacks

Source code in `src/agents/voice/workflow.py`

|  |  |
| --- | --- |
| ```56575859``` | ```md-code__contentclass SingleAgentWorkflowCallbacks:    def on_run(self, workflow: SingleAgentVoiceWorkflow, transcription: str) -> None:        """Called when the workflow is run."""        pass``` |

#### on\_run

```
on_run(
    workflow: SingleAgentVoiceWorkflow, transcription: str
) -> None

```

Called when the workflow is run.

Source code in `src/agents/voice/workflow.py`

|  |  |
| --- | --- |
| ```575859``` | ```md-code__contentdef on_run(self, workflow: SingleAgentVoiceWorkflow, transcription: str) -> None:    """Called when the workflow is run."""    pass``` |

### SingleAgentVoiceWorkflow

Bases: `VoiceWorkflowBase`

A simple voice workflow that runs a single agent. Each transcription and result is added to
the input history.
For more complex workflows (e.g. multiple Runner calls, custom message history, custom logic,
custom configs), subclass `VoiceWorkflowBase` and implement your own logic.

Source code in `src/agents/voice/workflow.py`

|  |  |
| --- | --- |
| ``` 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99100101``` | ```md-code__contentclass SingleAgentVoiceWorkflow(VoiceWorkflowBase):    """A simple voice workflow that runs a single agent. Each transcription and result is added to    the input history.    For more complex workflows (e.g. multiple Runner calls, custom message history, custom logic,    custom configs), subclass `VoiceWorkflowBase` and implement your own logic.    """    def __init__(self, agent: Agent[Any], callbacks: SingleAgentWorkflowCallbacks | None = None):        """Create a new single agent voice workflow.        Args:            agent: The agent to run.            callbacks: Optional callbacks to call during the workflow.        """        self._input_history: list[TResponseInputItem] = []        self._current_agent = agent        self._callbacks = callbacks    async def run(self, transcription: str) -> AsyncIterator[str]:        if self._callbacks:            self._callbacks.on_run(self, transcription)        # Add the transcription to the input history        self._input_history.append(            {                "role": "user",                "content": transcription,            }        )        # Run the agent        result = Runner.run_streamed(self._current_agent, self._input_history)        # Stream the text from the result        async for chunk in VoiceWorkflowHelper.stream_text_from(result):            yield chunk        # Update the input history and current agent        self._input_history = result.to_input_list()        self._current_agent = result.last_agent``` |

#### \_\_init\_\_

```
__init__(
    agent: Agent[Any],
    callbacks: SingleAgentWorkflowCallbacks | None = None,
)

```

Create a new single agent voice workflow.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `agent` | `Agent[Any]` | The agent to run. | _required_ |
| `callbacks` | `SingleAgentWorkflowCallbacks | None` | Optional callbacks to call during the workflow. | `None` |

Source code in `src/agents/voice/workflow.py`

|  |  |
| --- | --- |
| ```69707172737475767778``` | ```md-code__contentdef __init__(self, agent: Agent[Any], callbacks: SingleAgentWorkflowCallbacks | None = None):    """Create a new single agent voice workflow.    Args:        agent: The agent to run.        callbacks: Optional callbacks to call during the workflow.    """    self._input_history: list[TResponseInputItem] = []    self._current_agent = agent    self._callbacks = callbacks``` |

#### on\_start`async`

```
on_start() -> AsyncIterator[str]

```

Optional method that runs before any user input is received. Can be used
to deliver a greeting or instruction via TTS. Defaults to doing nothing.

Source code in `src/agents/voice/workflow.py`

|  |  |
| --- | --- |
| ```35363738394041``` | ```md-code__contentasync def on_start(self) -> AsyncIterator[str]:    """    Optional method that runs before any user input is received. Can be used    to deliver a greeting or instruction via TTS. Defaults to doing nothing.    """    return    yield``` |