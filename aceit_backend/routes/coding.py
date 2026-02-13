from fastapi import APIRouter, HTTPException, Depends
from database import questions_data, progress_data
from database_postgres import get_db, SessionLocal
from models.coding_problem_sql import CodingProblem
from models.user_coding_progress import UserCodingProgress
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import pytz
from services.leetcode import get_leetcode_problems, get_problem_details
from services.code_executor import execute_code
from services.local_problems import get_local_problems
import uuid

router = APIRouter()

# In-memory cache for problems to avoid hitting DB/API too often
problem_cache = {}

# Indian Standard Time timezone
IST = pytz.timezone('Asia/Kolkata')

def get_ist_now():
    """Get current time in IST"""
    return datetime.now(IST)


def get_db_problems(db: Session):
    """Fetch all problems from the database, ordered by difficulty (Easy -> Medium -> Hard)."""
    from sqlalchemy import case
    
    # Custom ordering: Easy=1, Medium=2, Hard=3
    difficulty_order = case(
        (CodingProblem.difficulty == "Easy", 1),
        (CodingProblem.difficulty == "Medium", 2),
        (CodingProblem.difficulty == "Hard", 3),
        else_=4
    )
    return db.query(CodingProblem).order_by(difficulty_order).all()


def get_db_problem_by_id(db: Session, problem_id: str):
    """Fetch a specific problem from the database by ID."""
    return db.query(CodingProblem).filter(CodingProblem.id == problem_id).first()


@router.get("/problems")
def get_coding_problems_route():
    """
    Get all coding problems.
    Fetches from Neon PostgreSQL database, falls back to local_problems.py if DB is unavailable.
    Also combines with fetched LeetCode questions.
    """
    combined_problems = []
    local_slugs = set()
    
    # Check if database is available
    if SessionLocal is None:
        print("⚠️ Database not available, using local_problems.py")
        # Fallback to local problems
        local_probs = get_local_problems()
        for p in local_probs:
            slug = p.get("titleSlug", "")
            if slug:
                local_slugs.add(slug)
            combined_problems.append(p)
    else:
        # Try to get problems from database first
        db = SessionLocal()
        try:
            db_problems = get_db_problems(db)
            
            if db_problems:
                # Use database problems
                for p in db_problems:
                    slug = p.title_slug or ""
                    if slug:
                        local_slugs.add(slug)
                    
                    problem_dict = {
                        "id": p.id,
                        "title": p.title,
                        "titleSlug": slug,
                        "description": p.description,
                        "difficulty": p.difficulty,
                        "tags": p.tags or [],
                        "examples": [],
                        "starterCode": p.starter_code or {},
                        "source": "AceIt Premium",
                        "is_premium": True
                    }
                    combined_problems.append(problem_dict)
                    
                    # Cache the full problem for later use
                    problem_cache[p.id] = {
                        "id": p.id,
                        "title": p.title,
                        "titleSlug": slug,
                        "description": p.description,
                        "difficulty": p.difficulty,
                        "tags": p.tags or [],
                        "function_name": p.function_name,
                        "starter_code": p.starter_code or {},
                        "test_cases": p.test_cases or [],
                        "solution": p.solution
                    }
            else:
                # Fallback to local_problems.py if database is empty
                print("⚠️ No problems in database, falling back to local_problems.py")
                local_problems = get_local_problems()
                
                # Sort by difficulty: Easy -> Medium -> Hard
                difficulty_order = {"Easy": 1, "Medium": 2, "Hard": 3}
                local_problems = sorted(local_problems, key=lambda x: difficulty_order.get(x.get("difficulty", "Medium"), 4))
                
                for p in local_problems:
                    slug = p.get("titleSlug", "")
                    if slug:
                        local_slugs.add(slug)
                        
                    combined_problems.append({
                        "id": p["id"],
                        "title": p["title"],
                        "titleSlug": slug,
                        "description": p["description"],
                        "difficulty": p["difficulty"],
                        "tags": p.get("tags", []),
                        "examples": [],
                        "starterCode": p["starter_code"],
                        "source": "AceIt Premium",
                        "is_premium": True
                    })
                    # Cache them
                    problem_cache[p["id"]] = p
        finally:
            db.close()

    # DISABLED: LeetCode API fetch (we have all problems in database)
    # Add LeetCode problems
    # lc_problems = get_leetcode_problems(limit=20)
    # for p in lc_problems:
    #     slug = p.get("titleSlug")
    #     
    #     # Avoid duplicates
    #     if slug in local_slugs:
    #         continue
    #         
    #     # Map LeetCode structure to ours
    #     p_id = f"lc-{slug}"
    #     
    #     # Extract tag names
    #     tags = [tag.get("name") for tag in p.get("topicTags", [])] if p.get("topicTags") else ["LeetCode"]
    #     
    #     combined_problems.append({
    #         "id": p_id,
    #         "title": p.get("title"),
    #         "titleSlug": slug,
    #         "description": "",  # Listed problems often don't have descriptions, fetch on demand
    #         "difficulty": p.get("difficulty", "Medium"),
    #         "tags": tags,
    #         "examples": [],
    #         "starterCode": {
    #             "python": f"def solution():\n    # Write your code here\n    pass",
    #         },
    #         "source": "LeetCode",
    #         "is_premium": False
    #     })
    
    return combined_problems


