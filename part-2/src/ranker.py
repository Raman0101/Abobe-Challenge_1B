import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def rank_chunks(embedded_chunks, query_embedding, top_k=5):
    """
    Ranks embedded chunks based on cosine similarity to query embedding.
    Returns top_k results sorted by importance_rank.
    """
    similarities = []
    for chunk in embedded_chunks:
        score = cosine_similarity(
            [chunk["embedding"]],
            [query_embedding]
        )[0][0]
        similarities.append((chunk, score))

    # Sort by descending similarity
    similarities.sort(key=lambda x: x[1], reverse=True)

    top_chunks = []
    for rank, (chunk, score) in enumerate(similarities[:top_k], start=1):
        top_chunks.append({
            "document": chunk["document"],
            "section_title": chunk["text"][:80].strip() + ("..." if len(chunk["text"]) > 80 else ""),
            "importance_rank": rank,
            "page_number": chunk["page_number"],
            "refined_text": chunk["text"]
        })

    return top_chunks
