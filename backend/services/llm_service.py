import os
from typing import Optional

_client = None

def get_llm_client():
    global _client

    if _client is None:
        import google.generativeai as genai

        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise RuntimeError("GOOGLE_API_KEY not set")

        genai.configure(api_key=api_key)

        # Store the model, not a "client"
        _client = genai.GenerativeModel("models/gemini-1.5-flash")

    return _client


class LLMService:
    def chat(self, prompt: str) -> str:
        model = get_llm_client()

        response = model.generate_content(prompt)

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
