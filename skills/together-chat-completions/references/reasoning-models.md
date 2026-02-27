# Reasoning Models Reference

## Full Model Table

| Model | API String | Context Length | Strengths | Quantization |
|-------|-----------|---------------|-----------|-------------|
| DeepSeek R1 (0528) | `deepseek-ai/DeepSeek-R1` | 163,839 | Math, code, complex reasoning | FP8 |
| DeepSeek R1 (throughput) | `deepseek-ai/DeepSeek-R1-0528-tput` | 163,839 | Batch-optimized R1 | FP8 |
| DeepSeek V3.1 | `deepseek-ai/DeepSeek-V3.1` | 128,000 | General + reasoning | FP8 |
| Kimi K2 Thinking | `moonshotai/Kimi-K2-Thinking` | 262,144 | Extended reasoning | INT4 |
| Kimi K2.5 | `moonshotai/Kimi-K2.5` | 262,144 | Chat + reasoning hybrid | INT4 |
| Qwen3 235B Thinking | `Qwen/Qwen3-235B-A22B-Thinking-2507` | 262,144 | Thinking mode | FP8 |
| Qwen3-Next 80B Thinking | `Qwen/Qwen3-Next-80B-A3B-Thinking` | 262,144 | Compact MoE thinking | BF16 |
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

All reasoning models output chain-of-thought in `<think>` tags:

```
<think>
Step-by-step reasoning here...
</think>

Final answer here.
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

The model reasons in `<think>` tags then produces structured JSON output.
