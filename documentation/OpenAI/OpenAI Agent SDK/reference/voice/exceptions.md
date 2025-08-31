---
title: `Exceptions`
source: https://openai.github.io/openai-agents-python/ref/voice/exceptions/
---

# `Exceptions`

### STTWebsocketConnectionError

Bases: `AgentsException`

Exception raised when the STT websocket connection fails.

Source code in `src/agents/voice/exceptions.py`

|  |  |
| --- | --- |
| ```45678``` | ```md-code__contentclass STTWebsocketConnectionError(AgentsException):    """Exception raised when the STT websocket connection fails."""    def __init__(self, message: str):        self.message = message``` |