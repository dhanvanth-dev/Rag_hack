from fastapi import APIRouter, Header ,Request
from pydantic import BaseModel
from typing import List
from app.rag_pipeline import process_query

router = APIRouter()

class QueryInput(BaseModel):
    documents: str
    questions: List[str]

@router.post("/hackrx/run")
async def run_rag_query(input_data: QueryInput, authorization: str = Header(...)):
    results = await process_query(input_data.documents, input_data.questions)

    # Extract only the final sentence (or clean summary) from each full answer
    final_answers = []
    for answer in results:
        # Option 1: Keep only first paragraph or sentence
        cleaned = answer.strip().split("**Answer:**")[-1].strip()
        if not cleaned:
            # fallback if pattern not found
            cleaned = answer.strip().split("\n\n")[0].strip()
        final_answers.append(cleaned)

    return {"answers": results}
