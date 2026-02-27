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

```typescript
import Together from "together-ai";
const together = new Together();

const endpoint = await together.endpoints.create({
  model: "meta-llama/Llama-3.3-70B-Instruct-Turbo",
  hardware: "4x_nvidia_h100_80gb_sxm",
  autoscaling: {
    min_replicas: 1,
    max_replicas: 3,
  },
});
console.log(endpoint.id);
```

```shell
curl -X POST "https://api.together.xyz/v1/endpoints" \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
    "hardware": "4x_nvidia_h100_80gb_sxm",
    "display_name": "My Llama Endpoint",
    "autoscaling": {
      "min_replicas": 1,
      "max_replicas": 3
    }
  }'
```

```shell
together endpoints create \
  --model meta-llama/Llama-3.3-70B-Instruct-Turbo \
  --hardware 4x_nvidia_h100_80gb_sxm \
  --display-name "My Llama Endpoint" \
  --min-replicas 1 --max-replicas 3 \
  --wait
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

## Get Endpoint

```python
endpoint = client.endpoints.retrieve("endpoint-abc123")
print(endpoint.state)
```

```typescript
import Together from "together-ai";
const together = new Together();

const endpoint = await together.endpoints.retrieve("endpoint-abc123");
console.log(endpoint);
```

```shell
curl "https://api.together.xyz/v1/endpoints/endpoint-abc123" \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -H "Content-Type: application/json"
```

```shell
together endpoints retrieve <ENDPOINT_ID>
together endpoints retrieve <ENDPOINT_ID> --json
```

## List Endpoints

```python
response = client.endpoints.list()
for ep in response.data:
    print(ep.id)
```

```typescript
import Together from "together-ai";
const together = new Together();

const endpoints = await together.endpoints.list();
for (const endpoint of endpoints.data) {
  console.log(endpoint);
}
```

```shell
curl "https://api.together.xyz/v1/endpoints" \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -H "Content-Type: application/json"
```

```shell
together endpoints list --mine
together endpoints list --type dedicated
together endpoints list --json
```

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
    "endpoint-abc123",
    autoscaling={"min_replicas": 2, "max_replicas": 5},
    display_name="Updated Name",
)
```

```typescript
import Together from "together-ai";
const together = new Together();

await together.endpoints.update("endpoint-abc123", {
  autoscaling: { min_replicas: 2, max_replicas: 5 },
  display_name: "Updated Name",
});
```

```shell
curl -X PATCH "https://api.together.xyz/v1/endpoints/endpoint-abc123" \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "autoscaling": {
      "min_replicas": 2,
      "max_replicas": 5
    },
    "display_name": "Updated Name"
  }'
```

```shell
together endpoints update --min-replicas 2 --max-replicas 5 <ENDPOINT_ID>
together endpoints update --display-name "Updated Name" <ENDPOINT_ID>
```

### Updatable Fields
- `display_name`
- `state` (`"STARTED"` or `"STOPPED"`)
- `autoscaling`
- `inactive_timeout`

## Start / Stop

```python
# Start
client.endpoints.update("endpoint-abc123", state="STARTED")

# Stop
client.endpoints.update("endpoint-abc123", state="STOPPED")
```

```typescript
import Together from "together-ai";
const together = new Together();

// Start
await together.endpoints.update("endpoint-abc123", { state: "STARTED" });

// Stop
await together.endpoints.update("endpoint-abc123", { state: "STOPPED" });
```

```shell
# Start
curl -X PATCH "https://api.together.xyz/v1/endpoints/endpoint-abc123" \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"state": "STARTED"}'

# Stop
curl -X PATCH "https://api.together.xyz/v1/endpoints/endpoint-abc123" \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"state": "STOPPED"}'
```

```shell
together endpoints start <ENDPOINT_ID>
together endpoints start <ENDPOINT_ID> --wait
together endpoints stop <ENDPOINT_ID>
together endpoints stop <ENDPOINT_ID> --wait
```

## Delete

```python
client.endpoints.delete("endpoint-abc123")
```

```typescript
import Together from "together-ai";
const together = new Together();

await together.endpoints.delete("endpoint-abc123");
```

```shell
curl -X DELETE "https://api.together.xyz/v1/endpoints/endpoint-abc123" \
  -H "Authorization: Bearer $TOGETHER_API_KEY"
```

```shell
together endpoints delete <ENDPOINT_ID>
```

## List Hardware

```python
response = client.endpoints.list_hardware()
for hw in response.data:
    print(hw.id)
```

```typescript
import Together from "together-ai";
const together = new Together();

const hardware = await together.endpoints.list_hardware();
console.log(hardware);
```

```shell
curl "https://api.together.xyz/v1/hardware" \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -H "Content-Type: application/json"

# Filter by model
curl "https://api.together.xyz/v1/hardware?model=meta-llama/Llama-3.3-70B-Instruct-Turbo" \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -H "Content-Type: application/json"
```

```shell
together endpoints hardware
together endpoints hardware --model meta-llama/Llama-3.3-70B-Instruct-Turbo
together endpoints hardware --model meta-llama/Llama-3.3-70B-Instruct-Turbo --available
together endpoints hardware --model meta-llama/Llama-3.3-70B-Instruct-Turbo --json
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

```typescript
import Together from "together-ai";
const together = new Together();

const response = await together.chat.completions.create({
  model: "endpoint-abc123",  // or endpoint name
  messages: [{ role: "user", content: "Hello!" }],
});
console.log(response.choices[0].message.content);
```

```shell
curl -X POST "https://api.together.xyz/v1/chat/completions" \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "endpoint-abc123",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

## CLI Reference

| Command | Description |
|---------|-------------|
| `together endpoints create` | Create a new endpoint |
| `together endpoints retrieve <ID>` | Get endpoint details |
| `together endpoints list` | List endpoints |
| `together endpoints update <ID>` | Update endpoint config |
| `together endpoints start <ID>` | Start a stopped endpoint |
| `together endpoints stop <ID>` | Stop a running endpoint |
| `together endpoints delete <ID>` | Delete an endpoint |
| `together endpoints hardware` | List available hardware |
| `together endpoints availability-zones` | List availability zones |

### Create Options

| Flag | Description |
|------|-------------|
| `--model` | (required) Model to deploy |
| `--hardware` | (required) Hardware config ID |
| `--min-replicas` | Minimum replica count |
| `--max-replicas` | Maximum replica count |
| `--display-name` | Human-readable name |
| `--no-auto-start` | Create in STOPPED state |
| `--no-speculative-decoding` | Disable speculative decoding |
| `--availability-zone` | Preferred availability zone |
| `--wait` | Wait for endpoint to be ready |
| `--json` | Output in JSON format |

### Hardware Options

| Flag | Description |
|------|-------------|
| `--model` | Filter by model compatibility |
| `--available` | Show only available hardware (requires `--model`) |
| `--json` | Output in JSON format |

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
