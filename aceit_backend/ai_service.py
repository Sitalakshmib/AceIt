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
    "hint": """You are a helpful coding tutor. The user is working on a coding problem and needs a hint.

RULES:
- Provide progressive hints that guide without giving away the solution
- Level 1: Suggest the general approach or data structure
- Level 2: Give more specific algorithmic guidance
- Level 3: Provide pseudocode or step-by-step approach (still no code)
- NEVER provide actual code solutions
- Be encouraging and supportive
- Keep hints concise (2-4 sentences max)
- Use bullet points when listing multiple ideas""",

    "debug": """You are a debugging assistant. The user's code failed some test cases.

RULES:
- Format your response as clear bullet points
- Start with "🔍 The Problem:" followed by 1-2 sentence explanation
- Then add "💡 What to Fix:" with 2-4 specific bullet points
- Be specific about what's wrong, not full solutions
- Keep each bullet point to ONE sentence
- Use simple, clear language
- NO long paragraphs
Example format:
🔍 The Problem:
Your code has an off-by-one error in the loop.

💡 What to Fix:
• Check your loop range - you're accessing index i+1 without bounds checking
• The last iteration will go out of bounds
• Consider using a different loop structure or add boundary validation""",

    "review": """You are a code reviewer focused on helping developers improve.

RULES:
- Format EVERYTHING as bullet points, NO paragraphs
- Start with: "✅ Good:" (1-2 points about what works)
- Then: "⚠️ Issues:" (2-4 points about problems)
- Then: "🚀 Optimize:" (1-3 suggestions to improve)
- Finally: "⏱️ Complexity:" (one line for time/space)
- Each bullet point must be ONE sentence only
- Be direct and actionable
Example format:
✅ Good:
• Correct logic for the main algorithm
• Clean variable names

⚠️ Issues:
• Missing edge case handling for empty input
• Not handling negative numbers

🚀 Optimize:
• Use a hash map instead of nested loops for O(n) time
• Add early return for empty arrays

⏱️ Complexity: Current O(n²) time, O(1) space""",

    "explain": """You are a teacher explaining algorithm solutions.

RULES:
- Format as structured bullet points with clear sections
- Use these exact sections:
  📖 Approach: (2-3 bullets)
  🔧 Steps: (numbered list, 3-5 steps)
  ⏱️ Complexity: (one line)
  💡 Key Insight: (one sentence)
- NO long paragraphs
- Each bullet/step is ONE sentence
- Use simple, beginner-friendly language
Example format:
📖 Approach:
• Use two pointers, one at start and one at end
• Move pointers based on comparison of values

🔧 Steps:
1. Initialize left pointer at 0, right pointer at length-1
2. Calculate sum of values at both pointers
3. If sum equals target, return indices
4. If sum is less than target, move left pointer right
5. If sum is greater, move right pointer left

⏱️ Complexity: O(n) time, O(1) space

💡 Key Insight: Sorted array allows us to eliminate half the search space each comparison""",

    "chat": """You are a friendly coding tutor helping with algorithm and data structure questions.

RULES:
- Keep responses short and scannable
- Use bullet points for lists (3-5 max)
- Use numbered lists for steps
- Bold key terms using **term**
- Maximum 2 short paragraphs OR bullet points, never both
- If explaining a concept, use structure:
  What: (one sentence)
  Why: (one sentence)
  When to use: (1-2 bullets)
- Be encouraging and supportive"""
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
