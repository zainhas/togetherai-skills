# Together AI Skills for Claude Code

A collection of 15 Claude Code skills that provide comprehensive knowledge of the [Together AI](https://together.ai) platform — inference, training, embeddings, audio, video, images, function calling, and infrastructure.

Each skill teaches Claude Code how to use a specific Together AI product, including API patterns, SDK usage, model selection, and best practices. Skills include runnable Python scripts using the **Together Python v2 SDK**.

## What Are Skills?

[Skills](https://docs.anthropic.com/en/docs/claude-code/skills) are markdown instruction files that give Claude Code domain-specific knowledge. When Claude detects that a skill is relevant to your task, it loads the skill's instructions and uses them to write better code.

Each skill contains:

- **`SKILL.md`** — Core instructions with API patterns, code examples, and best practices
- **`references/`** — Detailed reference docs (model lists, API parameters, CLI commands)
- **`scripts/`** — Runnable Python scripts demonstrating complete workflows

## Skills Overview

| Skill | Description | Scripts |
|-------|-------------|---------|
| **together-chat-completions** | Serverless chat/text completion with 100+ open-source models. Includes function calling, structured outputs (JSON mode, json_schema, regex), and reasoning models. | — |
| **together-function-calling** | Function calling (tool use) and structured outputs. 6 calling patterns, parallel tool calls, json_schema with Pydantic. | `tool_call_loop.py` |
| **together-reasoning** | Reasoning/thinking models — DeepSeek R1, Kimi K2, Qwen3. Extended thinking, reasoning_effort control, thought parsing. | — |
| **together-images** | Image generation with FLUX.1/FLUX.2, Kontext (image editing), LoRA fine-tuned styles. URL and base64 output. | `generate_image.py` |
| **together-video** | Video generation from text/image prompts. 15+ models including Veo 3, Sora 2, Kling 2.1. Async polling workflow. | `generate_video.py` |
| **together-audio** | Text-to-speech (Orpheus, Kokoro, Cartesia) and speech-to-text (Whisper). REST, streaming, and WebSocket TTS modes. | `tts_generate.py`, `stt_transcribe.py` |
| **together-embeddings** | Text embeddings (BGE, GTE, E5) and document reranking (Mxbai). Cosine similarity, batch processing. | `embed_and_rerank.py` |
| **together-fine-tuning** | Fine-tune LLMs with LoRA, Full, DPO, and VLM tuning. Data upload, training, monitoring, and deployment. | `finetune_workflow.py` |
| **together-batch-inference** | Async batch processing at up to 50% lower cost. Upload JSONL, create batch, poll, download results. | `batch_workflow.py` |
| **together-evaluations** | LLM-as-a-Judge evaluation framework. Classify, Score, and Compare evaluation types. | `run_evaluation.py` |
| **together-code-interpreter** | Execute Python in a sandboxed environment. Session reuse, package support, chart generation. | `execute_with_session.py` |
| **together-code-sandbox** | Full VM sandboxes with Docker support via CodeSandbox. File I/O, port forwarding, persistent sessions. | — |
| **together-dedicated-endpoints** | Single-tenant GPU endpoints. Create, autoscale, monitor, stop/delete. No rate limits, predictable latency. | `manage_endpoint.py` |
| **together-dedicated-containers** | Deploy custom Docker containers on managed GPU infra. Sprocket SDK for workers, Jig CLI for deployment. | `sprocket_hello_world.py` |
| **together-gpu-clusters** | Provision H100/H200/B200 GPU clusters. tcloud CLI, SLURM jobs, shared filesystem, multi-node training. | — |

## Installation

### Install all skills

Copy the skill folders into your project's `.claude/skills/` directory:

```bash
# From the repo root
cp -r together-skills/together-* your-project/.claude/skills/
```

Or into your home directory for global availability:

```bash
cp -r together-skills/together-* ~/.claude/skills/
```

### Install individual skills

Copy only the skills you need:

```bash
# Just chat completions and function calling
cp -r together-skills/together-chat-completions your-project/.claude/skills/
cp -r together-skills/together-function-calling your-project/.claude/skills/
```

### Verify installation

```bash
ls your-project/.claude/skills/together-*/SKILL.md
```

You should see one `SKILL.md` per installed skill.

## Usage

Once installed, skills activate automatically when Claude Code detects a relevant task. No explicit invocation is needed.

### Examples

**Chat completions** — Ask Claude to build a chat app:

```
> Build a multi-turn chatbot using Together AI with Llama 3.3 70B
```

Claude will use the `together-chat-completions` skill to generate correct v2 SDK code with proper model IDs, parameters, and streaming patterns.

**Function calling** — Ask for tool-using agents:

```
> Create an agent that can check weather and stock prices using Together AI function calling
```

Claude will reference `together-function-calling` for the complete tool call loop pattern, including parallel tool calls and tool_choice options.

**Image generation** — Ask for image workflows:

```
> Generate a FLUX image with Together AI and save it locally as PNG
```

Claude will use `together-images` to write code with the correct model ID, base64 decoding, and file saving.

**Fine-tuning** — Ask to fine-tune a model:

```
> Fine-tune Llama 3.1 8B on my dataset using Together AI with LoRA
```

Claude will reference `together-fine-tuning` for data format requirements, training parameters, monitoring, and deployment.

### Using the scripts

Each script is a standalone, runnable example. They require the Together Python SDK and an API key:

```bash
pip install together
export TOGETHER_API_KEY=your_key

# Run any script directly
python together-skills/together-images/scripts/generate_image.py
python together-skills/together-audio/scripts/tts_generate.py
python together-skills/together-batch-inference/scripts/batch_workflow.py
```

Scripts use the **Together Python v2 SDK** (`together>=1.0.0`) with keyword-only arguments, updated method names, and current response shapes.

## Skill Structure

```
together-<product>/
├── SKILL.md              # Core instructions (always loaded on trigger)
├── references/           # Detailed docs (loaded when needed)
│   ├── models.md         # Supported models, IDs, context lengths
│   ├── api-reference.md  # Full API parameters and response shapes
│   └── ...
└── scripts/              # Runnable Python examples (v2 SDK)
    └── <workflow>.py     # Complete end-to-end workflow
```

### How skills are loaded

1. **Metadata** (YAML frontmatter) — Always available to Claude (~100 words). Used to decide whether to load the skill.
2. **Body** (Markdown) — Loaded when the skill is triggered. Contains API patterns, code examples, and best practices.
3. **References** — Loaded on demand when Claude needs deeper detail (model lists, full API specs).
4. **Scripts** — Available as runnable code that Claude can reference or execute directly.

## SDK Compatibility

All code examples and scripts target the **Together Python v2 SDK** (`together>=1.0.0`), which uses:

- Keyword-only arguments (not positional)
- `client.batches.create()` / `client.batches.retrieve()` (not `create_batch()` / `get_batch()`)
- `client.endpoints.retrieve()` (not `get()`)
- `client.code_interpreter.execute()` (not `run()`)
- `client.evals.create()` (not `client.evaluation.create()`)
- File objects via context managers (`with open(..., "rb") as f:`)
- Typed parameter classes for evaluations

If you're using the v1 SDK, see the [migration guide](https://docs.together.ai/docs/v2-migration-guide).

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI
- [Together AI API key](https://api.together.ai/settings/api-keys)
- Python 3.10+ (for scripts)
- `pip install together` (v2 SDK, `>=1.0.0`)

## License

MIT
