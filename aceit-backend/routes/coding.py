from fastapi import APIRouter
from database import questions_data, progress_data
from datetime import datetime

router = APIRouter()

# Get all coding problems
@router.get("/problems")
async def get_coding_problems():
    """
    Get all coding problems from database
    """
    # Filter questions that have a title (coding problems)
    problems = [q for q in questions_data if 'title' in q]
    
    # Format problems to match frontend expectations
    formatted_problems = []
    for problem in problems:
        formatted_problem = {
            "id": problem.get("id"),
            "title": problem.get("title"),
            "description": problem.get("description", ""),
            "difficulty": problem.get("difficulty", "Medium"),
            "examples": problem.get("examples", []),
            "starterCode": {
                "javascript": problem.get("starter_code", "// Write your solution here")
            }
        }
        formatted_problems.append(formatted_problem)
    
    return formatted_problems

# Get a specific coding problem by ID
@router.get("/problems/{problem_id}")
async def get_coding_problem(problem_id: str):
    """
    Get a specific coding problem by its ID
    """
    problem = next((p for p in questions_data if p.get('id') == problem_id and 'title' in p), None)
    
    if not problem:
        return {"error": "Problem not found"}
    
    # Format problem to match frontend expectations
    formatted_problem = {
        "id": problem.get("id"),
        "title": problem.get("title"),
        "description": problem.get("description", ""),
        "difficulty": problem.get("difficulty", "Medium"),
        "examples": problem.get("examples", []),
        "starterCode": {
            "javascript": problem.get("starter_code", "// Write your solution here")
        }
    }
    
    return formatted_problem

# Submit code for evaluation
@router.post("/submit")
async def submit_code(payload: dict):
    """
    Submit code for a coding problem
    Expected input: {"problemId": "code1", "code": "def fibonacci(n):..."}
    """
    problem_id = payload.get("problemId")
    code = payload.get("code")
    
    # Get the problem from database
    problem = next((p for p in questions_data if p.get('id') == problem_id), None)
    
    if not problem:
        return {"error": "Problem not found"}
    
    # For demo purposes, we'll simulate code evaluation
    test_cases = problem.get("test_cases", [])
    passed_tests = 0
    total_tests = len(test_cases)
    
    # Mock evaluation - in demo, we'll pass 2 out of 3 tests for Fibonacci
    if problem_id == "code1":  # Fibonacci problem
        passed_tests = 2  # Mock: passed 2 tests
    elif problem_id == "code2":  # Palindrome problem  
        passed_tests = 1  # Mock: passed 1 test
    else:
        passed_tests = total_tests  # Mock: pass all for other problems
    
    # Calculate percentage
    percentage = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
    
    # Save progress to database
    progress_data.append({
        "module": "coding",
        "problem_id": problem_id,
        "problem_title": problem.get("title", ""),
        "passed_tests": passed_tests,
        "total_tests": total_tests,
        "percentage": percentage,
        "timestamp": datetime.utcnow(),
        "code_submitted": code  # Store the submitted code
    })
    
    return {
        "problem_id": problem_id,
        "problem_title": problem.get("title", ""),
        "passed_tests": passed_tests,
        "total_tests": total_tests,
        "percentage": round(percentage, 2),
        "feedback": f"Your code passed {passed_tests} out of {total_tests} test cases"
    }