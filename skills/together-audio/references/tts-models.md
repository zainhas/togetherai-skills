# TTS Models & Voices Reference

## Models

| Model | API String | Endpoints | Pricing |
|-------|-----------|-----------|---------|
| Orpheus 3B | `canopylabs/orpheus-3b-0.1-ft` | REST, Streaming, WebSocket | $15/1M chars |
| Kokoro 82M | `hexgrad/Kokoro-82M` | REST, Streaming, WebSocket | $4/1M chars |
| Cartesia Sonic 2 | `cartesia/sonic-2` | REST | $65/1M chars |
| Cartesia Sonic | `cartesia/sonic` | REST | - |
| Rime Arcana v3 Turbo* | `rime-labs/rime-arcana-v3-turbo` | REST, Streaming, WebSocket | DE only |
| Rime Arcana v3* | `rime-labs/rime-arcana-v3` | REST, Streaming, WebSocket | DE only |
| Rime Arcana v2* | `rime-labs/rime-arcana-v2` | REST, Streaming, WebSocket | DE only |
| Rime Mist v2* | `rime-labs/rime-mist-v2` | REST, Streaming, WebSocket | DE only |
| MiniMax Speech 2.6 Turbo* | `minimax/speech-2.6-turbo` | REST, Streaming, WebSocket | DE only |

*Dedicated Endpoint only

## Voice Lists

### Orpheus (8 voices)
`tara`, `leah`, `jess`, `leo`, `dan`, `mia`, `zac`, `zoe`

### Kokoro (51 voices)

**American Female (af_):** `af_heart`, `af_alloy`, `af_aoede`, `af_bella`, `af_jessica`, `af_kore`, `af_nicole`, `af_nova`, `af_river`, `af_sarah`, `af_sky`

**American Male (am_):** `am_adam`, `am_echo`, `am_eric`, `am_fenrir`, `am_liam`, `am_michael`, `am_onyx`, `am_puck`, `am_santa`

**British Female (bf_):** `bf_alice`, `bf_emma`, `bf_isabella`, `bf_lily`

**British Male (bm_):** `bm_daniel`, `bm_fable`, `bm_george`, `bm_lewis`

**Japanese Female (jf_):** `jf_alpha`, `jf_gongitsune`, `jf_nezumi`, `jf_tebukuro`

**Japanese Male (jm_):** `jm_kumo`

**Chinese Female (zf_):** `zf_xiaobei`, `zf_xiaoni`, `zf_xiaoxiao`, `zf_xiaoyi`

**Chinese Male (zm_):** `zm_yunjian`, `zm_yunxi`, `zm_yunxia`, `zm_yunyang`

**Other Languages:** `ef_dora`, `em_alex`, `em_santa`, `ff_siwis`, `hf_alpha`, `hf_beta`, `hm_omega`, `hm_psi`, `if_sara`, `im_nicola`, `pf_dora`, `pm_alex`, `pm_santa`

### Cartesia (94+ voices)
Key voices include: `reading lady`, `newsman`, `child`, `meditation lady`, `maria`, `calm lady`, `helpful woman`, `reading man`, `new york man`, `barbershop man`, `customer support man`, `sarah`, `laidback woman`, `reflective woman`, `professional woman`, `california girl`, `john`, `anna`

Regional voices: `german conversational woman`, `french conversational lady`, `indian lady`, `british reading lady`, `japanese children book`, `korean narrator woman`, `russian calm lady`, `chinese female conversational`, `spanish narrator man`, `dutch confident man`, `hindi reporter man`, `italian calm man`, `swedish narrator man`, `polish confident man`

### Rime Mist v2 (14 voices)
`cove`, `eucalyptus`, `lagoon`, `mari`, `marlu`, `mesa_extra`, `moon`, `moraine`, `peak`, `summit`, `talon`, `thunder`, `tundra`, `wildflower`

### Rime Arcana v2/v3/v3 Turbo (22+ voices)
`albion`, `arcade`, `astra`, `atrium`, `bond`, `cupola`, `eliphas`, `estelle`, `eucalyptus`, `fern`, `lintel`, `luna`, `lyra`, `marlu`, `masonry`, `moss`, `oculus`, `parapet`, `pilaster`, `sirius`, `stucco`, `transom`, `truss`, `vashti`, `vespera`, `walnut`

