# Reasoning Models Reference

## Full Model Table

| Model | API String | Context Length | Strengths | Quantization |
|-------|-----------|---------------|-----------|-------------|
| DeepSeek R1 (0528) | `deepseek-ai/DeepSeek-R1` | 163,839 | Math, code, complex reasoning | FP8 |
| DeepSeek R1 (throughput) | `deepseek-ai/DeepSeek-R1-0528-tput` | 163,839 | Batch-optimized R1 | FP8 |
| DeepSeek V3.1 | `deepseek-ai/DeepSeek-V3.1` | 128,000 | General + reasoning | FP8 |
| GLM-5 | `zai-org/GLM-5` | 131,072 | Hybrid | FP8 |
| GPT-OSS 120B | `openai/gpt-oss-120b` | 131,072 | Reasoning only (adjustable effort) | FP8 |
| GPT-OSS 20B | `openai/gpt-oss-20b` | 131,072 | Reasoning only (adjustable effort) | FP8 |
| Kimi K2 Thinking | `moonshotai/Kimi-K2-Thinking` | 262,144 | Extended reasoning | INT4 |
| Kimi K2.5 | `moonshotai/Kimi-K2.5` | 262,144 | Chat + reasoning hybrid | INT4 |
| MiniMax M2.5 | `MiniMaxAI/MiniMax-M2.5` | 131,072 | Reasoning only | FP8 |
| Qwen3 235B Thinking | `Qwen/Qwen3-235B-A22B-Thinking-2507` | 262,144 | Thinking mode | FP8 |
| Qwen3-Next 80B Thinking | `Qwen/Qwen3-Next-80B-A3B-Thinking` | 262,144 | Compact MoE thinking | BF16 |
| Qwen3.5 397B | `Qwen/Qwen3.5-397B-A17B` | 262,144 | Hybrid | FP8 |
| QwQ 32B | `Qwen/QwQ-32B` | 32,768 | Compact reasoning | - |
| R1 Distill Llama 70B | `deepseek-ai/DeepSeek-R1-Distill-Llama-70B` | 131,072 | Distilled reasoning | - |
| R1 Distill Qwen 14B | `deepseek-ai/DeepSeek-R1-Distill-Qwen-14B` | 32,768 | Compact distilled | - |

## Reasoning Effort Levels

| Level | Behavior | Best For |
|-------|----------|----------|
| `"low"` | Minimal thinking, fast | Simple factual questions |
| `"medium"` | Balanced | Most tasks |
| `"high"` | Extensive thinking, thorough | Complex math, code, logic proofs |

## Output Format

**Most reasoning models** (Kimi K2.5, GLM-5, GPT-OSS, Qwen3 Thinking, etc.) return reasoning in a separate `reasoning` field:

```python
response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[{"role": "user", "content": "Which is bigger: 9.9 or 9.11?"}],
)
reasoning = response.choices[0].message.reasoning  # step-by-step thinking
answer = response.choices[0].message.content         # final answer
```

**DeepSeek R1** is a special case that outputs reasoning inside `<think>` tags within the `content` field:

```
<think>
Step-by-step reasoning here...
</think>

Final answer here.
```

## Reasoning Effort Examples

### Python

```python
response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[{"role": "user", "content": "Prove the infinitude of primes"}],
    reasoning_effort="high",
)
```

### TypeScript

```typescript
import Together from "together-ai";
const together = new Together();

const stream = await together.chat.completions.create({
  model: "openai/gpt-oss-120b",
  messages: [{ role: "user", content: "Prove the infinitude of primes" }],
  reasoning_effort: "high",
  stream: true,
});

for await (const chunk of stream) {
  process.stdout.write(chunk.choices[0]?.delta?.content || "");
}
```

### cURL

```shell
curl -X POST "https://api.together.xyz/v1/chat/completions" \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai/gpt-oss-120b",
    "messages": [
      {"role": "user", "content": "Prove the infinitude of primes"}
    ],
    "reasoning_effort": "high"
  }'
```

## Qwen3 Thinking Toggle

**Thinking enabled:** Use the `-Thinking` model variant
```python
model="Qwen/Qwen3-235B-A22B-Thinking-2507"
```

**Thinking disabled (faster, cheaper):** Use the `-Instruct` or `-tput` variant
```python
model="Qwen/Qwen3-235B-A22B-Instruct-2507-tput"
```

## Best Practices by Model

### DeepSeek R1
- **Temperature:** 0.5-0.7 (recommended 0.6)
- **System prompts:** Omit — put all instructions in user message
- **Prompting:** High-level objectives, let model determine methodology
- Avoid micromanaging reasoning steps

### Kimi K2 Thinking
- Supports extended reasoning chains
- Good for multi-step planning tasks

### Qwen3 Thinking
- Toggle thinking on/off via model variant selection
- Good for tasks where you want optional reasoning depth

## Structured Outputs with Reasoning

Reasoning models support JSON mode for structured output extraction:

```python
response = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-R1",
    messages=[...],
    response_format={
        "type": "json_schema",
        "schema": YourSchema.model_json_schema(),
    },
)
```

The model reasons internally (via `reasoning` field or `<think>` tags depending on the model) then produces structured JSON output.
