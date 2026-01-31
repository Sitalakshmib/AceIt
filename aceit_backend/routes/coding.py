from fastapi import APIRouter, HTTPException
try:
    from ..database import questions_data, progress_data
except (ImportError, ValueError):
    from database import questions_data, progress_data
from datetime import datetime
from services.leetcode import get_leetcode_problems, get_problem_details
from services.code_executor import execute_code
from services.local_problems import get_local_problems
import uuid

router = APIRouter()

# In-memory cache for problems to avoid hitting LeetCode API too often
problem_cache = {}

# Get all coding problems
@router.get("/problems")
async def get_coding_problems_route():
    """
    Get all coding problems.
    Combines local "Premium" strategy-based questions with fetched LeetCode questions.
    """
    combined_problems = []
    
    # 1. Add Local Premium Problems
    local_problems = get_local_problems()
    for p in local_problems:
        combined_problems.append({
            "id": p["id"],
            "title": p["title"],
            "description": p["description"],
            "difficulty": p["difficulty"],
            "examples": [], # We can simulate examples from test cases if needed
            "starterCode": p["starter_code"],
            "source": "AceIt Premium",
            "is_premium": True
        })
        # Cache them
        problem_cache[p["id"]] = p

    # 2. Add LeetCode Problems
    # Fetch from API
    lc_problems = get_leetcode_problems(limit=10)
    for p in lc_problems:
        # Map LeetCode structure to ours
        p_id = f"lc-{p.get('titleSlug')}"
        combined_problems.append({
            "id": p_id,
            "title": p.get("title"),
            "description": "", # Listed problems often don't have descriptions, fetch on demand
            "difficulty": p.get("difficulty", "Medium"),
            "examples": [],
            "starterCode": {
                "python": f"def solution():\n    # Write your code here\n    pass",
            },
            "source": "LeetCode",
            "is_premium": False
        })
    
    return combined_problems

# Get a specific coding problem by ID
@router.get("/problems/{problem_id}")
async def get_coding_problem_route(problem_id: str):
    """
    Get a specific coding problem by its ID
    """
    # Check cache first
    if problem_id in problem_cache:
        p = problem_cache[problem_id]
        return {
            "id": p["id"],
            "title": p["title"],
            "description": p.get("description", ""),
            "difficulty": p.get("difficulty", "Medium"),
            "starterCode": p["starter_code"],
            "test_cases": p.get("test_cases", [])
        }
    
    # If not in cache and looks like leetcode
    if problem_id.startswith("lc-"):
        slug = problem_id.replace("lc-", "")
        details = get_problem_details(slug)
        if details:
            # Parse detail (HTML description, stats, etc)
            # This is a simplification
            real_desc = details.get('question', {}).get('content', 'No description available.')
            return {
                "id": problem_id,
                "title": details.get('question', {}).get('title'),
                "description": real_desc,
                "difficulty": details.get('question', {}).get('difficulty'),
                "starterCode": {"python": "def solution():\n    pass"} # We'd parse code snippets if available
            }

    return {"error": "Problem not found"}

# Submit code for evaluation
@router.post("/submit")
async def submit_code(payload: dict):
    """
    Execute code for a problem (LeetCode-like).
    """
    problem_id = payload.get("problemId")
    code = payload.get("code")
    language = payload.get("language", "python").lower()
    user_id = payload.get("user_id")
    
    if not code:
        return {"error": "No code provided", "passed": 0, "total": 0, "results": []}
    
    if not problem_id:
        return {"error": "No problem ID provided", "passed": 0, "total": 0, "results": []}
    
    # Get problem definition
    problem = None
    if problem_id in problem_cache:
        problem = problem_cache[problem_id]
    
    if not problem:
        return {"error": "Problem not found. Only local problems support execution.", "passed": 0, "total": 0, "results": []}
        
    test_cases = problem.get("test_cases", [])
    function_name = problem.get("function_name")
    
    if not test_cases:
        return {"error": "No test cases for this problem", "passed": 0, "total": 0, "results": []}
    
    # Execute Code
    result = execute_code(language, code, test_cases, function_name)
    
    # Process Result
    passed_tests = result.get("passed", 0)
    total_tests = result.get("total", 0)
    results_details = result.get("results", [])
    
    percentage = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
    
    # Save Progress
    progress_record = {
        "id": str(uuid.uuid4()),
        "module": "coding",
        "problem_id": problem_id,
        "problem_title": problem.get("title", ""),
        "passed_tests": passed_tests,
        "total_tests": total_tests,
        "percentage": percentage,
        "timestamp": datetime.utcnow().isoformat(),
        "code_submitted": code,
        "user_id": user_id
    }
    progress_data.append(progress_record)
    
    from database import save_progress
    save_progress()
    
    # Generate feedback message
    if "error" in result and result["error"]:
        feedback = f"❌ Error: {result.get('error')}\n{result.get('message', '')}"
    elif passed_tests == total_tests and total_tests > 0:
        feedback = f"✅ Accepted! All {total_tests} test cases passed."
    elif total_tests > 0:
        feedback = f"❌ Wrong Answer: {passed_tests}/{total_tests} test cases passed.\n\n"
        # Show first failed test case
        for r in results_details:
            if r.get("status") == "failed":
                feedback += f"Failed on input: {r.get('input')}\n"
                feedback += f"Expected: {r.get('expected')}\n"
                feedback += f"Got: {r.get('actual')}"
                break
            elif r.get("status") == "error":
                feedback += f"Error on input: {r.get('input')}\n"
                feedback += f"Error: {r.get('error')}"
                break
    else:
        feedback = "No test cases executed."
    
    return {
        "problem_id": problem_id,
        "problem_title": problem.get("title", ""),
        "passed_tests": passed_tests,
        "total_tests": total_tests,
        "percentage": round(percentage, 2),
        "feedback": feedback,
        "results": results_details,
        "raw_output": result  # Debug info
    }

@router.get("/problems/{problem_id}/solution")
async def get_solution(problem_id: str):
    if problem_id in problem_cache:
         return {"solution": problem_cache[problem_id].get("solution", "No solution available")}
    return {"solution": "No solution available for this problem"}
