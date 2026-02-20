---
name: together-function-calling
description: Implement function calling (tool use) and structured outputs (JSON mode, json_schema, regex) via Together AI. 6 calling patterns from simple to multi-turn. Use when users need function calling, tool use, structured JSON responses, schema-constrained outputs, agent tool integration, or programmatic LLM output parsing.
---

# Together Function Calling & Structured Outputs

## Overview

Two capabilities for structured LLM interactions:
1. **Function calling**: Model returns structured function calls you execute
2. **Structured outputs**: Model responds in JSON matching a schema

## Function Calling

### Basic Example

```python
import json
from together import Together
client = Together()

tools = [{
    "type": "function",
    "function": {
        "name": "get_current_weather",
        "description": "Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "City and state, e.g. San Francisco, CA"},
                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
            },
        },
    },
}]

response = client.chat.completions.create(
    model="Qwen/Qwen2.5-7B-Instruct-Turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant that can access external functions."},
        {"role": "user", "content": "What is the current temperature of New York?"},
    ],
    tools=tools,
)

tool_calls = response.choices[0].message.tool_calls
print(json.dumps([tc.model_dump() for tc in tool_calls], indent=2))
```

### Processing Tool Calls

```python
# Execute the function
result = get_current_weather(location="New York, NY", unit="fahrenheit")

# Pass result back to model
messages.append(response.choices[0].message)
messages.append({
    "role": "tool",
    "tool_call_id": tool_calls[0].id,
    "content": json.dumps(result),
})

final_response = client.chat.completions.create(
    model="Qwen/Qwen2.5-7B-Instruct-Turbo",
    messages=messages,
    tools=tools,
)
```

### tool_choice Parameter

- `"auto"` (default): Model decides whether to call functions
- `"none"`: Never call functions
- `{"type": "function", "function": {"name": "fn_name"}}`: Force specific function

## 6 Function Calling Patterns

1. **Simple**: Single function, single call
2. **Multiple functions**: Multiple tools available, model picks one
3. **Parallel**: Model calls same function multiple times in one turn
4. **Parallel multiple**: Multiple different functions in one turn
5. **Multi-step**: Chain of function calls (call → result → call → result)
6. **Multi-turn**: Function calls across conversation turns

See [references/patterns.md](references/patterns.md) for detailed examples of each pattern.

## Structured Outputs (JSON Mode)

### json_schema (Recommended)

```python
from pydantic import BaseModel, Field

class VoiceNote(BaseModel):
    title: str = Field(description="A title for the voice note")
    summary: str = Field(description="Short summary")
    actionItems: list[str] = Field(description="Action items")

response = client.chat.completions.create(
    model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
    messages=[{"role": "user", "content": "Summarize: Meeting about Q4 planning..."}],
    response_format={
        "type": "json_object",
        "schema": VoiceNote.model_json_schema(),
    },
)
result = VoiceNote.model_validate_json(response.choices[0].message.content)
```

### json_object (Simple)

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

### regex (Pattern Matching)

```python
response = client.chat.completions.create(
    model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
    messages=[{"role": "user", "content": "Generate a US phone number"}],
    response_format={
        "type": "regex",
        "regex": r"\(\d{3}\) \d{3}-\d{4}",
    },
)
```

## Supported Models

**Function calling**: Qwen2.5 family, Llama 3.x family, DeepSeek V3, Mistral, and most chat models.

**JSON mode**: DeepSeek R1/V3, GLM-5, Kimi K2, Llama 4, Qwen3/2.5 family, and many more. See [references/structured-outputs.md](references/structured-outputs.md) for the complete list.

## Resources

- **All 6 calling patterns**: See [references/patterns.md](references/patterns.md)
- **Structured output details**: See [references/structured-outputs.md](references/structured-outputs.md)
- **Runnable script**: See [scripts/tool_call_loop.py](scripts/tool_call_loop.py) — complete tool call loop with parallel call handling (v2 SDK)
