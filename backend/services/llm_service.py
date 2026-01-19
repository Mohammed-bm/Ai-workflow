import os
from typing import Optional
from google import genai
from dotenv import load_dotenv

load_dotenv() 

class LLMService:
    def __init__(self):
        self.client = genai.Client(
            api_key=os.getenv("GOOGLE_API_KEY")
        )

    def chat(self, prompt: str) -> str:
        response = self.client.models.generate_content(
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
