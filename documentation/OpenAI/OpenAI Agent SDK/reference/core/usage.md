---
title: `Usage`
source: https://openai.github.io/openai-agents-python/ref/usage/
---

# `Usage`

### Usage

Source code in `src/agents/usage.py`

|  |  |
| --- | --- |
| ``` 7 8 910111213141516171819202122232425262728293031323334353637383940414243``` | ```md-code__content@dataclassclass Usage:    requests: int = 0    """Total requests made to the LLM API."""    input_tokens: int = 0    """Total input tokens sent, across all requests."""    input_tokens_details: InputTokensDetails = field(        default_factory=lambda: InputTokensDetails(cached_tokens=0)    )    """Details about the input tokens, matching responses API usage details."""    output_tokens: int = 0    """Total output tokens received, across all requests."""    output_tokens_details: OutputTokensDetails = field(        default_factory=lambda: OutputTokensDetails(reasoning_tokens=0)    )    """Details about the output tokens, matching responses API usage details."""    total_tokens: int = 0    """Total tokens sent and received, across all requests."""    def add(self, other: "Usage") -> None:        self.requests += other.requests if other.requests else 0        self.input_tokens += other.input_tokens if other.input_tokens else 0        self.output_tokens += other.output_tokens if other.output_tokens else 0        self.total_tokens += other.total_tokens if other.total_tokens else 0        self.input_tokens_details = InputTokensDetails(            cached_tokens=self.input_tokens_details.cached_tokens            + other.input_tokens_details.cached_tokens        )        self.output_tokens_details = OutputTokensDetails(            reasoning_tokens=self.output_tokens_details.reasoning_tokens            + other.output_tokens_details.reasoning_tokens        )``` |

#### requests`class-attribute``instance-attribute`

```
requests: int = 0

```

Total requests made to the LLM API.

#### input\_tokens`class-attribute``instance-attribute`

```
input_tokens: int = 0

```

Total input tokens sent, across all requests.

#### input\_tokens\_details`class-attribute``instance-attribute`

```
input_tokens_details: InputTokensDetails = field(
    default_factory=lambda: InputTokensDetails(
        cached_tokens=0
    )
)

```

Details about the input tokens, matching responses API usage details.

#### output\_tokens`class-attribute``instance-attribute`

```
output_tokens: int = 0

```

Total output tokens received, across all requests.

#### output\_tokens\_details`class-attribute``instance-attribute`

```
output_tokens_details: OutputTokensDetails = field(
    default_factory=lambda: OutputTokensDetails(
        reasoning_tokens=0
    )
)

```

Details about the output tokens, matching responses API usage details.

#### total\_tokens`class-attribute``instance-attribute`

```
total_tokens: int = 0

```

Total tokens sent and received, across all requests.