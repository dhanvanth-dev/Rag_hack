import faiss
import numpy as np

def build_faiss_index(embeddings, chunks):
    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype("float32"))
    return index

def retrieve_top_k(query_embed, index, chunks, k=5):
    D, I = index.search(np.array([query_embed]).astype("float32"), k)
    return [chunks[i] for i in I[0]]
