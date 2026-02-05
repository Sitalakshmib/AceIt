"""
Video Presence Interview - PROFESSIONAL Audio Hesitation Analysis Service

SCOPE: Video Presence Interview ONLY
PURPOSE: Professional AI-grade analysis of student audio for hesitation patterns

ENHANCEMENTS:
- Temporal progression tracking (start/middle/end)
- Advanced hesitation pattern detection (thinking vs nervous pauses)
- Filler word clustering analysis
- Explainability layer (signal → insight mapping)
- Professional feedback structuring

IMPORTANT RULES:
- Analyze ONLY student audio (microphone input)
- Do NOT analyze: accent, pronunciation, grammar, emotions, personality
- Use observable signals only (filler words, pauses, speech flow)
- Provide practice-oriented feedback, NOT psychological diagnoses
- Never make medical or emotional claims

Author: AceIt Backend Team
"""

import whisper
import re
from typing import Dict, List, Optional, Tuple
import os
import statistics

# Global Whisper model cache
_WHISPER_MODEL = None

# Filler words to detect (case-insensitive)
FILLER_WORDS = [
    'uh', 'um', 'ah', 'mm', 'hmm',
    'er', 'erm', 'uhm',
    'like', 'you know', 'actually', 'basically',
    'sort of', 'kind of'
]

# Prolonged vowel patterns (e.g., "sooo", "weeeell")
PROLONGED_VOWEL_PATTERN = r'\b\w*([aeiou])\1{2,}\w*\b'


def load_whisper_model():
    """
    Load Whisper model (lazy loading, cached globally)
    """
    global _WHISPER_MODEL
    if _WHISPER_MODEL is None:
        print("[WHISPER] Loading Whisper model for video analysis...")
        try:
            _WHISPER_MODEL = whisper.load_model("base")
            print("[WHISPER] Whisper model loaded successfully")
        except Exception as e:
            print(f"[ERROR] Failed to load Whisper model: {e}")
            raise RuntimeError("Could not load Whisper model for audio analysis")
    return _WHISPER_MODEL


def analyze_audio_hesitation(audio_file_path: str) -> Dict:
    """
    Main function: Professional AI-grade analysis of student audio
    
    Args:
        audio_file_path: Path to the student's audio file (microphone only)
    
    Returns:
        Dictionary containing professional hesitation analysis with explainability
    """
    try:
        # Validate file exists
        if not os.path.exists(audio_file_path):
            raise FileNotFoundError(f"Audio file not found: {audio_file_path}")
        
        # Load Whisper model
        model = load_whisper_model()
        
        # Transcribe audio with word-level timestamps
        print(f"[WHISPER] Transcribing audio: {audio_file_path}")
        result = model.transcribe(
            audio_file_path,
            language="en",
            temperature=0.0,
            word_timestamps=True,  # Critical for temporal analysis
            condition_on_previous_text=False,
            initial_prompt="This is a student answering an interview question."
        )
        
        transcript = result.get("text", "").strip()
        segments = result.get("segments", [])
        
        # If no speech detected
        if not transcript or len(transcript) < 5:
            return {
                "status": "no_speech",
                "message": "No speech detected. Please check your microphone.",
                "transcript": "",
                "hesitation_analysis": None
            }
        
        # Calculate total duration for temporal analysis
        total_duration = segments[-1].get("end", 0) if segments else 0
        
        # PROFESSIONAL ENHANCEMENTS
        
        # 1. Advanced filler word analysis with clustering
        filler_analysis = detect_filler_words_advanced(transcript, segments, total_duration)
        
        # 2. Advanced pause analysis (thinking vs nervous)
        pause_analysis = analyze_pauses_advanced(segments, total_duration)
        
        # 3. Speech continuity with temporal awareness
        continuity_analysis = analyze_speech_continuity(segments)
        
        # 4. Temporal progression analysis (start/middle/end)
        temporal_analysis = analyze_temporal_progression(
            segments, 
            filler_analysis, 
            pause_analysis,
            total_duration
        )
        
        # 5. Calculate professional confidence indicators with explainability
        indicators = calculate_professional_confidence(
            filler_analysis, 
            pause_analysis, 
            continuity_analysis,
            temporal_analysis
        )
        
        # 6. Generate structured professional feedback
        professional_feedback = generate_professional_feedback(
            filler_analysis,
            pause_analysis,
            continuity_analysis,
            temporal_analysis,
            indicators
        )
        
        return {
            "status": "success",
            "transcript": transcript,
            "duration": round(total_duration, 2),
            "word_count": filler_analysis.get("word_count", 0),
            "hesitation_analysis": {
                "filler_words": filler_analysis,
                "pauses": pause_analysis,
                "speech_continuity": continuity_analysis,
                "temporal_progression": temporal_analysis,
                "confidence_indicator": indicators["confidence"],
                "stress_indicator": indicators["stress"],
                "confidence_score": indicators["confidence_score"],
                "feedback": professional_feedback
            }
        }
        
    except Exception as e:
        print(f"[ERROR] Audio analysis failed: {e}")
        return {
            "status": "error",
            "message": "Audio analysis unavailable",
            "error": str(e)
        }


