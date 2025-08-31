---
title: `OpenAI STT`
source: https://openai.github.io/openai-agents-python/ref/voice/models/openai_stt/
---

# `OpenAI STT`

### OpenAISTTTranscriptionSession

Bases: `StreamedTranscriptionSession`

A transcription session for OpenAI's STT model.

Source code in `src/agents/voice/models/openai_stt.py`

|  |  |
| --- | --- |
| ``` 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99100101102103104105106107108109110111112113114115116117118119120121122123124125126127128129130131132133134135136137138139140141142143144145146147148149150151152153154155156157158159160161162163164165166167168169170171172173174175176177178179180181182183184185186187188189190191192193194195196197198199200201202203204205206207208209210211212213214215216217218219220221222223224225226227228229230231232233234235236237238239240241242243244245246247248249250251252253254255256257258259260261262263264265266267268269270271272273274275276277278279280281282283284285286287288289290291292293294295296297298299300301302303304305306307308309310311312313314315316317318319320321322323324325326327328329330331332333334335336337338339340341342343344345346347348349350351352353354355356357358359360361362``` | ```md-code__contentclass OpenAISTTTranscriptionSession(StreamedTranscriptionSession):    """A transcription session for OpenAI's STT model."""    def __init__(        self,        input: StreamedAudioInput,        client: AsyncOpenAI,        model: str,        settings: STTModelSettings,        trace_include_sensitive_data: bool,        trace_include_sensitive_audio_data: bool,    ):        self.connected: bool = False        self._client = client        self._model = model        self._settings = settings        self._turn_detection = settings.turn_detection or DEFAULT_TURN_DETECTION        self._trace_include_sensitive_data = trace_include_sensitive_data        self._trace_include_sensitive_audio_data = trace_include_sensitive_audio_data        self._input_queue: asyncio.Queue[npt.NDArray[np.int16 | np.float32]] = input.queue        self._output_queue: asyncio.Queue[str | ErrorSentinel | SessionCompleteSentinel] = (            asyncio.Queue()        )        self._websocket: websockets.ClientConnection | None = None        self._event_queue: asyncio.Queue[dict[str, Any] | WebsocketDoneSentinel] = asyncio.Queue()        self._state_queue: asyncio.Queue[dict[str, Any]] = asyncio.Queue()        self._turn_audio_buffer: list[npt.NDArray[np.int16 | np.float32]] = []        self._tracing_span: Span[TranscriptionSpanData] | None = None        # tasks        self._listener_task: asyncio.Task[Any] | None = None        self._process_events_task: asyncio.Task[Any] | None = None        self._stream_audio_task: asyncio.Task[Any] | None = None        self._connection_task: asyncio.Task[Any] | None = None        self._stored_exception: Exception | None = None    def _start_turn(self) -> None:        self._tracing_span = transcription_span(            model=self._model,            model_config={                "temperature": self._settings.temperature,                "language": self._settings.language,                "prompt": self._settings.prompt,                "turn_detection": self._turn_detection,            },        )        self._tracing_span.start()    def _end_turn(self, _transcript: str) -> None:        if len(_transcript)             return        if self._tracing_span:            if self._trace_include_sensitive_audio_data:                self._tracing_span.span_data.input = _audio_to_base64(self._turn_audio_buffer)            self._tracing_span.span_data.input_format = "pcm"            if self._trace_include_sensitive_data:                self._tracing_span.span_data.output = _transcript            self._tracing_span.finish()            self._turn_audio_buffer = []            self._tracing_span = None    async def _event_listener(self) -> None:        assert self._websocket is not None, "Websocket not initialized"        async for message in self._websocket:            try:                event = json.loads(message)                if event.get("type") == "error":                    raise STTWebsocketConnectionError(f"Error event: {event.get('error')}")                if event.get("type") in [                    "session.updated",                    "transcription_session.updated",                    "session.created",                    "transcription_session.created",                ]:                    await self._state_queue.put(event)                await self._event_queue.put(event)            except Exception as e:                await self._output_queue.put(ErrorSentinel(e))                raise STTWebsocketConnectionError("Error parsing events") from e        await self._event_queue.put(WebsocketDoneSentinel())    async def _configure_session(self) -> None:        assert self._websocket is not None, "Websocket not initialized"        await self._websocket.send(            json.dumps(                {                    "type": "transcription_session.update",                    "session": {                        "input_audio_format": "pcm16",                        "input_audio_transcription": {"model": self._model},                        "turn_detection": self._turn_detection,                    },                }            )        )    async def _setup_connection(self, ws: websockets.ClientConnection) -> None:        self._websocket = ws        self._listener_task = asyncio.create_task(self._event_listener())        try:            event = await _wait_for_event(                self._state_queue,                ["session.created", "transcription_session.created"],                SESSION_CREATION_TIMEOUT,            )        except TimeoutError as e:            wrapped_err = STTWebsocketConnectionError(                "Timeout waiting for transcription_session.created event"            )            await self._output_queue.put(ErrorSentinel(wrapped_err))            raise wrapped_err from e        except Exception as e:            await self._output_queue.put(ErrorSentinel(e))            raise e        await self._configure_session()        try:            event = await _wait_for_event(                self._state_queue,                ["session.updated", "transcription_session.updated"],                SESSION_UPDATE_TIMEOUT,            )            if _debug.DONT_LOG_MODEL_DATA:                logger.debug("Session updated")            else:                logger.debug(f"Session updated: {event}")        except TimeoutError as e:            wrapped_err = STTWebsocketConnectionError(                "Timeout waiting for transcription_session.updated event"            )            await self._output_queue.put(ErrorSentinel(wrapped_err))            raise wrapped_err from e        except Exception as e:            await self._output_queue.put(ErrorSentinel(e))            raise    async def _handle_events(self) -> None:        while True:            try:                event = await asyncio.wait_for(                    self._event_queue.get(), timeout=EVENT_INACTIVITY_TIMEOUT                )                if isinstance(event, WebsocketDoneSentinel):                    # processed all events and websocket is done                    break                event_type = event.get("type", "unknown")                if event_type == "input_audio_transcription_completed":                    transcript = cast(str, event.get("transcript", ""))                    if len(transcript) > 0:                        self._end_turn(transcript)                        self._start_turn()                        await self._output_queue.put(transcript)                await asyncio.sleep(0)  # yield control            except asyncio.TimeoutError:                # No new events for a while. Assume the session is done.                break            except Exception as e:                await self._output_queue.put(ErrorSentinel(e))                raise e        await self._output_queue.put(SessionCompleteSentinel())    async def _stream_audio(        self, audio_queue: asyncio.Queue[npt.NDArray[np.int16 | np.float32]]    ) -> None:        assert self._websocket is not None, "Websocket not initialized"        self._start_turn()        while True:            buffer = await audio_queue.get()            if buffer is None:                break            self._turn_audio_buffer.append(buffer)            try:                await self._websocket.send(                    json.dumps(                        {                            "type": "input_audio_buffer.append",                            "audio": base64.b64encode(buffer.tobytes()).decode("utf-8"),                        }                    )                )            except websockets.ConnectionClosed:                break            except Exception as e:                await self._output_queue.put(ErrorSentinel(e))                raise e            await asyncio.sleep(0)  # yield control    async def _process_websocket_connection(self) -> None:        try:            async with websockets.connect(                "wss://api.openai.com/v1/realtime?intent=transcription",                additional_headers={                    "Authorization": f"Bearer {self._client.api_key}",                    "OpenAI-Beta": "realtime=v1",                    "OpenAI-Log-Session": "1",                },            ) as ws:                await self._setup_connection(ws)                self._process_events_task = asyncio.create_task(self._handle_events())                self._stream_audio_task = asyncio.create_task(self._stream_audio(self._input_queue))                self.connected = True                if self._listener_task:                    await self._listener_task                else:                    logger.error("Listener task not initialized")                    raise AgentsException("Listener task not initialized")        except Exception as e:            await self._output_queue.put(ErrorSentinel(e))            raise e    def _check_errors(self) -> None:        if self._connection_task and self._connection_task.done():            exc = self._connection_task.exception()            if exc and isinstance(exc, Exception):                self._stored_exception = exc        if self._process_events_task and self._process_events_task.done():            exc = self._process_events_task.exception()            if exc and isinstance(exc, Exception):                self._stored_exception = exc        if self._stream_audio_task and self._stream_audio_task.done():            exc = self._stream_audio_task.exception()            if exc and isinstance(exc, Exception):                self._stored_exception = exc        if self._listener_task and self._listener_task.done():            exc = self._listener_task.exception()            if exc and isinstance(exc, Exception):                self._stored_exception = exc    def _cleanup_tasks(self) -> None:        if self._listener_task and not self._listener_task.done():            self._listener_task.cancel()        if self._process_events_task and not self._process_events_task.done():            self._process_events_task.cancel()        if self._stream_audio_task and not self._stream_audio_task.done():            self._stream_audio_task.cancel()        if self._connection_task and not self._connection_task.done():            self._connection_task.cancel()    async def transcribe_turns(self) -> AsyncIterator[str]:        self._connection_task = asyncio.create_task(self._process_websocket_connection())        while True:            try:                turn = await self._output_queue.get()            except asyncio.CancelledError:                break            if (                turn is None                or isinstance(turn, ErrorSentinel)                or isinstance(turn, SessionCompleteSentinel)            ):                self._output_queue.task_done()                break            yield turn            self._output_queue.task_done()        if self._tracing_span:            self._end_turn("")        if self._websocket:            await self._websocket.close()        self._check_errors()        if self._stored_exception:            raise self._stored_exception    async def close(self) -> None:        if self._websocket:            await self._websocket.close()        self._cleanup_tasks()``` |

