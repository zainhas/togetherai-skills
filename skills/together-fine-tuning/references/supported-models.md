# Fine-tuning Supported Models

## LoRA Fine-tuning

### Large Models
| Model | API String | Max Batch |
|-------|-----------|-----------|
| Kimi K2 Thinking | `moonshotai/Kimi-K2-Thinking` | 1 |
| Kimi K2 Instruct | `moonshotai/Kimi-K2-Instruct` | 1 |
| GLM-4.7 | `zai-org/GLM-4.7` | 1 |
| GPT-OSS 120B | `openai/gpt-oss-120b` | - |
| DeepSeek R1 | `deepseek-ai/DeepSeek-R1` | - |
| DeepSeek V3 | `deepseek-ai/DeepSeek-V3` | - |
| Qwen3 235B Thinking | `Qwen/Qwen3-235B-A22B-Thinking-2507` | - |
| Qwen3 235B Instruct | `Qwen/Qwen3-235B-A22B-Instruct-2507` | - |

### Medium Models (7B-70B)
| Model | API String |
|-------|-----------|
| Llama 3.3 70B | `meta-llama/Llama-3.3-70B-Instruct-Turbo` |
| Llama 3.1 70B | `meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo` |
| Llama 3.1 8B | `meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo` |
| GPT-OSS 20B | `openai/gpt-oss-20b` |
| Qwen 2.5 72B | `Qwen/Qwen2.5-72B-Instruct-Turbo` |
| Qwen 2.5 7B | `Qwen/Qwen2.5-7B-Instruct-Turbo` |
| Mixtral 8x7B | `mistralai/Mixtral-8x7B-Instruct-v0.1` |

### Small Models (<7B)
| Model | API String |
|-------|-----------|
| Llama 3.2 3B | `meta-llama/Llama-3.2-3B-Instruct-Turbo` |
| Llama 3.2 1B | `meta-llama/Llama-3.2-1B-Instruct-Turbo` |
| Gemma 3 4B | `google/gemma-3-4b-it` |
| Gemma 3 1B | `google/gemma-3-1b-it` |
| Qwen 2.5 0.5B | `Qwen/Qwen2.5-0.5B-Instruct` |

### Long-context LoRA (32K-131K)
| Model | API String | Max Context |
|-------|-----------|-------------|
| DeepSeek R1 | `deepseek-ai/DeepSeek-R1` | 131K |
| Llama 3.3 70B | `meta-llama/Llama-3.3-70B-Instruct-Turbo` | 131K |
| Llama 3.1 8B | `meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo` | 131K |
| Qwen3 variants | Various | 32K-131K |

## Full Fine-tuning

Supports the same models as LoRA with generally smaller batch sizes (1-32 vs 8-128 for LoRA).

## VLM Fine-tuning

| Model | API String | Full | LoRA |
|-------|-----------|------|------|
| Qwen3-VL-8B | `Qwen/Qwen3-VL-8B-Instruct` | Yes | Yes |
| Qwen3-VL-32B | `Qwen/Qwen3-VL-32B-Instruct` | Yes | Yes |
| Qwen3-VL-30B-A3B | `Qwen/Qwen3-VL-30B-A3B-Instruct` | Yes | Yes |
| Qwen3-VL-235B | `Qwen/Qwen3-VL-235B-A22B-Instruct` | No | Yes |
| Llama 4 Maverick VLM | `meta-llama/Llama-4-Maverick-17B-128E-Instruct-VLM` | No | Yes |
| Llama 4 Scout VLM | `meta-llama/Llama-4-Scout-17B-16E-Instruct-VLM` | No | Yes |
| Gemma 3 4B VLM | `google/gemma-3-4b-it-VLM` | Yes | Yes |
| Gemma 3 12B VLM | `google/gemma-3-12b-it-VLM` | Yes | Yes |
| Gemma 3 27B VLM | `google/gemma-3-27b-it-VLM` | Yes | Yes |

## DPO/Preference Training

Same models as LoRA/Full fine-tuning. Additional parameters:
- `dpo_beta`: 0.05-0.9 (default 0.1)
- `training_method`: `"dpo"`

## BYOM (Bring Your Own Model)

Fine-tune custom HuggingFace models:
```python
response = client.fine_tuning.create(
    training_file=file_id,
    model="my-org/my-model",
    from_hf_model="my-org/my-model",
    hf_api_token="hf_xxx",
)
```
