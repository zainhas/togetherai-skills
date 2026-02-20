# tcloud CLI Reference

## Installation

**Mac (Universal):**
```shell
curl -LO https://tcloud-cli-downloads.s3.us-west-2.amazonaws.com/releases/latest/tcloud-darwin-universal.tar.gz
tar xzf tcloud-darwin-universal.tar.gz
```

**Linux (AMD64):**
```shell
curl -LO https://tcloud-cli-downloads.s3.us-west-2.amazonaws.com/releases/latest/tcloud-linux-amd64.tar.gz
tar xzf tcloud-linux-amd64.tar.gz
```

## Authentication

```shell
tcloud sso login
```

## Cluster Commands

### Create Cluster

```shell
# On-demand
tcloud cluster create my-cluster \
  --num-gpus 8 \
  --billing-type on_demand \
  --instance-type H100-SXM \
  --region us-central-8 \
  --shared-volume-name my-volume \
  --size-tib 1

# Reserved (prepaid)
tcloud cluster create my-cluster \
  --num-gpus 8 \
  --billing-type prepaid \
  --reservation-duration 30 \
  --instance-type H100-SXM \
  --region us-central-8 \
  --shared-volume-name my-volume \
  --size-tib 1
```

### List Clusters
```shell
tcloud cluster list
```

### Scale Cluster
```shell
tcloud cluster scale <CLUSTER_UUID> --num-gpus 16
```

### Delete Cluster
```shell
tcloud cluster delete <CLUSTER_UUID>
```

## Parameters

| Parameter | Description | Values |
|-----------|-------------|--------|
| `--num-gpus` | Total GPU count | 8, 16, 32, ... |
| `--instance-type` | GPU type | `H100-SXM`, `H200`, `B200` |
| `--region` | Deployment region | `us-central-8`, etc. |
| `--billing-type` | Billing model | `on_demand`, `prepaid` |
| `--reservation-duration` | Days (prepaid only) | 1-90 |
| `--shared-volume-name` | Shared storage name | Any string |
| `--size-tib` | Storage size in TiB | 1+ |

## Instance Types

| Type | GPU | Memory | Networking |
|------|-----|--------|-----------|
| `H100-SXM` | NVIDIA H100 | 80GB | InfiniBand |
| `H100-SXM-Inference` | NVIDIA H100 | 80GB | Lower IB bandwidth |
| `H200` | NVIDIA H200 | 141GB | InfiniBand |
| `B200` | NVIDIA B200 | 192GB | InfiniBand |
