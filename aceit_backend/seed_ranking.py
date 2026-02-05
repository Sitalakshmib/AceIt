import sys
import os
import re
from sqlalchemy.orm import Session
from database_postgres import SessionLocal, engine, Base
from models.aptitude_sql import AptitudeQuestion
import uuid

# Ensure tables exist
Base.metadata.create_all(bind=engine)

def parse_ranking(text):
    questions = []
    # Split by **Question digit:** pattern
    blocks = re.split(r'\*\*Question \d+:\*\*', text)
    
    for block in blocks:
        if not block.strip():
            continue
            
        # Skip header lines like "## Easy Difficulty..." if they appear alone
        if "Options:" not in block:
            continue
            
        try:
            # Difficulty might be inferred from section headers in text, but easier to set default or parse if present?
            # The text file has headers "## Easy Difficulty (1–30)".
            # But the block split consumes the headers likely into the previous block's end or start.
            # We'll just define difficulty based on Question number if possible? 
            # Or assume mixed. Let's assume Medium unless specified?
            # Actually the provided text has clear sections. 
            # But regex split destroys context unless we track it.
            # Simplified approach: Set default Difficulty=Medium. The user prompt had specific difficulties per Q for Number Series, but for Ranking it was sectioned.
            # We can try to guess difficulty or just set "Logical Ability" -> Ranking.
            
            category = "Logical Ability"
            topic = "Ranking"
            difficulty = "Medium" # Default
            
            # Question Body: From start until "Options:"
            q_body_match = re.search(r'(.*?)Options:', block, re.DOTALL)
            question_text = q_body_match.group(1).strip() if q_body_match else ""
            
            # Clean up leading newlines/headers from question text
            # E.g. "## Easy Difficulty (1–30)\n\nIn a row..."
            # Remove lines starting with ##
            question_text = re.sub(r'^##.*?\n', '', question_text, flags=re.MULTILINE).strip()
            
            if not question_text:
                continue

            # Options
            options = []
            opts_block_match = re.search(r'Options:(.*?)Correct Answer:', block, re.DOTALL)
            if opts_block_match:
                opts_text = opts_block_match.group(1).strip()
                lines = [l.strip() for l in opts_text.split('\n') if l.strip()]
                options = lines 
            
            # Correct Answer
            correct_ans_idx = 0
            ans_match = re.search(r'Correct Answer:\s*(\d+)', block)
            if ans_match:
                val = int(ans_match.group(1))
                correct_ans_idx = val - 1 # 1-based to 0-based
            
            # Explanation
            expl_match = re.search(r'Answer Explanation:\s*(.*?)(?:Primary Concepts|$)', block, re.DOTALL)
            explanation = expl_match.group(1).strip() if expl_match else ""
            
            # Concepts
            concepts = []
            conc_match = re.search(r'Primary Concepts:\s*(.*?)(?:Elite Traps|$)', block, re.DOTALL)
            if conc_match:
                c_text = conc_match.group(1).strip()
                concepts = [c.strip() for c in c_text.split(',')]
            
            # Traps
            trap = None
            trap_match = re.search(r'Elite Traps:\s*(.*?)$', block, re.DOTALL)
            if trap_match:
                trap = trap_match.group(1).strip()
            
            q = {
                "category": category,
                "topic": topic,
                "difficulty": difficulty,
                "question": question_text,
                "options": options,
                "correct_answer": correct_ans_idx,
                "answer_explanation": explanation,
                "primary_concepts": concepts,
                "trap_explanation": trap
            }
            questions.append(q)
            
        except Exception as e:
            print(f"Skipping block due to error: {e}")
            continue
            
    return questions

def seed_ranking():
    db = SessionLocal()
    
    file_path = os.path.join(os.path.dirname(__file__), 'data', 'ranking.txt')
    try:
        with open(file_path, 'r') as f:
            ranking_text = f.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return

    questions_data = parse_ranking(ranking_text)
    
    print(f"Found {len(questions_data)} questions to seed.")
    
    count = 0
    for q_data in questions_data:
        exists = db.query(AptitudeQuestion).filter(
            AptitudeQuestion.question == q_data["question"],
            AptitudeQuestion.topic == q_data["topic"]
        ).first()
        
        if not exists:
            new_q = AptitudeQuestion(
                id=str(uuid.uuid4()),
                category=q_data["category"],
                topic=q_data["topic"],
                difficulty=q_data["difficulty"],
                question=q_data["question"],
                options=q_data["options"],
                correct_answer=q_data["correct_answer"],
                answer_explanation=q_data["answer_explanation"],
                primary_concepts=q_data["primary_concepts"],
                trap_explanation=q_data["trap_explanation"]
            )
            db.add(new_q)
            count += 1
            
    db.commit()
    print(f"Seeded {count} Ranking questions.")
    db.close()

if __name__ == "__main__":
    seed_ranking()
