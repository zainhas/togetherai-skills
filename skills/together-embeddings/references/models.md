# Embedding & Rerank Models Reference

## Embedding Models

| Model | API String | Size | Dimensions | Context | Best For |
|-------|-----------|------|-----------|---------|----------|
| BGE Base EN v1.5 | `BAAI/bge-base-en-v1.5` | 102M | 768 | 512 tokens | General English retrieval |
| Multilingual E5 Large | `intfloat/multilingual-e5-large-instruct` | 560M | 1,024 | 514 tokens | Multilingual retrieval (recommended) |

**Deprecated models (still functional, being removed):**

| Model | API String | Dimensions | Context | Deprecated |
|-------|-----------|-----------|---------|------------|
| BGE Large EN v1.5 | `BAAI/bge-large-en-v1.5` | 1,024 | 512 tokens | 2026-02-06 |
| E5 Mistral 7B | `intfloat/e5-mistral-7b-instruct` | 4,096 | 32,768 tokens | Limited support |

## Rerank Models

| Model | API String | Size | Max Doc Tokens | Max Docs |
|-------|-----------|------|---------------|----------|
| MixedBread Rerank Large V2 | `mixedbread-ai/Mxbai-Rerank-Large-V2` | 1.6B | 32,768 | Unlimited |

**Deprecated rerank models:**

| Model | API String | Max Doc Tokens |
|-------|-----------|---------------|
| Salesforce Llama Rank V1 | `Salesforce/Llama-Rank-V1` | 8,192 |

## Rerank Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `model` | string | Yes | Rerank model identifier |
| `query` | string | Yes | Search query |
| `documents` | string[] or object[] | Yes | Documents to rerank. Pass objects with named fields for structured documents. |
| `top_n` | int | No | Return only top N results |
| `return_documents` | bool | No | Include document text in response |
| `rank_fields` | string[] | No | Fields to use for ranking when documents are JSON objects (e.g., `["title", "text"]`) |

## Rerank Response

```json
{
  "results": [
    {"index": 0, "relevance_score": 0.9823},
    {"index": 3, "relevance_score": 0.8451},
    {"index": 1, "relevance_score": 0.2134}
  ]
}
```

## Choosing a Model

- **English-only, short docs:** `BAAI/bge-base-en-v1.5` (fastest, 768d)
- **Multilingual:** `intfloat/multilingual-e5-large-instruct` (1024d, recommended)
- **Reranking:** `mixedbread-ai/Mxbai-Rerank-Large-V2` (32K context per doc)
