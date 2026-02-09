"""
Visual Analysis Service for Video Presence Interview

SCOPE: Video Presence Interview ONLY
PURPOSE: Professional visual analysis using MediaPipe (Eye Contact, Head Movement, Facial Tension)

ARCHITECTURE:
- Uses MediaPipe Face Mesh for facial landmark detection
- Uses MediaPipe Pose for head/body movement tracking
- Implements FACS-style observable signal extraction
- Provides temporal trend analysis
- Generates qualitative, practice-oriented feedback

IMPORTANT RULES:
- NO emotion classification or psychological diagnosis
- Observable signals only (facial landmarks, movement patterns)
- Qualitative descriptors (Low/Moderate/Good)
- Never store raw video data
- Process in-memory only

Author: AceIt Backend Team
"""

import mediapipe as mp
import cv2
import numpy as np
from typing import List, Dict, Optional, Tuple
import statistics
import logging

logger = logging.getLogger(__name__)

# Global MediaPipe model cache
_FACE_LANDMARKER = None
_POSE_LANDMARKER = None

# MediaPipe solutions - check if solutions API is available
# Note: MediaPipe 0.10.32+ uses the new 'tasks' API instead of 'solutions'
# This service requires the legacy 'solutions' API

# Raise ImportError immediately if solutions API is not available
# This prevents the module from loading and allows graceful fallback
if not hasattr(mp, 'solutions'):
    raise ImportError(
        "MediaPipe 'solutions' API not available. "
        "This version of MediaPipe uses the new 'tasks' API. "
        "Visual analysis is disabled. "
        "To enable, the code needs to be updated to use the new MediaPipe tasks API."
    )

# Only reached if solutions API exists
mp_face_mesh = mp.solutions.face_mesh
mp_pose = mp.solutions.pose


def load_mediapipe_models():
    """
    Load MediaPipe models (lazy loading, cached globally)
    """
    global _FACE_LANDMARKER, _POSE_LANDMARKER
    
    if _FACE_LANDMARKER is None:
        logger.info("[MEDIAPIPE] Loading Face Mesh model...")
        try:
            _FACE_LANDMARKER = mp_face_mesh.FaceMesh(
                static_image_mode=False,
                max_num_faces=1,
                refine_landmarks=True,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5
            )
            logger.info("[MEDIAPIPE] Face Mesh model loaded successfully")
        except Exception as e:
            logger.error(f"[ERROR] Failed to load Face Mesh model: {e}")
            raise RuntimeError("Could not load MediaPipe Face Mesh model")
    
    if _POSE_LANDMARKER is None:
        logger.info("[MEDIAPIPE] Loading Pose model...")
        try:
            _POSE_LANDMARKER = mp_pose.Pose(
                static_image_mode=False,
                model_complexity=1,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5
            )
            logger.info("[MEDIAPIPE] Pose model loaded successfully")
        except Exception as e:
            logger.error(f"[ERROR] Failed to load Pose model: {e}")
            raise RuntimeError("Could not load MediaPipe Pose model")
    
    return _FACE_LANDMARKER, _POSE_LANDMARKER


