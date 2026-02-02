import os
import time
import google.generativeai as genai
from openai import OpenAI
from groq import Groq
from typing import List, Dict, Any

class LLMClient:
    # Model pool - ordered by preference (quality -> speed)
    # Each model entry specifies its provider and model ID
    MODELS = [
        {"provider": "groq", "id": "llama-3.3-70b-versatile"}, # Primary: High speed & quality
        {"provider": "openai", "id": "gpt-4o-mini"},          # Secondary: Reliable & cheap
        {"provider": "groq", "id": "mixtral-8x7b-32768"},     # Fallback: Extremely fast
        {"provider": "openai", "id": "gpt-4o"},               # Final Backup: High intelligence
    ]
    
    def __init__(self, groq_env_key="GROQ_API_KEY", openai_env_key="OPENAI_API_KEY"):
        # Initialize Google Gemini
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if gemini_api_key:
            genai.configure(api_key=gemini_api_key)
            self.gemini_available = True
        else:
            print("[LLM] WARNING: GEMINI_API_KEY not found")
            self.gemini_available = False
            
        # Initialize OpenAI
        openai_api_key = os.getenv(openai_env_key)
        if openai_api_key:
            self.openai_client = OpenAI(api_key=openai_api_key)
            self.openai_available = True
        else:
            print(f"[LLM] WARNING: {openai_env_key} not found")
            self.openai_available = False

        # Initialize Groq
        groq_api_key = os.getenv(groq_env_key)
        if groq_api_key:
            self.groq_client = Groq(api_key=groq_api_key)
            self.groq_available = True
        else:
            print(f"[LLM] WARNING: {groq_env_key} not found (Groq unavailable)")
            self.groq_available = False
            
        self.current_model_index = 0
        
    def generate_response(self, prompt: str, max_retries: int = None) -> str:
        """
        Generate response with automatic model rotation across providers on failures.
        """
        if max_retries is None:
            max_retries = len(self.MODELS)
            
        last_error = None
        
        for attempt in range(max_retries):
            model_info = self.MODELS[self.current_model_index % len(self.MODELS)]
            provider = model_info["provider"]
            model_id = model_info["id"]
            
            try:
                print(f"[LLM] Trying {provider} model: {model_id} (attempt {attempt + 1}/{max_retries})")
                
                if provider == "google":
                    if not self.gemini_available:
                        raise Exception("Gemini API key missing")
                    model = genai.GenerativeModel(model_id)
                    response = model.generate_content(prompt)
                    return response.text
                
                elif provider == "openai":
                    if not self.openai_available:
                        raise Exception("OpenAI API key missing")
                    response = self.openai_client.chat.completions.create(
                        model=model_id,
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.7,
                    )
                    return response.choices[0].message.content

                elif provider == "groq":
                    if not self.groq_available:
                        raise Exception("Groq API key missing")
                    chat_completion = self.groq_client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model=model_id,
                        temperature=0.7,
                    )
                    return chat_completion.choices[0].message.content
                
            except Exception as e:
                error_str = str(e)
                print(f"[LLM] Error with {model_id}: {error_str}")
                
                # Check for rate limit or quota errors
                is_rate_limit = any(kw in error_str.lower() for kw in ["429", "quota", "rate limit", "busy", "exhausted"])
                
                if is_rate_limit or "API key missing" in error_str:
                    print(f"[LLM] Rotating to next model due to: {error_str[:50]}...")
                    self.current_model_index += 1
                    last_error = e
                    continue
                else:
                    # Non-temporary error, but we'll try rotating anyway for robustness
                    print(f"[LLM] Critical error, trying next model anyway...")
                    self.current_model_index += 1
                    last_error = e
                    continue
        
        error_msg = f"All {max_retries} AI providers exhausted. Please try again later."
        print(f"[LLM ERROR]: {error_msg}")
        raise Exception(error_msg) from last_error

    def generate_response_from_messages(self, messages: List[Dict], max_retries: int = None) -> str:
        """
        Adapts messages list and routes to provider-specific logic.
        """
        # Flattening to single prompt for consistent multi-provider support
        
        formatted_prompt = ""
        for msg in messages:
            role = "Coach" if msg['role'] == 'assistant' else "Student"
            if msg['role'] == 'system':
                role = "SYSTEM"
            formatted_prompt += f"{role}: {msg['content']}\n"
        
        formatted_prompt += "\nCoach:"
        
        return self.generate_response(formatted_prompt, max_retries)