def detect_filler_words_advanced(transcript: str, segments: List[Dict], total_duration: float) -> Dict:
    """
    ENHANCED: Detect filler words with clustering and temporal distribution
    
    Returns:
        Dictionary with advanced filler word analysis including clusters and distribution
    """
    transcript_lower = transcript.lower()
    
    # Count filler words
    filler_counts = {}
    total_filler_count = 0
    filler_positions = []  # Track when fillers occur
    
    for filler in FILLER_WORDS:
        pattern = r'\b' + re.escape(filler) + r'\b'
        matches = re.findall(pattern, transcript_lower)
        count = len(matches)
        if count > 0:
            filler_counts[filler] = count
            total_filler_count += count
    
    # Detect prolonged vowels
    prolonged_matches = re.findall(PROLONGED_VOWEL_PATTERN, transcript_lower)
    prolonged_count = len(prolonged_matches)
    
    # Calculate word count and frequency
    word_count = len(transcript.split())
    filler_frequency = (total_filler_count / word_count * 100) if word_count > 0 else 0
    
    # ENHANCEMENT: Detect filler word clusters (multiple fillers close together)
    clusters = detect_filler_clusters(transcript_lower)
    
    # ENHANCEMENT: Analyze temporal distribution (where fillers occur)
    distribution = analyze_filler_distribution(segments, filler_counts, total_duration)
    
    return {
        "total_count": total_filler_count,
        "prolonged_vowels_count": prolonged_count,
        "filler_words_detected": list(filler_counts.keys()),
        "filler_frequency_percent": round(filler_frequency, 2),
        "word_count": word_count,
        "details": filler_counts,
        "clusters": clusters,  # NEW: Cluster detection
        "distribution": distribution  # NEW: Temporal distribution
    }


def detect_filler_clusters(transcript: str) -> Dict:
    """
    Detect clusters of filler words (multiple fillers close together)
    Indicates nervous speech patterns
    """
    words = transcript.lower().split()
    clusters_found = 0
    max_cluster_size = 0
    
    i = 0
    while i < len(words):
        cluster_size = 0
        # Count consecutive or near-consecutive fillers (within 2 words)
        j = i
        while j < len(words) and j < i + 5:  # Look ahead max 5 words
            if any(filler in words[j] for filler in FILLER_WORDS):
                cluster_size += 1
            j += 1
        
        if cluster_size >= 2:  # At least 2 fillers close together
            clusters_found += 1
            max_cluster_size = max(max_cluster_size, cluster_size)
            i = j  # Skip past this cluster
        else:
            i += 1
    
    cluster_level = "none"
    if clusters_found >= 3:
        cluster_level = "frequent"
    elif clusters_found >= 1:
        cluster_level = "occasional"
    
    return {
        "count": clusters_found,
        "max_size": max_cluster_size,
        "level": cluster_level,
        "interpretation": "Filler word clusters often indicate nervous or uncertain speech" if clusters_found > 0 else "No filler clustering detected"
    }