# Get a specific coding problem by ID
@router.get("/problems/{problem_id}")
def get_coding_problem_route(problem_id: str):
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
            "starterCode": p.get("starter_code", {}),
            "test_cases": p.get("test_cases", [])
        }
    
    # Try database
    db = SessionLocal()
    try:
        db_problem = get_db_problem_by_id(db, problem_id)
        if db_problem:
            # Cache it
            problem_cache[problem_id] = {
                "id": db_problem.id,
                "title": db_problem.title,
                "titleSlug": db_problem.title_slug,
                "description": db_problem.description,
                "difficulty": db_problem.difficulty,
                "tags": db_problem.tags or [],
                "function_name": db_problem.function_name,
                "starter_code": db_problem.starter_code or {},
                "test_cases": db_problem.test_cases or [],
                "solution": db_problem.solution
            }
            return {
                "id": db_problem.id,
                "title": db_problem.title,
                "description": db_problem.description,
                "difficulty": db_problem.difficulty,
                "starterCode": db_problem.starter_code,
                "test_cases": db_problem.test_cases
            }
    finally:
        db.close()
    
    # If not in cache/DB and looks like leetcode
    if problem_id.startswith("lc-"):
        slug = problem_id.replace("lc-", "")
        details = get_problem_details(slug)
        if details:
            # The API might return the description in 'question' or 'question.content'
            question_data = details.get('question')
            if isinstance(question_data, dict):
                real_desc = question_data.get('content', 'No description available.')
                real_title = question_data.get('title', details.get('questionTitle'))
                real_diff = question_data.get('difficulty', details.get('difficulty'))
            else:
                real_desc = question_data if question_data else 'No description available.'
                real_title = details.get('questionTitle')
                real_diff = details.get('difficulty')

            return {
                "id": problem_id,
                "title": real_title,
                "description": real_desc,
                "difficulty": real_diff,
                "starterCode": {"python": "def solution():\n    pass"}  # We'd parse code snippets if available
            }

    return {"error": "Problem not found"}


