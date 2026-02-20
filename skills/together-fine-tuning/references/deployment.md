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

```shell
together fine-tuning download <FT-JOB-ID>
# Downloads as .tar.zst file
tar -xf model-name.tar.zst
```

Options:
- `--output`, `-o` — Custom filename
- `--step`, `-s` — Download specific checkpoint (default: latest)

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
| `train_on_inputs` | bool/str | false | Train on prompts/user msgs |
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

### CLI
```shell
together fine-tuning retrieve <JOB_ID>
together fine-tuning list-events <JOB_ID>
together fine-tuning list
together fine-tuning cancel <JOB_ID>
```

### Python SDK
```python
status = client.fine_tuning.retrieve(job_id)
print(status.status)

events = client.fine_tuning.list_events(id=job_id)
for event in events.data:
    print(event.message)
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
- Minimum: $5 per job
- Token calculation: `(n_epochs × training_tokens) + (n_evals × validation_tokens)`
- Varies by model size and method (LoRA vs Full, SFT vs DPO)
