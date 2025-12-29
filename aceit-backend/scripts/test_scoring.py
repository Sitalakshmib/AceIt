import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from routes.interview import calculate_confidence, SpeechMetrics, VideoMetrics

def test_scenario(name, text, duration, expected_range):
    print(f"\n--- Testing Scenario: {name} ---")
    print(f"Text: '{text[:50]}...' ({len(text.split())} words)")
    
    s_m = SpeechMetrics(audio_duration_seconds=duration)
    v_m = VideoMetrics(face_visible_pct=0.98, looking_away_pct=0.0)
    
    result = calculate_confidence(text, s_m, v_m)
    score = result['score']
    
    print(f"Score: {score}")
    print(f"Breakdown: {result['breakdown']}")
    
    if expected_range[0] <= score <= expected_range[1]:
        print("✅ PASS")
    else:
        print(f"❌ FAIL (Expected {expected_range}, got {score})")

# 1. Perfect Answer
# ~60 words, ~140 WPM, Power words, No fillers
perfect_text = "I successfully managed the project by leading the team through critical challenges. We definitely achieved our goals and optimized the workflow. I believe communication was crucial for this success. I solved complex problems efficiently and delivered results on time."
test_scenario("Perfect Answer", perfect_text, 25, (85, 100))

# 2. Short / Bad Answer
# 5 words, too short
short_text = "I am good at python."
test_scenario("Short Answer", short_text, 5, (0, 50))

# 3. Nervous Answer
# ~50 words, fillers, weak words
nervous_text = "Um, I think I am maybe good at coding. Like, I guess I can solve problems. You know, sort of like that. Uh, basically I try to write code. Actually it is okay."
test_scenario("Nervous Answer", nervous_text, 20, (30, 65))

# 4. Fast Answer
# High WPM
fast_text = "I talk very fast and I want to say everything in a single breath because I am nervous and I do not know when to stop talking so I just keep going and going without pausing."
test_scenario("Fast Answer", fast_text, 10, (40, 80)) # Should have WPM penalty
