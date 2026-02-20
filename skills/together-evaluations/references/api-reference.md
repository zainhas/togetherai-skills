# AI Evaluations API Reference

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST /evaluation` | Create evaluation | Start a new evaluation |
| `GET /evaluation/{id}` | Get evaluation | Retrieve evaluation details |
| `GET /evaluation/{id}/status` | Get status | Check evaluation progress |
| `GET /evaluation` | List evaluations | List all evaluations |
| `GET /evaluation/model-list` | List models | Models available for judging |

## Evaluation Types

### 1. Classify
Categorizes responses into predefined labels.

```python
eval = client.evals.create(
    type="classify",
    judge_model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
    judge_model_source="serverless",
    judge_system_template="Classify the response quality as: {{labels}}",
    labels=["good", "bad", "neutral"],
    pass_labels=["good"],
    model_to_evaluate={
        "model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        "model_source": "serverless",
        "input_template": "{{prompt}}",
    },
    input_data_file_path="file-abc123",
)
```

**Result:** `label_counts`, `pass_percentage`

### 2. Score
Rates responses on a numerical scale.

```python
eval = client.evals.create(
    type="score",
    judge_model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
    judge_model_source="serverless",
    judge_system_template="Rate the response from {{min_score}} to {{max_score}}",
    min_score=1.0,
    max_score=10.0,
    pass_threshold=7.0,
    model_to_evaluate={...},
    input_data_file_path="file-abc123",
)
```

**Result:** `mean_score`, `std_score`, `pass_percentage`

### 3. Compare
Pits two models against each other.

```python
eval = client.evals.create(
    type="compare",
    judge_model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
    judge_model_source="serverless",
    judge_system_template="Compare responses A and B. Which is better?",
    model_a={"model": "model-a", "model_source": "serverless", ...},
    model_b={"model": "model-b", "model_source": "serverless", ...},
    input_data_file_path="file-abc123",
)
```

**Result:** `A_wins`, `B_wins`, `Ties`

## Model Configuration Object

```python
{
    "model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
    "model_source": "serverless",  # "serverless", "dedicated", "external"
    "system_template": "You are a helpful assistant.",
    "input_template": "{{prompt}}",
    "max_tokens": 512,
    "temperature": 0.7,
    # For external models:
    "external_api_token": "sk-...",
    "external_base_url": "https://api.openai.com/v1",
}
```

## Model Sources

### Serverless
Any Together AI serverless model.

### Dedicated
Your deployed dedicated endpoint (use endpoint ID).

### External (Supported Shortcuts)

| Provider | Models |
|----------|--------|
| OpenAI | `openai/gpt-5`, `openai/gpt-5-mini`, `openai/gpt-4o`, `openai/gpt-4o-mini` |
| Anthropic | `anthropic/claude-sonnet-4-5`, `anthropic/claude-haiku-4-5`, `anthropic/claude-opus-4-5` |
| Google | `google/gemini-2.5-pro`, `google/gemini-2.5-flash`, `google/gemini-2.0-flash` |

## Jinja2 Templates

Both `system_template` and `input_template` support Jinja2:
- `{{column_name}}` — Simple substitution from dataset
- `{{column_name.field}}` — Nested fields
- Conditional logic and loops supported

## Evaluation Status Flow

`pending` → `queued` → `running` → `completed`

## CLI Commands

```shell
together evals create --type classify --judge-model meta-llama/Llama-3.3-70B-Instruct-Turbo ...
together evals list
together evals retrieve <EVAL_ID>
together evals status <EVAL_ID>
```
