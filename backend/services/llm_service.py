import os
from typing import Optional

_client = None

def get_llm_client():
    global _client

    if _client is None:
        from google import genai

        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise RuntimeError("GOOGLE_API_KEY not set")

        _client = genai.Client(api_key=api_key)

    return _client

class LLMService:
    def __init__(self):
        pass

    def chat(self, prompt: str) -> str:
        client = get_llm_client()
        response = client.models.generate_content(
            model="models/gemini-flash-latest",
            contents=prompt,
        )
        return response.text

    def generate(self, question: str, context: Optional[str] = None) -> str:
        if context:
            prompt = f"""
You are a helpful assistant.
Use the following context to answer the question.

Context:
{context}

Question:
{question}
"""
        else:
            prompt = question

        return self.chat(prompt)
