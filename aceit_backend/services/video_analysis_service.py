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

# Professional hesitation words to detect (case-insensitive)
# Focused on true filler sounds as requested
FILLER_WORDS = [
    'uh', 'um', 'ah', 'mm', 'hmm',
    'er', 'erm', 'uhm'
]

# Common conversational fillers (separate from true hesitation sounds)
CONVERSATIONAL_FILLERS = [
    'like', 'you know', 'actually', 'basically',
    'sort of', 'kind of'
]

# Prolonged vowel patterns (e.g., "sooo", "weeeell")
PROLONGED_VOWEL_PATTERN = r'\b\w*([aeiou])\1{2,}\w*\b'


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
        
        # Use Groq Whisper API to avoid ffmpeg dependency and for faster processing
        from groq import Groq
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY missing for audio analysis.")
            
        client = Groq(api_key=api_key)
        
        print(f"[GROQ] Transcribing audio: {audio_file_path}")
        with open(audio_file_path, "rb") as audio_file:
            result_obj = client.audio.transcriptions.create(
                file=(os.path.basename(audio_file_path), audio_file.read()),
                model="whisper-large-v3-turbo",
                response_format="verbose_json",
                language="en",
                temperature=0.0,
                prompt="Umm, let me think. Uh, okay, well, like, I think that... um, so basically...",
                timestamp_granularities=["word", "segment"]
            )
        
        # Groq returns an object, local Whisper returns a dict. 
        # Convert Groq object to a format compatible with our analysis functions.
        # Handle both dict-like and attribute-like access just in case
        def get_attr(obj, attr, default=None):
            if isinstance(obj, dict):
                return obj.get(attr, default)
            return getattr(obj, attr, default)

        segments_raw = get_attr(result_obj, "segments", [])
        
        result = {
            "text": get_attr(result_obj, "text", ""),
            "segments": [
                {
                    "start": get_attr(s, "start"),
                    "end": get_attr(s, "end"),
                    "text": get_attr(s, "text"),
                    "words": [
                        {
                            "word": get_attr(w, "word"),
                            "start": get_attr(w, "start"),
                            "end": get_attr(w, "end")
                        } for w in get_attr(s, "words", [])
                    ]
                } for s in segments_raw
            ]
        }
        
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
        
        # 2. Advanced pause analysis (using 1.2s threshold for long pauses)
        pause_analysis = analyze_pauses_advanced(segments, total_duration)
        
        # 3. Speech continuity and flow (Repetitions and Restarts)
        continuity_analysis = analyze_speech_flow_advanced(segments, transcript)
        
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
                "transcript": transcript, # NEW: for frontend transparency
                "filler_words": filler_analysis,
                "pauses": pause_analysis,
                "speech_continuity": continuity_analysis,
                "temporal_progression": temporal_analysis,
                "confidence_indicator": indicators["confidence"],
                "stress_indicator": indicators["stress"],
                "confidence_score": indicators["confidence_score"],
                "feedback": professional_feedback,
                "all_fillers_detected": list(set(filler_analysis.get("filler_words_detected", []) + filler_analysis.get("conversational_fillers_detected", [])))
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
    
    # NEW: Detect conversational fillers
    conv_filler_counts = {}
    total_conv_count = 0
    for filler in CONVERSATIONAL_FILLERS:
        pattern = r'\b' + re.escape(filler) + r'\b'
        matches = re.findall(pattern, transcript_lower)
        count = len(matches)
        if count > 0:
            conv_filler_counts[filler] = count
            total_conv_count += count
    
    # Calculate word count and frequency
    word_count = len(transcript.split())
    filler_frequency = (total_filler_count / word_count * 100) if word_count > 0 else 0
    
    # ENHANCEMENT: Detect filler word clusters (multiple fillers close together)
    clusters = detect_filler_clusters(transcript_lower)
    
    # ENHANCEMENT: Analyze temporal distribution (where fillers occur)
    distribution = analyze_filler_distribution(segments, filler_counts, total_duration)
    
    return {
        "total_count": total_filler_count,
        "conversational_count": total_conv_count,
        "prolonged_vowels_count": prolonged_count,
        "filler_words_detected": list(filler_counts.keys()),
        "conversational_fillers_detected": list(conv_filler_counts.keys()),
        "filler_frequency_percent": round(filler_frequency, 2),
        "word_count": word_count,
        "details": filler_counts,
        "conv_details": conv_filler_counts,
        "clusters": clusters,
        "distribution": distribution
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
    
    # Pause thresholds as per requirements
    PAUSE_THRESHOLD_LONG = 1.0  # Flag gaps > 1.0s as "long pauses"
    PAUSE_THRESHOLD_NERVOUS = 2.0 # Flag gaps > 2.0s as "nervous"
    
    # Extract word-level gaps for better precision if available
    word_pauses = []
    for seg in segments:
        words = seg.get("words", [])
        if len(words) > 1:
            for i in range(len(words) - 1):
                gap = words[i+1].get("start", 0) - words[i].get("end", 0)
                if gap > 0.3: # Ignore natural micro-pauses
                    word_pauses.append(gap)

    # Segment gaps
    segment_pauses = []
    for i in range(len(segments) - 1):
        gap = segments[i + 1].get("start", 0) - segments[i].get("end", 0)
        if gap > 0.3:
            segment_pauses.append(gap)
    
    # Combine or use best available
    pauses = word_pauses if word_pauses else segment_pauses
    
    thinking_pauses = sum(1 for p in pauses if 0.5 <= p < PAUSE_THRESHOLD_LONG)
    nervous_pauses = sum(1 for p in pauses if p >= PAUSE_THRESHOLD_NERVOUS)
    long_pauses_count = sum(1 for p in pauses if p >= PAUSE_THRESHOLD_LONG)
    
    total_pause_duration = sum(pauses)
    
    if not pauses:
        return {
            "long_pauses_count": 0,
            "thinking_pauses": 0,
            "nervous_pauses": 0,
            "average_pause_duration": 0.0,
            "pause_pattern": "smooth",
            "total_pause_duration": 0
        }
    
    avg_pause = total_pause_duration / len(pauses)
    max_pause = max(pauses)
    
    # Determine pause pattern with more nuance
    if nervous_pauses >= 1: # Even 1 nervous pause is flagged
        pattern = "frequent_uncertainty"
    elif long_pauses_count >= 2:
        pattern = "frequent_long_pauses"
    elif thinking_pauses > len(pauses) * 0.5:
        pattern = "thoughtful"
    elif avg_pause > 0.8: # Very strict: avg pause > 0.8s is moderate
        pattern = "moderate_pauses"
    else:
        pattern = "normal"
    
    return {
        "long_pauses_count": long_pauses_count,
        "thinking_pauses": thinking_pauses,
        "nervous_pauses": nervous_pauses,
        "average_pause_duration": round(avg_pause, 2),
        "max_pause_duration": round(max_pause, 2),
        "pause_pattern": pattern,
        "total_pauses": len(pauses),
        "total_pause_duration": round(total_pause_duration, 2),
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


def analyze_speech_flow_advanced(segments: List[Dict], transcript: str) -> Dict:
    """
    Detect broken speech flow: word repetitions and sentence restarts.
    Example: "I... I... I think..."
    """
    words = transcript.lower().split()
    repetitions = 0
    repetition_samples = []
    
    # 1. Word Frequency / Pattern Detection
    word_counts = {}
    for w in words:
        if len(w) > 3: # Ignore short functional words for redundancy
            word_counts[w] = word_counts.get(w, 0) + 1
    
    # Flag significant redundancy
    redundant_words = sum(1 for w, c in word_counts.items() if c > 3)
    
    # 2. Sequential Word Repetition Detection (consecutive)
    for i in range(len(words) - 1):
        if words[i] == words[i+1]:
            repetitions += 1
            if len(repetition_samples) < 3 and words[i] not in repetition_samples:
                repetition_samples.append(words[i])
                
    # 3. Fragmented Flow Detection (Short segments)
    total_words = len(words)
    total_segments = len(segments)
    avg_words_per_segment = total_words / max(total_segments, 1)
    
    # 4. Calculate flow score
    # Penalize repetitions, redundancy, and high fragmentation
    flow_penalty = (repetitions * 10) + (redundant_words * 15) + (max(0, 5 - avg_words_per_segment) * 10)
    continuity_score = max(30, 100 - flow_penalty)
    
    flow_pattern = "smooth"
    if continuity_score < 60:
        flow_pattern = "fragmented"
    elif continuity_score < 80:
        flow_pattern = "moderate"
        
    return {
        "continuity_score": round(continuity_score, 2),
        "flow_pattern": flow_pattern,
        "repetitions_count": repetitions,
        "repetition_samples": repetition_samples,
        "avg_words_per_phrase": round(avg_words_per_segment, 1),
        "interpretation": "Repetitive word patterns detected" if repetitions > 1 else "Flow appears natural"
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
        "total_duration": total_duration, # FIXED: Add this so indicators can find it
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
    
    # Deduct for fillers (Stricter: penalty for any fillers)
    if filler_freq > 8:
        confidence_score -= 45
    elif filler_freq > 4:
        confidence_score -= 30
    elif filler_freq > 1:
        confidence_score -= 15
    elif filler_count > 0:
        confidence_score -= 5 # Penalty even for 1 filler
    
    # Extra penalty for clusters (nervous speech)
    if clusters >= 3:
        confidence_score -= 20
    elif clusters >= 1:
        confidence_score -= 10
    
    # Deduct for pauses (distinguish nervous from thoughtful)
    if pause_pattern == "frequent_uncertainty":
        confidence_score -= 40  # Stricter
    elif pause_pattern == "frequent_long_pauses":
        confidence_score -= 30
    elif pause_pattern == "thoughtful":
        confidence_score -= 10  # Natural but still a slight impact
    elif pause_pattern == "moderate_pauses":
        confidence_score -= 20
    
    # Flat penalty for any long pause to prevent 100% scores in imperfect speech
    if long_pauses > 0:
        confidence_score -= (long_pauses * 5)
    
    # Deduct for fragmentation
    if continuity_score < 60:
        confidence_score -= 25
    elif continuity_score < 80:
        confidence_score -= 15
    
    # Penalty for conversational fillers
    conv_count = filler_analysis.get("conversational_count", 0)
    if conv_count > 4:
        confidence_score -= 15
    elif conv_count > 0:
        confidence_score -= 3 # Penalty for even 1 conversational filler
        
    # Penalty for short answers (Professional standard: > 15 words)
    word_count = filler_analysis.get("word_count", 0)
    if word_count < 10:
        confidence_score -= 30
    elif word_count < 20:
        confidence_score -= 15
        
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
        "confidence_score": confidence_score,
        "duration": temporal_analysis.get("total_duration", 0),
        "word_count": filler_analysis.get("word_count", 0)
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
        "faults_detected": [],
        "positive_notes": []
    }
    
    # RAW METRICS SUMMARY (Transparency)
    word_count = filler_analysis.get("word_count", 0)
    total_fillers = filler_analysis.get("total_count", 0) + filler_analysis.get("conversational_count", 0)
    total_pauses = pause_analysis.get("total_pauses", 0)
    confidence = indicators.get("confidence", "Unknown")
    trend = temporal_analysis.get("trend", "stable")
    
    feedback["summary"] = f"Presence Analysis: {word_count} words | {total_fillers} fillers | {total_pauses} pauses"
    
    # Extra performance detail
    feedback["positive_notes"].append(f"Recorded response duration: {indicators.get('duration', 0)} seconds")
    
    # Speech delivery observations with explanations
    filler_count = filler_analysis.get("total_count", 0)
    filler_freq = filler_analysis.get("filler_frequency_percent", 0)
    clusters = filler_analysis.get("clusters", {})
    distribution = filler_analysis.get("distribution", {})
    
    if filler_count > 0:
        filler_words = filler_analysis.get("filler_words_detected", [])
        word_count = filler_analysis.get("word_count", 0)
        obs = f"Speech analysis ({word_count} words): Detected {filler_count} filler word{'s' if filler_count > 1 else ''} "
        if filler_words:
            obs += f"({', '.join(filler_words[:3])})"
            
        exp = f"Specific hesitation sounds used: {', '.join(filler_words)}. Minimizing these will improve clarity."
        
        if clusters.get("level") == "frequent":
            obs += f" with {clusters.get('count')} nervous clusters"
            exp += ". Clusters of fillers suggest periods of significant uncertainty."
        
        feedback["speech_delivery"]["observations"].append(obs)
        feedback["speech_delivery"]["explanations"].append(exp)

    # Conversational fillers
    conv_count = filler_analysis.get("conversational_count", 0)
    if conv_count > 0:
        conv_words = filler_analysis.get("conversational_fillers_detected", [])
        obs = f"Detected {conv_count} conversational filler{'s' if conv_count > 1 else ''} (e.g., '{conv_words[0]}')"
        feedback["speech_delivery"]["observations"].append(obs)
        feedback["speech_delivery"]["explanations"].append("Using too many phrases like 'you know' or 'basically' can reduce professional impact.")

    # Short answer warning
    word_count = filler_analysis.get("word_count", 0)
    if word_count < 15:
        feedback["faults_detected"].append(f"Answer is very brief ({word_count} words). Longer responses demonstrate more depth and confidence.")
    
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
            
    # Broken speech flow (Repetitions)
    repetitions = continuity_analysis.get("repetitions_count", 0)
    if repetitions > 0:
        samples = continuity_analysis.get("repetition_samples", [])
        obs = f"Detected {repetitions} speech repetition{'s' if repetitions > 1 else ''}"
        if samples:
            obs += f" (e.g., '{samples[0]}... {samples[0]}')"
        feedback["speech_delivery"]["observations"].append(obs)
        feedback["speech_delivery"]["explanations"].append("Word repetitions can disrupt the natural flow of your answer.")
    
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
    
    # Faults Detected (Explicitly negative patterns for visibility as requested)
    faults = []
    
    if filler_count > 8:
        suggestions.append("Practice pausing silently instead of using filler words")
        faults.append(f"Too many hesitation words used ({filler_count} fillers). This distracts from your core message.")
    elif filler_count > 5:
        conc = distribution.get("concentration", "")
        if conc == "start":
            suggestions.append("Practice your opening statement to reduce early fillers")
        else:
            suggestions.append("Practice pausing silently instead of using filler words")
    
    if nervous_pauses > 2:
        suggestions.append("Organize your thoughts before speaking to reduce long pauses")
        faults.append(f"Significant long pauses (>2s) multiple times. This may be perceived as a lack of preparation.")
    
    if repetitions > 2:
        faults.append(f"Frequent word/phrase repetitions ({repetitions} detected). This breaks your speech flow.")
        
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
    feedback["faults_detected"] = faults
    
    return feedback
