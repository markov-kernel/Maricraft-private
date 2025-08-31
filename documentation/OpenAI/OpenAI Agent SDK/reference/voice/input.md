---
title: `Input`
source: https://openai.github.io/openai-agents-python/ref/voice/input/
---

# `Input`

### AudioInput`dataclass`

Static audio to be used as input for the VoicePipeline.

Source code in `src/agents/voice/input.py`

|  |  |
| --- | --- |
| ```4041424344454647484950515253545556575859606162636465666768697071``` | ```md-code__content@dataclassclass AudioInput:    """Static audio to be used as input for the VoicePipeline."""    buffer: npt.NDArray[np.int16 | np.float32]    """    A buffer containing the audio data for the agent. Must be a numpy array of int16 or float32.    """    frame_rate: int = DEFAULT_SAMPLE_RATE    """The sample rate of the audio data. Defaults to 24000."""    sample_width: int = 2    """The sample width of the audio data. Defaults to 2."""    channels: int = 1    """The number of channels in the audio data. Defaults to 1."""    def to_audio_file(self) -> tuple[str, io.BytesIO, str]:        """Returns a tuple of (filename, bytes, content_type)"""        return _buffer_to_audio_file(self.buffer, self.frame_rate, self.sample_width, self.channels)    def to_base64(self) -> str:        """Returns the audio data as a base64 encoded string."""        if self.buffer.dtype == np.float32:            # convert to int16            self.buffer = np.clip(self.buffer, -1.0, 1.0)            self.buffer = (self.buffer * 32767).astype(np.int16)        elif self.buffer.dtype != np.int16:            raise UserError("Buffer must be a numpy array of int16 or float32")        return base64.b64encode(self.buffer.tobytes()).decode("utf-8")``` |

#### buffer`instance-attribute`

```
buffer: NDArray[int16 | float32]

```

A buffer containing the audio data for the agent. Must be a numpy array of int16 or float32.

#### frame\_rate`class-attribute``instance-attribute`

```
frame_rate: int = DEFAULT_SAMPLE_RATE

```

The sample rate of the audio data. Defaults to 24000.

#### sample\_width`class-attribute``instance-attribute`

```
sample_width: int = 2

```

The sample width of the audio data. Defaults to 2.

#### channels`class-attribute``instance-attribute`

```
channels: int = 1

```

The number of channels in the audio data. Defaults to 1.

#### to\_audio\_file

```
to_audio_file() -> tuple[str, BytesIO, str]

```

Returns a tuple of (filename, bytes, content\_type)

Source code in `src/agents/voice/input.py`

|  |  |
| --- | --- |
| ```585960``` | ```md-code__contentdef to_audio_file(self) -> tuple[str, io.BytesIO, str]:    """Returns a tuple of (filename, bytes, content_type)"""    return _buffer_to_audio_file(self.buffer, self.frame_rate, self.sample_width, self.channels)``` |

#### to\_base64

```
to_base64() -> str

```

Returns the audio data as a base64 encoded string.

Source code in `src/agents/voice/input.py`

|  |  |
| --- | --- |
| ```62636465666768697071``` | ```md-code__contentdef to_base64(self) -> str:    """Returns the audio data as a base64 encoded string."""    if self.buffer.dtype == np.float32:        # convert to int16        self.buffer = np.clip(self.buffer, -1.0, 1.0)        self.buffer = (self.buffer * 32767).astype(np.int16)    elif self.buffer.dtype != np.int16:        raise UserError("Buffer must be a numpy array of int16 or float32")    return base64.b64encode(self.buffer.tobytes()).decode("utf-8")``` |

### StreamedAudioInput

Audio input represented as a stream of audio data. You can pass this to the `VoicePipeline`
and then push audio data into the queue using the `add_audio` method.

Source code in `src/agents/voice/input.py`

|  |  |
| --- | --- |
| ```747576777879808182838485868788``` | ```md-code__contentclass StreamedAudioInput:    """Audio input represented as a stream of audio data. You can pass this to the `VoicePipeline`    and then push audio data into the queue using the `add_audio` method.    """    def __init__(self):        self.queue: asyncio.Queue[npt.NDArray[np.int16 | np.float32]] = asyncio.Queue()    async def add_audio(self, audio: npt.NDArray[np.int16 | np.float32]):        """Adds more audio data to the stream.        Args:            audio: The audio data to add. Must be a numpy array of int16 or float32.        """        await self.queue.put(audio)``` |

#### add\_audio`async`

```
add_audio(audio: NDArray[int16 | float32])

```

Adds more audio data to the stream.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `audio` | `NDArray[int16 | float32]` | The audio data to add. Must be a numpy array of int16 or float32. | _required_ |

Source code in `src/agents/voice/input.py`

|  |  |
| --- | --- |
| ```82838485868788``` | ```md-code__contentasync def add_audio(self, audio: npt.NDArray[np.int16 | np.float32]):    """Adds more audio data to the stream.    Args:        audio: The audio data to add. Must be a numpy array of int16 or float32.    """    await self.queue.put(audio)``` |