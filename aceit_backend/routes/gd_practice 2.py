from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.gd_service import GDService

router = APIRouter()

class GDRequest(BaseModel):
    topic: str

@router.post("/generate")
async def generate_gd_points(request: GDRequest):
    """
    Generate For/Against points for a Group Discussion topic.
    Uses Groq or OpenAI (Stateless).
    """
    if not request.topic or len(request.topic.strip()) < 3:
        raise HTTPException(status_code=400, detail="Please enter a valid topic.")
        
    result = GDService.generate_points(request.topic)
    
    if result.get("error"):
        # We return 200 with error info so UI can display it nicely without crashing
        return {
            "status": "error",
            "message": result["message"]
        }
        
    return {
        "status": "success",
        "topic": request.topic,
        "for_points": result["for_points"],
        "against_points": result["against_points"]
    }
