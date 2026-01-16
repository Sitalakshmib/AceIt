import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_postgres import SessionLocal, engine
from models.aptitude_sql import AptitudeQuestion, Base
from models.user_sql import User # Required for ForeignKey resolution
from massive_database import massive_db
import random

def seed_aptitude_database():
    db = SessionLocal()
    
    print("🗑️  Cleaning up existing aptitude tables...")
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Clear existing questions to avoid duplicates on re-run
    db.query(AptitudeQuestion).delete()
    db.commit()
    
    questions_to_add = []
    
    print("🧮 Generating QUANTITATIVE questions...")
    # Load from massive_db (which generates them)
    quant_questions = massive_db.datasets["aptitude"]
    for q in quant_questions:
        questions_to_add.append(AptitudeQuestion(
            question=q["question"],
            options=q["options"],
            correct_answer=q["correct_answer"],
            answer_explanation=q["explanation"],
            topic=q["topic"],
            category="Quantitative",
            difficulty=q["difficulty"],
            source="generated"
        ))
        
    print("🧮 Generating ADDITIONAL QUANTITATIVE questions...")
    # New Quant Topics
    quant_topics = ["problems_on_trains", "time_and_distance", "simple_interest"]
    for _ in range(600): # 200 per topic
        topic = random.choice(quant_topics)
        difficulty = random.choice(["easy", "medium", "hard"])
        q_data = generate_quant_question(topic, difficulty)
        questions_to_add.append(AptitudeQuestion(
             question=q_data["question"],
            options=q_data["options"],
            correct_answer=q_data["correct_answer"],
            answer_explanation=q_data["explanation"],
            topic=topic,
            category="Quantitative",
            difficulty=difficulty,
            source="generated"
        ))

    print("🧩 Generating ADDITIONAL LOGICAL REASONING questions...")
    # Enhanced Logical Topics
    logical_topics = ["blood_relations", "coding_decoding", "direction_sense", "number_series", "syllogism", "seating_arrangement"]
    
    for _ in range(900): # 150 per topic
        topic = random.choice(logical_topics)
        difficulty = random.choice(["easy", "medium", "hard"])
        
        q_data = generate_logical_question(topic, difficulty)
        questions_to_add.append(AptitudeQuestion(
            question=q_data["question"],
            options=q_data["options"],
            correct_answer=q_data["correct_answer"],
            answer_explanation=q_data["explanation"],
            topic=topic,
            category="Logical",
            difficulty=difficulty,
            source="generated"
        ))

    print("📖 Generating ADDITIONAL VERBAL ABILITY questions...")
    # Enhanced Verbal Topics
    verbal_topics = ["synonyms", "antonyms", "sentence_correction", "idioms_and_phrases", "one_word_substitution"]
    
    for _ in range(750): # 150 per topic
        topic = random.choice(verbal_topics)
        difficulty = random.choice(["easy", "medium", "hard"])
        
        q_data = generate_verbal_question(topic, difficulty)
        questions_to_add.append(AptitudeQuestion(
            question=q_data["question"],
            options=q_data["options"],
            correct_answer=q_data["correct_answer"],
            answer_explanation=q_data["explanation"],
            topic=topic,
            category="Verbal",
            difficulty=difficulty,
            source="generated"
        ))
    
    print(f"💾 Saving {len(questions_to_add)} questions to database...")
    # Bulk insert
    db.bulk_save_objects(questions_to_add)
    db.commit()
    print("✅ Aptitude database seeded successfully!")
    db.close()

def generate_quant_question(topic, difficulty):
    if topic == "problems_on_trains":
        speed = random.randint(36, 108) # km/hr, divisible by 18 for m/s
        length = random.randint(100, 500)
        time_sec = (length / (speed * 5/18)) 
        
        question = f"A train {length}m long is running at a speed of {speed} km/hr. In how much time will it pass a pole?"
        ans = round(time_sec, 2)
        options = [f"{ans} sec", f"{ans+5} sec", f"{ans-2} sec", f"{ans*2} sec"]
        return {
            "question": question,
            "options": options,
            "correct_answer": 0,
            "explanation": f"Speed = {speed} * 5/18 = {speed*5/18} m/s. Time = Distance/Speed = {length}/{speed*5/18} = {ans} sec."
        }
    elif topic == "time_and_distance":
        speed = random.randint(40, 100)
        time = random.randint(2, 10)
        dist = speed * time
        question = f"A car covers a distance in {time} hours at a speed of {speed} km/hr. What is the distance?"
        options = [f"{dist} km", f"{dist+20} km", f"{dist-10} km", f"{dist*2} km"]
        return {
             "question": question,
            "options": options,
            "correct_answer": 0,
            "explanation": f"Distance = Speed x Time = {speed} x {time} = {dist} km."
        }
    else: # simple_interest
        p = random.randint(1000, 10000)
        r = random.randint(5, 15)
        t = random.randint(2, 5)
        si = (p * r * t) / 100
        question = f"Calculate the Simple Interest on Rs. {p} at {r}% per annum for {t} years."
        options = [f"Rs. {si}", f"Rs. {si+100}", f"Rs. {si-50}", f"Rs. {si*2}"]
        return {
            "question": question,
             "options": options,
            "correct_answer": 0,
            "explanation": f"SI = (P*R*T)/100 = ({p}*{r}*{t})/100 = {si}."
        }

