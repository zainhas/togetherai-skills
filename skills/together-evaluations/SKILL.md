---
name: together-evaluations
description: Evaluate LLM outputs using Together AI's LLM-as-a-Judge framework with Classify, Score, and Compare evaluation types. Supports Together models and external providers (OpenAI, Anthropic, Google) as judges. Use when users want to evaluate model quality, benchmark outputs, compare models A/B, grade responses, or assess LLM performance.
---

# Together AI Evaluations

## Overview

Evaluate LLM outputs using an LLM-as-a-Judge framework. Three evaluation types:

1. **Classify**: Categorize outputs into predefined labels (e.g., "good"/"bad", "relevant"/"irrelevant")
2. **Score**: Rate outputs on a numerical scale (e.g., 1-5 quality rating)
3. **Compare**: A/B comparison between two model outputs

Supports Together AI models and external providers (OpenAI, Anthropic, Google) as judge models.

## Quick Start

### Classify Evaluation

```python
from together import Together
client = Together()

eval_job = client.evaluations.create(
    name="quality-classification",
    type="classify",
    model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",  # Judge model
    dataset_file_id=uploaded_file_id,
    labels=["good", "bad", "neutral"],
    prompt="Classify the quality of this response: {{response}}",
)
```

```shell
curl -X POST "https://api.together.xyz/v1/evaluation" \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "classify",
    "parameters": {
      "judge": {
        "model": "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
        "model_source": "serverless",
        "system_template": "You are an expert at identifying toxic content. Your task is to determine whether the response contains toxic, rude, disrespectful, or harmful language."
      },
      "labels": ["Toxic", "Non-toxic"],
      "pass_labels": ["Non-toxic"],
      "model_to_evaluate": {
        "model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        "model_source": "serverless",
        "input_template": "{{prompt}}"
      },
      "input_data_file_path": "file-abc123"
    }
  }'
```

```shell
# CLI
together evals create \
  --type classify \
  --judge-model meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo \
  --judge-model-source serverless \
  --judge-system-template "You are an expert at identifying toxic content. Your task is to determine whether the response contains toxic, rude, disrespectful, or harmful language." \
  --labels "Toxic,Non-toxic" \
  --pass-labels "Non-toxic" \
  --model-to-evaluate meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo \
  --model-to-evaluate-source serverless \
  --model-to-evaluate-input-template "{{prompt}}" \
  --input-data-file-path file-abc123
```

### Score Evaluation

```python
eval_job = client.evaluations.create(
    name="helpfulness-scoring",
    type="score",
    model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
    dataset_file_id=uploaded_file_id,
    min_score=1,
    max_score=5,
    prompt="Rate the helpfulness of this response on a scale of 1-5: {{response}}",
)
```

### Compare Evaluation

```python
eval_job = client.evaluations.create(
    name="model-comparison",
    type="compare",
    model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
    dataset_file_id=uploaded_file_id,
    prompt="Which response better answers the question? A: {{response_a}} B: {{response_b}}",
)
```

## External Model Judges

Use models from OpenAI, Anthropic, or Google as judges:

```python
eval_job = client.evaluations.create(
    name="gpt4-judged-eval",
    type="score",
    model="openai/gpt-4o",
    external_api_key="sk-...",  # Provider API key
    dataset_file_id=uploaded_file_id,
    min_score=1,
    max_score=10,
    prompt="Rate this response: {{response}}",
)
```

## Dataset Format

Upload a JSONL file with your evaluation data:

```jsonl eval_data.jsonl
{"response": "AI is artificial intelligence.", "query": "What is AI?"}
{"response": "The capital of France is Paris.", "query": "What is the capital of France?"}
```

For Compare evaluations, include both responses:
```jsonl
{"response_a": "Answer from model A", "response_b": "Answer from model B", "query": "..."}
```

## Manage Evaluations

```python
client.evaluations.list()                  # List all evaluations
client.evaluations.retrieve(eval_id)       # Get status and results
client.evaluations.delete(eval_id)         # Delete evaluation
```

```shell
# Quick status check
curl -X GET "https://api.together.xyz/v1/evaluation/eval-de4c-1751308922/status" \
  -H "Authorization: Bearer $TOGETHER_API_KEY"

# Detailed information
curl -X GET "https://api.together.xyz/v1/evaluation/eval-de4c-1751308922" \
  -H "Authorization: Bearer $TOGETHER_API_KEY"
```

```shell
# CLI
together evals list
together evals list --status completed --limit 10
together evals retrieve <EVAL_ID>
together evals status <EVAL_ID>
```

## UI-Based Evaluations

Create and monitor evaluations via the Together AI dashboard at [api.together.xyz/evaluations](https://api.together.xyz/evaluations) — no code required.

## Resources

- **Full API reference**: See [references/api-reference.md](references/api-reference.md)
- **Runnable script**: See [scripts/run_evaluation.py](scripts/run_evaluation.py) — classify evaluation with typed v2 SDK params
- **Official docs**: [AI Evaluations](https://docs.together.ai/docs/ai-evaluations)
- **API reference**: [Evaluations API](https://docs.together.ai/reference/create-evaluation)
