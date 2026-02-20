# Jig CLI Reference

## Installation

```shell
pip install together --upgrade
# or
uv tool install together
```

Jig commands are under `together beta jig`.

## Commands

### Deploy
Build, push, and deploy container:
```shell
together beta jig deploy
```
Reads `pyproject.toml` for build and deploy configuration.

### Status
Check deployment status:
```shell
together beta jig status
```

### Logs
View container logs:
```shell
together beta jig logs
together beta jig logs --follow
```

### Destroy
Tear down deployment:
```shell
together beta jig destroy
```

### Secrets
Manage encrypted runtime secrets:
```shell
together beta jig secrets set --name HF_TOKEN --value hf_xxxxx
together beta jig secrets list
together beta jig secrets delete --name HF_TOKEN
```

### Volumes
Manage persistent storage:
```shell
together beta jig volumes create --name my-weights --source ./model_weights/
together beta jig volumes list
together beta jig volumes delete --name my-weights
```

### Queue Status
Check queue metrics:
```shell
together beta jig queue_status
```

## Configuration (pyproject.toml)

### `[tool.jig.image]` — Build Settings

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `python_version` | string | `"3.11"` | Python version |
| `system_packages` | string[] | `[]` | APT packages (e.g., `ffmpeg`, `git`) |
| `environment` | object | `{}` | Build-time + runtime env vars |
| `run` | string[] | `[]` | Extra shell commands during build |
| `cmd` | string | `"python app.py"` | Container startup command |
| `copy` | string[] | `[]` | Files to include in container |
| `auto_include_git` | bool | false | Auto-include git-tracked files |

### `[tool.jig.deploy]` — Runtime Settings

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `description` | string | - | Human-readable description |
| `gpu_type` | string | `"h100-80gb"` | `"h100-80gb"` or `"none"` |
| `gpu_count` | int | 1 | GPUs per replica |
| `cpu` | float | 1.0 | CPU cores per replica |
| `memory` | float | 8.0 | Memory in GB |
| `storage` | int | 100 | Ephemeral disk in GB |
| `min_replicas` | int | 1 | Min replicas (0 for scale-to-zero) |
| `max_replicas` | int | 1 | Max replicas |
| `port` | int | 8000 | Container listen port |
| `health_check_path` | string | `"/health"` | Health endpoint |
| `termination_grace_period_seconds` | int | 300 | Shutdown timeout |
| `command` | string | - | Override startup command |

### `[tool.jig.deploy.environment_variables]`
Runtime environment variables:
```toml
[tool.jig.deploy.environment_variables]
MODEL_PATH = "/models/weights"
TORCH_COMPILE = "1"
```

### `[tool.jig.autoscaling]`
```toml
[tool.jig.autoscaling]
profile = "QueueBacklogPerWorker"
targetValue = "1.05"  # 5% underprovisioning (recommended)
```

- `"1.0"` — Exact match (queue_depth = workers)
- `"1.05"` — 5% underprovisioning (recommended)
- `"0.9"` — 10% overprovisioning (lower latency)

Formula: `desired_replicas = queue_depth / targetValue`

### `[[tool.jig.volume_mounts]]`
```toml
[[tool.jig.volume_mounts]]
name = "my-weights"
mount_path = "/models"
```

## Full Example

```toml
[project]
name = "video-generator"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = ["torch>=2.0", "diffusers", "sprocket"]

[tool.jig.image]
python_version = "3.11"
system_packages = ["git", "ffmpeg", "libgl1"]
run = ["pip install flash-attn --no-build-isolation"]
cmd = "python app.py --queue"
copy = ["app.py", "models/"]

[tool.jig.deploy]
description = "Video generation model"
gpu_type = "h100-80gb"
gpu_count = 2
cpu = 8
memory = 64
min_replicas = 1
max_replicas = 20
port = 8000
health_check_path = "/health"

[[tool.jig.volume_mounts]]
name = "my-weights"
mount_path = "/models"

[tool.jig.autoscaling]
profile = "QueueBacklogPerWorker"
targetValue = "1.05"
```

## Container Registry
- **Host:** `registry.together.xyz`
- Private to your organization
- Images referenced by digest for reproducibility
- Authentication handled automatically by Jig CLI

## Debug Mode
```shell
export TOGETHER_DEBUG=1
together beta jig deploy
```
