---
title: Pipelines and workflows
source: https://openai.github.io/openai-agents-python/voice/pipeline/
---

# Pipelines and workflows

[`VoicePipeline`](https://openai.github.io/openai-agents-python/ref/voice/pipeline/#agents.voice.pipeline.VoicePipeline "VoicePipeline") is a class that makes it easy to turn your agentic workflows into a voice app. You pass in a workflow to run, and the pipeline takes care of transcribing input audio, detecting when the audio ends, calling your workflow at the right time, and turning the workflow output back into audio.

## Configuring a pipeline

When you create a pipeline, you can set a few things:

1. The [`workflow`](https://openai.github.io/openai-agents-python/ref/voice/workflow/#agents.voice.workflow.VoiceWorkflowBase "VoiceWorkflowBase"), which is the code that runs each time new audio is transcribed.
2. The [`speech-to-text`](https://openai.github.io/openai-agents-python/ref/voice/model/#agents.voice.model.STTModel "STTModel") and [`text-to-speech`](https://openai.github.io/openai-agents-python/ref/voice/model/#agents.voice.model.TTSModel "TTSModel") models used
3. The [`config`](https://openai.github.io/openai-agents-python/ref/voice/pipeline_config/#agents.voice.pipeline_config.VoicePipelineConfig "VoicePipelineConfig            dataclass   "), which lets you configure things like:
   - A model provider, which can map model names to models
   - Tracing, including whether to disable tracing, whether audio files are uploaded, the workflow name, trace IDs etc.
   - Settings on the TTS and STT models, like the prompt, language and data types used.

## Running a pipeline

You can run a pipeline via the [`run()`](https://openai.github.io/openai-agents-python/ref/voice/pipeline/#agents.voice.pipeline.VoicePipeline.run "run            async   ") method, which lets you pass in audio input in two forms:

1. [`AudioInput`](https://openai.github.io/openai-agents-python/ref/voice/input/#agents.voice.input.AudioInput "AudioInput            dataclass   ") is used when you have a full audio transcript, and just want to produce a result for it. This is useful in cases where you don't need to detect when a speaker is done speaking; for example, when you have pre-recorded audio or in push-to-talk apps where it's clear when the user is done speaking.
2. [`StreamedAudioInput`](https://openai.github.io/openai-agents-python/ref/voice/input/#agents.voice.input.StreamedAudioInput "StreamedAudioInput") is used when you might need to detect when a user is done speaking. It allows you to push audio chunks as they are detected, and the voice pipeline will automatically run the agent workflow at the right time, via a process called "activity detection".

## Results

The result of a voice pipeline run is a [`StreamedAudioResult`](https://openai.github.io/openai-agents-python/ref/voice/result/#agents.voice.result.StreamedAudioResult "StreamedAudioResult"). This is an object that lets you stream events as they occur. There are a few kinds of [`VoiceStreamEvent`](https://openai.github.io/openai-agents-python/ref/voice/events/#agents.voice.events.VoiceStreamEvent "VoiceStreamEvent            module-attribute   "), including:

1. [`VoiceStreamEventAudio`](https://openai.github.io/openai-agents-python/ref/voice/events/#agents.voice.events.VoiceStreamEventAudio "VoiceStreamEventAudio            dataclass   "), which contains a chunk of audio.
2. [`VoiceStreamEventLifecycle`](https://openai.github.io/openai-agents-python/ref/voice/events/#agents.voice.events.VoiceStreamEventLifecycle "VoiceStreamEventLifecycle            dataclass   "), which informs you of lifecycle events like a turn starting or ending.
3. [`VoiceStreamEventError`](https://openai.github.io/openai-agents-python/ref/voice/events/#agents.voice.events.VoiceStreamEventError "VoiceStreamEventError            dataclass   "), is an error event.

```
result = await pipeline.run(input)

async for event in result.stream():
    if event.type == "voice_stream_event_audio":

        # play audio

    elif event.type == "voice_stream_event_lifecycle":

        # lifecycle

    elif event.type == "voice_stream_event_error"

        # error

    ...

```

## Best practices

### Interruptions

The Agents SDK currently does not support any built-in interruptions support for [`StreamedAudioInput`](https://openai.github.io/openai-agents-python/ref/voice/input/#agents.voice.input.StreamedAudioInput "StreamedAudioInput"). Instead for every detected turn it will trigger a separate run of your workflow. If you want to handle interruptions inside your application you can listen to the [`VoiceStreamEventLifecycle`](https://openai.github.io/openai-agents-python/ref/voice/events/#agents.voice.events.VoiceStreamEventLifecycle "VoiceStreamEventLifecycle            dataclass   ") events. `turn_started` will indicate that a new turn was transcribed and processing is beginning. `turn_ended` will trigger after all the audio was dispatched for a respective turn. You could use these events to mute the microphone of the speaker when the model starts a turn and unmute it after you flushed all the related audio for a turn.