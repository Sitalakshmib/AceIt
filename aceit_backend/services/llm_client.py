import os
import time
import google.generativeai as genai

class LLMClient:
    # Model pool - ordered by preference (quality -> speed)
    # Each model has separate free-tier quota limits
    MODELS = [
        "gemini-2.5-flash",      # Best quality, 20 req/day
        "gemini-2.0-flash",      # Good balance, separate quota
        "gemini-flash-latest",   # Auto-updating, separate quota
        "gemini-2.5-flash-lite", # Fastest, separate quota
    ]
    
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY not found")
        genai.configure(api_key=api_key)
        self.current_model_index = 0
        
    def _get_model(self, model_name: str):
        """Get a GenerativeModel instance for the given model name."""
        return genai.GenerativeModel(model_name)
        
    def generate_response(self, prompt: str, max_retries: int = None) -> str:
        """
        Generate response with automatic model rotation on rate limits.
        
        Args:
            prompt: The prompt to generate content for
            max_retries: Maximum number of models to try (default: all models)
            
        Returns:
            Generated text response
            
        Raises:
            Exception: If all models fail or encounter non-rate-limit errors
        """
        if max_retries is None:
            max_retries = len(self.MODELS)
            
        last_error = None
        
        for attempt in range(max_retries):
            model_name = self.MODELS[self.current_model_index % len(self.MODELS)]
            
            try:
                print(f"[LLM] Trying model: {model_name} (attempt {attempt + 1}/{max_retries})")
                print(f"[LLM] Generating content with prompt len: {len(prompt)}...")
                
                model = self._get_model(model_name)
                response = model.generate_content(prompt)
                
                print(f"[LLM] SUCCESS with {model_name}")
                return response.text
                
            except Exception as e:
                error_str = str(e)
                
                # Check if it's a rate limit error (429)
                if "429" in error_str or "quota" in error_str.lower() or "rate limit" in error_str.lower():
                    print(f"[LLM] WARNING: Rate limit hit on {model_name}, rotating to next model...")
                    self.current_model_index += 1
                    last_error = e
                    
                    # If this was the last model, add a small delay before retrying
                    if attempt == max_retries - 1:
                        print(f"[LLM] All models exhausted. Last error: {error_str}")
                    
                    continue
                else:
                    # Non-rate-limit error, fail immediately
                    print(f"[LLM ERROR] Non-rate-limit error on {model_name}: {e}")
                    raise e
        
        # All models failed with rate limits
        error_msg = f"All {max_retries} models exhausted due to rate limits. Please try again later."
        print(f"[LLM ERROR]: {error_msg}")
        if last_error:
            raise Exception(error_msg) from last_error
        else:
            raise Exception(error_msg)
