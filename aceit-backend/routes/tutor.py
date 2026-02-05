"""
AI Tutor Routes for AceIt Coding Module
API endpoints for AI-powered tutoring features
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import ai_service

router = APIRouter()


# Request/Response Models
class HintRequest(BaseModel):
    problem_title: str
    problem_description: str
    user_code: Optional[str] = ""
    hint_level: int = 1  # 1-3
    tags: Optional[List[str]] = []


class DebugRequest(BaseModel):
    problem_title: str
    problem_description: str
    user_code: str
    test_input: str
    expected_output: str
    actual_output: str
    error_message: Optional[str] = None


class ReviewRequest(BaseModel):
    problem_title: str
    problem_description: str
    user_code: str
    passed_all_tests: bool = False
    tags: Optional[List[str]] = []


class ExplainRequest(BaseModel):
    problem_title: str
    problem_description: str
    optimal_solution: Optional[str] = None
    tags: Optional[List[str]] = []


class ChatRequest(BaseModel):
    message: str
    problem_context: Optional[Dict[str, Any]] = None
    conversation_history: Optional[List[Dict[str, str]]] = []


class TutorResponse(BaseModel):
    success: bool
    response: str
    type: str


# API Endpoints
@router.post("/hint", response_model=TutorResponse)
async def get_hint(request: HintRequest):
    """Get a progressive hint for the current problem"""
    try:
        # Validate hint level
        hint_level = max(1, min(3, request.hint_level))
        
        response = ai_service.get_hint(
            problem_title=request.problem_title,
            problem_description=request.problem_description,
            user_code=request.user_code,
            hint_level=hint_level,
            tags=request.tags
        )
        
        return TutorResponse(
            success=True,
            response=response,
            type="hint"
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")


@router.post("/debug", response_model=TutorResponse)
async def debug_code(request: DebugRequest):
    """Analyze why code failed a test case"""
    try:
        response = ai_service.debug_code(
            problem_title=request.problem_title,
            problem_description=request.problem_description,
            user_code=request.user_code,
            test_input=request.test_input,
            expected_output=request.expected_output,
            actual_output=request.actual_output,
            error_message=request.error_message
        )
        
        return TutorResponse(
            success=True,
            response=response,
            type="debug"
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")


@router.post("/review", response_model=TutorResponse)
async def review_code(request: ReviewRequest):
    """Review submitted code for improvements"""
    try:
        response = ai_service.review_code(
            problem_title=request.problem_title,
            problem_description=request.problem_description,
            user_code=request.user_code,
            passed_all_tests=request.passed_all_tests,
            tags=request.tags
        )
        
        return TutorResponse(
            success=True,
            response=response,
            type="review"
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")


@router.post("/explain", response_model=TutorResponse)
async def explain_solution(request: ExplainRequest):
    """Explain the optimal solution approach"""
    try:
        response = ai_service.explain_solution(
            problem_title=request.problem_title,
            problem_description=request.problem_description,
            optimal_solution=request.optimal_solution,
            tags=request.tags
        )
        
        return TutorResponse(
            success=True,
            response=response,
            type="explain"
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")


@router.post("/chat", response_model=TutorResponse)
async def chat(request: ChatRequest):
    """General Q&A about algorithms and concepts"""
    try:
        response = ai_service.chat(
            user_message=request.message,
            problem_context=request.problem_context,
            conversation_history=request.conversation_history
        )
        
        return TutorResponse(
            success=True,
            response=response,
            type="chat"
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")


@router.get("/status")
async def get_status():
    """Check if AI tutor service is available"""
    import os
    has_key = bool(os.getenv("GEMINI_API_KEY_HELL"))
    return {
        "available": has_key,
        "message": "AI Tutor is ready!" if has_key else "GEMINI_API_KEY_HELL not configured"
    }
