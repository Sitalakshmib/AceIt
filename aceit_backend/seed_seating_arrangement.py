import sys
import os
import re
from sqlalchemy.orm import Session
from database_postgres import SessionLocal, engine, Base
from models.aptitude_sql import AptitudeQuestion
import uuid

# Ensure tables exist
Base.metadata.create_all(bind=engine)

def parse_seating_arrangement(text):
    questions = []
    # Split by "**Question digit:**" pattern
    blocks = re.split(r'\*\*Question \d+:\*\*', text)
    
    for block in blocks:
        if not block.strip():
            continue
            
        try:
            category = "Logical Ability"
            topic = "Seating Arrangement"
            difficulty = "Medium" # Default
            
            # Check for header-based difficulty assumption or just use default
            # The user provided text has "Difficulty: Easy", "Difficulty: Medium", "Difficulty: Hard" headers.
            # But the split might have consumed them or left them attached to previous/current block.
            # We can try to detect them. 
            # Actually, since the split is by Question X, the headers "Difficulty: ..." usually appear BEFORE a question.
            # So "Difficulty: Medium (Continued)" might be at the end of the previous block?
            # Or inside the block? 
            # In the user text:
            # ## Difficulty: Easy (Continued)
            # **Question 9:** ...
            # So the header is BEFORE Question 9.
            # The split consumes "Question 9:", so the header is in the "preamble" or previous block?
            # Actually, the split leaves the "preamble" in the first block (index 0).
            # But subsequent headers (Medium, Hard) will be embedded in the block of the preceding question?
            # E.g. Block for Q20 will contain "Question 20... \n\n ## Difficulty: Medium... \n\n" ? 
            # No, "Question 28" starts the next section.
            # So the block for Q20 ends, then "Difficulty: Medium" appears, then "Question 28" starts.
            # The split is `\*\*Question \d+:\*\*`.
            # So the text `...Answer Explanation... \n\n ## Difficulty: Medium \n\n` will be at the end of the Q20 block.
            # We can regex search for "Difficulty: X" in each block to set the *next* questions' difficulty?
            # Or simpler:
            # Q9-27: Easy ? (User says Easy Continued)
            # Q28-60: Medium ?
            # Q61-80: Hard ?
            # Based on the user provided numbers:
            # Easy: 9-20.
            # Medium: 28-40.
            # Hard: 61-80.
            # We can use the question number to set difficulty.
            
            # Extract question number from the block?
            # The split removes the delimiter. So we don't have the number easily unless we capture it.
            # Let's change split to capture.
            pass
        except:
            pass
            
    # Re-implement with capture split to get Question Numbers
    
    # Split keeping the delimiter
    parts = re.split(r'(\*\*Question \d+:\*\*)', text)
    # parts[0] is preamble. parts[1] is "Question 9:", parts[2] is body. parts[3] is "Question 10:", parts[4] is body...
    
    current_difficulty = "Easy" # Default start
    
    for i in range(1, len(parts), 2):
        header = parts[i] # "**Question 9:**"
        body = parts[i+1]
        
        # Check if body contains a new Difficulty Header at the END (which belongs to next section)?
        # Actually headers "Difficulty: Medium" usually appear *before* the questions.
        # So it would be in parts[i-1] (the end of previous body).
        # We can check parts[i-1] for difficulty change strings.
        
        prev_text = parts[i-1]
        if "Difficulty: Easy" in prev_text:
            current_difficulty = "Easy"
        elif "Difficulty: Medium" in prev_text:
            current_difficulty = "Medium"
        elif "Difficulty: Hard" in prev_text:
            current_difficulty = "Hard"
            
        # Extract Question Number
        q_num_match = re.search(r'\d+', header)
        q_num = int(q_num_match.group(0)) if q_num_match else 0
        
        # Manual override based on range if detection fails
        if 1 <= q_num <= 27:
            current_difficulty = "Easy"
        elif 28 <= q_num <= 60:
            current_difficulty = "Medium"
        elif 61 <= q_num <= 80:
            current_difficulty = "Hard"
            
        try:
            # Question Text
            # Format: [Question Text] Options: ...
            q_text_match = re.search(r'(.*?)Options:', body, re.DOTALL)
            question_text = q_text_match.group(1).strip() if q_text_match else ""
            
            if not question_text:
                continue

            # Options
            # Format: 1) A ... 2) B ...
            options = []
            opts_text_match = re.search(r'Options:(.*?)\*\*Correct Answer:', body, re.DOTALL)
            if opts_text_match:
                opts_text = opts_text_match.group(1).strip()
                # Split by number paranthesis "1) ", "2) "
                # Regex split?
                # options = re.split(r'\d+\)\s*', opts_text)
                # This leaves empty string at start.
                # Also handles single line options?
                # User format:
                # 1) Alia
                # 2) Bina
                # ...
                # Let's clean lines.
                lines = [l.strip() for l in opts_text.split('\n') if l.strip()]
                for line in lines:
                    # Remove "1) " prefix
                    clean = re.sub(r'^\d+\)\s*', '', line)
                    options.append(clean)
            
            # Correct Answer
            # Format: **Correct Answer:** 3
            correct_ans_idx = 0
            ans_match = re.search(r'\*\*Correct Answer:\*\*\s*(\d+)', body)
            if ans_match:
                val = int(ans_match.group(1))
                correct_ans_idx = val - 1
            
            # Explanation
            expl_match = re.search(r'\*\*Answer Explanation:\*\*\s*(.*?)(?:\*\*Primary Concepts|$)', body, re.DOTALL)
            explanation = expl_match.group(1).strip() if expl_match else ""
            
            # Concepts
            concepts = []
            conc_match = re.search(r'\*\*Primary Concepts:\*\*\s*(.*?)(?:\*\*Elite Traps|$)', body, re.DOTALL)
            if conc_match:
                c_text = conc_match.group(1).strip()
                concepts = [c.strip() for c in c_text.split(',')]
            
            # Traps
            trap = None
            trap_match = re.search(r'\*\*Elite Traps:\*\*\s*(.*?)$', body, re.DOTALL)
            if trap_match:
                trap = trap_match.group(1).strip()

            q = {
                "category": category,
                "topic": topic,
                "difficulty": current_difficulty,
                "question": question_text,
                "options": options,
                "correct_answer": correct_ans_idx,
                "answer_explanation": explanation,
                "primary_concepts": concepts,
                "trap_explanation": trap
            }
            questions.append(q)

        except Exception as e:
            print(f"Skipping Q{q_num}: {e}")
            continue
            
    return questions

def seed_seating():
    db = SessionLocal()
    
    file_path = os.path.join(os.path.dirname(__file__), 'data', 'seating_arrangement.txt')
    try:
        with open(file_path, 'r') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return

    questions_data = parse_seating_arrangement(text)
    
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
    print(f"Seeded {count} Seating Arrangement questions.")
    db.close()

if __name__ == "__main__":
    seed_seating()
