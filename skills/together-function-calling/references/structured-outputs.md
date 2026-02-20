# Structured Outputs Reference

## Three Modes

### 1. json_schema (Recommended)

Constrains output to match your JSON schema exactly.

```python
from pydantic import BaseModel, Field

class VoiceNote(BaseModel):
    title: str = Field(description="A title")
    summary: str = Field(description="Short summary")
    actionItems: list[str] = Field(description="Action items")

response = client.chat.completions.create(
    model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
    messages=[
        {"role": "system", "content": f"Respond in JSON: {json.dumps(VoiceNote.model_json_schema())}"},
        {"role": "user", "content": transcript},
    ],
    response_format={
        "type": "json_schema",
        "schema": VoiceNote.model_json_schema(),
    },
)
result = VoiceNote.model_validate_json(response.choices[0].message.content)
```

**TypeScript:**
```typescript
import { z } from "zod";
import { zodToJsonSchema } from "zod-to-json-schema";

const schema = z.object({
  title: z.string(),
  summary: z.string(),
  actionItems: z.array(z.string()),
});

const response = await together.chat.completions.create({
  model: "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
  messages: [...],
  response_format: { type: "json_schema", schema: zodToJsonSchema(schema, { target: "openAi" }) },
});
```

### 2. json_object (Simple)

Model outputs valid JSON but structure is guided by prompt only.

```python
response = client.chat.completions.create(
    model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
    messages=[
        {"role": "system", "content": "Respond in JSON with keys: name, age, city"},
        {"role": "user", "content": "Tell me about yourself"},
    ],
    response_format={"type": "json_object"},
)
```

### 3. regex (Pattern Matching)

Constrains output to match a regex pattern.

```python
# Sentiment classification
response = client.chat.completions.create(
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
    messages=[
        {"role": "system", "content": "Classify sentiment."},
        {"role": "user", "content": "I loved the movie!"},
    ],
    response_format={
        "type": "regex",
        "pattern": "(positive|neutral|negative)",
    },
)

# Phone number
response_format={"type": "regex", "regex": r"\(\d{3}\) \d{3}-\d{4}"}

# Email
response_format={"type": "regex", "pattern": r"\w+@\w+\.com\n"}
```

## Supported Models

### Top Models (json_schema, json_object, regex)
- `openai/gpt-oss-120b`
- `openai/gpt-oss-20b`
- `moonshotai/Kimi-K2-Instruct`
- `zai-org/GLM-5`
- `zai-org/GLM-4.5-Air-FP8`
- `MiniMaxAI/MiniMax-M2.5`
- `Qwen/Qwen3.5-397B-A17B`
- `Qwen/Qwen3-235B-A22B-Thinking-2507`
- `Qwen/Qwen3-Coder-480B-A35B-Instruct-FP8`
- `deepseek-ai/DeepSeek-R1`
- `deepseek-ai/DeepSeek-V3`
- `meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8`
- `Qwen/Qwen2.5-VL-72B-Instruct`

### Additional Supported Models
- `meta-llama/Llama-3.3-70B-Instruct-Turbo`
- `deepcogito/cogito-v2-preview-llama-70B`
- `deepcogito/cogito-v2-preview-llama-405B`
- `deepseek-ai/DeepSeek-R1-Distill-Llama-70B`
- `deepseek-ai/DeepSeek-R1-Distill-Qwen-14B`
- `meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo`
- `Qwen/Qwen2.5-7B-Instruct-Turbo`
- `Qwen/Qwen2.5-Coder-32B-Instruct`
- `Qwen/QwQ-32B`
- `meta-llama/Llama-3.2-3B-Instruct-Turbo`
- `google/gemma-3n-E4B-it`
- `mistralai/Mistral-7B-Instruct-v0.1`
- `mistralai/Mistral-7B-Instruct-v0.2`
- `mistralai/Mistral-7B-Instruct-v0.3`

## Prompting Best Practices

1. Always tell the model to respond **only in JSON**
2. Include a plain-text copy of the schema in the prompt
3. Use `json_schema` mode when you need guaranteed structure
4. Use `regex` mode for simple constrained outputs (classification, IDs)
5. Works with vision models (e.g., `Qwen/Qwen2.5-VL-72B-Instruct`)
6. Works with reasoning models (e.g., `deepseek-ai/DeepSeek-R1`)
