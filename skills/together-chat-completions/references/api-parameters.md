# Chat Completions API Parameters

## Required Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model` | string | Model identifier (e.g., `meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo`) |
| `messages` | array | Array of message objects with `role` and `content` |

## Generation Parameters

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| `max_tokens` | integer | varies | 1+ | Maximum tokens to generate |
| `temperature` | float | varies | 0-1 | Randomness. Lower = more deterministic |
| `top_p` | float | 1.0 | 0-1 | Nucleus sampling threshold |
| `top_k` | integer | - | 1+ | Limit choices per token step |
| `min_p` | float | - | 0-1 | Alternative to top_p/top_k |
| `repetition_penalty` | float | 1.0 | - | Higher = less repetition |
| `presence_penalty` | float | 0 | -2.0 to 2.0 | Penalize tokens already present |
| `frequency_penalty` | float | 0 | -2.0 to 2.0 | Penalize frequent tokens |
| `stop` | string[] | - | - | Sequences that stop generation |
| `n` | integer | 1 | 1-128 | Number of completions to generate |
| `seed` | integer | - | - | For reproducible outputs |

## Output Control

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `stream` | bool | false | Stream tokens as Server-Sent Events |
| `logprobs` | integer | - | Return top-k token log probs (0-20) |
| `echo` | bool | false | Include prompt in response |
| `logit_bias` | object | - | Token ID to bias value mapping |

## Response Format

| Parameter | Type | Description |
|-----------|------|-------------|
| `response_format` | object | Control output structure |

Options:
```python
# Plain text (default)
response_format={"type": "text"}

# JSON object (model decides structure)
response_format={"type": "json_object"}

# JSON schema (constrained to your schema)
response_format={"type": "json_schema", "schema": {...}}

# Regex pattern matching
response_format={"type": "regex", "pattern": "..."}
```

## Function Calling

| Parameter | Type | Description |
|-----------|------|-------------|
| `tools` | array | Tool definitions the model can call |
| `tool_choice` | string/object | `"auto"`, `"none"`, or `{"type": "function", "function": {"name": "..."}}` |

## Safety & Compliance

| Parameter | Type | Description |
|-----------|------|-------------|
| `safety_model` | string | Moderation model (e.g., `meta-llama/Llama-Guard-4-12B`) |
| `compliance` | string | Set to `"hipaa"` for HIPAA mode |

## Reasoning

| Parameter | Type | Values | Description |
|-----------|------|--------|-------------|
| `reasoning_effort` | string | `"low"`, `"medium"`, `"high"` | Control reasoning depth |
| `reasoning` | object | `{"enabled": true/false}` | Toggle reasoning |

## Context Handling

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `context_length_exceeded_behavior` | string | `"error"` | `"truncate"` or `"error"` when exceeding context |

## Message Object

```python
{"role": "system", "content": "You are a helpful assistant."}
{"role": "user", "content": "Hello!"}
{"role": "assistant", "content": "Hi there!"}
{"role": "tool", "tool_call_id": "...", "content": "..."}
```

Multimodal content (vision models):
```python
{"role": "user", "content": [
    {"type": "text", "text": "What's in this image?"},
    {"type": "image_url", "image_url": {"url": "https://..."}},
    {"type": "video_url", "video_url": {"url": "https://..."}},
    {"type": "audio_url", "audio_url": {"url": "https://..."}},
]}
```

## HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad request (invalid params) |
| 401 | Unauthorized (invalid API key) |
| 404 | Model not found |
| 429 | Rate limit exceeded |
| 503 | Service overloaded |
| 504 | Request timeout |
