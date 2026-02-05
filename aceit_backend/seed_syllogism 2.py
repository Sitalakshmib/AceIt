import sys
import os
import re
from sqlalchemy.orm import Session
from database_postgres import SessionLocal, engine, Base
from models.aptitude_sql import AptitudeQuestion
import uuid

# Ensure tables exist
Base.metadata.create_all(bind=engine)

def parse_syllogism(text):
    questions = []
    
    # 1. Parse Full Schema Questions (Schema ... Correct Answer)
    # 2. Parse Summary Questions (**Q4:** ...)
    
    # Use split to handle blocks
    
    # First, let's extract the summary questions separately because they are one-liners
    # Regex for summary: **Q(\d+):** Statements: (.*?) Conclusions: (.*?) \*\*Ans: (.*?)\*\*
    
    summary_matches = re.finditer(r'\*\*Q(\d+):\*\*\s*Statements:\s*(.*?)\s*Conclusions:\s*(.*?)\s*\*\*Ans:\s*(.*?)\*\*', text, re.DOTALL)
    
    summary_q_nums = set()
    
    for match in summary_matches:
        q_num = int(match.group(1))
        summary_q_nums.add(q_num)
        
        stmts = match.group(2).strip()
        concls = match.group(3).strip()
        ans_text = match.group(4).strip()
        
        # Construct Question Text
        question_text = f"Statements:\n{stmts}\nConclusions:\n{concls}"
        
        # Construct Standard Options
        options = [
            "Only conclusion I follows",
            "Only conclusion II follows",
            "Either I or II follows",
            "Neither I nor II follows",
            "Both I and II follow"
        ]
        
        # Map Answer to Index
        # "Both follow" -> 4
        # "Neither follows" -> 3
        # "Only I follows" -> 0
        # "Only II follows" -> 1 # Provided explanation suggests II follows in Q1 example, but answer key was 4. 
        # But for Q4 "Ans: Both follow", it maps to Both.
        
        ans_lower = ans_text.lower()
        correct_ans_idx = 0
        
        if "both" in ans_lower:
            correct_ans_idx = 4
        elif "neither" in ans_lower:
            correct_ans_idx = 3
        elif "only conclusion i" in ans_lower or "only i" in ans_lower:
            correct_ans_idx = 0
        elif "only conclusion ii" in ans_lower or "only ii" in ans_lower:
            correct_ans_idx = 1
        elif "either" in ans_lower:
            correct_ans_idx = 2
        else:
            # Fallback or specific parsing
            pass
            
        q = {
            "category": "Logical Ability",
            "topic": "Syllogism",
            "difficulty": "Easy", # Summary questions are in Easy section
            "question": question_text,
            "options": options,
            "correct_answer": correct_ans_idx,
            "answer_explanation": f"Statements: {stmts}. Conclusions: {concls}. Answer: {ans_text}",
            "primary_concepts": ["Syllogism basics"],
            "trap_explanation": None
        }
        questions.append(q)
        
    # Now Parse Full Schema Questions
    # Split by "**Question" or "Question X:" 
    # The text uses "**Question X:**"
    
    blocks = re.split(r'\*\*Question \d+:\*\*', text)
    
    # Skip preamble (block 0) usually
    # But check if block 0 contains schema? regex split consumes delimiter.
    # Actually, let's look for "Schema" keyword to identify blocks.
    
    # We can iterate over blocks and check if they contain "Schema"
    
    for block in blocks:
        if "Schema" not in block:
            continue
            
        try:
            category_match = re.search(r'Category:\s*(.*)', block)
            category = category_match.group(1).strip() if category_match else "Logical Ability"
            
            topic_match = re.search(r'Topic:\s*(.*)', block)
            topic = topic_match.group(1).strip() if topic_match else "Syllogism"
            
            difficulty_match = re.search(r'Difficulty:\s*(.*)', block)
            difficulty = difficulty_match.group(1).strip() if difficulty_match else "Medium"
            
            # Question Body
            q_body_match = re.search(r'Question:(.*?)Options:', block, re.DOTALL)
            question_text = q_body_match.group(1).strip() if q_body_match else ""
            
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
                # 1-based usually
                correct_ans_idx = val - 1
            
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

def seed_syllogism():
    db = SessionLocal()
    
    file_path = os.path.join(os.path.dirname(__file__), 'data', 'syllogism.txt')
    try:
        with open(file_path, 'r') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return

    questions_data = parse_syllogism(text)
    
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
    print(f"Seeded {count} Syllogism questions.")
    db.close()

if __name__ == "__main__":
    seed_syllogism()