def analyze_video_frames(frames: List[np.ndarray]) -> Dict:
    """
    Main function: Analyze video frames for visual presence indicators
    
    Args:
        frames: List of video frames (BGR format from OpenCV)
    
    Returns:
        Dictionary containing comprehensive visual analysis
    """
    try:
        if not frames or len(frames) == 0:
            return {
                "status": "error",
                "message": "No frames provided for analysis",
                "visual_analysis": None
            }
        
        # Load MediaPipe models
        face_mesh, pose = load_mediapipe_models()
        
        logger.info(f"[VISUAL] Analyzing {len(frames)} frames...")
        
        # Process all frames and extract features
        frames_data = []
        
        for idx, frame in enumerate(frames):
            # Convert BGR to RGB for MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process with Face Mesh
            face_results = face_mesh.process(rgb_frame)
            
            # Process with Pose
            pose_results = pose.process(rgb_frame)
            
            frame_data = {
                "frame_index": idx,
                "has_face": face_results.multi_face_landmarks is not None,
                "has_pose": pose_results.pose_landmarks is not None,
                "face_landmarks": face_results.multi_face_landmarks[0] if face_results.multi_face_landmarks else None,
                "pose_landmarks": pose_results.pose_landmarks,
                "timestamp": idx / 5.0  # Assuming 5 FPS
            }
            
            frames_data.append(frame_data)
        
        # Filter out frames without face detection
        valid_frames = [f for f in frames_data if f["has_face"]]
        
        if len(valid_frames) < 5:
            return {
                "status": "insufficient_data",
                "message": "Insufficient face detection. Please ensure your face is visible.",
                "visual_analysis": None
            }
        
        logger.info(f"[VISUAL] Valid frames with face detection: {len(valid_frames)}/{len(frames_data)}")
        
        # Perform analyses
        eye_contact_analysis = analyze_eye_contact(valid_frames)
        head_movement_analysis = analyze_head_movement(valid_frames)
        facial_tension_analysis = analyze_facial_tension(valid_frames)
        temporal_analysis = analyze_temporal_trends(
            valid_frames,
            eye_contact_analysis,
            head_movement_analysis,
            facial_tension_analysis
        )
        
        # Generate feedback
        visual_feedback = generate_visual_feedback(
            eye_contact_analysis,
            head_movement_analysis,
            facial_tension_analysis,
            temporal_analysis
        )
        
        return {
            "status": "success",
            "total_frames": len(frames_data),
            "valid_frames": len(valid_frames),
            "visual_analysis": {
                "eye_contact": eye_contact_analysis,
                "head_movement": head_movement_analysis,
                "facial_tension": facial_tension_analysis,
                "temporal_trends": temporal_analysis,
                "feedback": visual_feedback
            }
        }
        
    except Exception as e:
        logger.error(f"[ERROR] Visual analysis failed: {e}")
        return {
            "status": "error",
            "message": "Visual analysis unavailable",
            "error": str(e)
        }


def analyze_eye_contact(frames_data: List[Dict]) -> Dict:
    """
    Analyze eye contact and face orientation
    
    Measures:
    - % time facing camera
    - Frequency of gaze shifts
    - Consistency over time
    
    Returns:
        Dictionary with eye contact metrics and qualitative assessment
    """
    if not frames_data:
        return {"status": "no_data"}
    
    facing_camera_count = 0
    gaze_shifts = 0
    previous_facing = None
    
    face_orientations = []
    
    for frame in frames_data:
        landmarks = frame.get("face_landmarks")
        if not landmarks:
            continue
        
        # Get key landmarks for face orientation
        # Nose tip (1), Left cheek (234), Right cheek (454)
        nose_tip = landmarks.landmark[1]
        left_cheek = landmarks.landmark[234]
        right_cheek = landmarks.landmark[454]
        
        # Calculate face center
        face_center_x = (left_cheek.x + right_cheek.x) / 2
        
        # Check if facing camera (nose close to center)
        deviation = abs(nose_tip.x - face_center_x)
        is_facing = deviation < 0.04  # Threshold for "facing camera"
        
        face_orientations.append(deviation)
        
        if is_facing:
            facing_camera_count += 1
        
        # Detect gaze shifts
        if previous_facing is not None and previous_facing != is_facing:
            gaze_shifts += 1
        
        previous_facing = is_facing
    
    total_frames = len(frames_data)
    facing_percentage = (facing_camera_count / total_frames * 100) if total_frames > 0 else 0
    
    # Calculate consistency (lower standard deviation = more consistent)
    consistency_score = 100 - (statistics.stdev(face_orientations) * 1000) if len(face_orientations) > 1 else 50
    consistency_score = max(0, min(100, consistency_score))
    
    # Qualitative assessment
    if facing_percentage >= 75:
        quality = "Strong"
        observation = "Maintained consistent eye contact with camera"
    elif facing_percentage >= 50:
        quality = "Good"
        observation = "Generally maintained eye contact with occasional shifts"
    else:
        quality = "Needs Improvement"
        observation = "Frequent gaze shifts away from camera observed"
    
    return {
        "facing_camera_percentage": round(facing_percentage, 2),
        "gaze_shifts": gaze_shifts,
        "consistency_score": round(consistency_score, 2),
        "quality": quality,
        "observation": observation
    }


