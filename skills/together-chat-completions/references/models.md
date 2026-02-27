# Chat Model Catalog

## Recommended Models by Use Case

| Use Case | Model | API String |
|----------|-------|-----------|
| Chat (best) | Kimi K2.5 | `moonshotai/Kimi-K2.5` |
| Reasoning | Kimi K2.5 | `moonshotai/Kimi-K2.5` |
| Coding Agents | Qwen3-Coder 480B | `Qwen/Qwen3-Coder-480B-A35B-Instruct-FP8` |
| Small & Fast | GPT-OSS 20B | `openai/gpt-oss-20b` |
| Medium General | GPT-OSS 120B | `openai/gpt-oss-120b` |
| Function Calling | GLM-5 | `zai-org/GLM-5` |
| Vision | Llama 4 Maverick | `meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8` |

## Full Chat Model Catalog

| Organization | Model | API String | Context | Quant |
|-------------|-------|-----------|---------|-------|
| Moonshot | Kimi K2.5 | `moonshotai/Kimi-K2.5` | 262,144 | INT4 |
| Moonshot | Kimi K2 Thinking | `moonshotai/Kimi-K2-Thinking` | 262,144 | INT4 |
| Moonshot | Kimi K2 Instruct 0905 | `moonshotai/Kimi-K2-Instruct-0905` | 262,144 | FP8 |
| Moonshot | Kimi K2 Instruct | `moonshotai/Kimi-K2-Instruct` | 128,000 | FP8 |
| Qwen | Qwen3.5 397B | `Qwen/Qwen3.5-397B-A17B` | 262,144 | BF16 |
| Qwen | Qwen3-Coder 480B | `Qwen/Qwen3-Coder-480B-A35B-Instruct-FP8` | 256,000 | FP8 |
| Qwen | Qwen3-Coder-Next | `Qwen/Qwen3-Coder-Next-FP8` | 262,144 | FP8 |
| Qwen | Qwen3 235B Thinking | `Qwen/Qwen3-235B-A22B-Thinking-2507` | 262,144 | FP8 |
| Qwen | Qwen3 235B Instruct | `Qwen/Qwen3-235B-A22B-Instruct-2507-tput` | 262,144 | FP8 |
| Qwen | Qwen3-Next 80B Instruct | `Qwen/Qwen3-Next-80B-A3B-Instruct` | 262,144 | BF16 |
| Qwen | Qwen3-Next 80B Thinking | `Qwen/Qwen3-Next-80B-A3B-Thinking` | 262,144 | BF16 |
| MiniMax | MiniMax M2.5 | `MiniMaxAI/MiniMax-M2.5` | 228,700 | FP4 |
| DeepSeek | DeepSeek-V3.1 | `deepseek-ai/DeepSeek-V3.1` | 128,000 | FP8 |
| DeepSeek | DeepSeek-R1 | `deepseek-ai/DeepSeek-R1` | 163,839 | FP8 |
| DeepSeek | DeepSeek-R1 (throughput) | `deepseek-ai/DeepSeek-R1-0528-tput` | 163,839 | FP8 |
| DeepSeek | R1 Distill Llama 70B | `deepseek-ai/DeepSeek-R1-Distill-Llama-70B` | 131,072 | - |
| DeepSeek | R1 Distill Qwen 14B | `deepseek-ai/DeepSeek-R1-Distill-Qwen-14B` | 32,768 | - |
| OpenAI | GPT-OSS 120B | `openai/gpt-oss-120b` | 128,000 | MXFP4 |
| OpenAI | GPT-OSS 20B | `openai/gpt-oss-20b` | 128,000 | MXFP4 |
| Z.ai | GLM-5 | `zai-org/GLM-5` | 202,752 | FP4 |
| Z.ai | GLM 4.7 | `zai-org/GLM-4.7` | 202,752 | FP8 |
| Z.ai | GLM 4.5 Air | `zai-org/GLM-4.5-Air-FP8` | 131,072 | FP8 |
| Meta | Llama 4 Maverick | `meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8` | 1,048,576 | FP8 |
| Meta | Llama 3.3 70B Turbo | `meta-llama/Llama-3.3-70B-Instruct-Turbo` | 131,072 | FP8 |
| Meta | Llama 3.1 8B Turbo | `meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo` | 131,072 | FP8 |
| Meta | Llama 3.2 3B Turbo | `meta-llama/Llama-3.2-3B-Instruct-Turbo` | 131,072 | FP16 |
| Meta | Llama 3 70B | `meta-llama/Llama-3-70b-chat-hf` | 8,192 | FP16 |
| Meta | Llama 3 8B Lite | `meta-llama/Meta-Llama-3-8B-Instruct-Lite` | 8,192 | INT4 |
| Deep Cogito | Cogito v2.1 671B | `deepcogito/cogito-v2-1-671b` | 32,768 | FP8 |
| Mistral | Ministral 3 14B | `mistralai/Ministral-3-14B-Instruct-2512` | 262,144 | BF16 |
| Mistral | Mistral Small 24B | `mistralai/Mistral-Small-24B-Instruct-2501` | 32,768 | FP16 |
| Mistral | Mistral 7B v0.2 | `mistralai/Mistral-7B-Instruct-v0.2` | 32,768 | FP16 |
| NVIDIA | Nemotron Nano 9B v2 | `nvidia/NVIDIA-Nemotron-Nano-9B-v2` | 131,072 | BF16 |
| Google | Gemma 3N E4B | `google/gemma-3n-E4B-it` | 32,768 | FP8 |
| Qwen | QwQ 32B | `Qwen/QwQ-32B` | 32,768 | - |
| Qwen | Qwen 2.5 7B Turbo | `Qwen/Qwen2.5-7B-Instruct-Turbo` | 32,768 | FP8 |
| Marin | Marin 8B Instruct | `marin-community/marin-8b-instruct` | 4,096 | FP16 |
| Essential AI | Rnj-1 Instruct | `essentialai/rnj-1-instruct` | 32,768 | BF16 |
| Gryphe | MythoMax-L2 13B | `Gryphe/MythoMax-L2-13b` | 4,096 | FP16 |

## Vision Models

| Organization | Model | API String | Context |
|-------------|-------|-----------|---------|
| Meta | Llama 4 Maverick | `meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8` | 524,288 |
| Qwen | Qwen3-VL-32B | `Qwen/Qwen3-VL-32B-Instruct` | 256,000 |
| Qwen | Qwen3-VL-8B | `Qwen/Qwen3-VL-8B-Instruct` | 262,100 |

## Moderation Models

| Model | API String | Context |
|-------|-----------|---------|
| Llama Guard 4 (12B) | `meta-llama/Llama-Guard-4-12B` | 1,048,576 |
| Virtue Guard | `VirtueAI/VirtueGuard-Text-Lite` | 32,768 |

## Quantization Types
- **FP16/BF16:** Full precision
- **FP8:** 8-bit floating point (Turbo models)
- **FP4/MXFP4:** 4-bit floating point
- **INT4:** 4-bit integer (Lite models)
