"""
Composite Analysis Service for Video Presence Interview

SCOPE: Video Presence Interview ONLY
PURPOSE: Combine visual and audio analyses into unified multi-modal feedback

ARCHITECTURE:
- Aggregates signals from visual_analysis_service and video_analysis_service
- Calculates composite presence indicators (qualitative only)
- Generates professional, explainable feedback
- Implements "never zero" scoring logic

IMPORTANT:
- NO numeric scores exposed to user (qualitative only: Low/Moderate/Good)
- Balanced weighting across modalities
- Observable signals with clear explanations
- Practice-oriented improvement suggestions

Author: AceIt Backend Team
"""

from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


def calculate_composite_indicators(
    visual_analysis: Optional[Dict],
    audio_analysis: Optional[Dict]
) -> Dict:
    """
    Calculate composite presence indicators from visual and audio analyses
    
    Args:
        visual_analysis: Results from visual_analysis_service
        audio_analysis: Results from video_analysis_service (audio hesitation)
    
    Returns:
        Dictionary with composite indicators (qualitative)
    """
    # Initialize scores (internal use only, not exposed)
    eye_contact_score = 50
    head_stability_score = 50
    facial_composure_score = 50
    audio_confidence_score = 50
    
    # Extract visual metrics if available
    if visual_analysis and visual_analysis.get("status") == "success":
        va = visual_analysis.get("visual_analysis", {})
        
        # Eye contact
        eye_data = va.get("eye_contact", {})
        eye_percentage = eye_data.get("facing_camera_percentage", 50)
        eye_contact_score = eye_percentage
        
        # Head stability
        head_data = va.get("head_movement", {})
        head_stability_score = head_data.get("stability_score", 50)
        
        # Facial composure (inverse of tension)
        tension_data = va.get("facial_tension", {})
        tension_score = tension_data.get("composite_tension_score", 50)
        facial_composure_score = max(0, 100 - tension_score)
    
    # Extract audio metrics if available
    if audio_analysis and audio_analysis.get("status") == "success":
        hesitation = audio_analysis.get("hesitation_analysis", {})
        audio_confidence_score = hesitation.get("confidence_score", 50)
    
    # Calculate separate scores
    # Visual Score: Simple average of Eye, Head, and Facial Composure (as requested)
    visual_score = (eye_contact_score + head_stability_score + facial_composure_score) / 3
    
    # Audio Score: From hesitation analysis
    audio_score = audio_confidence_score
    
    # Combined Overall Score (for legacy/summary use)
    composite_score = (visual_score + audio_score) / 2
    
    # Apply "never zero" logic - minimum score of 30
    composite_score = max(composite_score, 30)
    visual_score = max(visual_score, 30)
    audio_score = max(audio_score, 30)
    
    # Map to qualitative confidence indicator
    if composite_score >= 75:
        confidence = "Good"
    elif composite_score >= 50:
        confidence = "Moderate"
    else:
        confidence = "Low"
    
    # Calculate stress indicator (based on tension and hesitation)
    stress_signals = []
    
    if visual_analysis and visual_analysis.get("status") == "success":
        va = visual_analysis.get("visual_analysis", {})
        tension_level = va.get("facial_tension", {}).get("tension_level", "Minimal")
        if tension_level == "Noticeable":
            stress_signals.append("high_facial_tension")
        elif tension_level == "Mild":
            stress_signals.append("mild_facial_tension")
    
    if audio_analysis and audio_analysis.get("status") == "success":
        hesitation = audio_analysis.get("hesitation_analysis", {})
        filler_freq = hesitation.get("filler_words", {}).get("filler_frequency_percent", 0)
        pauses = hesitation.get("pauses", {})
        nervous_pauses = pauses.get("nervous_pauses", 0)
        long_pauses = pauses.get("long_pauses_count", 0)
        repetitions = hesitation.get("speech_continuity", {}).get("repetitions_count", 0)
        
        if filler_freq > 8 or nervous_pauses > 3 or long_pauses > 4 or repetitions > 3:
            stress_signals.append("high_hesitation")
        elif filler_freq > 4 or nervous_pauses > 1 or long_pauses > 1 or repetitions > 0:
            stress_signals.append("moderate_hesitation")
    
    # Map to qualitative stress indicator
    if len(stress_signals) >= 2 or "high_facial_tension" in stress_signals or "high_hesitation" in stress_signals:
        stress = "Noticeable"
    elif len(stress_signals) >= 1:
        stress = "Moderate"
    else:
        stress = "Mild"
    
    # Calculate presence quality
    if confidence == "Good" and stress == "Mild":
        presence_quality = "Strong"
    elif confidence == "Low" or stress == "Noticeable":
        presence_quality = "Needs Improvement"
    else:
        presence_quality = "Fair"
    
    return {
        "confidence": confidence,
        "stress": stress,
        "presence_quality": presence_quality,
        "overall_score": round(composite_score, 1),
        "visual_score": round(visual_score, 1),
        "audio_score": round(audio_score, 1),
        "component_scores": {  # For debugging/logging
            "eye_contact": round(eye_contact_score, 1),
            "head_stability": round(head_stability_score, 1),
            "audio_confidence": round(audio_confidence_score, 1),
            "facial_composure": round(facial_composure_score, 1)
        }
    }


