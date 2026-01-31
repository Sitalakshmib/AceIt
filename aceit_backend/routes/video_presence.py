"""
Video Presence Interview Routes

SCOPE: Video Presence Interview ONLY (Body Language & Presence Practice)
PURPOSE: Handle audio analysis requests for hesitation detection

IMPORTANT:
- This is SEPARATE from HR/Technical/Topic interviews
- Analyzes ONLY student microphone audio
- Does NOT store audio files permanently
- Provides practice-oriented feedback only

Author: AceIt Backend Team
"""

from fastapi import APIRouter, HTTPException, File, UploadFile, Form
from typing import Optional
import shutil
import os
import uuid
from services.video_analysis_service import analyze_audio_hesitation

router = APIRouter()

# Temporary directory for audio processing
TEMP_AUDIO_DIR = "temp_audio"
os.makedirs(TEMP_AUDIO_DIR, exist_ok=True)


@router.post("/analyze-answer")
async def analyze_video_presence_answer(
    audio_file: UploadFile = File(...),
    session_id: Optional[str] = Form(None)
):
    """
    Analyze student audio for hesitation patterns
    
    This endpoint:
    1. Receives student microphone audio ONLY (no interviewer TTS)
    2. Performs real hesitation analysis (filler words, pauses, continuity)
    3. Returns practice-oriented feedback
    4. Deletes temporary audio file immediately
    
    Args:
        audio_file: Student's audio recording (microphone only)
        session_id: Optional session identifier for tracking
    
    Returns:
        JSON with hesitation analysis results or error status
    """
    temp_file_path = None
    
    try:
        # Validate file
        if not audio_file:
            raise HTTPException(status_code=400, detail="No audio file provided")
        
        # Generate unique filename to avoid collisions
        file_extension = os.path.splitext(audio_file.filename)[1] or ".webm"
        unique_filename = f"{session_id or uuid.uuid4()}_{uuid.uuid4()}{file_extension}"
        temp_file_path = os.path.join(TEMP_AUDIO_DIR, unique_filename)
        
        # Save uploaded file temporarily
        print(f"[AUDIO] Receiving audio file: {audio_file.filename}")
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(audio_file.file, buffer)
        
        print(f"[AUDIO] Saved to: {temp_file_path}")
        
        # Perform hesitation analysis
        print(f"[AUDIO] Analyzing audio for hesitation patterns...")
        analysis_result = analyze_audio_hesitation(temp_file_path)
        
        # Check analysis status
        if analysis_result["status"] == "error":
            print(f"[ERROR] Analysis failed: {analysis_result.get('message')}")
            return {
                "status": "unavailable",
                "message": "Audio analysis unavailable. Please try again.",
                "hesitation_analysis": None
            }
        
        if analysis_result["status"] == "no_speech":
            print(f"[WARNING] No speech detected in audio")
            return {
                "status": "no_speech",
                "message": "No speech detected. Please check your microphone.",
                "hesitation_analysis": None
            }
        
        # Success - return analysis
        print(f"[SUCCESS] Analysis complete")
        return {
            "status": "success",
            "message": "Audio analysis completed successfully",
            "hesitation_analysis": analysis_result["hesitation_analysis"],
            "transcript": analysis_result.get("transcript", "")  # Optional: for debugging
        }
        
    except Exception as e:
        print(f"[ERROR] Error in analyze_video_presence_answer: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Audio analysis failed: {str(e)}"
        )
    
    finally:
        # CRITICAL: Always delete temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
                print(f"[CLEANUP] Deleted temporary file: {temp_file_path}")
            except Exception as cleanup_error:
                print(f"[WARNING] Failed to delete temp file: {cleanup_error}")


@router.get("/health")
async def health_check():
    """
    Health check endpoint for video presence analysis service
    """
    return {
        "status": "healthy",
        "service": "video_presence_analysis",
        "message": "Video Presence Interview analysis service is running"
    }