### MiniMax Speech 2.6 Turbo (sample voices)
`English_DeterminedMan`, `English_Diligent_Man`, `English_expressive_narrator`, `English_FriendlyNeighbor`, `English_Graceful_Lady`, `Japanese_GentleButler`

Query the full list via API:

```python
response = client.audio.voices.list()
```

```typescript
import fetch from "node-fetch";

async function getVoices() {
  const apiKey = process.env.TOGETHER_API_KEY;
  const model = "canopylabs/orpheus-3b-0.1-ft";
  const url = `https://api.together.xyz/v1/voices?model=${model}`;

  const response = await fetch(url, {
    headers: {
      Authorization: `Bearer ${apiKey}`,
    },
  });

  const data = await response.json();

  console.log(`Available voices for ${model}:`);
  for (const voice of data.voices || []) {
    console.log(voice.name || "Unknown voice");
  }
}

getVoices();
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `model` | string | Yes | TTS model identifier |
| `input` | string | Yes | Text to synthesize |
| `voice` | string | Yes | Voice ID |
| `response_format` | string | No | `mp3`, `wav`, `raw`, `mulaw`. MiniMax also: `opus`, `aac`, `flac`. Default: `wav` |
| `stream` | bool | No | Enable streaming (raw format only) |
| `response_encoding` | string | No | `pcm_s16le`, `pcm_f32le` for raw format |
| `sample_rate` | int | No | Audio sample rate (e.g., 44100, 48000) |

## WebSocket Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model_id` | string | TTS model |
| `voice` | string | Voice ID |
| `response_format` | string | `mp3`, `opus`, `aac`, `flac`, `wav`, `pcm` |
| `speed` | float | Playback speed (default: 1.0) |
| `max_partial_length` | int | Character buffer before triggering TTS |

## WebSocket Events

**Client to Server:**
- `input_text_buffer.append` — Append text
- `input_text_buffer.commit` — Force processing
- `input_text_buffer.clear` — Clear buffer
- `tts_session.updated` — Update session (e.g., voice)

**Server to Client:**
- `session.created` — Session established
- `conversation.item.input_text.received` — Text acknowledged
- `conversation.item.audio_output.delta` — Audio chunk (base64)
- `conversation.item.audio_output.done` — Generation complete
- `conversation.item.tts.failed` — Error

### WebSocket Example (TypeScript)

```typescript
import WebSocket from "ws";
import fs from "fs";

const apiKey = process.env.TOGETHER_API_KEY;
const url =
  "wss://api.together.ai/v1/audio/speech/websocket?model=hexgrad/Kokoro-82M&voice=af_alloy";

const ws = new WebSocket(url, {
  headers: {
    Authorization: `Bearer ${apiKey}`,
  },
});

const audioData: Buffer[] = [];

ws.on("open", () => {
  console.log("WebSocket connection established!");
});

ws.on("message", (data) => {
  const message = JSON.parse(data.toString());

  if (message.type === "session.created") {
    console.log(`Session created: ${message.session.id}`);

    const textChunks = [
      "Hello, this is a test.",
      "This is the second sentence.",
      "And this is the final one.",
    ];

    textChunks.forEach((text, index) => {
      setTimeout(() => {
        ws.send(
          JSON.stringify({
            type: "input_text_buffer.append",
            text: text,
          })
        );
      }, index * 500);
    });

    setTimeout(() => {
      ws.send(JSON.stringify({ type: "input_text_buffer.commit" }));
    }, textChunks.length * 500 + 100);
  } else if (message.type === "conversation.item.input_text.received") {
    console.log(`Text received: ${message.text}`);
  } else if (message.type === "conversation.item.audio_output.delta") {
    const audioChunk = Buffer.from(message.delta, "base64");
    audioData.push(audioChunk);
    console.log(`Received audio chunk for item ${message.item_id}`);
  } else if (message.type === "conversation.item.audio_output.done") {
    console.log(`Audio generation complete for item ${message.item_id}`);
  } else if (message.type === "conversation.item.tts.failed") {
    const errorMessage = message.error?.message ?? "Unknown error";
    console.error(`Error: ${errorMessage}`);
    ws.close();
  }
});

ws.on("close", () => {
  if (audioData.length > 0) {
    const completeAudio = Buffer.concat(audioData);
    fs.writeFileSync("output.wav", completeAudio);
    console.log("Audio saved to output.wav");
  }
});

ws.on("error", (error) => {
  console.error("WebSocket error:", error);
});
```