def generate_composite_feedback(
    indicators: Dict,
    visual_analysis: Optional[Dict],
    audio_analysis: Optional[Dict]
) -> Dict:
    """
    Generate comprehensive professional feedback combining all analyses
    
    Args:
        indicators: Composite indicators from calculate_composite_indicators
        visual_analysis: Visual analysis results
        audio_analysis: Audio analysis results
    
    Returns:
        Structured feedback dictionary
    """
    feedback = {
        "presence_summary": "",
        "visual_observations": [],
        "speech_observations": [],
        "confidence_indicators": {},
        "temporal_insights": [],
        "improvement_tips": [],
        "faults_detected": [],
        "strengths": []
    }
    
    # Presence summary
    confidence = indicators.get("confidence", "Unknown")
    stress = indicators.get("stress", "Unknown")
    presence = indicators.get("presence_quality", "Unknown")
    
    feedback["presence_summary"] = f"Overall Presence: {presence} | Confidence: {confidence} | Stress Indicators: {stress}"
    
    # Confidence indicators (qualitative only)
    feedback["confidence_indicators"] = {
        "confidence_level": confidence,
        "stress_level": stress,
        "presence_quality": presence
    }
    
    # Visual observations
    if visual_analysis and visual_analysis.get("status") == "success":
        va = visual_analysis.get("visual_analysis", {})
        
        visual_feedback = va.get("feedback", {})
        feedback["visual_observations"] = visual_feedback.get("observations", [])
        
        # Add temporal insights
        temporal = va.get("temporal_trends", {})
        if temporal.get("overall_trend") != "stable":
            feedback["temporal_insights"].append(temporal.get("interpretation", ""))
        
        # Add visual strengths
        feedback["strengths"].extend(visual_feedback.get("strengths", []))
    
    # Speech observations
    if audio_analysis and audio_analysis.get("status") == "success":
        hesitation = audio_analysis.get("hesitation_analysis", {})
        
        audio_feedback = hesitation.get("feedback", {})
        speech_delivery = audio_feedback.get("speech_delivery", {})
        
        # Combine observations with explanations
        observations = speech_delivery.get("observations", [])
        explanations = speech_delivery.get("explanations", [])
        
        for i, obs in enumerate(observations):
            obs_dict = {
                "observation": obs,
                "explanation": explanations[i] if i < len(explanations) else ""
            }
            feedback["speech_observations"].append(obs_dict)
        
        # Add temporal progression
        temporal_prog = hesitation.get("temporal_progression", {})
        if temporal_prog.get("trend") != "stable":
            feedback["temporal_insights"].append(temporal_prog.get("interpretation", ""))
        
        # Add audio strengths
        positive_notes = audio_feedback.get("positive_notes", [])
        feedback["strengths"].extend(positive_notes)
        
        # NEW: Add audio faults
        faults_detected = audio_feedback.get("faults_detected", [])
        feedback["faults_detected"].extend(faults_detected)
    
    # Combine improvement tips from both modalities
    improvement_tips = []
    
    # Visual tips
    if visual_analysis and visual_analysis.get("status") == "success":
        va = visual_analysis.get("visual_analysis", {})
        visual_tips = va.get("feedback", {}).get("improvement_suggestions", [])
        improvement_tips.extend(visual_tips)
    
    # Audio tips
    if audio_analysis and audio_analysis.get("status") == "success":
        hesitation = audio_analysis.get("hesitation_analysis", {})
        audio_tips = hesitation.get("feedback", {}).get("improvement_suggestions", [])
        improvement_tips.extend(audio_tips)
    
    # Prioritize and limit to top 3
    feedback["improvement_tips"] = prioritize_improvement_tips(
        improvement_tips,
        indicators
    )[:3]
    
    return feedback


