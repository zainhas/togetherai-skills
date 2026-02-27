---
name: together-gpu-clusters
description: Provision on-demand and reserved GPU clusters (Instant Clusters) on Together AI with H100, H200, and B200 hardware. Supports Kubernetes and Slurm orchestration, tcloud CLI, Terraform, and SkyPilot. Use when users need GPU clusters, distributed training, multi-node compute, HPC workloads, or large-scale ML infrastructure.
---

# Together GPU Clusters

## Overview

Provision GPU clusters on Together AI for distributed training, large-scale inference, and HPC workloads.

- **Hardware**: NVIDIA H100, H200, B200 (80GB SXM)
- **Cluster types**: On-demand (pay-as-you-go) or Reserved (committed)
- **Orchestration**: Kubernetes or Slurm
- **Management**: tcloud CLI, Terraform, SkyPilot, REST API
- **Networking**: InfiniBand for high-bandwidth inter-node communication

## Workflow

1. Choose hardware and cluster size
2. Create cluster via tcloud CLI, Terraform, or API
3. Configure orchestration (K8s or Slurm)
4. Run workloads
5. Monitor health and manage nodes
6. Delete when done

## Quick Start with tcloud CLI

### Install

```shell
pip install tcloud
tcloud auth login
```

### Create a Cluster

```shell
tcloud cluster create \
  --name my-training-cluster \
  --gpu-type h100 \
  --num-nodes 8 \
  --orchestrator kubernetes
```

### Check Status

```shell
tcloud cluster list
tcloud cluster get my-training-cluster
```

### Access the Cluster

```shell
# Get kubeconfig for Kubernetes clusters
tcloud cluster kubeconfig my-training-cluster > kubeconfig.yaml
export KUBECONFIG=kubeconfig.yaml
kubectl get nodes

# SSH for Slurm clusters
tcloud cluster ssh my-training-cluster
```

### Delete

```shell
tcloud cluster delete my-training-cluster
```

## Kubernetes vs Slurm

**Choose Kubernetes when:**
- Running containerized workloads
- Need auto-scheduling and scaling
- Using cloud-native ML frameworks (KubeFlow, Ray)

**Choose Slurm when:**
- Traditional HPC workloads
- Multi-node MPI training
- Familiar with Slurm job scripts
- Need fine-grained resource allocation

## Key tcloud Commands

| Command | Description |
|---------|-------------|
| `tcloud cluster create` | Create a new cluster |
| `tcloud cluster list` | List all clusters |
| `tcloud cluster get <name>` | Get cluster details |
| `tcloud cluster delete <name>` | Delete a cluster |
| `tcloud cluster kubeconfig <name>` | Get K8s kubeconfig |
| `tcloud cluster ssh <name>` | SSH into Slurm head node |
| `tcloud cluster health <name>` | Check node health |

## Terraform Integration

```hcl
resource "together_cluster" "training" {
  name         = "my-training-cluster"
  gpu_type     = "h100"
  num_nodes    = 4
  orchestrator = "kubernetes"
}
```

```shell
terraform init
terraform plan
terraform apply
```

## SkyPilot Integration

```yaml
# sky.yaml
resources:
  cloud: together
  accelerators: H100:8
  num_nodes: 4

setup: |
  pip install torch

run: |
  torchrun --nproc_per_node=8 train.py
```

```shell
sky launch sky.yaml
```

## Health Monitoring

```shell
tcloud cluster health my-cluster
```

- Automatic health checks on GPU, network, and storage
- Unhealthy nodes flagged for repair or replacement
- Node repair can be triggered manually or automatically

## Storage

- **NFS**: Shared filesystem across all nodes
- **Object storage**: S3-compatible for large datasets
- Persistent storage survives node restarts

## Billing

- **On-demand**: Per-GPU-hour billing, no commitment
- **Reserved**: Committed capacity with discounted rates
- Billed while cluster is running (even if idle)

## Resources

- **tcloud CLI reference**: See [references/tcloud-cli.md](references/tcloud-cli.md)
- **Cluster management details**: See [references/cluster-management.md](references/cluster-management.md)
- **Official docs**: [GPU Clusters Overview](https://docs.together.ai/docs/gpu-clusters-overview)
- **Official docs**: [GPU Clusters Quickstart](https://docs.together.ai/docs/gpu-clusters-quickstart)
- **API reference**: [Clusters API](https://docs.together.ai/reference/clusters-create)
