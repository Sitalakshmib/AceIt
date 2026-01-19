"""
Generate thousands of aptitude questions programmatically.
Run this script from the aceit_backend directory:
    python scripts/generate_aptitude_questions.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_postgres import SessionLocal
from models.aptitude_sql import AptitudeQuestion
import random
import uuid

def generate_number_series_questions(count=100):
    """Generate number series questions with various patterns"""
    questions = []
    
    # Pattern generators
    patterns = [
        # Arithmetic progression
        lambda: {
            "pattern": "arithmetic",
            "start": random.randint(2, 20),
            "diff": random.randint(2, 10)
        },
        # Geometric progression
        lambda: {
            "pattern": "geometric",
            "start": random.randint(2, 5),
            "ratio": random.randint(2, 3)
        },
        # Squares
        lambda: {
            "pattern": "squares",
            "start_n": random.randint(1, 10)
        },
        # Cubes
        lambda: {
            "pattern": "cubes",
            "start_n": random.randint(1, 6)
        },
        # Fibonacci-like
        lambda: {
            "pattern": "fibonacci",
            "a": random.randint(1, 5),
            "b": random.randint(1, 5)
        },
        # +1, +2, +3...
        lambda: {
            "pattern": "increasing_diff",
            "start": random.randint(1, 10)
        },
        # *2+1 pattern
        lambda: {
            "pattern": "multiply_add",
            "start": random.randint(1, 5),
            "mult": random.randint(2, 3),
            "add": random.randint(1, 3)
        }
    ]
    
    for i in range(count):
        pattern_gen = random.choice(patterns)
        config = pattern_gen()
        
        if config["pattern"] == "arithmetic":
            series = [config["start"] + j * config["diff"] for j in range(6)]
            answer = series[-1]
            series_display = series[:5]
            explanation = f"This is an arithmetic progression with common difference {config['diff']}. {series_display[-1]} + {config['diff']} = {answer}"
            
        elif config["pattern"] == "geometric":
            series = [config["start"] * (config["ratio"] ** j) for j in range(6)]
            answer = series[-1]
            series_display = series[:5]
            explanation = f"Each number is multiplied by {config['ratio']}. {series_display[-1]} × {config['ratio']} = {answer}"
            
        elif config["pattern"] == "squares":
            series = [(config["start_n"] + j) ** 2 for j in range(6)]
            answer = series[-1]
            series_display = series[:5]
            n = config["start_n"] + 5
            explanation = f"These are perfect squares: {config['start_n']}², {config['start_n']+1}²... {n}² = {answer}"
            
        elif config["pattern"] == "cubes":
            series = [(config["start_n"] + j) ** 3 for j in range(6)]
            answer = series[-1]
            series_display = series[:5]
            n = config["start_n"] + 5
            explanation = f"These are perfect cubes: {config['start_n']}³, {config['start_n']+1}³... {n}³ = {answer}"
            
        elif config["pattern"] == "fibonacci":
            series = [config["a"], config["b"]]
            for _ in range(4):
                series.append(series[-1] + series[-2])
            answer = series[-1]
            series_display = series[:5]
            explanation = f"Each number is the sum of the previous two. {series_display[-2]} + {series_display[-1]} = {answer}"
            
        elif config["pattern"] == "increasing_diff":
            series = [config["start"]]
            for j in range(1, 6):
                series.append(series[-1] + j)
            answer = series[-1]
            series_display = series[:5]
            explanation = f"Differences increase: +1, +2, +3, +4, +5. {series_display[-1]} + 5 = {answer}"
            
        else:  # multiply_add
            series = [config["start"]]
            for _ in range(5):
                series.append(series[-1] * config["mult"] + config["add"])
            answer = series[-1]
            series_display = series[:5]
            explanation = f"Pattern: ×{config['mult']}+{config['add']}. {series_display[-1]} × {config['mult']} + {config['add']} = {answer}"
        
        # Generate options
        options = [str(answer)]
        while len(options) < 4:
            wrong = answer + random.randint(-10, 10)
            if wrong != answer and str(wrong) not in options:
                options.append(str(wrong))
        random.shuffle(options)
        correct_idx = options.index(str(answer))
        
        question_text = f"Find the next number in the series: {', '.join(map(str, series_display))}, ?"
        
        difficulty = random.choice(["easy", "medium", "hard"])
        
        questions.append({
            "question": question_text,
            "options": options,
            "correct_answer": correct_idx,
            "answer_explanation": explanation,
            "topic": "Number Series",
            "category": "Logical Ability",
            "difficulty": difficulty
        })
    
    return questions


def generate_percentage_questions(count=100):
    """Generate percentage calculation questions"""
    questions = []
    
    for i in range(count):
        q_type = random.choice(["basic", "increase", "decrease", "successive", "find_number"])
        
        if q_type == "basic":
            percent = random.choice([5, 10, 15, 20, 25, 30, 40, 50, 75])
            number = random.randint(2, 20) * 10
            answer = (percent * number) // 100
            question_text = f"What is {percent}% of {number}?"
            explanation = f"{percent}% of {number} = ({percent}/100) × {number} = {answer}"
            difficulty = "easy"
            
        elif q_type == "increase":
            original = random.randint(5, 50) * 10
            percent = random.choice([10, 20, 25, 50])
            answer = original + (original * percent // 100)
            question_text = f"If {original} is increased by {percent}%, what is the new value?"
            explanation = f"Increase = {original} × {percent}/100 = {original * percent // 100}. New value = {original} + {original * percent // 100} = {answer}"
            difficulty = "easy"
            
        elif q_type == "decrease":
            original = random.randint(5, 50) * 10
            percent = random.choice([10, 20, 25, 50])
            answer = original - (original * percent // 100)
            question_text = f"If {original} is decreased by {percent}%, what is the new value?"
            explanation = f"Decrease = {original} × {percent}/100 = {original * percent // 100}. New value = {original} - {original * percent // 100} = {answer}"
            difficulty = "easy"
            
        elif q_type == "successive":
            p1 = random.choice([10, 20])
            p2 = random.choice([10, 20])
            # Successive discount formula
            answer = p1 + p2 - (p1 * p2 // 100)
            question_text = f"Two successive discounts of {p1}% and {p2}% are equivalent to a single discount of what percent?"
            explanation = f"Successive discount = {p1} + {p2} - ({p1} × {p2}/100) = {p1 + p2} - {p1 * p2 // 100} = {answer}%"
            difficulty = "hard"
            
        else:  # find_number
            percent = random.choice([20, 25, 40, 50])
            result = random.randint(2, 10) * 10
            answer = result * 100 // percent
            question_text = f"If {percent}% of a number is {result}, what is the number?"
            explanation = f"{percent}% × x = {result}, so x = {result} × 100/{percent} = {answer}"
            difficulty = "medium"
        
        # Generate options
        options = [str(answer)]
        while len(options) < 4:
            wrong = answer + random.randint(-20, 20)
            if wrong > 0 and wrong != answer and str(wrong) not in options:
                options.append(str(wrong))
        random.shuffle(options)
        correct_idx = options.index(str(answer))
        
        questions.append({
            "question": question_text,
            "options": options,
            "correct_answer": correct_idx,
            "answer_explanation": explanation,
            "topic": "Percentages",
            "category": "Quantitative Ability",
            "difficulty": difficulty
        })
    
    return questions


def generate_profit_loss_questions(count=100):
    """Generate profit and loss questions"""
    questions = []
    
    for i in range(count):
        cp = random.randint(5, 50) * 10  # Cost price
        profit_or_loss = random.choice(["profit", "loss"])
        percent = random.choice([10, 15, 20, 25, 30])
        
        if profit_or_loss == "profit":
            sp = cp + (cp * percent // 100)
            question_text = f"A shopkeeper buys an item for ₹{cp} and sells it at {percent}% profit. What is the selling price?"
            explanation = f"Profit = {cp} × {percent}/100 = ₹{cp * percent // 100}. SP = CP + Profit = {cp} + {cp * percent // 100} = ₹{sp}"
        else:
            sp = cp - (cp * percent // 100)
            question_text = f"A shopkeeper buys an item for ₹{cp} and sells it at {percent}% loss. What is the selling price?"
            explanation = f"Loss = {cp} × {percent}/100 = ₹{cp * percent // 100}. SP = CP - Loss = {cp} - {cp * percent // 100} = ₹{sp}"
        
        answer = sp
        difficulty = "easy" if percent in [10, 20, 25] else "medium"
        
        # Generate options
        options = [f"₹{answer}"]
        while len(options) < 4:
            wrong = answer + random.randint(-50, 50)
            if wrong > 0 and wrong != answer and f"₹{wrong}" not in options:
                options.append(f"₹{wrong}")
        random.shuffle(options)
        correct_idx = options.index(f"₹{answer}")
        
        questions.append({
            "question": question_text,
            "options": options,
            "correct_answer": correct_idx,
            "answer_explanation": explanation,
            "topic": "Profit & Loss",
            "category": "Quantitative Ability",
            "difficulty": difficulty
        })
    
    return questions


def generate_time_work_questions(count=100):
    """Generate time and work questions"""
    questions = []
    
    for i in range(count):
        q_type = random.choice(["individual", "together", "pipes"])
        
        if q_type == "individual":
            days = random.randint(5, 20)
            work_fraction = f"1/{days}"
            question_text = f"A can complete a work in {days} days. What fraction of work can A do in 1 day?"
            explanation = f"If work is done in {days} days, 1 day's work = 1/{days}"
            options = [f"1/{days}", f"1/{days+2}", f"1/{days-2 if days > 2 else days+5}", f"1/{days*2}"]
            random.shuffle(options)
            correct_idx = options.index(f"1/{days}")
            difficulty = "easy"
            
        elif q_type == "together":
            a_days = random.randint(6, 18)
            b_days = a_days + random.randint(2, 6)
            # LCM shortcut for combined work
            combined_rate = 1/a_days + 1/b_days
            combined_days = round(1/combined_rate, 2)
            question_text = f"A can do work in {a_days} days, B can do it in {b_days} days. How many days will they take together?"
            explanation = f"Combined rate = 1/{a_days} + 1/{b_days}. Time = 1/(combined rate) ≈ {combined_days} days"
            
            options = [str(combined_days)]
            while len(options) < 4:
                wrong = round(combined_days + random.uniform(-3, 3), 2)
                if wrong > 0 and str(wrong) not in options:
                    options.append(str(wrong))
            random.shuffle(options)
            correct_idx = options.index(str(combined_days))
            difficulty = "medium"
            
        else:  # pipes
            fill_time = random.randint(4, 12)
            empty_time = fill_time + random.randint(2, 6)
            combined_rate = 1/fill_time - 1/empty_time
            if combined_rate > 0:
                combined_time = round(1/combined_rate, 2)
                question_text = f"A pipe can fill a tank in {fill_time} hours. Another pipe can empty it in {empty_time} hours. How long to fill with both open?"
                explanation = f"Net rate = 1/{fill_time} - 1/{empty_time}. Time = {combined_time} hours"
            else:
                combined_time = "Never"
                question_text = f"A pipe fills a tank in {empty_time} hours. Another empties it in {fill_time} hours. Can the tank be filled?"
                explanation = f"Emptying rate is faster than filling rate. Tank can never be filled."
            
            if combined_time != "Never":
                options = [str(combined_time)]
                while len(options) < 4:
                    wrong = round(combined_time + random.uniform(-3, 3), 2)
                    if wrong > 0 and str(wrong) not in options:
                        options.append(str(wrong))
                random.shuffle(options)
                correct_idx = options.index(str(combined_time))
            else:
                options = ["Never", str(fill_time), str(empty_time), str(fill_time + empty_time)]
                correct_idx = 0
            difficulty = "hard"
        
        questions.append({
            "question": question_text,
            "options": options,
            "correct_answer": correct_idx,
            "answer_explanation": explanation,
            "topic": "Time & Work",
            "category": "Quantitative Ability",
            "difficulty": difficulty
        })
    
    return questions


def generate_speed_distance_questions(count=100):
    """Generate speed, distance, time questions"""
    questions = []
    
    for i in range(count):
        q_type = random.choice(["basic", "train", "relative"])
        
        if q_type == "basic":
            speed = random.randint(4, 12) * 10  # km/h
            time = random.randint(2, 8)  # hours
            distance = speed * time
            question_text = f"A car travels at {speed} km/h for {time} hours. What distance does it cover?"
            explanation = f"Distance = Speed × Time = {speed} × {time} = {distance} km"
            answer = distance
            difficulty = "easy"
            
        elif q_type == "train":
            length = random.randint(1, 5) * 100  # meters
            time = random.randint(5, 20)  # seconds
            speed_ms = length / time
            speed_kmh = round(speed_ms * 18/5, 2)
            question_text = f"A train {length}m long crosses a pole in {time} seconds. What is its speed in km/h?"
            explanation = f"Speed = {length}/{time} = {speed_ms} m/s = {speed_ms} × 18/5 = {speed_kmh} km/h"
            answer = speed_kmh
            difficulty = "medium"
            
        else:  # relative
            speed1 = random.randint(4, 8) * 10
            speed2 = random.randint(3, 7) * 10
            direction = random.choice(["same", "opposite"])
            if direction == "same":
                relative_speed = abs(speed1 - speed2)
                question_text = f"Two trains running at {speed1} km/h and {speed2} km/h in same direction. Relative speed?"
                explanation = f"Same direction: Relative speed = |{speed1} - {speed2}| = {relative_speed} km/h"
            else:
                relative_speed = speed1 + speed2
                question_text = f"Two trains running at {speed1} km/h and {speed2} km/h in opposite directions. Relative speed?"
                explanation = f"Opposite directions: Relative speed = {speed1} + {speed2} = {relative_speed} km/h"
            answer = relative_speed
            difficulty = "medium"
        
        # Generate options
        options = [str(answer)]
        while len(options) < 4:
            wrong = answer + random.randint(-20, 20)
            if wrong > 0 and wrong != answer and str(wrong) not in options:
                options.append(str(wrong))
        random.shuffle(options)
        correct_idx = options.index(str(answer))
        
        questions.append({
            "question": question_text,
            "options": options,
            "correct_answer": correct_idx,
            "answer_explanation": explanation,
            "topic": "Time Speed Distance",
            "category": "Quantitative Ability",
            "difficulty": difficulty
        })
    
    return questions


def generate_simple_interest_questions(count=100):
    """Generate simple and compound interest questions"""
    questions = []
    
    for i in range(count):
        q_type = random.choice(["simple", "compound", "find_rate"])
        
        principal = random.randint(5, 50) * 100
        rate = random.choice([5, 8, 10, 12, 15])
        time = random.randint(2, 5)
        
        if q_type == "simple":
            si = principal * rate * time // 100
            question_text = f"Find the simple interest on ₹{principal} at {rate}% per annum for {time} years."
            explanation = f"SI = P × R × T / 100 = {principal} × {rate} × {time} / 100 = ₹{si}"
            answer = si
            difficulty = "easy"
            
        elif q_type == "compound":
            amount = round(principal * ((1 + rate/100) ** time), 2)
            ci = round(amount - principal, 2)
            question_text = f"Find the compound interest on ₹{principal} at {rate}% for {time} years."
            explanation = f"A = P(1 + R/100)^T = {principal}(1.{rate:02d})^{time} = ₹{amount}. CI = {amount} - {principal} = ₹{ci}"
            answer = ci
            difficulty = "medium"
            
        else:  # find_rate
            si = principal * rate * time // 100
            amount = principal + si
            question_text = f"₹{principal} becomes ₹{amount} in {time} years at simple interest. Find the rate."
            explanation = f"SI = {amount} - {principal} = {si}. R = SI × 100 / (P × T) = {si} × 100 / ({principal} × {time}) = {rate}%"
            answer = rate
            difficulty = "hard"
        
        # Generate options
        if q_type == "find_rate":
            options = [f"{answer}%"]
            while len(options) < 4:
                wrong = answer + random.randint(-5, 5)
                if wrong > 0 and f"{wrong}%" not in options:
                    options.append(f"{wrong}%")
        else:
            options = [f"₹{answer}"]
            while len(options) < 4:
                wrong = int(answer + random.randint(-100, 100))
                if wrong > 0 and f"₹{wrong}" not in options:
                    options.append(f"₹{wrong}")
        
        random.shuffle(options)
        if q_type == "find_rate":
            correct_idx = options.index(f"{answer}%")
        else:
            correct_idx = options.index(f"₹{answer}")
        
        questions.append({
            "question": question_text,
            "options": options,
            "correct_answer": correct_idx,
            "answer_explanation": explanation,
            "topic": "Simple & Compound Interest",
            "category": "Quantitative Ability",
            "difficulty": difficulty
        })
    
    return questions


def generate_blood_relation_questions(count=50):
    """Generate blood relation questions"""
    questions = []
    
    relations = [
        {
            "statement": "Pointing to a photograph, A says 'He is the son of my father's only son.' How is the person in photograph related to A?",
            "answer": "Son",
            "explanation": "A's father's only son is A himself. So the person is A's son.",
            "options": ["Son", "Brother", "Father", "Uncle"]
        },
        {
            "statement": "If A is B's sister and B is C's mother, how is A related to C?",
            "answer": "Aunt",
            "explanation": "A is sister of B, and B is C's mother. So A is C's maternal aunt.",
            "options": ["Aunt", "Mother", "Grandmother", "Sister"]
        },
        {
            "statement": "A's mother is B's sister. B has a daughter C. How is A related to C?",
            "answer": "Cousin",
            "explanation": "A's mother and B are siblings. So A and C (B's daughter) are cousins.",
            "options": ["Cousin", "Brother", "Uncle", "Nephew"]
        },
        {
            "statement": "If X is the brother of the son of Y's son, how is X related to Y?",
            "answer": "Grandson",
            "explanation": "Y's son's son's brother is also Y's grandson.",
            "options": ["Grandson", "Son", "Nephew", "Brother"]
        },
        {
            "statement": "A's father is B's son. How is B related to A?",
            "answer": "Grandfather",
            "explanation": "If A's father is B's son, then B is A's grandfather.",
            "options": ["Grandfather", "Father", "Uncle", "Brother"]
        },
    ]
    
    for i in range(count):
        rel = random.choice(relations)
        questions.append({
            "question": rel["statement"],
            "options": rel["options"],
            "correct_answer": rel["options"].index(rel["answer"]),
            "answer_explanation": rel["explanation"],
            "topic": "Blood Relations",
            "category": "Logical Ability",
            "difficulty": random.choice(["medium", "hard"])
        })
    
    return questions


def generate_coding_decoding_questions(count=100):
    """Generate coding-decoding questions"""
    questions = []
    
    for i in range(count):
        q_type = random.choice(["reverse", "shift", "value"])
        
        words = ["APPLE", "MANGO", "HOUSE", "PAPER", "CHAIR", "TABLE", "HORSE", "RIVER", "TRAIN", "BRAIN"]
        word = random.choice(words)
        
        if q_type == "reverse":
            coded = word[::-1]
            test_words = ["WATER", "CLOUD", "STONE", "FRUIT", "LIGHT"]
            test_word = random.choice(test_words)
            answer = test_word[::-1]
            question_text = f"If '{word}' is coded as '{coded}', how is '{test_word}' coded?"
            explanation = f"The word is reversed. {test_word} reversed is {answer}"
            difficulty = "easy"
            
        elif q_type == "shift":
            shift = random.choice([1, 2])
            coded = ''.join(chr((ord(c) - 65 + shift) % 26 + 65) for c in word)
            test_word = random.choice(["CAT", "DOG", "BAT", "RAT"])
            answer = ''.join(chr((ord(c) - 65 + shift) % 26 + 65) for c in test_word)
            question_text = f"If '{word}' is coded as '{coded}', how is '{test_word}' coded?"
            explanation = f"Each letter is shifted by +{shift}. {test_word} becomes {answer}"
            difficulty = "medium"
            
        else:  # value
            # A=1, B=2, etc.
            value = sum(ord(c) - 64 for c in word)
            test_word = random.choice(["CAT", "DOG", "BAT"])
            answer = sum(ord(c) - 64 for c in test_word)
            question_text = f"If A=1, B=2, C=3... Z=26, what is the value of '{test_word}'?"
            explanation = f"Sum of letter values: {' + '.join(str(ord(c)-64) for c in test_word)} = {answer}"
            difficulty = "medium"
        
        # Generate options
        options = [answer]
        while len(options) < 4:
            if q_type == "value":
                wrong = answer + random.randint(-10, 10)
                if wrong > 0 and wrong not in options:
                    options.append(wrong)
            else:
                # Generate wrong string options
                wrong = answer
                while wrong == answer or wrong in options:
                    wrong = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(len(answer)))
                options.append(wrong)
        
        options = [str(o) for o in options]
        random.shuffle(options)
        correct_idx = options.index(str(answer))
        
        questions.append({
            "question": question_text,
            "options": options,
            "correct_answer": correct_idx,
            "answer_explanation": explanation,
            "topic": "Coding-Decoding",
            "category": "Logical Ability",
            "difficulty": difficulty
        })
    
    return questions


def generate_direction_questions(count=50):
    """Generate direction sense questions"""
    questions = []
    
    directions = ["North", "South", "East", "West"]
    
    for i in range(count):
        q_type = random.choice(["turn", "distance"])
        
        if q_type == "turn":
            start = random.choice(directions)
            turns = random.choice([(90, "right"), (-90, "left"), (180, "opposite")])
            
            dir_map = {"North": 0, "East": 90, "South": 180, "West": 270}
            rev_map = {0: "North", 90: "East", 180: "South", 270: "West"}
            
            new_angle = (dir_map[start] + turns[0]) % 360
            answer = rev_map[new_angle]
            
            question_text = f"A person faces {start}, turns 90° to the {turns[1]}. Which direction is he facing?"
            explanation = f"{start} + 90° {turns[1]} = {answer}"
            
            options = directions.copy()
            random.shuffle(options)
            correct_idx = options.index(answer)
            difficulty = "easy"
            
        else:  # distance
            d1 = random.randint(3, 6)
            d2 = random.randint(3, 6)
            # Pythagorean calculation
            distance = round((d1**2 + d2**2)**0.5, 2)
            question_text = f"A man walks {d1} km North, then {d2} km East. How far is he from starting point?"
            explanation = f"Using Pythagoras: √({d1}² + {d2}²) = √{d1**2 + d2**2} = {distance} km"
            answer = distance
            
            options = [str(answer)]
            while len(options) < 4:
                wrong = round(answer + random.uniform(-2, 2), 2)
                if wrong > 0 and str(wrong) not in options:
                    options.append(str(wrong))
            random.shuffle(options)
            correct_idx = options.index(str(answer))
            difficulty = "medium"
        
        questions.append({
            "question": question_text,
            "options": options,
            "correct_answer": correct_idx,
            "answer_explanation": explanation,
            "topic": "Direction Sense",
            "category": "Logical Ability",
            "difficulty": difficulty
        })
    
    return questions


def generate_synonym_antonym_questions(count=100):
    """Generate synonym and antonym questions"""
    
    word_pairs = [
        # Format: (word, synonym, antonym)
        ("Happy", "Joyful", "Sad"),
        ("Big", "Large", "Small"),
        ("Fast", "Quick", "Slow"),
        ("Hot", "Warm", "Cold"),
        ("Strong", "Powerful", "Weak"),
        ("Rich", "Wealthy", "Poor"),
        ("Beautiful", "Gorgeous", "Ugly"),
        ("Smart", "Intelligent", "Dumb"),
        ("Brave", "Courageous", "Cowardly"),
        ("Honest", "Truthful", "Dishonest"),
        ("Kind", "Generous", "Cruel"),
        ("Clean", "Tidy", "Dirty"),
        ("Ancient", "Old", "Modern"),
        ("Bright", "Luminous", "Dim"),
        ("Calm", "Peaceful", "Agitated"),
        ("Difficult", "Hard", "Easy"),
        ("Empty", "Vacant", "Full"),
        ("Famous", "Renowned", "Unknown"),
        ("Genuine", "Authentic", "Fake"),
        ("Humble", "Modest", "Arrogant"),
    ]
    
    questions = []
    
    for i in range(count):
        pair = random.choice(word_pairs)
        q_type = random.choice(["synonym", "antonym"])
        
        if q_type == "synonym":
            answer = pair[1]
            question_text = f"Choose the synonym of '{pair[0]}':"
            explanation = f"'{pair[0]}' means {pair[1].lower()}."
            wrong_options = [pair[2]] + random.sample([p[0] for p in word_pairs if p != pair], 2)
        else:
            answer = pair[2]
            question_text = f"Choose the antonym of '{pair[0]}':"
            explanation = f"'{pair[0]}' means the opposite of {pair[2].lower()}."
            wrong_options = [pair[1]] + random.sample([p[0] for p in word_pairs if p != pair], 2)
        
        options = [answer] + wrong_options
        random.shuffle(options)
        correct_idx = options.index(answer)
        
        questions.append({
            "question": question_text,
            "options": options,
            "correct_answer": correct_idx,
            "answer_explanation": explanation,
            "topic": "Synonyms & Antonyms",
            "category": "Verbal Ability",
            "difficulty": random.choice(["easy", "medium"])
        })
    
    return questions


def generate_fill_blanks_questions(count=100):
    """Generate fill in the blanks questions"""
    
    blank_questions = [
        ("She is ___ honest person.", "an", ["a", "an", "the", "no article"], "Use 'an' before vowel sounds. 'Honest' has silent 'h'."),
        ("The sun rises in ___ east.", "the", ["a", "an", "the", "no article"], "Use 'the' with directions and unique things."),
        ("He has been working ___ morning.", "since", ["since", "for", "from", "by"], "Use 'since' for point in time."),
        ("I have known him ___ ten years.", "for", ["since", "for", "from", "by"], "Use 'for' for duration of time."),
        ("She is ___ than her sister.", "taller", ["tall", "taller", "tallest", "more tall"], "Comparative degree uses -er for short adjectives."),
        ("This is ___ best book I have ever read.", "the", ["a", "an", "the", "no article"], "Use 'the' with superlatives."),
        ("Neither of the boys ___ present.", "was", ["was", "were", "is", "are"], "'Neither' takes singular verb."),
        ("Each of the students ___ given a book.", "was", ["was", "were", "is", "are"], "'Each' takes singular verb."),
        ("He walked ___ the bridge.", "across", ["across", "through", "along", "into"], "'Across' means from one side to another."),
        ("The train arrived ___ time.", "on", ["on", "in", "at", "by"], "'On time' means punctually."),
    ]
    
    questions = []
    
    for i in range(count):
        q_data = random.choice(blank_questions)
        
        question_text = q_data[0]
        answer = q_data[1]
        options = q_data[2].copy()
        explanation = q_data[3]
        
        random.shuffle(options)
        correct_idx = options.index(answer)
        
        questions.append({
            "question": question_text,
            "options": options,
            "correct_answer": correct_idx,
            "answer_explanation": explanation,
            "topic": "Fill in the Blanks",
            "category": "Verbal Ability",
            "difficulty": random.choice(["easy", "medium"])
        })
    
    return questions


def seed_all_questions():
    """Generate and seed all questions to database"""
    db = SessionLocal()
    
    try:
        # Check current count
        existing_count = db.query(AptitudeQuestion).count()
        print(f"Current questions in database: {existing_count}")
        
        # Generate questions
        all_questions = []
        
        print("Generating Number Series questions...")
        all_questions.extend(generate_number_series_questions(150))
        
        print("Generating Percentage questions...")
        all_questions.extend(generate_percentage_questions(150))
        
        print("Generating Profit & Loss questions...")
        all_questions.extend(generate_profit_loss_questions(150))
        
        print("Generating Time & Work questions...")
        all_questions.extend(generate_time_work_questions(150))
        
        print("Generating Speed & Distance questions...")
        all_questions.extend(generate_speed_distance_questions(150))
        
        print("Generating Interest questions...")
        all_questions.extend(generate_simple_interest_questions(150))
        
        print("Generating Blood Relations questions...")
        all_questions.extend(generate_blood_relation_questions(100))
        
        print("Generating Coding-Decoding questions...")
        all_questions.extend(generate_coding_decoding_questions(150))
        
        print("Generating Direction questions...")
        all_questions.extend(generate_direction_questions(100))
        
        print("Generating Synonym/Antonym questions...")
        all_questions.extend(generate_synonym_antonym_questions(150))
        
        print("Generating Fill in the Blanks questions...")
        all_questions.extend(generate_fill_blanks_questions(150))
        
        print(f"\nTotal questions generated: {len(all_questions)}")
        
        # Add to database
        for q_data in all_questions:
            question = AptitudeQuestion(**q_data)
            db.add(question)
        
        db.commit()
        
        # Print summary
        final_count = db.query(AptitudeQuestion).count()
        print(f"Successfully added {len(all_questions)} questions!")
        print(f"Total questions now: {final_count}")
        
        # Topic summary
        print("\nQuestions by Topic:")
        topics = db.query(AptitudeQuestion.topic, AptitudeQuestion.category).distinct().all()
        for topic, category in sorted(topics, key=lambda x: x[1]):
            count = db.query(AptitudeQuestion).filter(AptitudeQuestion.topic == topic).count()
            print(f"  {category} > {topic}: {count}")
            
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("Starting Aptitude Question Generator...")
    seed_all_questions()
    print("\nDone!")
