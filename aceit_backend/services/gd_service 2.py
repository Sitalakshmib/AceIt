import os
# Force reload for groq installation (attempt 2)

import json
from typing import Dict, List, Optional

# Try imports
try:
    from groq import Groq
except ImportError:
    Groq = None

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

class GDService:
    @staticmethod
    def _get_client():
        """
        Returns (client, provider_name) or raises error.
        Priority: Groq -> OpenAI
        """
        groq_key = os.getenv("GROQ_API_KEY")
        openai_key = os.getenv("OPENAI_API_KEY")

        if groq_key and Groq:
            return Groq(api_key=groq_key), "groq"
        
        if openai_key and OpenAI:
            return OpenAI(api_key=openai_key), "openai"
            
        return None, None

    @staticmethod
    def generate_points(topic: str) -> Dict[str, List[str]]:
        client, provider = GDService._get_client()
        
        if not client:
            debug_info = []
            if not groq_key: debug_info.append("Missing GROQ_API_KEY")
            if not openai_key: debug_info.append("Missing OPENAI_API_KEY")
            if not Groq: debug_info.append("Groq lib not imported")
            if not OpenAI: debug_info.append("OpenAI lib not imported")
            
            return {
                "error": True,
                "message": f"Configuration Error: {', '.join(debug_info)}"
            }

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
            model = "llama-3.3-70b-versatile" if provider == "groq" else "gpt-4o-mini"
            
            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful GD training assistant. Output JSON only."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7
            )
            
            content = completion.choices[0].message.content
            data = json.loads(content)
            
            return {
                "status": "success",
                "for_points": data.get("for_points", []),
                "against_points": data.get("against_points", [])
            }

        except Exception as e:
            print(f"[GD Error] {provider}: {str(e)}")
            return {
                "error": True,
                "message": f"AI Generation Failed: {str(e)}"
            }
