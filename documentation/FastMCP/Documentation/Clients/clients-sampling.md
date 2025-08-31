# Your LLM integration logic here
# Your LLM integration logic here

> **Category:** Clients
> **Source:** gofastmcp.com_clients_sampling.json

---

Advanced Features

LLM Sampling

`New in version: 2.0.0` MCP servers can request LLM completions from clients. The client handles these requests through a sampling handler callback.

## Sampling Handler

Provide a `sampling_handler` function when creating the client:

Copy

```
from fastmcp import Client
from fastmcp.client.sampling import (
SamplingMessage,
SamplingParams,
RequestContext,
)

async def sampling_handler(
messages: list[SamplingMessage],
params: SamplingParams,
context: RequestContext
) -> str:
# Your LLM integration logic here
# Extract text from messages and generate a response
return "Generated response based on the messages"

client = Client(
"my_mcp_server.py",
sampling_handler=sampling_handler,
)

```

### Handler Parameters

The sampling handler receives three parameters:

## Sampling Handler Parameters

SamplingMessage

Sampling Message Object

Show attributes

role

Literal\["user", "assistant"\]

The role of the message.

content

TextContent \| ImageContent \| AudioContent

The content of the message.TextContent is most common, and has a `.text` attribute.

SamplingParams

Sampling Parameters Object

Show attributes

messages

list\[SamplingMessage\]

The messages to sample from

modelPreferences

ModelPreferences \| None

The server’s preferences for which model to select. The client MAY ignore
these preferences.

Show attributes

hints

list\[ModelHint\] \| None

The hints to use for model selection.

costPriority

float \| None

The cost priority for model selection.

speedPriority

float \| None

The speed priority for model selection.

intelligencePriority

float \| None

The intelligence priority for model selection.

systemPrompt

str \| None

An optional system prompt the server wants to use for sampling.

includeContext

IncludeContext \| None

A request to include context from one or more MCP servers (including the caller), to
be attached to the prompt.

temperature

float \| None

The sampling temperature.

maxTokens

int

The maximum number of tokens to sample.

stopSequences

list\[str\] \| None

The stop sequences to use for sampling.

metadata

dict\[str, Any\] \| None

Optional metadata to pass through to the LLM provider.

RequestContext

Request Context Object

Show attributes

request\_id

RequestId

Unique identifier for the MCP request

## Basic Example

Copy

```
from fastmcp import Client
from fastmcp.client.sampling import SamplingMessage, SamplingParams, RequestContext

async def basic_sampling_handler(
messages: list[SamplingMessage],
params: SamplingParams,
context: RequestContext
) -> str:
# Extract message content
conversation = []
for message in messages:
content = message.content.text if hasattr(message.content, 'text') else str(message.content)
conversation.append(f"{message.role}: {content}")

# Use the system prompt if provided
system_prompt = params.systemPrompt or "You are a helpful assistant."

# Here you would integrate with your preferred LLM service
# This is just a placeholder response
return f"Response based on conversation: {' | '.join(conversation)}"

client = Client(
"my_mcp_server.py",
sampling_handler=basic_sampling_handler
)

```

[Progress](https://gofastmcp.com/clients/progress) [Messages](https://gofastmcp.com/clients/messages)