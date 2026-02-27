# Function Calling Patterns Reference

## 6 Calling Patterns

### 1. Simple — Single function, single call

Model picks one function and calls it once.

```python
tools = [{
    "type": "function",
    "function": {
        "name": "get_current_weather",
        "description": "Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA",
                },
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

tool_call = response.choices[0].message.tool_calls[0]
# Execute: get_current_weather(location="New York, NY", unit="fahrenheit")
```

```typescript
import Together from "together-ai";
const together = new Together();

const response = await together.chat.completions.create({
  model: "Qwen/Qwen2.5-7B-Instruct-Turbo",
  messages: [
    {
      role: "system",
      content: "You are a helpful assistant that can access external functions.",
    },
    { role: "user", content: "What is the current temperature of New York?" },
  ],
  tools: [
    {
      type: "function",
      function: {
        name: "getCurrentWeather",
        description: "Get the current weather in a given location",
        parameters: {
          type: "object",
          properties: {
            location: {
              type: "string",
              description: "The city and state, e.g. San Francisco, CA",
            },
            unit: {
              type: "string",
              description: "The unit of temperature",
              enum: ["celsius", "fahrenheit"],
            },
          },
        },
      },
    },
  ],
});

console.log(JSON.stringify(response.choices[0].message?.tool_calls, null, 2));
```

### 2. Multiple Functions — Model picks which to call

Multiple tools available, model chooses the right one.

```python
tools = [
    {"type": "function", "function": {"name": "get_weather", ...}},
    {"type": "function", "function": {"name": "get_restaurant", ...}},
]

# User: "Find me a restaurant in SF"
# Model picks: get_restaurant(location="San Francisco")
```

### 3. Parallel — Same function, multiple calls

Model calls the same function multiple times in one turn.

```python
import json
from together import Together
client = Together()

response = client.chat.completions.create(
    model="Qwen/Qwen2.5-7B-Instruct-Turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant that can access external functions."},
        {"role": "user", "content": "What is the current temperature of New York, San Francisco and Chicago?"},
    ],
    tools=[{
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "The city and state, e.g. San Francisco, CA"},
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
            },
        },
    }],
)

# Model returns 3 tool_calls:
#   get_current_weather(location="New York, NY", unit="fahrenheit")
#   get_current_weather(location="San Francisco, CA", unit="fahrenheit")
#   get_current_weather(location="Chicago, IL", unit="fahrenheit")
for tc in response.choices[0].message.tool_calls:
    result = execute_function(tc.function.name, tc.function.arguments)
    messages.append({
        "role": "tool",
        "tool_call_id": tc.id,
        "content": json.dumps(result),
    })
```

```typescript
import Together from "together-ai";
const together = new Together();

const response = await together.chat.completions.create({
  model: "Qwen/Qwen2.5-7B-Instruct-Turbo",
  messages: [
    {
      role: "system",
      content: "You are a helpful assistant that can access external functions.",
    },
    {
      role: "user",
      content: "What is the current temperature of New York, San Francisco and Chicago?",
    },
  ],
  tools: [
    {
      type: "function",
      function: {
        name: "getCurrentWeather",
        description: "Get the current weather in a given location",
        parameters: {
          type: "object",
          properties: {
            location: {
              type: "string",
              description: "The city and state, e.g. San Francisco, CA",
            },
            unit: {
              type: "string",
              description: "The unit of temperature",
              enum: ["celsius", "fahrenheit"],
            },
          },
        },
      },
    },
  ],
});

// Model returns 3 tool_calls for NYC, SF, and Chicago
console.log(JSON.stringify(response.choices[0].message?.tool_calls, null, 2));
```

### 4. Parallel Multiple — Different functions in one turn

Model calls multiple different functions simultaneously.

```python
# User: "What's the weather in NYC and find restaurants there?"
# Model returns 2 tool_calls:
#   get_weather(location="New York")
#   get_restaurant(location="New York")
```

### 5. Multi-step — Chained function calls

Result of one call informs the next call.

```python
# Turn 1: Model calls get_weather(location="NYC")
# You return result, model processes it
# Turn 2: Model calls get_restaurant(location="NYC", cuisine="outdoor-friendly")
# Based on weather being nice
```

### 6. Multi-turn — Function calls across conversation turns

Function calls happening across a full conversation with user.

```python
messages = [{"role": "system", "content": "Travel planning assistant."}]

# Turn 1: User asks about weather
# → Model calls get_weather for 3 cities
# → Returns weather info

# Turn 2: User asks for restaurant based on weather
# → Model remembers previous weather data
# → Calls get_restaurant for best weather city
```

## Processing Tool Calls

```python
# 1. Get tool calls from response
tool_calls = response.choices[0].message.tool_calls

# 2. Add assistant message to history
messages.append(response.choices[0].message)

# 3. Execute each function and add results
for tc in tool_calls:
    args = json.loads(tc.function.arguments)
    result = execute_function(tc.function.name, args)
    messages.append({
        "role": "tool",
        "tool_call_id": tc.id,
        "content": json.dumps(result),
    })

# 4. Get final response
final = client.chat.completions.create(
    model="Qwen/Qwen2.5-7B-Instruct-Turbo",
    messages=messages,
    tools=tools,
)
```

## tool_choice Parameter

| Value | Behavior |
|-------|----------|
| `"auto"` (default) | Model decides whether to call functions |
| `"none"` | Never call functions |
| `{"type": "function", "function": {"name": "fn"}}` | Force specific function |

## Supported Models

Function calling works with: Qwen2.5 family, Llama 3.x family, DeepSeek V3, Mistral, GLM, Kimi K2, and most chat models.
