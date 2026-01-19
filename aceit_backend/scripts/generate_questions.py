
import os
import sys
import json
import time
import re
from typing import List, Dict

# Add backend to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_postgres import SessionLocal
from models.aptitude_sql import AptitudeQuestion
from services.llm_client import LLMClient

# Topics Configuration
TOPICS = {
    "Quantitative Aptitude": [
        "Number System", "HCF and LCM", "Percentages", "Profit and Loss", 
        "Simple Interest", "Compound Interest", "Time and Work", 
        "Speed, Time and Distance", "Trains", "Boats and Streams"
    ],
    "Logical Reasoning": [
        "Series Completion", "Coding-Decoding", "Blood Relations", 
        "Direction Sense", "Seating Arrangement", "Syllogism"
    ],
    "Verbal Ability": [
        "Synonyms", "Antonyms", "Spotting Errors", "Sentence Correction",
        "Reading Comprehension", "Idioms and Phrases"
    ]
}

def clean_json_response(text: str) -> str:
    """Clean markdown code blocks from response"""
    text = text.strip()
    # Remove ```json ... ``` wrapper
    if text.startswith("```"):
        text = re.sub(r"^```(\w+)?", "", text)
        text = re.sub(r"```$", "", text)
    return text.strip()

def generate_topic_questions(llm: LLMClient, category: str, topic: str, counts: Dict[str, int]) -> List[Dict]:
    total_count = sum(counts.values())
    breakdown_str = ", ".join([f"{v} {k}" for k, v in counts.items()])
    
    prompt = f"""
    Generate {total_count} unique aptitude questions for the topic '{topic}' in the category '{category}'.
    
    Difficulty Breakdown: {breakdown_str}.
    
    IMPORTANT: The questions should be in the style of professional aptitude training sites.
    - Clear, concise, standard for competitive exams.
    
    Output MUST be valid, raw JSON. Do NOT use markdown code blocks.
    Do not include any text before or after the JSON.
    
    The JSON must be an ARRAY of objects with this EXACT structure:
    [
        {{
            "question": "The question text here?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct_answer_index": 0,
            "explanation": "Detailed explanation.",
            "difficulty": "easy"  // or "medium" or "hard"
        }}
    ]
    
    Rules:
    1. options must be a list of 4 strings.
    2. correct_answer_index must be an integer (0-3).
    3. difficulty must be exactly "easy", "medium", or "hard", matching the requested breakdown.
    4. NO trailing commas.
    """
    
    print(f"Requesting {breakdown_str} questions for {topic}...")
    try:
        response_text = llm.generate_response(prompt)
        if not response_text:
            print("Empty response from LLM")
            return []
            
        clean_text = clean_json_response(response_text)
        questions = json.loads(clean_text)
        
        if isinstance(questions, list):
            return questions
        else:
            print("LLM response was not a list")
            return []
            
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        return []
    except Exception as e:
        print(f"Error generating questions: {e}")
        return []

def save_questions(db, questions: List[Dict], category: str, topic: str):
    count = 0
    for q_data in questions:
        try:
            # Basic validation
            if not all(k in q_data for k in ["question", "options", "correct_answer_index", "explanation", "difficulty"]):
                # Maybe map difficulty if missing?
                if "difficulty" not in q_data:
                    q_data["difficulty"] = "medium" # Default
                else: 
                     print("Skipping invalid question format")
                     continue
                
            # Duplicate check (simple)
            exists = db.query(AptitudeQuestion).filter(AptitudeQuestion.question == q_data["question"]).first()
            if exists:
                continue
                
            new_q = AptitudeQuestion(
                category=category,
                topic=topic,
                difficulty=q_data["difficulty"].lower(),
                question=q_data["question"],
                options=q_data["options"],
                correct_answer=int(q_data["correct_answer_index"]),
                answer_explanation=q_data["explanation"]
            )
            db.add(new_q)
            count += 1
        except Exception as e:
            print(f"Error saving question: {e}")
            
    if count > 0:
        db.commit()
        print(f"Saved {count} new questions to DB.")
    else:
        print("No questions saved.")

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Generate Aptitude Questions using Gemini')
    parser.add_argument('--limit', type=int, default=1000, help='Max questions to add per session')
    parser.add_argument('--dry-run', action='store_true', help='Do not save to DB')
    args = parser.parse_args()

    print(f"Initializing Question Generator (Limit: {args.limit})...")
    try:
        llm = LLMClient()
    except Exception as e:
        print(f"Failed to init LLM: {e}")
        return

    db = SessionLocal()
    
    total_added = 0
    
    # Configuration
    # We want ~30 questions per topic (10 easy, 10 medium, 10 hard)
    # Total topics = 22. 22 * 30 = 660 questions.
    # Requests = 22. Should fit in 20/day limit? 
    # If limit is strictly 20, we miss 2 topics.
    # We can ask for 40 questions per topic for the first 15 topics?
    
    # Increase count per request to maximize yield per API call
    COUNTS = {"easy": 15, "medium": 20, "hard": 15} # 50 per request
    
    try:
        for category, topic_list in TOPICS.items():
            if total_added >= args.limit: break
            print(f"\n--- Processing Category: {category} ---")
            
            for topic in topic_list:
                if total_added >= args.limit: break
                
                generated_qs = generate_topic_questions(llm, category, topic, COUNTS)
                
                if generated_qs:
                    if not args.dry_run:
                        save_questions(db, generated_qs, category, topic)
                    else:
                        print(f"[Dry Run] Would save {len(generated_qs)} questions")
                    
                    total_added += len(generated_qs)
                    print(f"Total Added Session: {total_added}")
                
                # Sleep to respect rate limits
                time.sleep(10) 
                        
    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Saving progress...")
    finally:
        db.close()
        print(f"\nDone. Total questions added this session: {total_added}")

if __name__ == "__main__":
    main()
