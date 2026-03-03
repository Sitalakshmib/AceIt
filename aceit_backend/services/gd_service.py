import os
# Force reload for groq installation (attempt 2)

import json
from typing import Dict, List, Optional, Any

# Try imports
try:
    from groq import Groq
except ImportError:
    Groq = None

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

from services.llm_client import LLMClient

class GDService:
    @staticmethod
    def generate_points(topic: str) -> Dict[str, Any]:
        llm = LLMClient()
        
        prompt = f"""
        You are a placement training assistant helping students prepare for Group Discussions (GD).
        
        Topic: "{topic}"
        
        Task: Generate 5-7 clear, balanced arguments FOR the topic and 5-7 practical arguments AGAINST it.
        
        Rules:
        - Use simple, professional language.
        - Keep points concise (1 sentence each).
        - Avoid extreme/offensive views.
        - JSON Format ONLY.
        
        Output JSON Structure:
        {{
            "for_points": ["point 1", "point 2", ...],
            "against_points": ["point 1", "point 2", ...]
        }}
        """

        try:
            response_text = llm.generate_response(prompt)
            # LLMClient might return JSON string, let's try to parse it
            import re
            
            # Find JSON block if it exists
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group(0))
            else:
                # If no JSON block found, try parsing the whole thing
                data = json.loads(response_text)
            
            return {
                "status": "success",
                "for_points": data.get("for_points", []),
                "against_points": data.get("against_points", [])
            }

        except Exception as e:
            print(f"[GD Error]: {str(e)}")
            return {
                "error": True,
                "message": f"AI Generation Failed: {str(e)}"
            }