# Submit code for evaluation
@router.post("/submit")
def submit_code(payload: dict):
    """
    Execute code for a problem (HackerRank-style).
    Supports two actions:
    - "run": Tests only first 3 test cases (sample tests)
    - "submit": Tests all test cases and updates solved status
    """
    problem_id = payload.get("problemId")
    code = payload.get("code")
    language = payload.get("language", "python").lower()
    user_id = payload.get("user_id")
    action = payload.get("action", "run")  # "run" or "submit"
    
    if not code:
        return {"error": "No code provided", "passed": 0, "total": 0, "results": [], "action": action}
    
    if not problem_id:
        return {"error": "No problem ID provided", "passed": 0, "total": 0, "results": [], "action": action}
    
    # Get problem definition
    problem = None
    if problem_id in problem_cache:
        problem = problem_cache[problem_id]
    else:
        # Try to fetch from database
        db = SessionLocal()
        try:
            db_problem = get_db_problem_by_id(db, problem_id)
            if db_problem:
                problem = {
                    "id": db_problem.id,
                    "title": db_problem.title,
                    "function_name": db_problem.function_name,
                    "test_cases": db_problem.test_cases or [],
                    "solution": db_problem.solution
                }
                problem_cache[problem_id] = problem
        finally:
            db.close()
    
    if not problem:
        return {"error": "Problem not found. Only local problems support execution.", "passed": 0, "total": 0, "results": [], "action": action}
        
    all_test_cases = problem.get("test_cases", [])
    function_name = problem.get("function_name")
    
    if not all_test_cases:
        return {"error": "No test cases for this problem", "passed": 0, "total": 0, "results": [], "action": action}
    
    # Determine which test cases to run based on action
    if action == "run":
        # For "run", only test first 3 test cases (visible sample tests)
        test_cases_to_run = all_test_cases[:3]
        visible_count = len(test_cases_to_run)
        hidden_count = len(all_test_cases) - visible_count
    else:
        # For "submit", test all test cases
        test_cases_to_run = all_test_cases
        visible_count = min(3, len(all_test_cases))
        hidden_count = max(0, len(all_test_cases) - 3)
    
    # Execute Code
    result = execute_code(language, code, test_cases_to_run, function_name)
    
    # Process Result
    passed_tests = result.get("passed", 0)
    total_tests = result.get("total", 0)
    results_details = result.get("results", [])
    
    # Mark which test cases are visible (first 3)
    for i, r in enumerate(results_details):
        r["is_visible"] = i < 3
    
    percentage = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
    
    # Update solved status if this is a submit action and all tests passed
    is_solved = False
    if action == "submit" and user_id and passed_tests == len(all_test_cases) and len(all_test_cases) > 0:
        db = SessionLocal()
        try:
            # Check if progress record exists
            progress_record = db.query(UserCodingProgress).filter(
                UserCodingProgress.user_id == user_id,
                UserCodingProgress.problem_id == problem_id
            ).first()
            
            if progress_record:
                # Update existing record
                progress_record.is_solved = True
                progress_record.attempts += 1
                progress_record.last_submission_code = code
                progress_record.last_submission_date = datetime.utcnow()
            else:
                # Create new record
                progress_record = UserCodingProgress(
                    user_id=user_id,
                    problem_id=problem_id,
                    is_solved=True,
                    attempts=1,
                    last_submission_code=code,
                    last_submission_date=datetime.utcnow()
                )
                db.add(progress_record)
            
            db.commit()
            is_solved = True
        except Exception as e:
            print(f"Error updating solved status: {e}")
            db.rollback()
        finally:
            db.close()
    elif action == "submit" and user_id:
        # Update attempts even if not solved
        db = SessionLocal()
        try:
            progress_record = db.query(UserCodingProgress).filter(
                UserCodingProgress.user_id == user_id,
                UserCodingProgress.problem_id == problem_id
            ).first()
            
            if progress_record:
                progress_record.attempts += 1
                progress_record.last_submission_code = code
                progress_record.last_submission_date = datetime.utcnow()
            else:
                progress_record = UserCodingProgress(
                    user_id=user_id,
                    problem_id=problem_id,
                    is_solved=False,
                    attempts=1,
                    last_submission_code=code,
                    last_submission_date=datetime.utcnow()
                )
                db.add(progress_record)
            
            db.commit()
        except Exception as e:
            print(f"Error updating attempts: {e}")
            db.rollback()
        finally:
            db.close()
    
    # Save to in-memory progress for backward compatibility
    progress_record_memory = {
        "id": str(uuid.uuid4()),
        "module": "coding",
        "problem_id": problem_id,
        "problem_title": problem.get("title", ""),
        "passed_tests": passed_tests,
        "total_tests": total_tests,
        "percentage": percentage,
        "timestamp": datetime.utcnow().isoformat(),
        "code_submitted": code,
        "user_id": user_id,
        "action": action
    }
    progress_data.append(progress_record_memory)
    
    from database import save_progress
    save_progress()
    
    # Generate feedback message
    if "error" in result and result["error"]:
        feedback = f"❌ Error: {result.get('error')}\n{result.get('message', '')}"
    elif action == "submit" and passed_tests == len(all_test_cases) and len(all_test_cases) > 0:
        feedback = f"✅ Accepted! All {len(all_test_cases)} test cases passed.\n🎉 Problem marked as solved!"
    elif action == "run" and passed_tests == total_tests and total_tests > 0:
        feedback = f"✅ Sample tests passed ({passed_tests}/{total_tests})!\n💡 Click 'Submit' to test against all {len(all_test_cases)} test cases."
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
        "total_all_tests": len(all_test_cases),
        "visible_count": visible_count,
        "hidden_count": hidden_count,
        "percentage": round(percentage, 2),
        "feedback": feedback,
        "results": results_details,
        "action": action,
        "is_solved": is_solved,
        "raw_output": result  # Debug info
    }


