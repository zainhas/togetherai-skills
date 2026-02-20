# Embedding & Rerank Models Reference

## Embedding Models

| Model | API String | Size | Dimensions | Context | Best For |
|-------|-----------|------|-----------|---------|----------|
| BGE Base EN v1.5 | `BAAI/bge-base-en-v1.5` | 102M | 768 | 512 tokens | General English retrieval |
| GTE Modernbert Base | `Alibaba-NLP/gte-modernbert-base` | 149M | 768 | 8,192 tokens | Long-context retrieval (recommended) |
| Multilingual E5 Large | `intfloat/multilingual-e5-large-instruct` | 560M | 1,024 | 514 tokens | Multilingual retrieval |

**Deprecated models (still functional):**

| Model | API String | Dimensions | Context |
|-------|-----------|-----------|---------|
| BGE Large EN v1.5 | `BAAI/bge-large-en-v1.5` | 1,024 | 512 tokens |
| E5 Mistral 7B | `intfloat/e5-mistral-7b-instruct` | 4,096 | 32,768 tokens |
| GTE Large | `thenlper/gte-large` | 1,024 | 512 tokens |
| UAE Large v1 | `WhereIsAI/UAE-Large-V1` | 1,024 | 512 tokens |
| M2 BERT 80M 8K | `togethercomputer/m2-bert-80M-8k-retrieval` | 768 | 8,192 tokens |
| M2 BERT 80M 32K | `togethercomputer/m2-bert-80M-32k-retrieval` | 768 | 32,768 tokens |

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
| `documents` | string[] | Yes | Documents to rerank |
| `top_n` | int | No | Return only top N results |
| `return_documents` | bool | No | Include document text in response |

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
- **English, long docs:** `Alibaba-NLP/gte-modernbert-base` (8K context, recommended)
- **Multilingual:** `intfloat/multilingual-e5-large-instruct` (1024d)
- **Reranking:** `mixedbread-ai/Mxbai-Rerank-Large-V2` (32K context per doc)