### OpenAISTTModel

Bases: `STTModel`

A speech-to-text model for OpenAI.

Source code in `src/agents/voice/models/openai_stt.py`

|  |  |
| --- | --- |
| ```365366367368369370371372373374375376377378379380381382383384385386387388389390391392393394395396397398399400401402403404405406407408409410411412413414415416417418419420421422423424425426427428429430431432433434435436437438439440441442443444445446447448449450451452453454455456``` | ```md-code__contentclass OpenAISTTModel(STTModel):    """A speech-to-text model for OpenAI."""    def __init__(        self,        model: str,        openai_client: AsyncOpenAI,    ):        """Create a new OpenAI speech-to-text model.        Args:            model: The name of the model to use.            openai_client: The OpenAI client to use.        """        self.model = model        self._client = openai_client    @property    def model_name(self) -> str:        return self.model    def _non_null_or_not_given(self, value: Any) -> Any:        return value if value is not None else None  # NOT_GIVEN    async def transcribe(        self,        input: AudioInput,        settings: STTModelSettings,        trace_include_sensitive_data: bool,        trace_include_sensitive_audio_data: bool,    ) -> str:        """Transcribe an audio input.        Args:            input: The audio input to transcribe.            settings: The settings to use for the transcription.        Returns:            The transcribed text.        """        with transcription_span(            model=self.model,            input=input.to_base64() if trace_include_sensitive_audio_data else "",            input_format="pcm",            model_config={                "temperature": self._non_null_or_not_given(settings.temperature),                "language": self._non_null_or_not_given(settings.language),                "prompt": self._non_null_or_not_given(settings.prompt),            },        ) as span:            try:                response = await self._client.audio.transcriptions.create(                    model=self.model,                    file=input.to_audio_file(),                    prompt=self._non_null_or_not_given(settings.prompt),                    language=self._non_null_or_not_given(settings.language),                    temperature=self._non_null_or_not_given(settings.temperature),                )                if trace_include_sensitive_data:                    span.span_data.output = response.text                return response.text            except Exception as e:                span.span_data.output = ""                span.set_error(SpanError(message=str(e), data={}))                raise e    async def create_session(        self,        input: StreamedAudioInput,        settings: STTModelSettings,        trace_include_sensitive_data: bool,        trace_include_sensitive_audio_data: bool,    ) -> StreamedTranscriptionSession:        """Create a new transcription session.        Args:            input: The audio input to transcribe.            settings: The settings to use for the transcription.            trace_include_sensitive_data: Whether to include sensitive data in traces.            trace_include_sensitive_audio_data: Whether to include sensitive audio data in traces.        Returns:            A new transcription session.        """        return OpenAISTTTranscriptionSession(            input,            self._client,            self.model,            settings,            trace_include_sensitive_data,            trace_include_sensitive_audio_data,        )``` |