def generate_logical_question(topic, difficulty):
    # Expanded Logical Generators
    if topic == "number_series":
        start = random.randint(1, 10)
        diff = random.randint(2, 5)
        series = [start + i*diff for i in range(5)]
        question = f"Find the next number in method series: {series[0]}, {series[1]}, {series[2]}, {series[3]}, ...?"
        ans = series[4]
        options = [str(ans), str(ans+1), str(ans-1), str(ans+2)]
        return {
             "question": question,
            "options": options,
            "correct_answer": 0,
            "explanation": f"The series increases by {diff} each step."
        }
    elif topic == "syllogism":
        question = "Statement:\n1. All cars are cats.\n2. All cats are bats.\nConclusion:\nI. All cars are bats.\nII. Some bats are cars."
        options = ["Only I follows", "Only II follows", "Both I and II follow", "Neither follows"]
        return {
            "question": question,
            "options": options,
            "correct_answer": 2,
            "explanation": "Standard syllogism logic: A->B, B->C => A->C."
        }
    elif topic == "seating_arrangement":
        question = "A, B, C, D, E are sitting in a row. A is at the extreme right. B is second to left of A. Who is sitting to the immediate right of B?"
        options = ["C", "D", "E", "Can't be determined"]
        return {
            "question": question,
            "options": options,
            "correct_answer": 3, 
            "explanation": "We only know A is extreme right (Position 5) and B is 2nd left of A (Position 3). Pos 4 could be C, D, or E."
        }
    # Fallback to existing logic for basic topics
    elif topic == "blood_relations":
        relations = ["father", "mother", "brother", "sister", "uncle", "aunt"]
        p1 = "A"
        p2 = "B"
        rel = random.choice(relations)
        question = f"If {p1} is the {rel} of {p2}, how is {p2} related to {p1}?"
        options = ["Son/Daughter", "Father/Mother", "Nephew/Niece", "Cousin"]
        return {
            "question": question,
            "options": options,
            "correct_answer": 0,
            "explanation": f"Standard blood relation."
        }
    elif topic == "coding_decoding":
         word = random.choice(["APPLE", "MANGO", "TIGER", "EARTH"])
         shift = 1
         coded = "".join([chr(ord(c) + shift) for c in word])
         question = f"{word} is coded as {coded}. Pattern?"
         options = ["+1 shift", "-1 shift", "Reverse", "Shuffle"]
         return {
             "question": question,
             "options": options,
             "correct_answer": 0,
             "explanation": "+1 shift logic."
         }
    else: # direction_sense
         return {
             "question": "Walk 5km North, turn Right. Heading?",
             "options": ["East", "West", "North", "South"],
             "correct_answer": 0,
             "explanation": "Right of North is East."
         }

def generate_verbal_question(topic, difficulty):
    if topic == "idioms_and_phrases":
        idioms = [("Once in a blue moon", "Very rarely"), ("Piece of cake", "Very easy"), ("Break a leg", "Good luck")]
        idiom, meaning = random.choice(idioms)
        question = f"Meaning of idiom: '{idiom}'?"
        options = [meaning, "Frequently", "Difficult task", "Bad luck"]
        random.shuffle(options)
        return {
            "question": question,
            "options": options,
            "correct_answer": options.index(meaning),
            "explanation": f"'{idiom}' means {meaning}."
        }
    elif topic == "one_word_substitution":
        subs = [("A person who loves books", "Bibliophile"), ("Life history written by self", "Autobiography"), ("Sound of Lions", "Roar")]
        phrase, word = random.choice(subs)
        question = f"One word for: '{phrase}'?"
        options = [word, "Biography", "Democracy", "Somnambulist"]
        random.shuffle(options)
        return {
            "question": question,
            "options": options,
            "correct_answer": options.index(word),
            "explanation": f"Definition of {word}."
        }
    # Fallback to existing
    elif topic == "synonyms":
        word_pairs = [("HAPPY", "JOYFUL"), ("SAD", "UNHAPPY"), ("BIG", "HUGE"), ("FAST", "QUICK")]
        word, syn = random.choice(word_pairs)
        question = f"Synonym for: {word}"
        options = [syn, "OPPOSITE", "UNAFFECTED", "DIFFERENT"]
        random.shuffle(options)
        return {
            "question": question,
            "options": options,
            "correct_answer": options.index(syn),
            "explanation": f"{syn} means {word}."
        }
    elif topic == "antonyms":
        word_pairs = [("GOOD", "BAD"), ("HOT", "COLD"), ("DAY", "NIGHT")]
        word, ant = random.choice(word_pairs)
        question = f"Antonym for: {word}"
        options = [ant, "SYNONYM", "SIMILAR", "RELATED"]
        random.shuffle(options)
        return {
            "question": question,
            "options": options,
            "correct_answer": options.index(ant),
            "explanation": f"Opposite of {word} is {ant}."
        }
    else: # sentence_correction
        return {
            "question": "Identify correct sentence:",
            "options": ["He run fast.", "He runs fast.", "He running fast.", "He ran fastly."],
            "correct_answer": 1,
            "explanation": "Subject-verb agreement."
        }

if __name__ == "__main__":
    seed_aptitude_database()
