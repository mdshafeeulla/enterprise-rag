# core/prompt_builder.py


def build_prompt(chunks: list[dict], question: str, department: str) -> str:
    """
    Build a structured prompt for the LLM.
    Includes department context and source attribution.
    """
    context_parts = []
    for c in chunks:
        context_parts.append(c['text'])
    context = "\n\n---\n\n".join(context_parts)

    return f"""You are a knowledgeable AI assistant for the **{department.upper()}** department.

## Rules
1. If the user is just saying hello, greeting you, or making casual conversation, respond politely and naturally.
2. For domain-specific questions, answer using the context documents provided below.
3. Answer the user's question directly and naturally. Do NOT mention "Document 1", "Source A", or "According to the reference" in your response.
4. If the answer is NOT in the context, say: "I don't have enough information in the {department} documents to answer this."
5. Do NOT make up information or use knowledge outside the provided context for factual questions.
6. Use markdown formatting for clarity.

## Context Data ({department.upper()} department)
{context}

## Question
{question}

## Answer"""
