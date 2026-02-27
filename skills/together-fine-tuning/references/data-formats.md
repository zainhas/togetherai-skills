# Fine-tuning Data Formats Reference

## Format Overview

| Format | Use Case | Key Field |
|--------|----------|-----------|
| Conversational | Multi-turn chat | `messages` |
| Instruction | Prompt-completion pairs | `prompt` + `completion` |
| Generic Text | Text completion | `text` |
| Preference/DPO | Preference learning | `input` + `preferred_output` + `non_preferred_output` |
| VLM | Vision + language | `messages` with image content |

## Conversational Format

```json
{
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"},
    {"role": "assistant", "content": "Hi! How can I help?"},
    {"role": "user", "content": "Explain ML", "weight": 0},
    {"role": "assistant", "content": "Machine learning is...", "weight": 1}
  ]
}
```

- `weight: 0` — Exclude from loss (masking)
- `weight: 1` — Include in loss (default for assistant)
- By default, only assistant messages are trained on

## Instruction Format

```json
{"prompt": "What is photosynthesis?", "completion": "Photosynthesis is..."}
```

- By default, model not trained on prompt text
- Use `train_on_inputs=true` to train on prompts too

## Generic Text Format

```json
{"text": "The quick brown fox jumps over the lazy dog."}
```

## Preference/DPO Format

```json
{
  "input": {
    "messages": [
      {"role": "user", "content": "What's open-source AI?"}
    ]
  },
  "preferred_output": [
    {"role": "assistant", "content": "Open-source AI means models are free to use, modify, and share..."}
  ],
  "non_preferred_output": [
    {"role": "assistant", "content": "It means the code is public."}
  ]
}
```

## VLM Conversational Format

```json
{
  "messages": [
    {"role": "system", "content": [{"type": "text", "text": "Vision assistant."}]},
    {"role": "user", "content": [
      {"type": "text", "text": "How many oranges?"},
      {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64,iVBORw0KG..."}}
    ]},
    {"role": "assistant", "content": [{"type": "text", "text": "There are 7 oranges."}]}
  ]
}
```

- Images must be base64 encoded with MIME prefix
- Max 10 images per example, 10MB each
- Formats: PNG, JPEG, WEBP
- Only user messages can contain images

## VLM Instruction Format

```json
{
  "prompt": [
    {"type": "text", "text": "Describe this image."},
    {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64,..."}}
  ],
  "completion": [{"type": "text", "text": "The image shows..."}]
}
```

## File Formats

### JSONL (Default)
- One JSON object per line
- Text data
- Automatic sample packing

### Parquet (Advanced)
- Pre-tokenized data
- Required: `input_ids`, `attention_mask`
- Optional: `labels` (use -100 to mask tokens)
- Max file size: 25GB

## Data Validation

```python
from together import Together
from together.utils import check_file

client = Together()

# Check format locally
report = check_file("my_data.jsonl")
print(report)  # {"is_check_passed": true, "message": "Checks passed", ...}

# Upload with server-side validation
file = client.files.upload(file="my_data.jsonl", purpose="fine-tune", check=True)
print(file.id)  # file-abc123
```

```typescript
import { upload } from "together-ai/lib/upload";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const filepath = path.join(__dirname, "my_data.jsonl");
const file = await upload(filepath);
console.log(file.id);
```

```shell
# cURL: upload a file
curl "https://api.together.xyz/v1/files/upload" \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -F "file=@my_data.jsonl" \
  -F "file_name=my_data.jsonl" \
  -F "purpose=fine-tune"
```

```shell
# CLI: check format and upload
together files check my_data.jsonl
together files upload my_data.jsonl

# Upload without format checking
together files upload my_data.jsonl --no-check

# List uploaded files
together files list

# Retrieve file metadata
together files retrieve <FILE-ID>

# Download a previously uploaded file
together files retrieve-content <FILE-ID>
```

## Converting Image URLs to Base64

```python
import base64, requests

def url_to_base64(url, mime_type="image/jpeg"):
    response = requests.get(url)
    encoded = base64.b64encode(response.content).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"
```
