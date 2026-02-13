"""
AI Tutor Service for AceIt Coding Module
Provides intelligent tutoring features using Google Gemini
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai
from typing import Optional, List, Dict, Any

# Load environment variables from .env file
load_dotenv()

# Initialize Gemini client
genai.configure(api_key=os.getenv("GEMINI_API_KEY_HELL"))
model = genai.GenerativeModel('gemini-2.5-flash')


# System prompts for different tutor modes
SYSTEM_PROMPTS = {
    "hint": """You are a friendly and encouraging coding tutor. The user is stuck and needs a hint.

RULES:
- RESPONSE FORMAT: Always use a simple list of bullet points.
- LANGUAGE: Use very simple, easy-to-understand English. Avoid complex jargon.
- TONE: Be very nice, encouraging, and supportive (e.g., "You're doing great!", "Let's look at this together").
- CONTENT:
  - Level 1: Give a gentle nudge about the general idea.
  - Level 2: Suggest the specific steps or logic needed.
  - Level 3: Describe the solution steps clearly (but no code!).
- LENGTH: Keep it short and sweet. 3-4 bullet points max.
- NEVER provide the actual code solution.""",

    "debug": """You are a kind and helpful debugging assistant. The user's code has a mistake.

RULES:
- RESPONSE FORMAT: Always use a simple list of bullet points.
- LANGUAGE: Use very simple, plain English. Explain technical terms if you must use them.
- TONE: Be empathetic and nice (e.g., "Don't worry, bugs happen to everyone!").
- STRUCTURE:
  - 🔍 What's Wrong: (1-2 simple points explaining the error)
  - 💡 How to Fix It: (2-3 simple steps to correct it)
- CONTENT: Focus on the specific error. Match the user's coding level.
- NEVER write the full corrected code, just guide them.""",

    "review": """You are a supportive code reviewer. You want to help the user improve.

RULES:
- RESPONSE FORMAT: Always use a simple list of bullet points.
- LANGUAGE: Use simple, friendly English.
- TONE: Be very positive and constructive.
- STRUCTURE:
  - ✅ Great Job: (Mention what they did well)
  - ⚠️ A Little Fix: (Point out potential issues gently)
  - 🚀 Make it Better: (Simple tips to improve efficiency or style)
- CONTENT: Keep feedback actionable and easy to grasp.
- Limit to 3-4 points per section.""",

    "explain": """You are a fantastic teacher explaining a coding solution.

RULES:
- RESPONSE FORMAT: Always use a simple list of bullet points.
- LANGUAGE: Use very simple, beginner-friendly English. Imagine explaining to a student.
- TONE: Be enthusiastic and clear.
- STRUCTURE:
  - 📖 The Idea: (Simple explanation of the approach)
  - 🔧 Steps: (Numbered list of simple steps)
  - ⏱️ Speed: (Simple explanation of time complexity)
  - 💡 Tip: (One key takeaway)
- CONTENT: Break down complex logic into small, easy chunks.""",

    "chat": """You are a friendly and knowledgeable AI Coding Tutor.

RULES:
- RESPONSE FORMAT: Always use a simple list of bullet points or short paragraphs.
- LANGUAGE: Use very simple, easy-to-understand English.
- TONE: Be super nice, encouraging, and helpful.
- CONTENT: Answer the user's question directly and simply.
- If explaining a concept, break it down:
  - What it is
  - Why we use it
  - An easy example
- Keep answers concise and easy to read."""
}



def get_hint(
    problem_title: str,
    problem_description: str,
    user_code: str,
    hint_level: int = 1,
    tags: List[str] = None
) -> str:
    """
    Get a progressive hint for the coding problem.
    
    Args:
        problem_title: Title of the problem
        problem_description: Full problem description
        user_code: User's current code attempt
        hint_level: 1-3, with 3 being most specific
        tags: Problem tags (e.g., ["Array", "Two Pointers"])
    
    Returns:
        A helpful hint string
    """
    try:
        prompt = f"""{SYSTEM_PROMPTS["hint"]}

Problem: {problem_title}
Tags: {', '.join(tags) if tags else 'N/A'}

Description:
{problem_description[:1500]}

