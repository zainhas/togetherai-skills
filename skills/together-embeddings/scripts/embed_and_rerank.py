#!/usr/bin/env python3
"""
Together AI Embeddings + Reranking Pipeline (v2 SDK)

Embed documents, compute similarity, and rerank results for a query.

Usage:
    python embed_and_rerank.py

Requires:
    pip install together
    export TOGETHER_API_KEY=your_key
"""

import math
from together import Together

client = Together()


def embed_texts(texts: list[str], model: str = "BAAI/bge-base-en-v1.5") -> list[list[float]]:
    """Embed a list of texts, returns list of embedding vectors."""
    response = client.embeddings.create(
        model=model,
        input=texts,
    )
    return [item.embedding for item in response.data]


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Compute cosine similarity between two vectors."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0


def rerank_documents(query: str, documents: list[str], top_n: int = 3) -> list[dict]:
    """Rerank documents by relevance to a query."""
    response = client.rerank.create(
        model="mixedbread-ai/Mxbai-Rerank-Large-V2",
        query=query,
        documents=documents,
        top_n=top_n,
    )
    results = []
    for item in response.results:
        results.append({
            "index": item.index,
            "score": item.relevance_score,
            "document": documents[item.index],
        })
    return results


if __name__ == "__main__":
    # --- Example: Embed and compute similarity ---
    texts = [
        "Python is a popular programming language",
        "JavaScript is used for web development",
        "Machine learning uses statistical models",
    ]
    query = "What language is good for data science?"

    embeddings = embed_texts(texts + [query])
    query_emb = embeddings[-1]
    doc_embs = embeddings[:-1]

    print("Embedding similarity:")
    for i, text in enumerate(texts):
        sim = cosine_similarity(query_emb, doc_embs[i])
        print(f"  {sim:.4f} — {text}")

    # --- Example: Rerank for better precision ---
    documents = [
        "Python is widely used in data science and machine learning.",
        "Java is a popular language for enterprise applications.",
        "R is a language designed for statistical computing.",
        "JavaScript powers most web applications.",
        "SQL is essential for database querying.",
    ]

    print(f"\nReranking for: '{query}'")
    ranked = rerank_documents(query, documents, top_n=3)
    for r in ranked:
        print(f"  [{r['score']:.4f}] {r['document']}")
