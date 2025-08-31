---
title: `Run context`
source: https://openai.github.io/openai-agents-python/ref/run_context/
---

# `Run context`

### RunContextWrapper`dataclass`

Bases: `Generic[TContext]`

This wraps the context object that you passed to `Runner.run()`. It also contains
information about the usage of the agent run so far.

NOTE: Contexts are not passed to the LLM. They're a way to pass dependencies and data to code
you implement, like tool functions, callbacks, hooks, etc.

Source code in `src/agents/run_context.py`

|  |  |
| --- | --- |
| ```11121314151617181920212223242526``` | ```md-code__content@dataclassclass RunContextWrapper(Generic[TContext]):    """This wraps the context object that you passed to `Runner.run()`. It also contains    information about the usage of the agent run so far.    NOTE: Contexts are not passed to the LLM. They're a way to pass dependencies and data to code    you implement, like tool functions, callbacks, hooks, etc.    """    context: TContext    """The context object (or None), passed by you to `Runner.run()`"""    usage: Usage = field(default_factory=Usage)    """The usage of the agent run so far. For streamed responses, the usage will be stale until the    last chunk of the stream is processed.    """``` |

#### context`instance-attribute`

```
context: TContext

```

The context object (or None), passed by you to `Runner.run()`

#### usage`class-attribute``instance-attribute`

```
usage: Usage = field(default_factory=Usage)

```

The usage of the agent run so far. For streamed responses, the usage will be stale until the
last chunk of the stream is processed.