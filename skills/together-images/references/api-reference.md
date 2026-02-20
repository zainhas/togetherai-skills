# Image Generation API Reference

## Endpoint
`POST https://api.together.xyz/v1/images/generations`

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | Yes* | - | Text description of image to generate |
| `model` | string | Yes | - | Model identifier |
| `width` | integer | No | 1024 | Image width in pixels |
| `height` | integer | No | 1024 | Image height in pixels |
| `n` | integer | No | 1 | Number of images (1-4) |
| `steps` | integer | No | varies | Diffusion steps (1-50) |
| `seed` | integer | No | random | Random seed for reproducibility |
| `negative_prompt` | string | No | - | What to avoid in generation |
| `response_format` | string | No | url | `"base64"` for inline data, or URL |
| `disable_safety_checker` | bool | No | false | Disable NSFW check |
| `image_url` | string | No | - | Reference image URL (for editing) |

*Required for all models except Kling

## Image Editing (Kontext Models)

For Kontext models, provide a reference image and editing instructions:

```python
response = client.images.generate(
    model="black-forest-labs/FLUX.1-kontext-pro",
    prompt="Change the shirt color to blue",
    image_url="https://example.com/photo.jpg",
    steps=28,
)
```

## Response

```json
{
  "id": "img-abc123",
  "model": "black-forest-labs/FLUX.1-schnell",
  "data": [
    {
      "index": 0,
      "url": "https://api.together.ai/v1/images/..."
    }
  ]
}
```

With `response_format="base64"`:
```json
{
  "data": [
    {
      "index": 0,
      "b64_json": "iVBORw0KGgo..."
    }
  ]
}
```

## Steps Guide

| Steps | Effect |
|-------|--------|
| 1-4 | Fast, lower quality (FLUX.1 schnell default: 4) |
| 10-20 | Good balance of speed and quality |
| 28 | High quality (FLUX.1 dev default) |
| 30-50 | Maximum quality, slower |

## Dimensions Guide

| Aspect Ratio | Dimensions | Use Case |
|-------------|-----------|----------|
| 1:1 | 1024x1024 | Square, social media |
| 16:9 | 1344x768 | Landscape, widescreen |
| 9:16 | 768x1344 | Portrait, mobile |
| 3:2 | 1248x832 | Photography standard |
| 4:3 | 1184x864 | Classic ratio |

## Python SDK

```python
from together import Together
client = Together()

response = client.images.generate(
    prompt="A sunset over mountains",
    model="black-forest-labs/FLUX.1-schnell",
    width=1024,
    height=1024,
    steps=4,
    n=1,
)
print(response.data[0].url)
```

## TypeScript SDK

```typescript
const response = await together.images.create({
  prompt: "A sunset over mountains",
  model: "black-forest-labs/FLUX.1-schnell",
  width: 1024,
  height: 1024,
  steps: 4,
  n: 1,
});
console.log(response.data[0].url);
```

## cURL

```shell
curl -X POST "https://api.together.xyz/v1/images/generations" \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A sunset over mountains",
    "model": "black-forest-labs/FLUX.1-schnell",
    "width": 1024,
    "height": 1024,
    "steps": 4,
    "n": 1
  }'
```
