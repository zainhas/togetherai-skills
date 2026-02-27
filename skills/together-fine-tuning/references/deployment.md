# Fine-tuned Model Deployment Reference

## Deployment Options

### Option 1: Serverless LoRA Inference (Instant)

Available immediately for LoRA fine-tuned models on supported base models. No deployment needed.

```python
response = client.chat.completions.create(
    model="your-username/Model-Name-your-suffix",
    messages=[{"role": "user", "content": "Hello!"}],
)
```

- First inference loads adapter weights (may be slower)
- Subsequent requests use cached weights
- No hosting fees — pay per token only

### Option 2: Dedicated Endpoint

For production workloads with guaranteed capacity.

```python
endpoint = client.endpoints.create(
    display_name="Fine-tuned Model",
    model="your-username/Model-Name-your-suffix",
    hardware="4x_nvidia_h100_80gb_sxm",
    autoscaling={"min_replicas": 1, "max_replicas": 1},
)
```

- Per-minute hosting charges while running
- Guaranteed capacity and latency
- Supports both LoRA and Full fine-tuned models

### Option 3: Download Weights

Download and run locally or on your infrastructure.

```python
# Download model weights
client.fine_tuning.download(
    id="ft-abc123",
    output="my-model/model.tar.zst",
)
```

```shell
# CLI: download model weights
together fine-tuning download ft-abc123

# Download to a specific directory
together fine-tuning download ft-abc123 --output_dir ./my-model

# Download a specific checkpoint step
together fine-tuning download ft-abc123 --checkpoint-step 48

# Download merged or adapter-only weights (LoRA jobs)
together fine-tuning download ft-abc123 --checkpoint-type merged
together fine-tuning download ft-abc123 --checkpoint-type adapter
```

```shell
# Extract the downloaded archive
tar -xf model-name.tar.zst
```

Options:
- `--output_dir`, `-o` — Specify the output directory
- `--checkpoint-step`, `-s` — Download a specific checkpoint's weights (default: latest)
- `--checkpoint-type` — Checkpoint type: `default`, `merged`, or `adapter` (merged/adapter only for LoRA jobs)

Extracted files include: `pytorch_model.bin`, `config.json`, tokenizer files.

## Training Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | string | Required | Base model |
| `training_file` | string | Required | File ID from upload |
| `validation_file` | string | - | Optional validation file |
| `suffix` | string | - | Custom model name suffix |
| `n_epochs` | int | 1-3 | Training epochs |
| `n_checkpoints` | int | 1 | Checkpoints to save |
| `batch_size` | int/str | `"max"` | Batch size (or "max" for auto) |
| `learning_rate` | float | ~1e-5 | Learning rate |
| `warmup_ratio` | float | 0 | Warmup step ratio |
| `lora` | bool | true | Use LoRA method |
| `lora_r` | int | 64 | LoRA rank |
| `lora_alpha` | int | 16 | LoRA scaling factor |
| `train_on_inputs` | bool/str | "auto" | Train on prompts/user msgs |
| `wandb_api_key` | string | - | W&B integration |

### DPO-specific Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `training_method` | string | - | Set to `"dpo"` |
| `dpo_beta` | float | 0.1 | Deviation control (0.05-0.9) |

### VLM-specific Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `train_vision` | bool | false | Update vision encoder |

## Job Monitoring

### Status Flow
`Pending` → `Queued` → `Running` → `Uploading` → `Completed`

### Python SDK
```python
status = client.fine_tuning.retrieve(job_id)
print(status.status)

events = client.fine_tuning.list_events(id=job_id)
for event in events.data:
    print(event.message)
```

### TypeScript SDK
```typescript
import Together from "together-ai";
const together = new Together();

const fineTune = await together.fineTuning.retrieve("ft-abc123");
console.log(fineTune.status);

const events = await together.fineTuning.listEvents("ft-abc123");
console.log(events);
```

### cURL
```shell
# Retrieve job details
curl "https://api.together.xyz/v1/fine-tunes/ft-abc123" \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -H "Content-Type: application/json"

# List events
curl "https://api.together.xyz/v1/fine-tunes/ft-abc123/events" \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -H "Content-Type: application/json"

# List checkpoints
curl "https://api.together.xyz/v1/fine-tunes/ft-abc123/checkpoints" \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -H "Content-Type: application/json"
```

### CLI
```shell
together fine-tuning status <JOB_ID>
together fine-tuning retrieve <JOB_ID>
together fine-tuning list-events <JOB_ID>
together fine-tuning list-checkpoints <JOB_ID>
together fine-tuning list
together fine-tuning cancel <JOB_ID>
together fine-tuning delete <JOB_ID>
```

## Continued Fine-tuning

Resume from a previous job's checkpoint:
```python
response = client.fine_tuning.create(
    training_file=new_file_id,
    model="base-model",
    from_checkpoint=previous_job_id,
)
```

## Pricing

- Based on total tokens processed
- No minimum price — you only pay for tokens processed
- Token calculation: `(n_epochs × training_tokens) + (n_evals × validation_tokens)`
- Varies by model size and method (LoRA vs Full, SFT vs DPO)