def analyze_head_movement(frames_data: List[Dict]) -> Dict:
    """
    Analyze head movement patterns
    
    Detects:
    - Excessive nodding
    - Side-to-side jitter
    - Sudden posture shifts
    - Differentiates natural emphasis from nervous movement
    
    Returns:
        Dictionary with head movement metrics and assessment
    """
    if not frames_data or len(frames_data) < 10:
        return {"status": "insufficient_data"}
    
    nose_positions = []
    vertical_movements = []
    horizontal_movements = []
    
    for frame in frames_data:
        landmarks = frame.get("face_landmarks")
        if landmarks:
            nose_tip = landmarks.landmark[1]
            nose_positions.append((nose_tip.x, nose_tip.y, nose_tip.z))
    
    if len(nose_positions) < 10:
        return {"status": "insufficient_data"}
    
    # Calculate movement between consecutive frames
    for i in range(1, len(nose_positions)):
        prev = nose_positions[i-1]
        curr = nose_positions[i]
        
        horizontal_movement = abs(curr[0] - prev[0])
        vertical_movement = abs(curr[1] - prev[1])
        
        horizontal_movements.append(horizontal_movement)
        vertical_movements.append(vertical_movement)
    
    # Calculate metrics
    avg_horizontal = statistics.mean(horizontal_movements) if horizontal_movements else 0
    avg_vertical = statistics.mean(vertical_movements) if vertical_movements else 0
    
    max_horizontal = max(horizontal_movements) if horizontal_movements else 0
    max_vertical = max(vertical_movements) if vertical_movements else 0
    
    # Detect patterns
    # Nodding: primarily vertical movement
    nodding_frames = sum(1 for v in vertical_movements if v > 0.02)
    # Jitter: frequent small horizontal movements
    jitter_frames = sum(1 for h in horizontal_movements if 0.01 < h < 0.03)
    # Sudden shifts: large movements
    sudden_shifts = sum(1 for h, v in zip(horizontal_movements, vertical_movements) 
                       if h > 0.05 or v > 0.05)
    
    total_movement_frames = len(horizontal_movements)
    
    # Calculate stability score (inverse of movement)
    movement_intensity = (avg_horizontal + avg_vertical) * 100
    stability_score = max(0, 100 - movement_intensity * 50)
    
    # Qualitative assessment
    if stability_score >= 75:
        quality = "Steady"
        observation = "Head position remained stable and composed"
    elif stability_score >= 50:
        quality = "Moderate"
        if nodding_frames > total_movement_frames * 0.3:
            observation = "Natural nodding detected, generally stable"
        else:
            observation = "Some head movement detected, mostly controlled"
    else:
        quality = "Needs Improvement"
        if jitter_frames > total_movement_frames * 0.4:
            observation = "Frequent small movements (fidgeting) detected"
        elif sudden_shifts > 5:
            observation = "Several sudden posture shifts observed"
        else:
            observation = "Noticeable head movement throughout response"
    
    return {
        "stability_score": round(stability_score, 2),
        "average_movement": round((avg_horizontal + avg_vertical) * 100, 2),
        "nodding_detected": nodding_frames > total_movement_frames * 0.2,
        "jitter_detected": jitter_frames > total_movement_frames * 0.3,
        "sudden_shifts": sudden_shifts,
        "quality": quality,
        "observation": observation
    }


