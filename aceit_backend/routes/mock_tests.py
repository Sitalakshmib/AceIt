"""
Mock Test API Routes

Endpoints for generating, managing, and completing mock aptitude tests.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database_postgres import get_db
from models.mock_test_sql import MockTest, MockTestAttempt
from models.aptitude_sql import AptitudeQuestion
from services.mock_test_service import MockTestService

router = APIRouter()


@router.post("/generate")
async def generate_mock_test(payload: dict, db: Session = Depends(get_db)):
    """
    Generate a new mock test
    
    Payload:
        - test_type: "full_length", "section_wise", or "topic_wise"
        - category: (optional) for section_wise tests
        - topic: (optional) for topic_wise tests
    """
    test_type = payload.get("test_type", "full_length")
    category = payload.get("category")
    topic = payload.get("topic")
    
    try:
        if test_type == "full_length":
            test = MockTestService.generate_full_length_test(db)
        elif test_type == "section_wise":
            if not category:
                raise HTTPException(status_code=400, detail="Category required for section_wise test")
            test = MockTestService.generate_section_test(db, category)
        elif test_type == "topic_wise":
            if not category or not topic:
                raise HTTPException(status_code=400, detail="Category and topic required for topic_wise test")
            test = MockTestService.generate_topic_test(db, category, topic)
        else:
            raise HTTPException(status_code=400, detail="Invalid test type")
        
        return {
            "test_id": test.id,
            "test_type": test.test_type,
            "total_questions": test.total_questions,
            "duration_minutes": test.duration_minutes,
            "category": test.category,
            "topic": test.topic
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate test: {str(e)}")


@router.get("/{test_id}")
async def get_mock_test(test_id: str, db: Session = Depends(get_db)):
    """Get mock test details"""
    test = db.query(MockTest).filter(MockTest.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Mock test not found")
    
    return {
        "test_id": test.id,
        "test_type": test.test_type,
        "category": test.category,
        "topic": test.topic,
        "total_questions": test.total_questions,
        "duration_minutes": test.duration_minutes,
        "difficulty_distribution": test.difficulty_distribution,
        "created_at": test.created_at.isoformat() if test.created_at else None
    }


@router.post("/{test_id}/start")
async def start_mock_test(test_id: str, payload: dict, db: Session = Depends(get_db)):
    """
    Start a mock test attempt
    
    Payload:
        - user_id: User ID
    """
    user_id = payload.get("user_id")
    print(f"[MOCK_TEST] Starting test {test_id} for user {user_id}")
    
    if not user_id:
        print("[MOCK_TEST] ERROR: No user_id provided")
        raise HTTPException(status_code=400, detail="user_id required")
    
    try:
        print(f"[MOCK_TEST] Calling MockTestService.start_attempt...")
        attempt = MockTestService.start_attempt(db, user_id, test_id)
        print(f"[MOCK_TEST] Attempt created: {attempt.id}")
        
        # Get test details
        test = db.query(MockTest).filter(MockTest.id == test_id).first()
        print(f"[MOCK_TEST] Test found: {test.id if test else 'None'}")
        
        # Get questions in order
        questions = []
        for q_id in test.question_ids:
            question = db.query(AptitudeQuestion).filter(AptitudeQuestion.id == q_id).first()
            if question:
                questions.append({
                    "id": question.id,
                    "question": question.question,
                    "options": question.options,
                    "topic": question.topic,
                    "category": question.category,
                    "difficulty": question.difficulty
                })
        
        print(f"[MOCK_TEST] Returning {len(questions)} questions")
        return {
            "attempt_id": attempt.id,
            "test_id": test_id,
            "duration_minutes": test.duration_minutes,
            "total_questions": test.total_questions,
            "started_at": attempt.started_at.isoformat() if attempt.started_at else None,
            "questions": questions
        }
    except ValueError as e:
        print(f"[MOCK_TEST] ValueError: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print(f"[MOCK_TEST] Exception: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to start test: {str(e)}")


@router.post("/{test_id}/submit-answer")
async def submit_mock_answer(test_id: str, payload: dict, db: Session = Depends(get_db)):
    """
    Submit answer during mock test
    
    Payload:
        - attempt_id: Attempt ID
        - question_id: Question ID
        - user_answer: Selected answer index
        - time_spent: Time spent on question in seconds
    """
    attempt_id = payload.get("attempt_id")
    question_id = payload.get("question_id")
    user_answer = payload.get("user_answer")
    time_spent = payload.get("time_spent", 0)
    
    if not all([attempt_id, question_id is not None, user_answer is not None]):
        raise HTTPException(status_code=400, detail="attempt_id, question_id, and user_answer required")
    
    try:
        MockTestService.submit_answer(db, attempt_id, question_id, user_answer, time_spent)
        return {"status": "recorded"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit answer: {str(e)}")


@router.post("/{test_id}/complete")
async def complete_mock_test(test_id: str, payload: dict, db: Session = Depends(get_db)):
    """
    Complete and score mock test
    
    Payload:
        - attempt_id: Attempt ID
    """
    attempt_id = payload.get("attempt_id")
    if not attempt_id:
        raise HTTPException(status_code=400, detail="attempt_id required")
    
    try:
        results = MockTestService.complete_attempt(db, attempt_id)
        return results
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to complete test: {str(e)}")


@router.get("/{test_id}/results/{attempt_id}")
async def get_test_results(test_id: str, attempt_id: str, db: Session = Depends(get_db)):
    """Get detailed results for a completed mock test"""
    try:
        results = MockTestService.get_test_results(db, attempt_id)
        return results
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get results: {str(e)}")


@router.get("/user/{user_id}/attempts")
async def get_user_attempts(user_id: str, db: Session = Depends(get_db)):
    """Get all mock test attempts for a user"""
    attempts = db.query(MockTestAttempt)\
        .filter(MockTestAttempt.user_id == user_id)\
        .order_by(MockTestAttempt.started_at.desc()).all()
    
    return {
        "user_id": user_id,
        "total_attempts": len(attempts),
        "attempts": [
            {
                "attempt_id": a.id,
                "test_id": a.mock_test_id,
                "status": a.status,
                "score": a.score,
                "total_questions": a.total_questions,
                "accuracy": round(a.accuracy_percentage, 2),
                "time_taken": a.time_taken_seconds,
                "started_at": a.started_at.isoformat() if a.started_at else None,
                "completed_at": a.completed_at.isoformat() if a.completed_at else None
            }
            for a in attempts
        ]
    }
