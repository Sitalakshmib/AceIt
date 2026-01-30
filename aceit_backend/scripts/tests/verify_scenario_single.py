import os
import sys
import time
import json
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.elite_question_generator import EliteQuestionGenerator

def verify_single():
    load_dotenv()
    generator = EliteQuestionGenerator()
    
    print("⏳ Waiting 20 seconds to clear rate limits...")
    time.sleep(20)
    
    print("🚀 Attempting to generate 1 Scenario-Based Question...")
    
    try:
        q = generator.generate_question(
            category="Quantitative",
            sub_topic="Percentages & Ratios",
            difficulty_level="Medium"
        )
        
        if q:
            print("\n✅ SUCCESS!")
            print(f"Question: {q['question']}")
            print(f"Options: {q['options']}")
            
            if "find" not in q['question'].lower()[:20] and len(q['question']) > 50:
                print("✅ Scenario detected (heuristic)")
            else:
                 print("⚠️ Warning: Question might not be scenario-based?")
                 
        else:
            print("❌ Failed to generate (returned None)")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    verify_single()