def analyze_facial_tension(frames_data: List[Dict]) -> Dict:
    """
    Analyze facial tension using FACS-style observable signals
    
    NO EMOTION CLASSIFICATION - Only observable muscle movements
    
    Analyzes:
    - Brow compression (AU4, AU5)
    - Jaw tightness (landmark variance)
    - Lip compression
    - Facial rigidity (low movement variance)
    - Expression stability
    
    Returns:
        Dictionary with tension indicators and observations
    """
    if not frames_data:
        return {"status": "no_data"}
    
    brow_positions = []
    jaw_positions = []
    mouth_positions = []
    
    for frame in frames_data:
        landmarks = frame.get("face_landmarks")
        if not landmarks:
            continue
        
        # Brow landmarks (inner brow points)
        left_brow = landmarks.landmark[70]  # Left inner brow
        right_brow = landmarks.landmark[300]  # Right inner brow
        brow_distance = abs(left_brow.y - right_brow.y)
        brow_positions.append(brow_distance)
        
        # Jaw landmarks (chin area)
        jaw_point = landmarks.landmark[152]  # Chin
        jaw_positions.append((jaw_point.x, jaw_point.y))
        
        # Mouth landmarks
        upper_lip = landmarks.landmark[13]
        lower_lip = landmarks.landmark[14]
        mouth_opening = abs(upper_lip.y - lower_lip.y)
        mouth_positions.append(mouth_opening)
    
    if len(brow_positions) < 5:
        return {"status": "insufficient_data"}
    
    # Calculate tension indicators
    
    # 1. Brow compression: Low variance = compressed/furrowed
    brow_variance = statistics.variance(brow_positions) if len(brow_positions) > 1 else 0
    brow_tension_score = max(0, 100 - (brow_variance * 10000))
    
    # 2. Jaw tightness: Low variance in jaw position = rigid
    jaw_x_positions = [j[0] for j in jaw_positions]
    jaw_y_positions = [j[1] for j in jaw_positions]
    jaw_variance = (statistics.variance(jaw_x_positions) + statistics.variance(jaw_y_positions)) / 2 if len(jaw_positions) > 1 else 0
    jaw_tension_score = max(0, 100 - (jaw_variance * 5000))
    
    # 3. Mouth compression: Small opening with low variance = tight lips
    avg_mouth_opening = statistics.mean(mouth_positions)
    mouth_variance = statistics.variance(mouth_positions) if len(mouth_positions) > 1 else 0
    mouth_tension_score = max(0, 100 - (avg_mouth_opening * 500) - (mouth_variance * 1000))
    
    # 4. Overall facial rigidity: Low variance across all features
    all_variances = [brow_variance, jaw_variance, mouth_variance]
    avg_variance = statistics.mean(all_variances)
    rigidity_score = max(0, 100 - (avg_variance * 8000))
    
    # Composite tension score (weighted average)
    composite_tension = (
        brow_tension_score * 0.35 +
        jaw_tension_score * 0.25 +
        mouth_tension_score * 0.25 +
        rigidity_score * 0.15
    )
    
    # Qualitative assessment (OBSERVATIONAL ONLY)
    if composite_tension < 30:
        level = "Minimal"
        observation = "Facial expression remained relaxed and natural"
    elif composite_tension < 60:
        level = "Mild"
        observation = "Some facial tension observed, particularly in brow or jaw area"
    else:
        level = "Noticeable"
        observation = "Visible facial tension detected (compressed brow, tight jaw, or rigid expression)"
    
    return {
        "composite_tension_score": round(composite_tension, 2),
        "brow_tension": round(brow_tension_score, 2),
        "jaw_tension": round(jaw_tension_score, 2),
        "mouth_tension": round(mouth_tension_score, 2),
        "rigidity_score": round(rigidity_score, 2),
        "tension_level": level,
        "observation": observation
    }


