# services/llm_service.py

import os
from google import genai
from google.genai import types

class LLMService:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("⚠️ WARNING: GOOGLE_API_KEY not found in .env")
            self.client = None
        else:
            self.client = genai.Client(api_key=api_key)
            print("✅ Google Gemini initialized (new SDK)")
    
    def generate(self, question: str, context: str = None, system_prompt: str = None, temperature: float = 0.7, model: str = None, **kwargs) -> str:
        """
        Generate response using Google Gemini (FREE)
        """
        
        if not self.client:
            return "LLM not configured. Please add GOOGLE_API_KEY to .env file."
        
        # Build prompt
        if context and context.strip():
            prompt = f"""You are a helpful assistant that answers questions based on provided context.

Context:
{context}

Question: {question}

Please answer the question based on the context provided above. Be concise and accurate."""
        else:
            prompt = f"""You are a helpful assistant.

Question: {question}

Please provide a helpful and accurate answer."""
        
        try:
            print(f"🔵 Calling Google Gemini API...")
            print(f"  Model: gemini-2.0-flash-exp (FREE)")
            print(f"  Has context: {context is not None}")
            print(f"  Question: {question[:50]}...")
            
            # Generate response using new SDK
            response = self.client.models.generate_content(
                model='gemini-2.0-flash-exp',  # Latest free model
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=temperature,
                    max_output_tokens=1000,
                )
            )
            
            # Extract answer
            answer = response.text
            
            if not answer or len(answer.strip()) == 0:
                print(f"  ⚠️ Empty response from Gemini")
                return self._fallback_response(question, context)
            
            print(f"  ✅ Generated response ({len(answer)} chars)")
            return answer.strip()
            
        except Exception as e:
            print(f"  ❌ Gemini API error: {e}")
            return self._fallback_response(question, context)
    
    def _fallback_response(self, question: str, context: str = None) -> str:
        """Fallback response when API fails"""
        if context and context.strip():
            summary = context[:400].strip()
            return f"Based on the available information: {summary}..."
        else:
            return f"I understand you're asking: '{question}'. However, I'm unable to generate a response at this moment."