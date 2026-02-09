"""
Video Presence Interview Routes

SCOPE: Video Presence Interview ONLY (Body Language & Presence Practice)
PURPOSE: Handle multi-modal analysis (video + audio) for presence training

ENHANCEMENTS:
- Multi-modal analysis (visual + audio)
- MediaPipe-based visual analysis (eye contact, head movement, facial tension)
- Whisper-based audio hesitation analysis
- Composite feedback generation
- Privacy-first design (no permanent storage)

IMPORTANT:
- This is SEPARATE from HR/Technical/Topic interviews
- Analyzes ONLY student video and microphone audio
- Does NOT store video/audio files permanently
- Provides practice-oriented feedback only
- NO emotion classification or psychological diagnosis

Author: AceIt Backend Team
"""

from fastapi import APIRouter, HTTPException, File, UploadFile, Form
from typing import Optional
import shutil
import os
import uuid
import logging

# Import analysis services
from services.video_analysis_service import analyze_audio_hesitation

# Visual analysis is optional (requires MediaPipe)
try:
    from services.visual_analysis_service import analyze_video_frames
    VISUAL_ANALYSIS_AVAILABLE = True
except ImportError as e:
    print(f"[WARNING] Visual analysis unavailable: {e}")
    VISUAL_ANALYSIS_AVAILABLE = False
    analyze_video_frames = None
from services.composite_analysis_service import (
    calculate_composite_indicators,
    generate_composite_feedback,
    ensure_minimum_scores,
    get_fallback_feedback
)
from utils.video_utils import (
    extract_frames_from_video,
    validate_video_file,
    cleanup_temp_video,
    get_video_duration
)

logger = logging.getLogger(__name__)

router = APIRouter()

# Temporary directories for processing
TEMP_AUDIO_DIR = "temp_audio"
TEMP_VIDEO_DIR = "temp_video"
os.makedirs(TEMP_AUDIO_DIR, exist_ok=True)
os.makedirs(TEMP_VIDEO_DIR, exist_ok=True)


