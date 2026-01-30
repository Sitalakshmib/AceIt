"""
Generate Scenario-Based Aptitude Questions
==========================================

This script uses the EliteQuestionGenerator to create scenario-based questions
for all categories and difficulty levels defined in the taxonomy.

It iterates through:
- Each Category
- Each Topic
- Each Difficulty (Easy, Medium, Hard)

And prints the generated questions to the console (and optionally saves to JSON).
"""

import sys
import os
import json
import time

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from services.elite_question_generator import EliteQuestionGenerator
from services.question_taxonomy import APTITUDE_TAXONOMY

def generate_full_suite(questions_per_level=1):
    """
    Generate questions for every topic in the taxonomy.
    """
    generator = EliteQuestionGenerator()
    
    difficulties = ["Easy", "Medium", "Hard"]
    
    total_generated = 0
    results_log = []
    
    print("="*60)
    print("🚀 STARTING SCENARIO-BASED QUESTION GENERATION")
    print("="*60)
    
    for category, topics in APTITUDE_TAXONOMY.items():
        print(f"\n📁 CATEGORY: {category}")
        
        for topic in topics.keys():
            print(f"  🔹 TOPIC: {topic}")
            
            for difficulty in difficulties:
                print(f"    👉 Generating {difficulty}...", end="", flush=True)
                
                for i in range(questions_per_level):
                    try:
                        # Generate
                        q_data = generator.generate_question(
                            category=category,
                            sub_topic=topic,
                            difficulty_level=difficulty
                        )
                        
                        if q_data:
                            print(" ✅", end="", flush=True)
                            total_generated += 1
                            
                            # Add metadata
                            q_data["_meta"] = {
                                "generated_at": time.time(),
                                "category": category,
                                "topic": topic
                            }
                            results_log.append(q_data)
                            
                            # Print preview of scenario
                            scenario_preview = q_data['question'].split('.')[0] + "..."
                            print(f"\n       📝 Scenario: {scenario_preview[:60]}")
                            
                        else:
                            print(" ❌", end="", flush=True)
                            
                    except Exception as e:
                        print(f" ⚠️ Error: {e}", end="", flush=True)
                        
                print() # Newline after difficulty batch
                
    # Save to file
    output_file = "generated_scenarios.json"
    with open(output_file, "w") as f:
        json.dump(results_log, f, indent=2)
        
    print("\n" + "="*60)
    print(f"🎉 GENERATION COMPLETE")
    print(f"Total Questions: {total_generated}")
    print(f"Saved to: {output_file}")
    print("="*60)

if __name__ == "__main__":
    # You can run this with: python3 scripts/generate_questions_scenario.py
    generate_full_suite(questions_per_level=1)
