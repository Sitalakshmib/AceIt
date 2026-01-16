import requests
import html
import random
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import time 
from database_postgres import SessionLocal
from models.aptitude_sql import AptitudeQuestion
from models.user_sql import User # Fixed: Import User model

def fetch_and_seed_opentdb():
    db = SessionLocal()
    
    # Configuration: (OpenTDB Category ID, Our Category Name, Our Topic Name)
    sources = [
        (19, "Quantitative", "mathematics"), # Science: Mathematics
        (18, "Logical", "computer_science"), # Science: Computers (Technical Logic)
        (9, "Verbal", "general_knowledge"),   # General Knowledge
        (17, "Quantitative", "science_nature") # Science & Nature
    ]
    
    total_added = 0
    
    for cat_id, category, topic_base in sources:
        print(f"🌍 Fetching from OpenTDB: Category {cat_id} ({category})...")
        time.sleep(5) # Rate limit: 1 req per 5 sec
        
        # Fetch 20 questions (more reliable than 50)
        url = f"https://opentdb.com/api.php?amount=20&category={cat_id}&type=multiple"
        
        try:
            resp = requests.get(url)
            data = resp.json()
            
            if data["response_code"] != 0:
                print(f"⚠️ API Error for category {cat_id}: Code {data['response_code']}")
                continue
                
            results = data["results"]
            questions_to_add = []
            
            for item in results:
                # OpenTDB returns HTML entities, need to decode
                question_text = html.unescape(item["question"])
                correct_ans = html.unescape(item["correct_answer"])
                incorrect_ans = [html.unescape(ans) for ans in item["incorrect_answers"]]
                
                # Create options list and shuffle
                options = incorrect_ans + [correct_ans]
                random.shuffle(options)
                
                # Find new index of correct answer
                correct_index = options.index(correct_ans)
                
                difficulty = item["difficulty"] # easy, medium, hard matches our schema!
                
                q = AptitudeQuestion(
                    question=question_text,
                    options=options,
                    correct_answer=correct_index,
                    answer_explanation=f"Correct Answer: {correct_ans}", # OpenTDB doesn't give explanations
                    topic=topic_base,
                    category=category,
                    difficulty=difficulty,
                    source="opentdb"
                )
                questions_to_add.append(q)
            
            # Save batch
            db.bulk_save_objects(questions_to_add)
            db.commit()
            print(f"✅ Added {len(questions_to_add)} questions for {category}/{topic_base}")
            total_added += len(questions_to_add)
            
        except Exception as e:
            print(f"❌ Failed to fetch/save category {cat_id}: {e}")
            
    print(f"🎉 Total new questions added from OpenTDB: {total_added}")
    db.close()

if __name__ == "__main__":
    fetch_and_seed_opentdb()
