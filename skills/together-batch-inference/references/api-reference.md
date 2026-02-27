# Batch Inference API Reference

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST /batches` | Create batch | Submit a new batch job |
| `GET /batches` | List batches | List all batch jobs |
| `GET /batches/{id}` | Get batch | Get batch details |
| `POST /batches/{id}/cancel` | Cancel batch | Cancel a batch job |

## Workflow

### 1. Upload Input File

```python
file = client.files.upload(file="batch_input.jsonl", purpose="batch-api", check=False)
print(file.id)  # file-abc123
```

```typescript
import Together from "together-ai";
const client = new Together();

// Use the file ID returned by the Files API upload
const fileId = "file-abc123";
```

```shell
curl -X POST "https://api.together.xyz/v1/files" \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -F "purpose=batch-api" \
  -F "file=@batch_input.jsonl"
```

### 2. Create Batch

```python
batch = client.batches.create(
    input_file_id=file.id,
    endpoint="/v1/chat/completions",
    completion_window="24h",
)
print(batch.job.id)  # batch-abc123
```

```typescript
const batch = await client.batches.create({
  endpoint: "/v1/chat/completions",
  input_file_id: fileId,
});

console.log(batch);
```

```shell
curl -X POST "https://api.together.xyz/v1/batches" \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input_file_id": "file-abc123", "endpoint": "/v1/chat/completions"}'
```

### 3. Check Status

```python
status = client.batches.retrieve(batch.id)
print(status.status)    # VALIDATING, IN_PROGRESS, COMPLETED, FAILED
print(status.progress)  # 0.0 to 100.0
```

```typescript
const batchId = batch.job?.id;

let batchInfo = await client.batches.retrieve(batchId);
console.log(batchInfo.status);
```

```shell
curl -X GET "https://api.together.xyz/v1/batches/batch-abc123" \
  -H "Authorization: Bearer $TOGETHER_API_KEY"
```

### 4. Download Results

```python
if status.status == "COMPLETED":
    with client.files.with_streaming_response.content(id=status.output_file_id) as response:
        output = b"".join(response.iter_bytes())
```

```typescript
const batchResult = await client.batches.retrieve(batchId);

if (batchResult.status === "COMPLETED" && batchResult.output_file_id) {
  const resp = await client.files.content(batchResult.output_file_id);
  const result = await resp.text();
  console.log(result);
}
```

### 5. Cancel Batch

```python
client.batches.cancel(batch_id)
```

```shell
curl -X POST "https://api.together.xyz/v1/batches/batch-abc123/cancel" \
  -H "Authorization: Bearer $TOGETHER_API_KEY"
```

### 6. List Batches

```python
batches = client.batches.list()
for batch in batches:
    print(batch)
```

```typescript
const allBatches = await client.batches.list();

for (const batch of allBatches) {
  console.log(batch);
}
```

```shell
curl -X GET "https://api.together.xyz/v1/batches" \
  -H "Authorization: Bearer $TOGETHER_API_KEY"
```

## Input File Format (JSONL)

Each line:
```json
{"custom_id": "request-1", "body": {"model": "deepseek-ai/DeepSeek-V3", "messages": [{"role": "user", "content": "Hello"}], "max_tokens": 200}}
```

- `custom_id`: Unique identifier (max 64 chars) — required
- `body`: Request matching chat completions schema — required

## Batch Job Status

| Status | Description |
|--------|-------------|
| `VALIDATING` | Input file being validated |
| `IN_PROGRESS` | Processing requests |
| `COMPLETED` | All requests processed |
| `FAILED` | Processing failed |
| `EXPIRED` | Job exceeded time limit |
| `CANCELLED` | User cancelled |

## Batch Job Object

```json
{
  "id": "batch-abc123",
  "status": "IN_PROGRESS",
  "input_file_id": "file-input123",
  "output_file_id": "file-output456",
  "error_file_id": "file-errors789",
  "progress": 75.0,
  "model_id": "deepseek-ai/DeepSeek-V3",
  "endpoint": "/v1/chat/completions",
  "created_at": "2024-01-15T14:30:00Z",
  "completed_at": null
}
```

## Models with 50% Discount

- `deepseek-ai/DeepSeek-R1-0528-tput`
- `meta-llama/Llama-3.3-70B-Instruct-Turbo`
- `meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8`
- `meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo`
- `meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo`
- `meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo`
- `Qwen/Qwen2.5-72B-Instruct-Turbo`
- `Qwen/Qwen2.5-7B-Instruct-Turbo`
- `Qwen/Qwen3-235B-A22B-fp8-tput`
- `Qwen/Qwen3-235B-A22B-Thinking-2507`
- `zai-org/GLM-4.5-Air-FP8`
- `Qwen/Qwen2.5-VL-72B-Instruct`
- `openai/whisper-large-v3`

## Rate Limits

| Limit | Value |
|-------|-------|
| Max requests per batch | 50,000 |
| Max file size | 100MB |
| Max tokens enqueued per model | 30B |
| Recommended batch size | 1,000-10,000 |

## Error Codes

| Code | Description |
|------|-------------|
| 400 | Invalid JSONL format |
| 401 | Authentication failed |
| 404 | Batch not found |
| 429 | Rate limit exceeded |
| 500 | Server error |

## CLI Commands

```shell
# Upload file
together files upload batch_input.jsonl --purpose batch-api

# Create batch
together batches create --input-file file-abc123 --endpoint /v1/chat/completions

# Check status
together batches retrieve batch-abc123

# List batches
together batches list

# Cancel
together batches cancel batch-abc123
```
