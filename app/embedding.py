from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def get_embeddings(texts: list):
    return model.encode(texts, convert_to_tensor=False).tolist()
