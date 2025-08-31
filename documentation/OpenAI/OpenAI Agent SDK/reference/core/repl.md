---
title: `repl`
source: https://openai.github.io/openai-agents-python/ref/repl/
---

# `repl`

### run\_demo\_loop`async`

```
run_demo_loop(
    agent: Agent[Any], *, stream: bool = True
) -> None

```

Run a simple REPL loop with the given agent.

This utility allows quick manual testing and debugging of an agent from the
command line. Conversation state is preserved across turns. Enter `exit`
or `quit` to stop the loop.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `agent` | `Agent[Any]` | The starting agent to run. | _required_ |
| `stream` | `bool` | Whether to stream the agent output. | `True` |

Source code in `src/agents/repl.py`

|  |  |
| --- | --- |
| ```14151617181920212223242526272829303132333435363738394041424344454647484950515253545556575859606162``` | ```md-code__contentasync def run_demo_loop(agent: Agent[Any], *, stream: bool = True) -> None:    """Run a simple REPL loop with the given agent.    This utility allows quick manual testing and debugging of an agent from the    command line. Conversation state is preserved across turns. Enter ``exit``    or ``quit`` to stop the loop.    Args:        agent: The starting agent to run.        stream: Whether to stream the agent output.    """    current_agent = agent    input_items: list[TResponseInputItem] = []    while True:        try:            user_input = input(" > ")        except (EOFError, KeyboardInterrupt):            print()            break        if user_input.strip().lower() in {"exit", "quit"}:            break        if not user_input:            continue        input_items.append({"role": "user", "content": user_input})        result: RunResultBase        if stream:            result = Runner.run_streamed(current_agent, input=input_items)            async for event in result.stream_events():                if isinstance(event, RawResponsesStreamEvent):                    if isinstance(event.data, ResponseTextDeltaEvent):                        print(event.data.delta, end="", flush=True)                elif isinstance(event, RunItemStreamEvent):                    if event.item.type == "tool_call_item":                        print("\n[tool called]", flush=True)                    elif event.item.type == "tool_call_output_item":                        print(f"\n[tool output: {event.item.output}]", flush=True)                elif isinstance(event, AgentUpdatedStreamEvent):                    print(f"\n[Agent updated: {event.new_agent.name}]", flush=True)            print()        else:            result = await Runner.run(current_agent, input_items)            if result.final_output is not None:                print(result.final_output)        current_agent = result.last_agent        input_items = result.to_input_list()``` |