User's Current Code:
```
{user_code[:2000] if user_code else '(No code yet)'}
```

Provide a Level {hint_level} hint. Remember:
- Level 1: General approach/data structure suggestion
- Level 2: More specific algorithmic guidance  
- Level 3: Detailed approach (still no actual code)

Current request is Level {hint_level}."""

        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"Sorry, I couldn't generate a hint right now. Error: {str(e)}"


def debug_code(
    problem_title: str,
    problem_description: str,
    user_code: str,
    test_input: str,
    expected_output: str,
    actual_output: str,
    error_message: str = None
) -> str:
    """
    Analyze why code failed a test case.
    
    Args:
        problem_title: Title of the problem
        problem_description: Problem description
        user_code: User's submitted code
        test_input: The input that failed
        expected_output: What the output should be
        actual_output: What the code actually produced
        error_message: Any runtime error message
    
    Returns:
        Debugging analysis and suggestions
    """
    try:
        prompt = f"""{SYSTEM_PROMPTS["debug"]}

Problem: {problem_title}

Description:
{problem_description[:1000]}

User's Code:
```
{user_code[:2500]}
```

Failed Test Case:
- Input: {test_input}
- Expected Output: {expected_output}
- Actual Output: {actual_output}
{f'- Error: {error_message}' if error_message else ''}

Explain why this code failed and what needs to be fixed (without giving the complete solution)."""

        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"Sorry, I couldn't analyze the code right now. Error: {str(e)}"


def review_code(
    problem_title: str,
    problem_description: str,
    user_code: str,
    passed_all_tests: bool,
    tags: List[str] = None
) -> str:
    """
    Review submitted code for improvements.
    
    Args:
        problem_title: Title of the problem
        problem_description: Problem description
        user_code: User's submitted code
        passed_all_tests: Whether the code passed all tests
        tags: Problem tags
    
    Returns:
        Code review with suggestions
    """
    try:
        status = "✅ All tests passed" if passed_all_tests else "❌ Some tests failed"
        
        prompt = f"""{SYSTEM_PROMPTS["review"]}

Problem: {problem_title}
Tags: {', '.join(tags) if tags else 'N/A'}
Status: {status}

Description:
{problem_description[:1000]}

User's Code:
```
{user_code[:3000]}
```

Please review this code and provide feedback on:
1. Correctness and edge cases
2. Time and space complexity
3. Code style and readability
4. Possible optimizations"""

        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"Sorry, I couldn't review the code right now. Error: {str(e)}"


def explain_solution(
    problem_title: str,
    problem_description: str,
    optimal_solution: str = None,
    tags: List[str] = None
) -> str:
    """
    Explain the optimal solution approach.
    
    Args:
        problem_title: Title of the problem
        problem_description: Problem description
        optimal_solution: The reference solution (optional)
        tags: Problem tags
    
    Returns:
        Step-by-step explanation of optimal approach
    """
    try:
        prompt = f"""{SYSTEM_PROMPTS["explain"]}

Problem: {problem_title}
Tags: {', '.join(tags) if tags else 'N/A'}

Description:
{problem_description[:1500]}

{f'Reference Solution:```{optimal_solution[:2000]}```' if optimal_solution else ''}

Please explain:
1. The optimal approach to solve this problem
2. The algorithm pattern being used
3. Step-by-step breakdown
4. Time and space complexity
5. Why this approach is optimal"""

        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"Sorry, I couldn't explain the solution right now. Error: {str(e)}"


def chat(
    user_message: str,
    problem_context: Dict[str, Any] = None,
    conversation_history: List[Dict[str, str]] = None
) -> str:
    """
    General Q&A chat about algorithms and concepts.
    
    Args:
        user_message: User's question
        problem_context: Optional context about current problem
        conversation_history: Previous messages in conversation
    
    Returns:
        AI response
    """
    try:
        context = ""
        if problem_context:
            context = f"\n[Context: User is working on \"{problem_context.get('title', 'a problem')}\" with tags: {', '.join(problem_context.get('tags', []))}]\n"
        
        prompt = f"""{SYSTEM_PROMPTS["chat"]}
{context}
User Question: {user_message}"""

        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"Sorry, I couldn't respond right now. Error: {str(e)}"
