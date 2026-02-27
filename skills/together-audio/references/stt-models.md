# STT Models & Transcription Reference

## Models

| Model | API String | Capabilities |
|-------|-----------|-------------|
| Whisper Large v3 | `openai/whisper-large-v3` | Transcription, Translation, Diarization, Real-time WebSocket |
| Voxtral Mini 3B | `mistralai/Voxtral-Mini-3B-2507` | Transcription |

## Supported Audio Formats
`.wav`, `.mp3`, `.m4a`, `.webm`, `.flac`

## Transcription Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file` | string/file | Yes | Audio file (path, URL, or file object) |
| `model` | string | Yes | STT model identifier |
| `language` | string | No | ISO 639-1 code: `en`, `es`, `fr`, `de`, `ja`, `zh`, `auto` |
| `response_format` | string | No | `json` (default) or `verbose_json` |
| `prompt` | string | No | Custom prompt for domain-specific accuracy |
| `temperature` | float | No | 0.0 (deterministic) to 1.0 (creative) |
| `timestamp_granularities` | string | No | `segment` or `word` |
| `diarize` | bool | No | Enable speaker identification |
| `min_speakers` | int | No | Minimum expected speakers |
| `max_speakers` | int | No | Maximum expected speakers |

## Response Formats

### JSON (Default)
```json
{"text": "Hello, this is a test recording."}
```

### Verbose JSON
Includes `text`, `language`, `duration`, `segments[]`, `words[]`, `speaker_segments[]`

**Segment object:**
```json
{"start": 0.11, "end": 10.85, "text": "..."}
```

**Word object (with `timestamp_granularities="word"`):**
```json
{"word": "Hello", "start": 0.00, "end": 0.36}
```

**Diarization (with `diarize=true`):**
```json
{
  "id": 1,
  "speaker_id": "SPEAKER_01",
  "start": 6.268,
  "end": 30.776,
  "text": "...",
  "words": [{"word": "Hello", "start": 6.268, "end": 11.314, "speaker_id": "SPEAKER_01"}]
}
```

## Real-time WebSocket STT

**URL:** `wss://api.together.ai/v1/realtime?model={model}&input_audio_format=pcm_s16le_16000`

**Headers:**
```
Authorization: Bearer YOUR_API_KEY
OpenAI-Beta: realtime=v1
```

**Client to Server:**
```json
{"type": "input_audio_buffer.append", "audio": "base64-audio-chunk"}
{"type": "input_audio_buffer.commit"}
```

**Server to Client:**
```json
{"type": "conversation.item.input_audio_transcription.delta", "delta": "partial text"}
{"type": "conversation.item.input_audio_transcription.completed", "transcript": "final text"}
{"type": "error", "message": "..."}
```

## Transcription with Timestamps

Get word-level timing information using `verbose_json` response format:

```python
response = client.audio.transcriptions.create(
    file="audio.mp3",
    model="openai/whisper-large-v3",
    response_format="verbose_json",
    timestamp_granularities="word",
)

print(f"Text: {response.text}")
print(f"Duration: {response.duration}s")

if response.words:
    for word in response.words:
        print(f"'{word.word}' [{word.start:.2f}s - {word.end:.2f}s]")
```

```typescript
import Together from "together-ai";

const together = new Together();

const response = await together.audio.transcriptions.create({
  file: "meeting_recording.mp3",
  model: "openai/whisper-large-v3",
  language: "en",
  response_format: "json",
});

console.log(`Transcription: ${response.text}`);
```

### Speaker Diarization

```typescript
import Together from "together-ai";

const together = new Together();

async function transcribeWithDiarization() {
  const response = await together.audio.transcriptions.create({
    file: "meeting.mp3",
    model: "openai/whisper-large-v3",
    diarize: true,
  });

  console.log(`Speaker Segments: ${response.speaker_segments}\n`);
}

transcribeWithDiarization();
```

## Translation

Translates any language to English:

```python
response = client.audio.translations.create(
    file="foreign_audio.mp3",
    model="openai/whisper-large-v3",
)
print(response.text)  # English translation
```

```typescript
import Together from "together-ai";

const together = new Together();

const translation = await together.audio.translations.create({
  file: "french_audio.mp3",
  model: "openai/whisper-large-v3",
});
console.log(`English translation: ${translation.text}`);
```

## Input Methods

```python
# Local file path
file="audio.mp3"

# Path object
file=Path("recordings/interview.wav")

# URL
file="https://example.com/audio.mp3"

# File-like object
file=open("audio.mp3", "rb")
```

## Async Support

```python
from together import AsyncTogether

async def transcribe():
    client = AsyncTogether()
    response = await client.audio.transcriptions.create(
        file="audio.mp3",
        model="openai/whisper-large-v3",
    )
    return response.text
```