#### \_\_init\_\_

```
__init__(model: str, openai_client: AsyncOpenAI)

```

Create a new OpenAI speech-to-text model.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `model` | `str` | The name of the model to use. | _required_ |
| `openai_client` | `AsyncOpenAI` | The OpenAI client to use. | _required_ |

Source code in `src/agents/voice/models/openai_stt.py`

|  |  |
| --- | --- |
| ```368369370371372373374375376377378379380``` | ```md-code__contentdef __init__(    self,    model: str,    openai_client: AsyncOpenAI,):    """Create a new OpenAI speech-to-text model.    Args:        model: The name of the model to use.        openai_client: The OpenAI client to use.    """    self.model = model    self._client = openai_client``` |

#### transcribe`async`

```
transcribe(
    input: AudioInput,
    settings: STTModelSettings,
    trace_include_sensitive_data: bool,
    trace_include_sensitive_audio_data: bool,
) -> str

```

Transcribe an audio input.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `input` | `AudioInput` | The audio input to transcribe. | _required_ |
| `settings` | `STTModelSettings` | The settings to use for the transcription. | _required_ |

Returns:

| Type | Description |
| --- | --- |
| `str` | The transcribed text. |

Source code in `src/agents/voice/models/openai_stt.py`

|  |  |
| --- | --- |
| ```389390391392393394395396397398399400401402403404405406407408409410411412413414415416417418419420421422423424425426427428429``` | ```md-code__contentasync def transcribe(    self,    input: AudioInput,    settings: STTModelSettings,    trace_include_sensitive_data: bool,    trace_include_sensitive_audio_data: bool,) -> str:    """Transcribe an audio input.    Args:        input: The audio input to transcribe.        settings: The settings to use for the transcription.    Returns:        The transcribed text.    """    with transcription_span(        model=self.model,        input=input.to_base64() if trace_include_sensitive_audio_data else "",        input_format="pcm",        model_config={            "temperature": self._non_null_or_not_given(settings.temperature),            "language": self._non_null_or_not_given(settings.language),            "prompt": self._non_null_or_not_given(settings.prompt),        },    ) as span:        try:            response = await self._client.audio.transcriptions.create(                model=self.model,                file=input.to_audio_file(),                prompt=self._non_null_or_not_given(settings.prompt),                language=self._non_null_or_not_given(settings.language),                temperature=self._non_null_or_not_given(settings.temperature),            )            if trace_include_sensitive_data:                span.span_data.output = response.text            return response.text        except Exception as e:            span.span_data.output = ""            span.set_error(SpanError(message=str(e), data={}))            raise e``` |

