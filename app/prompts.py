def format_query(user_question: str, chunks: list) -> str:
    context = "\n\n".join(chunks)
    return f"""You are an assistant answering questions based only on the following policy content:
    -----
    {context}
    -----
    Question: {user_question}
    Answer in full, with any clause or section name if possible.
    """
