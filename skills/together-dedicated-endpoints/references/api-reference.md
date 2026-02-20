# Dedicated Endpoints API Reference

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST /endpoints` | Create endpoint | Deploy a new dedicated endpoint |
| `GET /endpoints` | List endpoints | List all endpoints |
| `GET /endpoints/{id}` | Get endpoint | Get endpoint details |
| `PATCH /endpoints/{id}` | Update endpoint | Update config/scaling |
| `DELETE /endpoints/{id}` | Delete endpoint | Remove endpoint |
| `GET /hardware` | List hardware | Available hardware configs |

## Create Endpoint

```python
endpoint = client.endpoints.create(
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
    hardware="4x_nvidia_h100_80gb_sxm",
    display_name="My Llama Endpoint",
    autoscaling={"min_replicas": 1, "max_replicas": 3},
    inactive_timeout=60,  # minutes, None to disable
)
print(endpoint.id)  # endpoint-abc123
```

### Request Body

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `model` | string | Yes | - | Model to deploy |
| `hardware` | string | Yes | - | Hardware config ID |
| `autoscaling` | object | Yes | - | `{min_replicas, max_replicas}` |
| `display_name` | string | No | - | Human-readable name |
| `disable_speculative_decoding` | bool | No | false | Disable spec decoding |
| `state` | string | No | `"STARTED"` | `"STARTED"` or `"STOPPED"` |
| `inactive_timeout` | int/null | No | 60 | Minutes before auto-stop |
| `availability_zone` | string | No | - | Preferred zone |

## Endpoint States

| State | Description |
|-------|-------------|
| `PENDING` | Waiting for resources |
| `STARTING` | Initializing |
| `STARTED` | Running, accepting requests |
| `STOPPING` | Shutting down |
| `STOPPED` | Not running |
| `ERROR` | Failed |

## Update Endpoint

```python
client.endpoints.update(
    endpoint_id="endpoint-abc123",
    autoscaling={"min_replicas": 2, "max_replicas": 5},
    display_name="Updated Name",
)
```

### Updatable Fields
- `display_name`
- `state` (`"STARTED"` or `"STOPPED"`)
- `autoscaling`
- `inactive_timeout`

## Start / Stop

```python
# Start
client.endpoints.update(endpoint_id="endpoint-abc123", state="STARTED")

# Stop
client.endpoints.update(endpoint_id="endpoint-abc123", state="STOPPED")
```

## Delete

```python
client.endpoints.delete(endpoint_id="endpoint-abc123")
```

## Using the Endpoint

Once STARTED, use the same Chat Completions API with either:
- The endpoint **name** as the model parameter
- The endpoint **ID** as the model parameter

```python
response = client.chat.completions.create(
    model="endpoint-abc123",  # or endpoint name
    messages=[{"role": "user", "content": "Hello!"}],
)
```

## CLI Commands

```shell
# Create
together endpoints create --model meta-llama/Llama-3.3-70B-Instruct-Turbo \
  --hardware 4x_nvidia_h100_80gb_sxm --min-replicas 1 --max-replicas 3

# List hardware
together endpoints hardware --model meta-llama/Llama-3.3-70B-Instruct-Turbo

# Get status
together endpoints retrieve <ENDPOINT_ID>

# List yours
together endpoints list --mine

# Start/Stop
together endpoints start <ENDPOINT_ID>
together endpoints stop <ENDPOINT_ID>

# Update
together endpoints update --min-replicas 2 --max-replicas 5 <ENDPOINT_ID>

# Delete
together endpoints delete <ENDPOINT_ID>
```

## Endpoint Response Object

```json
{
  "object": "endpoint",
  "id": "endpoint-abc123",
  "name": "user/meta-llama/Llama-3-8b-a32b82a1",
  "display_name": "My Endpoint",
  "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
  "hardware": "4x_nvidia_h100_80gb_sxm",
  "type": "dedicated",
  "state": "STARTED",
  "autoscaling": {"min_replicas": 1, "max_replicas": 3},
  "created_at": "2024-01-15T14:30:00Z"
}
```