#### create\_session`async`

```
create_session(
    input: StreamedAudioInput,
    settings: STTModelSettings,
    trace_include_sensitive_data: bool,
    trace_include_sensitive_audio_data: bool,
) -> StreamedTranscriptionSession

```

Create a new transcription session.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `input` | `StreamedAudioInput` | The audio input to transcribe. | _required_ |
| `settings` | `STTModelSettings` | The settings to use for the transcription. | _required_ |
| `trace_include_sensitive_data` | `bool` | Whether to include sensitive data in traces. | _required_ |
| `trace_include_sensitive_audio_data` | `bool` | Whether to include sensitive audio data in traces. | _required_ |

Returns:

| Type | Description |
| --- | --- |
| `StreamedTranscriptionSession` | A new transcription session. |

Source code in `src/agents/voice/models/openai_stt.py`

|  |  |
| --- | --- |
| ```431432433434435436437438439440441442443444445446447448449450451452453454455456``` | ```md-code__contentasync def create_session(    self,    input: StreamedAudioInput,    settings: STTModelSettings,    trace_include_sensitive_data: bool,    trace_include_sensitive_audio_data: bool,) -> StreamedTranscriptionSession:    """Create a new transcription session.    Args:        input: The audio input to transcribe.        settings: The settings to use for the transcription.        trace_include_sensitive_data: Whether to include sensitive data in traces.        trace_include_sensitive_audio_data: Whether to include sensitive audio data in traces.    Returns:        A new transcription session.    """    return OpenAISTTTranscriptionSession(        input,        self._client,        self.model,        settings,        trace_include_sensitive_data,        trace_include_sensitive_audio_data,    )``` |