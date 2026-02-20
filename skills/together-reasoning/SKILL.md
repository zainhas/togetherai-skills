---
name: together-reasoning
description: Use reasoning and thinking models on Together AI including DeepSeek R1, DeepSeek V3.1, Kimi K2-Thinking, and Qwen3 with thinking mode. Models output chain-of-thought in think tags before answering. Adjustable reasoning effort (low/medium/high). Use when users need reasoning models, chain-of-thought, step-by-step thinking, math/code/logic problem solving, or adjustable reasoning depth.
---

# Together Reasoning Models

## Overview

Reasoning models think step-by-step before answering, excelling at complex tasks like coding, math, planning, and logic. They output chain-of-thought in `<think>` tags followed by the answer.

Tradeoff: Better reasoning quality, but longer outputs and higher cost.

## Quick Start

### DeepSeek R1

```python
from together import Together
client = Together()

stream = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-R1",
    messages=[{"role": "user", "content": "Which is bigger: 9.9 or 9.11?"}],
    stream=True,
)
for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="", flush=True)
```

Output includes thinking and answer:
```
<think>
Let me compare 9.9 and 9.11...
9.9 = 9.90, and 9.90 > 9.11
</think>

**Answer:** 9.9 is bigger.
```

### Parse Thinking vs Answer

```python
import re

response = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-R1",
    messages=[{"role": "user", "content": "Solve: 15% of 240"}],
)
content = response.choices[0].message.content

think_match = re.search(r"<think>(.*?)</think>", content, re.DOTALL)
thinking = think_match.group(1).strip() if think_match else ""
answer = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()

print(f"Thinking: {thinking[:100]}...")
print(f"Answer: {answer}")
```

## Reasoning Models

| Model | API String | Strengths |
|-------|-----------|-----------|
| DeepSeek R1 | `deepseek-ai/DeepSeek-R1` | Math, code, complex reasoning |
| DeepSeek R1 (throughput) | `deepseek-ai/DeepSeek-R1-0528-tput` | Batch-optimized R1 |
| DeepSeek V3.1 | `deepseek-ai/DeepSeek-V3-0324` | General + reasoning |
| Kimi K2 Thinking | `moonshotai/Kimi-K2-Thinking` | Extended reasoning |
| Qwen3 235B Thinking | `Qwen/Qwen3-235B-A22B-Thinking-2507` | Thinking mode |
| QwQ 32B | `Qwen/QwQ-32B` | Compact reasoning |
| R1 Distill Llama 70B | `deepseek-ai/DeepSeek-R1-Distill-Llama-70B` | Distilled reasoning |
| R1 Distill Qwen 14B | `deepseek-ai/DeepSeek-R1-Distill-Qwen-14B` | Compact distilled |

## Reasoning Effort

Control how much thinking the model does:

```python
# Low effort — fast, less thorough
response = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-R1",
    messages=[{"role": "user", "content": "What is 2+2?"}],
    reasoning_effort="low",
)

# High effort — slower, more thorough
response = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-R1",
    messages=[{"role": "user", "content": "Prove the infinitude of primes"}],
    reasoning_effort="high",
)
```

Values: `"low"`, `"medium"`, `"high"`

## Qwen3 Thinking Mode

Toggle thinking on/off for Qwen3 models:

```python
# With thinking enabled
response = client.chat.completions.create(
    model="Qwen/Qwen3-235B-A22B-Thinking-2507",
    messages=[{"role": "user", "content": "Explain quantum entanglement"}],
)

# Thinking disabled (faster, cheaper)
response = client.chat.completions.create(
    model="Qwen/Qwen3-235B-A22B-Instruct-2507-tput",
    messages=[{"role": "user", "content": "Explain quantum entanglement"}],
)
```

## Best Practices

### DeepSeek R1
- **Temperature**: 0.5-0.7 (recommended 0.6)
- **System prompts**: Omit — put all instructions in user message
- **Prompting**: Give high-level objectives, let model determine methodology
- Avoid over-prompting (micromanaging steps)

### General
- Use streaming — reasoning outputs are long
- Use `reasoning_effort="low"` for simple questions to save cost
- Use `reasoning_effort="high"` for complex math/code/logic
- Reasoning models cost more (more output tokens) — use standard models for simple tasks

## Resources

- **Model details**: See [references/models.md](references/models.md)