def analyze_temporal_trends(
    frames_data: List[Dict],
    eye_analysis: Dict,
    head_analysis: Dict,
    tension_analysis: Dict
) -> Dict:
    """
    Analyze how visual signals changed over time (start/middle/end)
    
    Detects:
    - Improving or declining trends
    - Consistency vs fluctuation
    - Temporal patterns
    
    Returns:
        Dictionary with temporal trend analysis
    """
    if not frames_data or len(frames_data) < 15:
        return {
            "trend": "unknown",
            "interpretation": "Insufficient data for temporal analysis"
        }
    
    # Divide frames into thirds
    third = len(frames_data) // 3
    
    start_frames = frames_data[:third]
    middle_frames = frames_data[third:2*third]
    end_frames = frames_data[2*third:]
    
    # Analyze each period
    start_eye = analyze_eye_contact(start_frames)
    middle_eye = analyze_eye_contact(middle_frames)
    end_eye = analyze_eye_contact(end_frames)
    
    start_tension = analyze_facial_tension(start_frames)
    middle_tension = analyze_facial_tension(middle_frames)
    end_tension = analyze_facial_tension(end_frames)
    
    # Detect trends
    eye_trend = "stable"
    if end_eye.get("facing_camera_percentage", 0) > start_eye.get("facing_camera_percentage", 0) * 1.2:
        eye_trend = "improving"
    elif end_eye.get("facing_camera_percentage", 0) < start_eye.get("facing_camera_percentage", 0) * 0.8:
        eye_trend = "declining"
    
    tension_trend = "stable"
    start_tension_val = start_tension.get("composite_tension_score", 50)
    end_tension_val = end_tension.get("composite_tension_score", 50)
    
    if end_tension_val < start_tension_val * 0.7:
        tension_trend = "decreasing"  # Getting more relaxed (good)
    elif end_tension_val > start_tension_val * 1.3:
        tension_trend = "increasing"  # Getting more tense (needs attention)
    
    # Overall trend
    if eye_trend == "improving" and tension_trend == "decreasing":
        overall_trend = "strong_improvement"
        interpretation = "Visual presence improved significantly throughout response"
    elif eye_trend == "improving" or tension_trend == "decreasing":
        overall_trend = "improving"
        interpretation = "Showed positive progression as response continued"
    elif eye_trend == "declining" or tension_trend == "increasing":
        overall_trend = "declining"
        interpretation = "Visual presence decreased toward end of response"
    else:
        overall_trend = "stable"
        interpretation = "Visual presence remained consistent throughout"
    
    return {
        "overall_trend": overall_trend,
        "eye_contact_trend": eye_trend,
        "tension_trend": tension_trend,
        "start_quality": start_eye.get("quality", "Unknown"),
        "end_quality": end_eye.get("quality", "Unknown"),
        "interpretation": interpretation
    }


def generate_visual_feedback(
    eye_analysis: Dict,
    head_analysis: Dict,
    tension_analysis: Dict,
    temporal_analysis: Dict
) -> Dict:
    """
    Generate structured professional feedback from visual analysis
    
    Returns:
        Dictionary with observations, patterns, and improvement suggestions
    """
    feedback = {
        "summary": "",
        "observations": [],
        "patterns": [],
        "strengths": [],
        "improvement_suggestions": []
    }
    
    # Generate summary
    eye_quality = eye_analysis.get("quality", "Unknown")
    head_quality = head_analysis.get("quality", "Unknown")
    tension_level = tension_analysis.get("tension_level", "Unknown")
    
    feedback["summary"] = f"Visual Presence: Eye Contact - {eye_quality}, Stability - {head_quality}, Tension - {tension_level}"
    
    # Observations
    feedback["observations"].append(eye_analysis.get("observation", "Eye contact analyzed"))
    feedback["observations"].append(head_analysis.get("observation", "Head movement analyzed"))
    feedback["observations"].append(tension_analysis.get("observation", "Facial composure analyzed"))
    
    # Temporal patterns
    if temporal_analysis.get("overall_trend") != "stable":
        feedback["patterns"].append(temporal_analysis.get("interpretation", ""))
    
    # Strengths
    if eye_quality == "Strong":
        feedback["strengths"].append("Excellent eye contact maintained throughout")
    if head_quality == "Steady":
        feedback["strengths"].append("Stable, composed posture")
    if tension_level == "Minimal":
        feedback["strengths"].append("Relaxed and natural facial expression")
    
    # Improvement suggestions
    if eye_quality == "Needs Improvement":
        feedback["improvement_suggestions"].append("Practice maintaining focus on the camera lens to improve perceived eye contact")
    
    if head_analysis.get("jitter_detected"):
        feedback["improvement_suggestions"].append("Work on minimizing small, repetitive head movements (fidgeting)")
    elif head_analysis.get("sudden_shifts", 0) > 3:
        feedback["improvement_suggestions"].append("Maintain a steady posture throughout your response")
    
    if tension_level in ["Mild", "Noticeable"]:
        feedback["improvement_suggestions"].append("Practice conscious facial relaxation before and during responses")
    
    # Limit to top 3 suggestions
    feedback["improvement_suggestions"] = feedback["improvement_suggestions"][:3]
    
    return feedback
