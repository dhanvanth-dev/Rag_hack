from app.loader import load_and_chunk_document
from app.embedding import get_embeddings
from app.vectorstore import build_faiss_index, retrieve_top_k
from app.prompts import format_query
from app.api_call import call_deepseek_r1
import asyncio

async def process_query(document_url: str, questions: list):
    chunks = load_and_chunk_document(document_url)
    embeddings = get_embeddings(chunks)

    print(f" Document URL: {document_url}")
    print(f" Questions received: {questions}")
    print(f" Total chunks loaded: {len(chunks)}")
    print(f" Embeddings shape: {embeddings.shape if hasattr(embeddings, 'shape') else 'Not available'}")
    faiss_index = build_faiss_index(embeddings, chunks)

    # results = []
    # for question in questions:
    #     print(f" Querying model for: {question}")
    #     query_embed = get_embeddings([question])[0]
    #     top_chunks = retrieve_top_k(query_embed, faiss_index, chunks, k=5)
    #     prompt = format_query(question, top_chunks)
    #     answer = call_deepseek_r1(prompt)
    #     print(f"✅ Answer: {answer}")
    #     results.append(answer)

    async def query_llm(question):
        print(f" Querying model for: {question}")
        query_embed = get_embeddings([question])[0]
        top_chunks = retrieve_top_k(query_embed, faiss_index, chunks, k=5)
        prompt = format_query(question, top_chunks)
        answer = await call_deepseek_r1(prompt)
        print(f"✅ Answer: {answer}")
        return answer
    
    # Run all queries in parallel
    results = await asyncio.gather(*(query_llm(q) for q in questions))
    
    return results
