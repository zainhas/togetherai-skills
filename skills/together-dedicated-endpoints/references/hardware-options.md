# Dedicated Endpoints Hardware Reference

## Hardware ID Format
`[count]x_nvidia_[gpu_type]_[memory]_[link]`

Example: `2x_nvidia_a100_80gb_sxm`

## Available Hardware

| Hardware ID | GPU | Memory | Count | Link |
|------------|-----|--------|-------|------|
| `1x_nvidia_a100_80gb_sxm` | A100 | 80GB | 1 | SXM |
| `2x_nvidia_a100_80gb_sxm` | A100 | 80GB | 2 | SXM |
| `4x_nvidia_a100_80gb_sxm` | A100 | 80GB | 4 | SXM |
| `8x_nvidia_a100_80gb_sxm` | A100 | 80GB | 8 | SXM |
| `1x_nvidia_h100_80gb_sxm` | H100 | 80GB | 1 | SXM |
| `2x_nvidia_h100_80gb_sxm` | H100 | 80GB | 2 | SXM |
| `4x_nvidia_h100_80gb_sxm` | H100 | 80GB | 4 | SXM |
| `8x_nvidia_h100_80gb_sxm` | H100 | 80GB | 8 | SXM |

## Hardware Availability Status

| Status | Meaning |
|--------|---------|
| `available` | Ready for deployment |
| `unavailable` | Currently not available |
| `insufficient` | Some capacity but may be limited |

## List Available Hardware

```python
# For a specific model
hardware = client.endpoints.hardware.list(model="meta-llama/Llama-3.3-70B-Instruct-Turbo")
for hw in hardware:
    print(f"{hw.id}: {hw.specs.gpu_count}x {hw.specs.gpu_type} @ ${hw.pricing.cents_per_minute:.2f}/min")
```

```shell
together endpoints hardware --model meta-llama/Llama-3.3-70B-Instruct-Turbo
```

## Pricing Model

- **Billed per minute** while endpoint is running (even when idle)
- **No charge** during spin-up or for failed deployments
- **Stop endpoint** to pause charges
- Price varies by hardware configuration (check `cents_per_minute`)

## GPU Selection Guide

| Need | Recommendation |
|------|---------------|
| Small models (<7B) | 1x A100 or 1x H100 |
| Medium models (7-13B) | 1-2x A100/H100 |
| Large models (70B) | 4-8x A100/H100 |
| Maximum throughput | 8x H100 |
| Cost-effective | A100 (lower per-minute cost) |
| Maximum performance | H100 (faster inference) |

## Scaling

### Horizontal (Replicas)
- Increases maximum QPS
- Linear cost scaling
- Best for high-concurrency workloads

### Vertical (GPU Count)
- Increases generation speed
- Reduces time-to-first-token
- Best for latency-sensitive workloads

## Autoscaling Schema

```json
{
  "min_replicas": 1,
  "max_replicas": 5
}
```

- `min_replicas`: Always running (even with no traffic)
- `max_replicas`: Maximum under load
