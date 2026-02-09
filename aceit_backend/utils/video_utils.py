"""
Video Processing Utilities for Video Presence Interview

SCOPE: Video Presence Interview ONLY
PURPOSE: Helper functions for video frame extraction and processing

IMPORTANT:
- Process video in-memory when possible
- Clean up temporary files immediately
- No permanent video storage
- Privacy-first design

Author: AceIt Backend Team
"""

import cv2
import os
import tempfile
import numpy as np
from typing import List, Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


def extract_frames_from_video(
    video_path: str, 
    fps: int = 5,
    max_frames: int = 150
) -> List[np.ndarray]:
    """
    Extract frames from video at specified FPS
    
    Args:
        video_path: Path to video file
        fps: Frames per second to extract (default: 5)
        max_frames: Maximum number of frames to extract (default: 150 = 30 seconds at 5fps)
    
    Returns:
        List of numpy arrays (frames in BGR format)
    
    Raises:
        ValueError: If video file is invalid or cannot be read
    """
    if not os.path.exists(video_path):
        raise ValueError(f"Video file not found: {video_path}")
    
    try:
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            raise ValueError(f"Cannot open video file: {video_path}")
        
        # Get video properties
        video_fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        if video_fps == 0:
            logger.warning(f"Could not determine video FPS, using default 30")
            video_fps = 30
        
        # Calculate frame interval
        frame_interval = max(1, int(video_fps / fps))
        
        frames = []
        frame_count = 0
        extracted_count = 0
        
        logger.info(f"[VIDEO] Extracting frames: video_fps={video_fps}, target_fps={fps}, interval={frame_interval}")
        
        while True:
            ret, frame = cap.read()
            
            if not ret:
                break
            
            # Extract frame at intervals
            if frame_count % frame_interval == 0:
                frames.append(frame)
                extracted_count += 1
                
                # Stop if we've reached max frames
                if extracted_count >= max_frames:
                    logger.info(f"[VIDEO] Reached max frames limit: {max_frames}")
                    break
            
            frame_count += 1
        
        cap.release()
        
        logger.info(f"[VIDEO] Extracted {len(frames)} frames from {total_frames} total frames")
        
        if len(frames) == 0:
            raise ValueError("No frames could be extracted from video")
        
        return frames
        
    except Exception as e:
        logger.error(f"[ERROR] Failed to extract frames: {e}")
        raise ValueError(f"Video processing failed: {str(e)}")


def validate_video_file(video_path: str) -> Tuple[bool, str]:
    """
    Validate video file format and readability
    
    Args:
        video_path: Path to video file
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not os.path.exists(video_path):
        return False, "Video file not found"
    
    # Check file size (must be > 0 and < 100MB)
    file_size = os.path.getsize(video_path)
    if file_size == 0:
        return False, "Video file is empty"
    
    if file_size > 100 * 1024 * 1024:  # 100MB
        return False, "Video file too large (max 100MB)"
    
    # Try to open with OpenCV
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return False, "Cannot open video file (invalid format)"
        
        # Try to read first frame
        ret, frame = cap.read()
        cap.release()
        
        if not ret or frame is None:
            return False, "Cannot read video frames"
        
        return True, "Valid video file"
        
    except Exception as e:
        return False, f"Video validation error: {str(e)}"


def cleanup_temp_video(video_path: str) -> bool:
    """
    Delete temporary video file
    
    Args:
        video_path: Path to temporary video file
    
    Returns:
        True if deleted successfully, False otherwise
    """
    try:
        if os.path.exists(video_path):
            os.remove(video_path)
            logger.info(f"[CLEANUP] Deleted temporary video: {video_path}")
            return True
        return False
    except Exception as e:
        logger.error(f"[ERROR] Failed to delete temp video: {e}")
        return False


def get_video_duration(video_path: str) -> float:
    """
    Get video duration in seconds
    
    Args:
        video_path: Path to video file
    
    Returns:
        Duration in seconds
    """
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return 0.0
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()
        
        if fps > 0:
            return frame_count / fps
        return 0.0
        
    except Exception as e:
        logger.error(f"[ERROR] Failed to get video duration: {e}")
        return 0.0


def resize_frame(frame: np.ndarray, max_width: int = 640) -> np.ndarray:
    """
    Resize frame while maintaining aspect ratio
    
    Args:
        frame: Input frame (numpy array)
        max_width: Maximum width in pixels
    
    Returns:
        Resized frame
    """
    height, width = frame.shape[:2]
    
    if width <= max_width:
        return frame
    
    # Calculate new dimensions
    ratio = max_width / width
    new_width = max_width
    new_height = int(height * ratio)
    
    resized = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)
    return resized
