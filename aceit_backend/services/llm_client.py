import os
import google.generativeai as genai

class LLMClient:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY not found")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("models/gemini-2.5-flash")
        
    def generate_response(self, prompt: str) -> str:
        try:
            print(f"[LLM] Generating content with prompt len: {len(prompt)}...")
            response = self.model.generate_content(prompt)
            print("[LLM] Response received.")
            return response.text
        except Exception as e:
            print("[LLM ERROR]:", e)
            return None
