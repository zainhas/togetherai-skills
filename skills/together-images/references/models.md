# Image Generation Models Reference

## Complete Model Table

| Organization | Model | API String | Default Steps |
|-------------|-------|-----------|--------------|
| Google | Imagen 4.0 Preview | `google/imagen-4.0-preview` | - |
| Google | Imagen 4.0 Fast | `google/imagen-4.0-fast` | - |
| Google | Imagen 4.0 Ultra | `google/imagen-4.0-ultra` | - |
| Google | Flash Image 2.5 | `google/flash-image-2.5` | - |
| Google | Gemini 3 Pro Image | `google/gemini-3-pro-image` | - |
| Black Forest Labs | FLUX.2 [pro] | `black-forest-labs/FLUX.2-pro` | - |
| Black Forest Labs | FLUX.2 [dev] | `black-forest-labs/FLUX.2-dev` | - |
| Black Forest Labs | FLUX.2 [flex] | `black-forest-labs/FLUX.2-flex` | - |
| Black Forest Labs | FLUX.1 [schnell] | `black-forest-labs/FLUX.1-schnell` | 4 |
| Black Forest Labs | FLUX.1.1 [pro] | `black-forest-labs/FLUX.1.1-pro` | - |
| Black Forest Labs | FLUX.1 Kontext [pro] | `black-forest-labs/FLUX.1-kontext-pro` | 28 |
| Black Forest Labs | FLUX.1 Kontext [max] | `black-forest-labs/FLUX.1-kontext-max` | 28 |
| Black Forest Labs | FLUX.1 Krea [dev] | `black-forest-labs/FLUX.1-krea-dev` | 28 |
| ByteDance | Seedream 4.0 | `ByteDance-Seed/Seedream-4.0` | - |
| ByteDance | Seedream 3.0 | `ByteDance-Seed/Seedream-3.0` | - |
| Qwen | Qwen Image | `Qwen/Qwen-Image` | - |
| Ideogram | Ideogram 3.0 | `ideogram/ideogram-3.0` | - |
| HiDream | HiDream-I1-Full | `HiDream-ai/HiDream-I1-Full` | - |
| HiDream | HiDream-I1-Dev | `HiDream-ai/HiDream-I1-Dev` | - |
| HiDream | HiDream-I1-Fast | `HiDream-ai/HiDream-I1-Fast` | - |
| RunDiffusion | Juggernaut Pro Flux | `RunDiffusion/Juggernaut-pro-flux` | - |
| RunDiffusion | Juggernaut Lightning | `Rundiffusion/Juggernaut-Lightning-Flux` | - |
| Lykon | DreamShaper | `Lykon/DreamShaper` | - |
| Stability AI | SD 3 Medium | `stabilityai/stable-diffusion-3-medium` | - |
| Stability AI | SDXL Base 1.0 | `stabilityai/stable-diffusion-xl-base-1.0` | - |

## Model Categories

### Text-to-Image (Generation)
All models above support text-to-image generation.

### Image Editing (Kontext)
- `black-forest-labs/FLUX.1-kontext-pro` — Best quality editing
- `black-forest-labs/FLUX.1-kontext-max` — Maximum capability
- `google/flash-image-2.5` — Fast image editing
- `google/gemini-3-pro-image` — Gemini-based editing

## Recommended Models

| Use Case | Model | API String |
|----------|-------|-----------|
| Best quality | Flash Image 2.5 | `google/flash-image-2.5` |
| Image editing | FLUX.1 Kontext Max | `black-forest-labs/FLUX.1-kontext-max` |
| Fast generation | FLUX.1 Schnell | `black-forest-labs/FLUX.1-schnell` |
| Highest quality | FLUX.2 Pro | `black-forest-labs/FLUX.2-pro` |

## FLUX Pricing Formula

```
Cost = MP × Price_per_MP × (Steps ÷ Default_Steps)
MP = Width × Height ÷ 1,000,000
```

## Supported Dimensions

### Standard (most models)
- 1024x1024 (1:1), 1344x768 (16:9), 768x1344 (9:16)
- 1248x832 (3:2), 832x1248 (2:3)
- 1184x864 (4:3), 864x1184 (3:4)

### Gemini 3 Pro Image — 1K
1024x1024, 1248x832, 832x1248, 1184x864, 864x1184, 896x1152, 1152x896, 768x1344, 1344x768, 1536x672

### Gemini 3 Pro Image — 2K
2048x2048, 2496x1664, 1664x2496, 2368x1728, 1728x2368, 1792x2304, 2304x1792, 1536x2688, 2688x1536, 3072x1344

### Gemini 3 Pro Image — 4K
4096x4096, 4992x3328, 3328x4992, 4736x3456, 3456x4736, 3584x4608, 4608x3584, 3072x5376, 5376x3072, 6144x2688
