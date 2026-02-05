import sys
import os
import re
from sqlalchemy.orm import Session
from database_postgres import SessionLocal, engine, Base
from models.aptitude_sql import AptitudeQuestion
import uuid

# Ensure tables exist
Base.metadata.create_all(bind=engine)

def parse_number_series(text):
    questions = []
    # Split by ### **Question digit:** pattern
    blocks = re.split(r'### \*\*Question \d+:\*\*', text)
    
    for block in blocks:
        if not block.strip():
            continue
            
        try:
            # Basic info
            category_match = re.search(r'Category:\s*(.*)', block)
            category = category_match.group(1).strip() if category_match else "Logical Ability"
            
            topic_match = re.search(r'Topic:\s*(.*)', block)
            topic = topic_match.group(1).strip() if topic_match else "Number Series"
            
            difficulty_match = re.search(r'Difficulty:\s*(.*)', block)
            difficulty = difficulty_match.group(1).strip() if difficulty_match else "Medium"
            
            # Question text
            q_match = re.search(r'\*\*Question:\*\*\s*(.*?)\n', block)
            question_text = q_match.group(1).strip() if q_match else ""
            if not question_text:
                continue

            # Options
            options = []
            opts_block_match = re.search(r'\*\*Options:\*\*(.*?)\*\*Correct Answer:', block, re.DOTALL)
            if opts_block_match:
                opts_text = opts_block_match.group(1).strip()
                # Parse numbered options 1. 11  2. 12 etc
                # Regex to find digit dot value
                # Or just split by newline and strip "1. "
                lines = [l.strip() for l in opts_text.split('\n') if l.strip()]
                for line in lines:
                    # Remove leading "1. " or "1."
                    clean_line = re.sub(r'^\d+\.\s*', '', line)
                    options.append(clean_line)
            
            # Correct Answer
            correct_ans_idx = 0
            ans_match = re.search(r'\*\*Correct Answer:\*\*\s*(\d+)', block)
            if ans_match:
                val = int(ans_match.group(1))
                # Assuming 1-based index (e.g. 1 means Option 1)
                correct_ans_idx = val - 1
            
            # Explanation
            expl_match = re.search(r'\*\*Answer Explanation:\*\*\s*(.*?)(?:\*\*Primary Concepts|$)', block, re.DOTALL)
            explanation = expl_match.group(1).strip() if expl_match else ""
            
            # Concepts
            concepts = []
            conc_match = re.search(r'\*\*Primary Concepts:\*\*\s*(.*?)(?:\*\*Elite Traps|$)', block, re.DOTALL)
            if conc_match:
                c_text = conc_match.group(1).strip()
                concepts = [c.strip() for c in c_text.split(',')]
            
            # Traps
            trap = None
            trap_match = re.search(r'\*\*Elite Traps:\*\*\s*(.*?)$', block, re.DOTALL)
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

def seed_number_series():
    db = SessionLocal()
    
    # Read from file
    file_path = os.path.join(os.path.dirname(__file__), 'data', 'number_series.txt')
    try:
        with open(file_path, 'r') as f:
            ns_text = f.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return

    questions_data = parse_number_series(ns_text)
    
    print(f"Found {len(questions_data)} questions to seed.")
    
    count = 0
    for q_data in questions_data:
        # Check duplicate by question text
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
    print(f"Seeded {count} Number Series questions.")
    db.close()

if __name__ == "__main__":
    seed_number_series()
