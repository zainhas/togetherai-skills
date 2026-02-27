# GPU Cluster Management Reference

## Cluster Architecture

### Kubernetes Mode
- **Control Plane** — Manages cluster state, scheduling, API access
- **Worker Nodes** — GPU-equipped nodes running workloads
- **Networking** — High-speed InfiniBand for multi-node communication
- **Storage Layer** — Persistent volumes, local NVMe, shared storage

### Slurm on Kubernetes (Slinky)
- **Slurm Controller** — Runs as K8s pods, manages job queues
- **Login Nodes** — SSH-accessible entry points
- **Compute Nodes** — GPU workers registered with both K8s and Slurm

## Access Methods

### Kubernetes Access
```shell
export KUBECONFIG=$HOME/.kube/together_cluster.kubeconfig
kubectl get nodes
kubectl top nodes
kubectl get pods --all-namespaces
```

### SSH Access
```shell
# Direct SSH to worker nodes
ssh <node-address>.cloud.together.ai

# Slurm login node
ssh <username>@slurm-login
```

### Slurm Commands
```shell
sinfo                    # Node and partition status
squeue                   # Job queue
srun --gres=gpu:8 --pty bash  # Interactive GPU session
sbatch script.sh         # Submit batch job
scancel <jobid>          # Cancel job
scontrol show node       # Detailed node info
```

## Scaling

### Real-time Scaling
Scale via UI, CLI, or API at any time.

### Targeted Scale-down
```shell
# Kubernetes - cordon specific nodes
kubectl cordon <node_name>

# Slurm - drain specific nodes
sudo scontrol update NodeName=<node_name> State=drain Reason="scaling down"
```

### Combining Capacity
Use reserved for baseline + on-demand for bursts.

## Storage

### Types
1. **Local NVMe** — High-speed local I/O per node
2. **Shared /home** — NFS-mounted across nodes
3. **Shared Volumes** — Multi-NIC, high-throughput persistent storage

### Kubernetes PVCs

**Shared storage (ReadWriteMany):**
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: shared-pvc
spec:
  accessModes: [ReadWriteMany]
  resources:
    requests:
      storage: 10Gi
  volumeName: <shared-volume-name>
```

**Local storage (ReadWriteOnce):**
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: local-pvc
spec:
  accessModes: [ReadWriteOnce]
  resources:
    requests:
      storage: 50Gi
  storageClassName: local-storage-class
```

### Data Upload
```shell
# Small files
kubectl cp LOCAL_FILE POD_NAME:/data/

# Large datasets (S3)
# Use a data-loader pod with aws-cli
```

## Monitoring

```shell
# Kubernetes
kubectl get nodes
kubectl top nodes
kubectl get pvc

# Slurm
sinfo
squeue
scontrol show job <jobid>
```

## User Management

### Roles
| Role | Control Plane | Data Plane |
|------|--------------|------------|
| **Admin** | Full write (create/delete/scale) | Full access |
| **Member** | Read-only (view only) | Full access |

### Managing Users
1. Settings → GPU Cluster Projects → View Project
2. Add User (email) or Remove User

## REST API

Base URL: `https://api.together.ai/v1`

### Create a Cluster

```shell
curl -X POST \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{
    "cluster_name": "my-gpu-cluster",
    "region": "us-central-8",
    "gpu_type": "H100_SXM",
    "num_gpus": 8,
    "driver_version": "CUDA_12_6_560",
    "billing_type": "ON_DEMAND"
  }' \
  https://api.together.ai/v1/compute/clusters
```

Request body fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `cluster_name` | string | Yes | Name of the cluster |
| `region` | string | Yes | Region (e.g., `us-central-8`) |
| `gpu_type` | string | Yes | `H100_SXM`, `H200_SXM`, `B200_SXM`, `H100_SXM_INF` |
| `num_gpus` | integer | Yes | Number of GPUs (multiple of 8) |
| `driver_version` | string | Yes | CUDA driver version |
| `billing_type` | string | Yes | `ON_DEMAND` or `RESERVED` |
| `cluster_type` | string | No | `KUBERNETES` or `SLURM` |
| `duration_days` | integer | No | Reservation length (only with `RESERVED` billing) |
| `volume_id` | string | No | Existing shared volume ID to attach |

### List All Clusters

```shell
curl -X GET \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  https://api.together.ai/v1/compute/clusters
```

### Retrieve a Cluster

```shell
curl -X GET \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  https://api.together.ai/v1/compute/clusters/${CLUSTER_ID}
```

### Update / Scale a Cluster

```shell
curl -X PUT \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{
    "num_gpus": 24,
    "cluster_type": "KUBERNETES"
  }' \
  https://api.together.ai/v1/compute/clusters/${CLUSTER_ID}
```

Update request body fields:

| Field | Type | Description |
|-------|------|-------------|
| `num_gpus` | integer | New GPU count (multiple of 8) |
| `cluster_type` | string | `KUBERNETES` or `SLURM` |

### Delete a Cluster

```shell
curl -X DELETE \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  https://api.together.ai/v1/compute/clusters/${CLUSTER_ID}
```

### List Regions

```shell
curl -X GET \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  https://api.together.ai/v1/compute/regions
```

### Create a Shared Volume

```shell
curl -X POST \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{
    "volume_name": "my-shared-volume",
    "size_tib": 2,
    "region": "us-central-8"
  }' \
  https://api.together.ai/v1/compute/clusters/storage/volumes
```

Shared volume create request fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `volume_name` | string | Yes | Name of the volume |
| `size_tib` | integer | Yes | Size in tebibytes |
| `region` | string | Yes | Region name |

### List Shared Volumes

```shell
curl -X GET \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  https://api.together.ai/v1/compute/clusters/storage/volumes
```

### Retrieve a Shared Volume

```shell
curl -X GET \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  https://api.together.ai/v1/compute/clusters/storage/volumes/${VOLUME_ID}
```

### Update a Shared Volume

```shell
curl -X PUT \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{
    "volume_id": "12345-67890-12345-67890",
    "size_tib": 3
  }' \
  https://api.together.ai/v1/compute/clusters/storage/volumes
```

### Delete a Shared Volume

The volume must not be attached to any cluster.

```shell
curl -X DELETE \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  https://api.together.ai/v1/compute/clusters/storage/volumes/${VOLUME_ID}
```

## Terraform

```hcl
resource "together_gpu_cluster" "training" {
  name              = "training-cluster"
  num_gpus          = 8
  instance_type     = "H100-SXM"
  region            = "us-central-8"
  billing_type      = "prepaid"
  reservation_days  = 30

  shared_volume {
    name     = "training-data"
    size_tib = 5
  }
}
```

## Billing

### Compute
- **Reserved:** Upfront payment, 1-90 days, discounted
- **On-demand:** Hourly billing, no commitment

### Storage
- Pay-per-TiB, independent of cluster lifecycle
- Persists across cluster creation/deletion

### Credit Exhaustion
- Reserved compute runs until end date
- On-demand compute paused then decommissioned
- Storage access revoked eventually