@router.get("/user-progress")
def get_user_progress(user_id: str = None):
    """
    Get user's coding progress including solved problems.
    Returns list of solved problem IDs.
    """
    if not user_id:
        return {"solved_problems": []}
    
    db = SessionLocal()
    try:
        # Get all solved problems for this user
        solved_records = db.query(UserCodingProgress).filter(
            UserCodingProgress.user_id == user_id,
            UserCodingProgress.is_solved == True
        ).all()
        
        solved_problem_ids = [record.problem_id for record in solved_records]
        
        # Also return detailed progress
        all_progress = db.query(UserCodingProgress).filter(
            UserCodingProgress.user_id == user_id
        ).all()
        
        progress_details = [record.to_dict() for record in all_progress]
        
        return {
            "solved_problems": solved_problem_ids,
            "total_solved": len(solved_problem_ids),
            "progress_details": progress_details
        }
    except Exception as e:
        print(f"Error fetching user progress: {e}")
        return {"solved_problems": [], "total_solved": 0, "progress_details": []}
    finally:
        db.close()


@router.get("/problems/{problem_id}/solution")
def get_solution(problem_id: str):
    # Check cache first
    if problem_id in problem_cache:
        return {"solution": problem_cache[problem_id].get("solution", "No solution available")}
    
    # Try database
    db = SessionLocal()
    try:
        db_problem = get_db_problem_by_id(db, problem_id)
        if db_problem and db_problem.solution:
            return {"solution": db_problem.solution}
    finally:
        db.close()
    
    return {"solution": "No solution available for this problem"}


# Bookmark endpoints
@router.post("/bookmarks")
def add_bookmark(payload: dict):
    """Add a problem to user's bookmarks"""
    from sqlalchemy import text
    
    user_id = payload.get("user_id")
    problem_id = payload.get("problem_id")
    
    if not user_id or not problem_id:
        raise HTTPException(status_code=400, detail="user_id and problem_id are required")
    
    db = SessionLocal()
    try:
        # Check if bookmark already exists
        result = db.execute(
            text("SELECT id FROM bookmarked_problems WHERE user_id = :user_id AND problem_id = :problem_id"),
            {"user_id": user_id, "problem_id": problem_id}
        )
        existing = result.fetchone()
        
        if existing:
            return {"message": "Already bookmarked", "bookmarked": True}
        
        # Add bookmark
        db.execute(
            text("INSERT INTO bookmarked_problems (user_id, problem_id) VALUES (:user_id, :problem_id)"),
            {"user_id": user_id, "problem_id": problem_id}
        )
        db.commit()
        
        return {"message": "Bookmark added successfully", "bookmarked": True}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error adding bookmark: {str(e)}")
    finally:
        db.close()


@router.delete("/bookmarks/{problem_id}")
def remove_bookmark(problem_id: str, user_id: str):
    """Remove a problem from user's bookmarks"""
    from sqlalchemy import text
    
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id is required")
    
    db = SessionLocal()
    try:
        result = db.execute(
            text("DELETE FROM bookmarked_problems WHERE user_id = :user_id AND problem_id = :problem_id"),
            {"user_id": user_id, "problem_id": problem_id}
        )
        db.commit()
        
        if result.rowcount == 0:
            return {"message": "Bookmark not found", "bookmarked": False}
        
        return {"message": "Bookmark removed successfully", "bookmarked": False}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error removing bookmark: {str(e)}")
    finally:
        db.close()