def prioritize_improvement_tips(tips: List[str], indicators: Dict) -> List[str]:
    """
    Prioritize improvement tips based on composite indicators
    
    Args:
        tips: List of improvement suggestions
        indicators: Composite indicators
    
    Returns:
        Prioritized list of tips
    """
    if not tips:
        return ["Continue practicing to maintain consistency"]
    
    # Create priority scores for each tip
    tip_priorities = []
    
    confidence = indicators.get("confidence", "Moderate")
    stress = indicators.get("stress", "Mild")
    
    for tip in tips:
        priority = 1  # Base priority
        
        # Boost priority for high-impact areas
        if confidence == "Low":
            if "eye contact" in tip.lower() or "camera" in tip.lower():
                priority += 2
            if "filler" in tip.lower() or "pause" in tip.lower():
                priority += 2
        
        if stress == "Noticeable":
            if "relax" in tip.lower() or "tension" in tip.lower():
                priority += 2
            if "pause" in tip.lower() or "organize" in tip.lower():
                priority += 1
        
        tip_priorities.append((tip, priority))
    
    # Sort by priority (descending)
    tip_priorities.sort(key=lambda x: x[1], reverse=True)
    
    # Return tips in priority order
    return [tip for tip, _ in tip_priorities]


def ensure_minimum_scores(indicators: Dict) -> Dict:
    """
    Ensure no indicator is zero or overly negative
    
    This implements the "never zero" policy for user-facing feedback
    
    Args:
        indicators: Composite indicators dictionary
    
    Returns:
        Adjusted indicators with minimum thresholds
    """
    # Ensure overall score is at least 30
    if indicators.get("overall_score", 0) < 30:
        indicators["overall_score"] = 30
        
        # Adjust confidence if needed
        if indicators.get("confidence") == "Low":
            # Keep it as Low, but ensure it's not zero-like
            pass
    
    # Ensure component scores are reasonable
    component_scores = indicators.get("component_scores", {})
    for key in component_scores:
        if component_scores[key] < 20:
            component_scores[key] = 20
    
    return indicators


def get_fallback_feedback(reason: str = "unavailable") -> Dict:
    """
    Generate fallback feedback when analysis fails
    
    Args:
        reason: Reason for fallback (e.g., "no_video", "no_audio", "error")
    
    Returns:
        Minimal feedback dictionary
    """
    if reason == "no_video":
        return {
            "presence_summary": "Visual analysis unavailable - audio analysis only",
            "visual_observations": ["Video analysis could not be performed"],
            "speech_observations": [],
            "confidence_indicators": {
                "confidence_level": "Moderate",
                "stress_level": "Unknown",
                "presence_quality": "Fair"
            },
            "temporal_insights": [],
            "improvement_tips": ["Ensure camera is enabled for full analysis"],
            "strengths": []
        }
    elif reason == "no_audio":
        return {
            "presence_summary": "Audio analysis unavailable - visual analysis only",
            "visual_observations": [],
            "speech_observations": ["Audio analysis could not be performed"],
            "confidence_indicators": {
                "confidence_level": "Moderate",
                "stress_level": "Unknown",
                "presence_quality": "Fair"
            },
            "temporal_insights": [],
            "improvement_tips": ["Ensure microphone is enabled for full analysis"],
            "strengths": []
        }
    else:
        return {
            "presence_summary": "Analysis unavailable - please try again",
            "visual_observations": ["Analysis could not be completed"],
            "speech_observations": ["Analysis could not be completed"],
            "confidence_indicators": {
                "confidence_level": "Unknown",
                "stress_level": "Unknown",
                "presence_quality": "Unknown"
            },
            "temporal_insights": [],
            "improvement_tips": ["Please check your camera and microphone settings"],
            "strengths": []
        }