def analyze_filler_distribution(segments: List[Dict], filler_counts: Dict, total_duration: float) -> Dict:
    """
    Analyze when fillers occur (start/middle/end)
    """
    if not segments or total_duration == 0:
        return {"pattern": "unknown", "concentration": "unknown"}
    
    # Divide into thirds
    third = total_duration / 3
    start_fillers = 0
    middle_fillers = 0
    end_fillers = 0
    
    for seg in segments:
        seg_start = seg.get("start", 0)
        seg_text = seg.get("text", "").lower()
        
        # Count fillers in this segment
        seg_filler_count = sum(seg_text.count(filler) for filler in FILLER_WORDS)
        
        if seg_start < third:
            start_fillers += seg_filler_count
        elif seg_start < 2 * third:
            middle_fillers += seg_filler_count
        else:
            end_fillers += seg_filler_count
    
    # Determine pattern
    max_fillers = max(start_fillers, middle_fillers, end_fillers)
    if max_fillers == 0:
        pattern = "none"
        concentration = "none"
    elif start_fillers == max_fillers:
        pattern = "front_loaded"
        concentration = "start"
    elif end_fillers == max_fillers:
        pattern = "end_heavy"
        concentration = "end"
    else:
        pattern = "middle_concentrated"
        concentration = "middle"
    
    return {
        "pattern": pattern,
        "concentration": concentration,
        "start_count": start_fillers,
        "middle_count": middle_fillers,
        "end_count": end_fillers,
        "interpretation": get_distribution_interpretation(pattern)
    }


def get_distribution_interpretation(pattern: str) -> str:
    """Get human-readable interpretation of filler distribution"""
    interpretations = {
        "front_loaded": "Most fillers occurred at the start, suggesting initial nervousness that decreased",
        "end_heavy": "Fillers increased toward the end, possibly indicating fatigue or loss of focus",
        "middle_concentrated": "Fillers were scattered throughout the response",
        "none": "No significant filler pattern detected"
    }
    return interpretations.get(pattern, "Filler distribution analyzed")


def analyze_pauses_advanced(segments: List[Dict], total_duration: float) -> Dict:
    """
    ENHANCED: Distinguish thinking pauses from nervous pauses
    """
    if not segments or len(segments) < 2:
        return {
            "long_pauses_count": 0,
            "thinking_pauses": 0,
            "nervous_pauses": 0,
            "average_pause_duration": 0.0,
            "pause_pattern": "insufficient_data"
        }
    
    pauses = []
    thinking_pauses = 0  # 0.5-1.5s (normal)
    nervous_pauses = 0   # >2.5s (uncertainty)
    long_pauses = 0      # >2.0s
    
    THINKING_PAUSE_MIN = 0.5
    THINKING_PAUSE_MAX = 1.5
    LONG_PAUSE_THRESHOLD = 2.0
    NERVOUS_PAUSE_THRESHOLD = 2.5
    
    for i in range(len(segments) - 1):
        current_end = segments[i].get("end", 0)
        next_start = segments[i + 1].get("start", 0)
        pause_duration = next_start - current_end
        
        if pause_duration > 0.3:  # Ignore very short natural pauses
            pauses.append(pause_duration)
            
            if THINKING_PAUSE_MIN <= pause_duration <= THINKING_PAUSE_MAX:
                thinking_pauses += 1
            elif pause_duration > NERVOUS_PAUSE_THRESHOLD:
                nervous_pauses += 1
            
            if pause_duration > LONG_PAUSE_THRESHOLD:
                long_pauses += 1
    
    if not pauses:
        return {
            "long_pauses_count": 0,
            "thinking_pauses": 0,
            "nervous_pauses": 0,
            "average_pause_duration": 0.0,
            "pause_pattern": "smooth"
        }
    
    avg_pause = sum(pauses) / len(pauses)
    max_pause = max(pauses)
    
    # Determine pause pattern with more nuance
    if nervous_pauses > 2:
        pattern = "frequent_uncertainty"
    elif long_pauses > 3:
        pattern = "frequent_long_pauses"
    elif thinking_pauses > len(pauses) * 0.6:
        pattern = "thoughtful"  # Mostly thinking pauses
    elif avg_pause > 1.5:
        pattern = "moderate_pauses"
    else:
        pattern = "normal"
    
    return {
        "long_pauses_count": long_pauses,
        "thinking_pauses": thinking_pauses,
        "nervous_pauses": nervous_pauses,
        "average_pause_duration": round(avg_pause, 2),
        "max_pause_duration": round(max_pause, 2),
        "pause_pattern": pattern,
        "total_pauses": len(pauses),
        "interpretation": get_pause_interpretation(pattern, thinking_pauses, nervous_pauses)
    }