@router.get("/bookmarks")
def get_bookmarks(user_id: str):
    """Get all bookmarked problems for a user"""
    from sqlalchemy import text
    
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id is required")
    
    db = SessionLocal()
    try:
        result = db.execute(
            text("SELECT problem_id, created_at FROM bookmarked_problems WHERE user_id = :user_id ORDER BY created_at DESC"),
            {"user_id": user_id}
        )
        bookmarks = result.fetchall()
        
        bookmark_list = [
            {
                "problem_id": row[0],
                "bookmarked_at": row[1].isoformat() if row[1] else None
            }
            for row in bookmarks
        ]
        
        return {
            "bookmarks": bookmark_list,
            "total": len(bookmark_list)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching bookmarks: {str(e)}")
    finally:
        db.close()


@router.get("/progress/stats")
def get_progress_stats(user_id: str):
    """
    Get comprehensive progress statistics for a user.
    Simplified version that actually works.
    """
    from sqlalchemy import text
    from datetime import datetime, timedelta
    from collections import defaultdict
    
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id is required")
    
    db = SessionLocal()
    try:
        # If user_id is an email, convert it to UUID
        if '@' in user_id:
            from models.user_sql import User
            user = db.query(User).filter(User.email == user_id).first()
            if user:
                user_id = str(user.id)
            else:
                # Return empty stats for non-existent user
                from models.coding_problem_sql import CodingProblem
                total_in_db = db.query(CodingProblem).count()
                return {
                    "total_solved": 0,
                    "total_problems": total_in_db,
                    "completion_percentage": 0,
                    "current_streak": 0,
                    "max_streak": 0,
                    "solved_today": 0,
                    "category_stats": {},
                    "difficulty_stats": {"Easy": {"solved": 0, "total": 0}, "Medium": {"solved": 0, "total": 0}, "Hard": {"solved": 0, "total": 0}},
                    "recent_activity": [],
                    "recent_solved": []
                }
        
        # Get all problems from database
        from models.coding_problem_sql import CodingProblem
        db_problems = db.query(CodingProblem).all()
        total_problems = len(db_problems)
        
        # Convert to dict format for processing
        all_problems = []
        for p in db_problems:
            all_problems.append({
                "id": p.id,
                "title": p.title,
                "difficulty": p.difficulty,
                "tags": p.tags if isinstance(p.tags, list) else []
            })
        
        # Get solved problems for this user
        solved_query = text("SELECT problem_id, last_submission_date FROM user_coding_progress WHERE user_id = :user_id AND is_solved = true")
        solved_result = db.execute(solved_query, {"user_id": user_id})
        solved_rows = solved_result.fetchall()
        
        total_solved = len(solved_rows)
        
        # Simple stats
        completion_percentage = round((total_solved / total_problems * 100), 1) if total_problems > 0 else 0
        
        # Count by difficulty and category
        difficulty_stats = {
            "Easy": {"solved": 0, "total": 0},
            "Medium": {"solved": 0, "total": 0},
            "Hard": {"solved": 0, "total": 0}
        }
        category_stats = defaultdict(lambda: {"solved": 0, "total": 0})
        
        solved_ids = set(row[0] for row in solved_rows)
        
        for problem in all_problems:
            diff = problem.get("difficulty", "Medium")
            if diff in difficulty_stats:
                difficulty_stats[diff]["total"] += 1
                if problem.get("id") in solved_ids:
                    difficulty_stats[diff]["solved"] += 1
            
            for tag in problem.get("tags", []):
                category_stats[tag]["total"] += 1
                if problem.get("id") in solved_ids:
                    category_stats[tag]["solved"] += 1
        
        # Calculate streak (simplified)
        today = get_ist_now().date()
        dates_with_solves = set()
        for row in solved_rows:
            if row[1]:
                dates_with_solves.add(row[1].date())
        
        current_streak = 0
        # Start counting streak if we solved today or yesterday
        if today in dates_with_solves or (today - timedelta(days=1)) in dates_with_solves:
            check_date = today
            while check_date in dates_with_solves:
                current_streak += 1
                check_date = check_date - timedelta(days=1)
        
        max_streak = current_streak  # Simplified
        
        # Solved today - count of unique problems solved today
        solved_today = len([d for d in dates_with_solves if d == today])
        
        # Recent activity (last 30 days)
        thirty_days_ago = today - timedelta(days=30)
        activity_data = {}
        for row in solved_rows:
            if row[1] and row[1].date() >= thirty_days_ago:
                date_str = row[1].strftime('%Y-%m-%d')
                activity_data[date_str] = activity_data.get(date_str, 0) + 1
        
        # Recent solved (last 10)
        recent_solved = []
        sorted_rows = sorted(solved_rows, key=lambda x: x[1] if x[1] else datetime.min, reverse=True)[:10]
        for row in sorted_rows:
            problem = next((p for p in all_problems if p.get("id") == row[0]), None)
            if problem:
                recent_solved.append({
                    "problem_id": problem.get("id"),
                    "title": problem.get("title", "Unknown"),
                    "difficulty": problem.get("difficulty", "Medium"),
                    "tags": problem.get("tags", []),
                    "solved_at": row[1].isoformat() if row[1] else None
                })
        
        return {
            "total_solved": total_solved,
            "total_problems": total_problems,
            "completion_percentage": completion_percentage,
            "current_streak": current_streak,
            "max_streak": max_streak,
            "solved_today": solved_today,
            "category_stats": dict(category_stats),
            "difficulty_stats": difficulty_stats,
            "recent_activity": [{"date": date, "count": count} for date, count in sorted(activity_data.items())],
            "recent_solved": recent_solved
        }
    except Exception as e:
        import traceback
        error_detail = f"Error fetching progress stats: {str(e)}\n{traceback.format_exc()}"
        print(error_detail)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        db.close()
