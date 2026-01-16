import requests
import sys
import os
import random
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database_postgres import SessionLocal
from models.aptitude_sql import AptitudeQuestion
from models.user_sql import User

def fetch_hq_questions():
    db = SessionLocal()
    
    # Dataset Configurations
    datasets = [
        {
            "name": "Quant (AQUA-RAT)",
            "url": "https://datasets-server.huggingface.co/rows?dataset=RikoteMaster/aqua-rat-mcqa&config=default&split=train&offset=0&length=100",
            "category": "Quantitative",
            "topic": "advanced_algebra",
            "parser": parse_aqua
        },
        {
            "name": "Logical (LogiQA)",
            "url": "https://datasets-server.huggingface.co/rows?dataset=lucasmccabe/logiqa&config=default&split=train&offset=0&length=100",
            "category": "Logical",
            "topic": "critical_reasoning",
            "parser": parse_logiqa
        },
        {
            "name": "Verbal (CommonsenseQA)",
            "url": "https://datasets-server.huggingface.co/rows?dataset=tau/commonsense_qa&config=default&split=train&offset=0&length=100",
            "category": "Verbal",
            "topic": "common_sense",
            "parser": parse_cqa
        }
    ]
    
    total_added = 0
    
    for ds in datasets:
        print(f"🚀 Fetching {ds['name']} from Hugging Face...")
        try:
            resp = requests.get(ds["url"])
            if resp.status_code != 200:
                print(f"❌ Error fetching {ds['name']}: {resp.status_code} - {resp.text}")
                continue
                
            rows = resp.json().get("rows", [])
            questions_to_add = []
            
            for row in rows:
                data = row["row"]
                try:
                    q_obj = ds["parser"](data, ds["category"], ds["topic"])
                    if q_obj:
                        questions_to_add.append(q_obj)
                except Exception as e:
                    pass # Skip malformed rows
            
            if questions_to_add:
                db.bulk_save_objects(questions_to_add)
                db.commit()
                print(f"✅ Added {len(questions_to_add)} questions to {ds['category']}")
                total_added += len(questions_to_add)
                
            time.sleep(1) # Be nice to HF API
            
        except Exception as e:
            print(f"❌ Failed to process {ds['name']}: {e}")

    print(f"🌟 Total High-Quality Questions Added: {total_added}")
    db.close()

def parse_aqua(data, category, topic):
    # AQUA-RAT: question, choices (list), answer_index (int), explanation
    q_text = data.get("question")
    options = data.get("choices")
    correct_idx = data.get("answer_index")
    explanation = data.get("explanation", "Solution derived from algebraic principles.")
    
    if not q_text or not options or correct_idx is None:
        return None
        
    # Clean options: remove "A.", "B." prefix if present
    clean_options = []
    for opt in options:
        if "." in opt and len(opt) > 2 and opt[1] == ".":
             clean_options.append(opt.split(".", 1)[1].strip())
        else:
             clean_options.append(opt)

    return AptitudeQuestion(
        question=q_text,
        options=clean_options,
        correct_answer=correct_idx,
        answer_explanation=explanation,
        topic=topic,
        category=category,
        difficulty="hard",
        source="huggingface_aqua"
    )

def parse_logiqa(data, category, topic):
    # LogiQA: context, query, options (list), correct_option (int)
    context = data.get("context", "")
    query = data.get("query", "")
    full_question = f"{context}\n\n{query}".strip()
    options = data.get("options")
    label = data.get("correct_option")
    
    if not full_question or not options or label is None:
        return None

    return AptitudeQuestion(
        question=full_question,
        options=options,
        correct_answer=int(label),
        answer_explanation="Logical deduction required.",
        topic=topic,
        category=category,
        difficulty="hard",
        source="huggingface_logiqa"
    )

def parse_cqa(data, category, topic):
    # CommonsenseQA: question, choices { "label": ["A","B"], "text": ["opt1", "opt2"] }, answerKey (label)
    q_text = data.get("question")
    choices = data.get("choices")
    answer_key = data.get("answerKey") # 'A', 'B'...
    
    if not q_text or not choices or not answer_key:
        return None
        
    options = choices.get("text", [])
    labels = choices.get("label", [])
    
    if not options:
        return None
        
    try:
        correct_idx = labels.index(answer_key)
    except ValueError:
        correct_idx = 0
        
    return AptitudeQuestion(
        question=q_text,
        options=options,
        correct_answer=correct_idx,
        answer_explanation="Based on common sense reasoning.",
        topic=topic,
        category=category,
        difficulty="medium",
        source="huggingface_cqa"
    )

if __name__ == "__main__":
    fetch_hq_questions()