def get_pause_interpretation(pattern: str, thinking: int, nervous: int) -> str:
    """Get human-readable pause interpretation"""
    if pattern == "thoughtful":
        return f"Pauses appear to be thoughtful ({thinking} thinking pauses), which is natural"
    elif pattern == "frequent_uncertainty":
        return f"Several long pauses ({nervous}) may indicate uncertainty or difficulty formulating thoughts"
    elif pattern == "frequent_long_pauses":
        return "Multiple long pauses detected - practice maintaining speech flow"
    elif pattern == "normal":
        return "Pause pattern is natural and appropriate"
    else:
        return "Moderate pausing observed"


def analyze_speech_continuity(segments: List[Dict]) -> Dict:
    """
    Analyze speech continuity and flow (unchanged from original)
    """
    if not segments:
        return {
            "continuity_score": 0,
            "flow_pattern": "no_data",
            "fragmentation_level": "unknown"
        }
    
    total_segments = len(segments)
    short_segments = sum(1 for seg in segments if len(seg.get("text", "").split()) < 3)
    fragmentation_ratio = short_segments / total_segments if total_segments > 0 else 0
    
    continuity_score = max(0, 100 - (fragmentation_ratio * 100))
    
    if continuity_score >= 75:
        flow_pattern = "smooth"
        fragmentation_level = "low"
    elif continuity_score >= 50:
        flow_pattern = "moderate"
        fragmentation_level = "moderate"
    else:
        flow_pattern = "fragmented"
        fragmentation_level = "high"
    
    return {
        "continuity_score": round(continuity_score, 2),
        "flow_pattern": flow_pattern,
        "fragmentation_level": fragmentation_level,
        "total_segments": total_segments,
        "short_segments": short_segments
    }


def analyze_temporal_progression(
    segments: List[Dict],
    filler_analysis: Dict,
    pause_analysis: Dict,
    total_duration: float
) -> Dict:
    """
    NEW: Analyze how speech quality changed over time (start/middle/end)
    Detects improvement or decline trends
    """
    if not segments or total_duration == 0:
        return {
            "trend": "unknown",
            "progression": "insufficient_data",
            "interpretation": "Not enough data for temporal analysis"
        }
    
    # Divide into thirds
    third = total_duration / 3
    
    # Analyze each third
    thirds_data = {
        "start": {"fillers": 0, "pauses": 0, "segments": 0},
        "middle": {"fillers": 0, "pauses": 0, "segments": 0},
        "end": {"fillers": 0, "pauses": 0, "segments": 0}
    }
    
    for i, seg in enumerate(segments):
        seg_start = seg.get("start", 0)
        seg_text = seg.get("text", "").lower()
        
        # Determine which third
        if seg_start < third:
            period = "start"
        elif seg_start < 2 * third:
            period = "middle"
        else:
            period = "end"
        
        # Count fillers in this segment
        seg_fillers = sum(seg_text.count(filler) for filler in FILLER_WORDS)
        thirds_data[period]["fillers"] += seg_fillers
        thirds_data[period]["segments"] += 1
    
    # Calculate filler density for each third
    start_density = thirds_data["start"]["fillers"] / max(thirds_data["start"]["segments"], 1)
    middle_density = thirds_data["middle"]["fillers"] / max(thirds_data["middle"]["segments"], 1)
    end_density = thirds_data["end"]["fillers"] / max(thirds_data["end"]["segments"], 1)
    
    # Determine trend
    if end_density < start_density * 0.7:  # Significant improvement
        trend = "improving"
        progression = "Speech became smoother as you progressed"
    elif end_density > start_density * 1.3:  # Decline
        trend = "declining"
        progression = "Speech flow decreased toward the end"
    else:
        trend = "stable"
        progression = "Speech quality remained consistent throughout"
    
    return {
        "trend": trend,
        "progression": progression,
        "start_quality": "good" if start_density < 0.5 else "moderate" if start_density < 1.0 else "needs_improvement",
        "end_quality": "good" if end_density < 0.5 else "moderate" if end_density < 1.0 else "needs_improvement",
        "filler_density": {
            "start": round(start_density, 2),
            "middle": round(middle_density, 2),
            "end": round(end_density, 2)
        },
        "interpretation": progression
    }


