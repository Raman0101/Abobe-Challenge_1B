from sentence_transformers import SentenceTransformer
import numpy as np

# Load the model once globally (CPU only)
model = SentenceTransformer("all-MiniLM-L6-v2")  # ~80MB, fast, CPU-compatible

def embed_chunks(chunk_data):
    """
    chunk_data: list of tuples (doc_name, chunk_text, page_number)
    Returns: list of dicts with embeddings and metadata
    """
    texts = [chunk[1] for chunk in chunk_data]
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)

    embedded_chunks = []
    for i, (doc_name, chunk_text, page_number) in enumerate(chunk_data):
        embedded_chunks.append({
            "document": doc_name,
            "text": chunk_text,
            "page_number": page_number,
            "embedding": embeddings[i]
        })

    return embedded_chunks


def embed_query(text):
    """
    Embeds a single query string (persona + job prompt).
    """
    return model.encode([text], convert_to_numpy=True)[0]