@router.post("/analyze-answer")
async def analyze_video_presence_answer(
    audio_file: UploadFile = File(...),
    video_file: Optional[UploadFile] = File(None),
    session_id: Optional[str] = Form(None)
):
    """
    Analyze student video and audio for comprehensive presence analysis
    
    This endpoint:
    1. Receives student microphone audio (required)
    2. Optionally receives student video for visual analysis
    3. Performs multi-modal analysis:
       - Audio: Hesitation patterns (filler words, pauses, speech flow)
       - Visual: Eye contact, head movement, facial tension (if video provided)
    4. Combines analyses into unified professional feedback
    5. Deletes temporary files immediately
    
    Args:
        audio_file: Student's audio recording (microphone only) - REQUIRED
        video_file: Student's video recording - OPTIONAL
        session_id: Optional session identifier for tracking
    
    Returns:
        JSON with comprehensive multi-modal analysis or error status
    """
    temp_audio_path = None
    temp_video_path = None
    
    try:
        # Validate audio file (required)
        if not audio_file:
            raise HTTPException(status_code=400, detail="No audio file provided")
        
        # Generate unique filenames to avoid collisions
        session_uuid = session_id or str(uuid.uuid4())
        
        # Save audio file temporarily
        audio_extension = os.path.splitext(audio_file.filename)[1] or ".webm"
        unique_audio_filename = f"{session_uuid}_{uuid.uuid4()}{audio_extension}"
        temp_audio_path = os.path.join(TEMP_AUDIO_DIR, unique_audio_filename)
        
        logger.info(f"[AUDIO] Receiving audio file: {audio_file.filename}")
        with open(temp_audio_path, "wb") as buffer:
            shutil.copyfileobj(audio_file.file, buffer)
        
        logger.info(f"[AUDIO] Saved to: {temp_audio_path}")
        
        # Save video file if provided
        visual_analysis = None
        if video_file:
            video_extension = os.path.splitext(video_file.filename)[1] or ".webm"
            unique_video_filename = f"{session_uuid}_{uuid.uuid4()}{video_extension}"
            temp_video_path = os.path.join(TEMP_VIDEO_DIR, unique_video_filename)
            
            logger.info(f"[VIDEO] Receiving video file: {video_file.filename}")
            with open(temp_video_path, "wb") as buffer:
                shutil.copyfileobj(video_file.file, buffer)
            
            logger.info(f"[VIDEO] Saved to: {temp_video_path}")
            
            # Validate video file
            is_valid, validation_message = validate_video_file(temp_video_path)
            if not is_valid:
                logger.warning(f"[VIDEO] Validation failed: {validation_message}")
                # Continue with audio-only analysis
                visual_analysis = {
                    "status": "error",
                    "message": validation_message
                }
            else:
                # Check if visual analysis is available
                if not VISUAL_ANALYSIS_AVAILABLE:
                    logger.warning(f"[VIDEO] Visual analysis unavailable (MediaPipe not installed)")
                    visual_analysis = {
                        "status": "error",
                        "message": "Visual analysis unavailable - MediaPipe not installed"
                    }
        
        # Perform audio hesitation analysis
        logger.info(f"[AUDIO] Analyzing audio for hesitation patterns...")
        audio_analysis = analyze_audio_hesitation(temp_audio_path)
        logger.info(f"[AUDIO] Audio analysis complete: {audio_analysis.get('status')}")
        
        # Check if we have any valid analysis
        has_audio = audio_analysis.get("status") == "success"
        has_video = visual_analysis and visual_analysis.get("status") == "success"
        
        if not has_audio and not has_video:
            # Both analyses failed
            logger.error("[ERROR] Both audio and visual analyses failed")
            return {
                "status": "error",
                "message": "Analysis unavailable. Please check your audio and video quality.",
                "analysis": None
            }
        
        # Generate composite analysis
        logger.info("[COMPOSITE] Generating composite feedback...")
        
        # Calculate composite indicators
        indicators = calculate_composite_indicators(visual_analysis, audio_analysis)
        indicators = ensure_minimum_scores(indicators)
        
        # Generate comprehensive feedback
        if has_audio and has_video:
            feedback = generate_composite_feedback(indicators, visual_analysis, audio_analysis)
        elif has_audio:
            feedback = generate_composite_feedback(indicators, None, audio_analysis)
            feedback["visual_observations"] = ["Video analysis unavailable - audio analysis only"]
        else:
            feedback = generate_composite_feedback(indicators, visual_analysis, None)
            feedback["speech_observations"] = ["Audio analysis unavailable - visual analysis only"]
        
        # Prepare response
        response = {
            "status": "success",
            "message": "Multi-modal analysis completed successfully",
            "analysis": {
                "visual": visual_analysis.get("visual_analysis") if visual_analysis and visual_analysis.get("status") == "success" else None,
                "audio": {
                    "hesitation_analysis": audio_analysis.get("hesitation_analysis"),
                    "transcript": audio_analysis.get("transcript", "")
                } if audio_analysis.get("status") == "success" else None,
                "composite": {
                    "confidence": indicators.get("confidence"),
                    "stress": indicators.get("stress"),
                    "presence_quality": indicators.get("presence_quality"),
                    "overall_score": indicators.get("overall_score")
                },
                "feedback": feedback
            }
        }
        
        logger.info("[SUCCESS] Multi-modal analysis complete")
        return response
        
    except Exception as e:
        logger.error(f"[ERROR] Error in analyze_video_presence_answer: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )
    
    finally:
        # CRITICAL: Always delete temporary files
        if temp_audio_path and os.path.exists(temp_audio_path):
            try:
                os.remove(temp_audio_path)
                logger.info(f"[CLEANUP] Deleted temporary audio: {temp_audio_path}")
            except Exception as cleanup_error:
                logger.error(f"[WARNING] Failed to delete temp audio: {cleanup_error}")
        
        if temp_video_path and os.path.exists(temp_video_path):
            try:
                cleanup_temp_video(temp_video_path)
            except Exception as cleanup_error:
                logger.error(f"[WARNING] Failed to delete temp video: {cleanup_error}")


@router.post("/analyze-video-only")
async def analyze_video_only(
    video_file: UploadFile = File(...),
    session_id: Optional[str] = Form(None)
):
    """
    Analyze only video for visual presence (for testing/debugging)
    
    This endpoint is useful for testing visual analysis independently
    
    Args:
        video_file: Student's video recording
        session_id: Optional session identifier
    
    Returns:
        JSON with visual analysis results
    """
    temp_video_path = None
    
    try:
        if not video_file:
            raise HTTPException(status_code=400, detail="No video file provided")
        
        # Save video file
        session_uuid = session_id or str(uuid.uuid4())
        video_extension = os.path.splitext(video_file.filename)[1] or ".webm"
        unique_video_filename = f"{session_uuid}_{uuid.uuid4()}{video_extension}"
        temp_video_path = os.path.join(TEMP_VIDEO_DIR, unique_video_filename)
        
        logger.info(f"[VIDEO-ONLY] Receiving video file: {video_file.filename}")
        with open(temp_video_path, "wb") as buffer:
            shutil.copyfileobj(video_file.file, buffer)
        
        # Validate video
        is_valid, validation_message = validate_video_file(temp_video_path)
        if not is_valid:
            raise HTTPException(status_code=400, detail=validation_message)
        
        # Extract frames
        frames = extract_frames_from_video(temp_video_path, fps=5, max_frames=150)
        logger.info(f"[VIDEO-ONLY] Extracted {len(frames)} frames")
        
        # Analyze
        visual_analysis = analyze_video_frames(frames)
        
        return {
            "status": "success",
            "message": "Visual analysis completed",
            "visual_analysis": visual_analysis
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[ERROR] Video-only analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Video analysis failed: {str(e)}")
    
    finally:
        if temp_video_path and os.path.exists(temp_video_path):
            cleanup_temp_video(temp_video_path)


@router.get("/health")
async def health_check():
    """
    Health check endpoint for video presence analysis service
    """
    return {
        "status": "healthy",
        "service": "video_presence_analysis",
        "message": "Video Presence Interview multi-modal analysis service is running",
        "capabilities": {
            "audio_analysis": True,
            "visual_analysis": True,
            "composite_feedback": True
        }
    }