def calculate_professional_confidence(
    filler_analysis: Dict,
    pause_analysis: Dict,
    continuity_analysis: Dict,
    temporal_analysis: Dict
) -> Dict:
    """
    ENHANCED: Calculate confidence with temporal awareness and better weighting
    """
    # Extract metrics
    filler_freq = filler_analysis.get("filler_frequency_percent", 0)
    filler_count = filler_analysis.get("total_count", 0)
    clusters = filler_analysis.get("clusters", {}).get("count", 0)
    
    long_pauses = pause_analysis.get("long_pauses_count", 0)
    nervous_pauses = pause_analysis.get("nervous_pauses", 0)
    pause_pattern = pause_analysis.get("pause_pattern", "normal")
    
    continuity_score = continuity_analysis.get("continuity_score", 50)
    trend = temporal_analysis.get("trend", "stable")
    
    # Calculate base confidence score
    confidence_score = 100
    
    # Deduct for fillers (with cluster penalty)
    if filler_freq > 10:
        confidence_score -= 40
    elif filler_freq > 5:
        confidence_score -= 25
    elif filler_freq > 2:
        confidence_score -= 10
    
    # Extra penalty for clusters (nervous speech)
    if clusters >= 3:
        confidence_score -= 15
    elif clusters >= 1:
        confidence_score -= 5
    
    # Deduct for pauses (distinguish nervous from thoughtful)
    if pause_pattern == "frequent_uncertainty":
        confidence_score -= 35  # Nervous pauses
    elif pause_pattern == "frequent_long_pauses":
        confidence_score -= 25
    elif pause_pattern == "thoughtful":
        confidence_score -= 5  # Minimal penalty for thinking pauses
    elif pause_pattern == "moderate_pauses":
        confidence_score -= 15
    
    # Deduct for fragmentation
    if continuity_score < 50:
        confidence_score -= 20
    elif continuity_score < 75:
        confidence_score -= 10
    
    # BONUS for improvement trend
    if trend == "improving":
        confidence_score += 10
    elif trend == "declining":
        confidence_score -= 10
    
    # Ensure minimum score
    confidence_score = max(confidence_score, 30)
    
    # Map to qualitative labels
    if confidence_score >= 75:
        confidence_label = "Good"
        stress_label = "Mild"
    elif confidence_score >= 50:
        confidence_label = "Moderate"
        stress_label = "Moderate"
    else:
        confidence_label = "Low"
        stress_label = "Noticeable"
    
    return {
        "confidence": confidence_label,
        "stress": stress_label,
        "confidence_score": confidence_score
    }


