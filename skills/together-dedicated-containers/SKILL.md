---
name: together-dedicated-containers
description: Deploy custom Dockerized inference workloads on Together AI's managed GPU infrastructure using Dedicated Container Inference (DCI). Tools include Jig CLI for building/deploying, Sprocket SDK for request handling, and a private container registry. Use when users need custom model serving, containerized inference, Docker-based GPU workloads, or workloads beyond standard model endpoints.
---

# Together Dedicated Containers

## Overview

Run custom Dockerized inference workloads on Together's managed GPU infrastructure. You bring the container — Together handles compute, autoscaling, networking, and observability.

**Components:**
- **Jig CLI**: Build, push, and deploy containers
- **Sprocket SDK**: Python SDK for handling inference requests inside containers
- **Container Registry**: `registry.together.xyz` for storing images
- **Queue API**: Async job submission with priority and progress tracking

## Workflow

1. Write inference code using Sprocket SDK (`setup()` + `predict()`)
2. Build container with Jig CLI (`jig build`)
3. Push to registry (`jig push`)
4. Deploy (`jig deploy`)
5. Send requests to your deployment

## Quick Start

### 1. Install Jig CLI

```shell
pip install jig-together
jig auth login  # Authenticate with Together AI
```

### 2. Create Inference Worker

```python
# worker.py
from sprocket import SprocketWorker

class MyWorker(SprocketWorker):
    def setup(self):
        """Load model and resources (runs once at startup)."""
        import torch
        self.model = torch.load("model.pt")

    def predict(self, request):
        """Handle a single inference request."""
        input_data = request.json()
        result = self.model(input_data["prompt"])
        return {"output": result}
```

### 3. Configure Project

```toml
# pyproject.toml
[tool.jig]
name = "my-inference-service"
gpu = "A100"
gpu_count = 1
worker = "worker:MyWorker"
```

### 4. Build, Push, Deploy

```shell
jig build                    # Build Docker image
jig push                     # Push to registry.together.xyz
jig deploy                   # Deploy to Together infrastructure
jig status                   # Check deployment status
jig logs                     # View logs
```

### 5. Send Requests

```python
import requests

response = requests.post(
    "https://api.together.xyz/v1/deployments/my-inference-service/predict",
    headers={"Authorization": "Bearer $TOGETHER_API_KEY"},
    json={"prompt": "Hello world"},
)
print(response.json())
```

## Sprocket SDK

The SDK provides the `SprocketWorker` base class:

- `setup()`: Called once at startup — load models, warm up caches
- `predict(request)`: Called per request — process input and return output
- File handling: Upload/download files within predictions
- GPU access: Full CUDA access inside the container

## Queue API

For async workloads, use the Queue API for job submission with:
- Priority-based fair queuing
- Progress tracking
- Job status polling

## Key Jig CLI Commands

| Command | Description |
|---------|-------------|
| `jig auth login` | Authenticate |
| `jig build` | Build container image |
| `jig push` | Push to registry |
| `jig deploy` | Deploy to GPU infrastructure |
| `jig status` | Check deployment status |
| `jig logs` | View deployment logs |
| `jig scale` | Scale replicas |
| `jig secrets set` | Manage secrets |

## Resources

- **Full Jig CLI reference**: See [references/jig-cli.md](references/jig-cli.md)
- **Sprocket SDK reference**: See [references/sprocket-sdk.md](references/sprocket-sdk.md)
- **App template**: See [scripts/sprocket_hello_world.py](scripts/sprocket_hello_world.py) — minimal Sprocket worker with pyproject.toml example