def generate_professional_feedback(
    filler_analysis: Dict,
    pause_analysis: Dict,
    continuity_analysis: Dict,
    temporal_analysis: Dict,
    indicators: Dict
) -> Dict:
    """
    NEW: Generate structured professional feedback with explainability
    """
    feedback = {
        "summary": "",
        "speech_delivery": {
            "observations": [],
            "explanations": []
        },
        "patterns_detected": [],
        "improvement_suggestions": [],
        "positive_notes": []
    }
    
    # Generate summary
    confidence = indicators["confidence"]
    trend = temporal_analysis.get("trend", "stable")
    trend_text = {
        "improving": " with improving trend ↑",
        "declining": " with declining trend ↓",
        "stable": ""
    }.get(trend, "")
    
    feedback["summary"] = f"Overall Confidence: {confidence}{trend_text}"
    
    # Speech delivery observations with explanations
    filler_count = filler_analysis.get("total_count", 0)
    filler_freq = filler_analysis.get("filler_frequency_percent", 0)
    clusters = filler_analysis.get("clusters", {})
    distribution = filler_analysis.get("distribution", {})
    
    if filler_count > 0:
        filler_words = filler_analysis.get("filler_words_detected", [])
        obs = f"Detected {filler_count} filler word{'s' if filler_count > 1 else ''}: {', '.join(filler_words[:3])}"
        exp = "Filler words often indicate hesitation or uncertainty while speaking"
        
        if clusters.get("level") == "frequent":
            obs += f" (including {clusters.get('count')} clusters)"
            exp += ". Clusters of fillers suggest nervous speech patterns"
        
        feedback["speech_delivery"]["observations"].append(obs)
        feedback["speech_delivery"]["explanations"].append(exp)
        
        # Add distribution insight
        if distribution.get("pattern") != "none":
            feedback["patterns_detected"].append(distribution.get("interpretation", ""))
    
    # Pause analysis
    thinking_pauses = pause_analysis.get("thinking_pauses", 0)
    nervous_pauses = pause_analysis.get("nervous_pauses", 0)
    pause_pattern = pause_analysis.get("pause_pattern", "normal")
    
    if pause_pattern != "normal" and pause_pattern != "smooth":
        obs = pause_analysis.get("interpretation", "Pauses detected")
        feedback["speech_delivery"]["observations"].append(obs)
        
        if nervous_pauses > 0:
            feedback["speech_delivery"]["explanations"].append(
                f"{nervous_pauses} long pause{'s' if nervous_pauses > 1 else ''} may indicate difficulty formulating thoughts"
            )
    
    # Temporal progression
    progression = temporal_analysis.get("progression", "")
    if trend != "stable":
        feedback["patterns_detected"].append(progression)
    
    # Positive notes
    if filler_count <= 2:
        feedback["positive_notes"].append("Speech was mostly smooth with minimal fillers")
    
    if thinking_pauses > nervous_pauses and thinking_pauses > 0:
        feedback["positive_notes"].append("Pauses appear thoughtful rather than nervous")
    
    if continuity_analysis.get("flow_pattern") == "smooth":
        feedback["positive_notes"].append("Speech flow was natural and well-organized")
    
    if trend == "improving":
        feedback["positive_notes"].append("Showed clear improvement as you progressed")
    
    # Improvement suggestions (top 3)
    suggestions = []
    
    if filler_count > 5:
        conc = distribution.get("concentration", "")
        if conc == "start":
            suggestions.append("Practice your opening statement to reduce early fillers")
        else:
            suggestions.append("Practice pausing silently instead of using filler words")
    
    if nervous_pauses > 2:
        suggestions.append("Organize your thoughts before speaking to reduce long pauses")
    
    if clusters.get("level") == "frequent":
        suggestions.append("When you feel uncertain, take one deliberate pause instead of multiple fillers")
    
    if continuity_analysis.get("fragmentation_level") == "high":
        suggestions.append("Work on connecting your ideas more smoothly")
    
    if trend == "declining":
        suggestions.append("Maintain your energy and focus throughout the entire response")
    
    # If doing well, give advanced tips
    if not suggestions and confidence == "Good":
        suggestions.append("Continue practicing to maintain consistency")
        suggestions.append("Try varying your pace to add more dynamism")
    
    feedback["improvement_suggestions"] = suggestions[:3]  # Top 3 only
    
    return feedback
