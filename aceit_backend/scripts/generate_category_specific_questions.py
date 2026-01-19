"""
Generate questions for specific categories to reach at least 100 each.
Categories: Quantitative Aptitude, Data Interpretation, Analytical Reasoning, Verbal Reasoning, TestCategory.
"""

import sys
import os
import random

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_postgres import SessionLocal
from models.aptitude_sql import AptitudeQuestion

def generate_data_interpretation(count=80):
    questions = []
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    items = ["Product A", "Sales", "Production", "Export"]
    
    for i in range(count):
        val1, val2, val3 = random.randint(100, 500), random.randint(100, 600), random.randint(100, 700)
        total = val1 + val2 + val3
        avg = round(total / 3, 2)
        q_type = random.choice(["average", "total", "percentage_increase"])
        
        if q_type == "average":
            question_text = f"Sales data for three months: {months[0]}-{val1}, {months[1]}-{val2}, {months[2]}-{val3}. What is the average sales?"
            answer = str(avg)
            explanation = f"Average = ({val1} + {val2} + {val3}) / 3 = {total} / 3 = {avg}"
        elif q_type == "total":
            question_text = f"Production data: {months[0]}-{val1}, {months[1]}-{val2}, {months[2]}-{val3}. What is the total production?"
            answer = str(total)
            explanation = f"Total = {val1} + {val2} + {val3} = {total}"
        else:
            diff = val2 - val1
            perc = round((diff / val1) * 100, 2)
            question_text = f"If sales in {months[0]} was {val1} and in {months[1]} was {val2}, find the percentage increase."
            answer = f"{perc}%"
            explanation = f"Increase = {val2} - {val1} = {diff}. Percentage = ({diff}/{val1}) * 100 = {perc}%"
            
        options = [answer]
        while len(options) < 4:
            if q_type == "percentage_increase":
                # Extract float value safely
                val = float(answer.replace('%', ''))
                wrong = f"{round(val + random.uniform(-10, 10), 2)}%"
            else:
                val = float(answer)
                wrong = str(round(val + random.randint(-50, 50), 2))
            if wrong not in options:
                options.append(wrong)
        
        random.shuffle(options)
        questions.append({
            "question": question_text,
            "options": options,
            "correct_answer": options.index(answer),
            "answer_explanation": explanation,
            "topic": "Data Interpretation",
            "category": "Data Interpretation",
            "difficulty": random.choice(["easy", "medium"])
        })
    return questions

def generate_analytical_reasoning(count=100):
    questions = []
    objects = ["Cats", "Dogs", "Birds", "Lions", "Tigers", "Animals", "Mortals", "Greek", "Socrates"]
    properties = ["Mammals", "Four-footed", "Mortal", "Warm-blooded", "Carnivores"]
    
    for i in range(count):
        q_type = random.choice(["syllogism", "inequality"])
        
        if q_type == "syllogism":
            a, b, c = random.sample(objects, 3)
            question_text = f"Statement: All {a} are {b}. All {b} are {c}. Conclusion:"
            answer = f"All {a} are {c}"
            explanation = f"This is a standard transitive syllogism: {a} \u2282 {b} and {b} \u2282 {c} implies {a} \u2282 {c}."
            options = [answer, f"Some {c} are not {a}", f"No {a} is {c}", f"Some {a} are {b}"]
        else:
            # Inequality
            names = ["A", "B", "C", "D", "E"]
            random.shuffle(names)
            question_text = f"If {names[0]} > {names[1]}, {names[1]} > {names[2]}, and {names[2]} > {names[3]}, which is the smallest?"
            answer = names[3]
            explanation = f"The order is {names[0]} > {names[1]} > {names[2]} > {names[3]}, so {names[3]} is the smallest."
            options = [names[0], names[1], names[2], names[3]]
            
        random.shuffle(options)
        questions.append({
            "question": question_text,
            "options": options,
            "correct_answer": options.index(answer),
            "answer_explanation": explanation,
            "topic": "Analytical Reasoning",
            "category": "Analytical Reasoning",
            "difficulty": random.choice(["easy", "medium"])
        })
    return questions

def generate_verbal_reasoning(count=110):
    questions = []
    sets = [
        (["Apple", "Mango", "Banana", "Onion"], "Onion", "Others are fruits, Onion is a vegetable."),
        (["Pencil", "Eraser", "Pen", "Bed"], "Bed", "Others are stationery items."),
        (["Lion", "Tiger", "Leopard", "Cow"], "Cow", "Others are wild animals/carnivores."),
        (["Mars", "Earth", "Venus", "Moon"], "Moon", "Others are planets."),
        (["Car", "Bike", "Truck", "Aeroplane"], "Aeroplane", "Others are land vehicles.")
    ]
    
    for i in range(count):
        q_type = random.choice(["odd_one", "logical_order"])
        
        if q_type == "odd_one":
            item_set, answer, explanation = random.choice(sets)
            question_text = f"Choose the odd one out: {', '.join(item_set)}"
            options = item_set
            # answer is already in options
        else:
            # Logical order
            ops = [
                (["Seed", "Plant", "Flower", "Fruit"], "Seed, Plant, Flower, Fruit", "Order of growth."),
                (["Morning", "Afternoon", "Evening", "Night"], "Morning, Afternoon, Evening, Night", "Time of day."),
                (["Infant", "Child", "Adult", "Old"], "Infant, Child, Adult, Old", "Life stages.")
            ]
            items, answer, explanation = random.choice(ops)
            question_text = f"Arrange in logical order: {', '.join(random.sample(items, len(items)))}"
            options = [answer, "Random Order 1", "Random Order 2", "Reverse Order"]
            
        random.shuffle(options)
        questions.append({
            "question": question_text,
            "options": options,
            "correct_answer": options.index(answer),
            "answer_explanation": explanation,
            "topic": "Verbal Reasoning",
            "category": "Verbal Reasoning",
            "difficulty": random.choice(["easy", "medium"])
        })
    return questions

def generate_quantitative_aptitude(count=20):
    questions = []
    for i in range(count):
        q_type = random.choice(["hcf", "lcm", "prime"])
        if q_type == "hcf":
            a, b = random.randint(10, 50), random.randint(10, 50)
            from math import gcd
            answer = str(gcd(a, b))
            question_text = f"Find the HCF of {a} and {b}."
            explanation = f"Common factors are used to find Highest Common Factor. HCF({a}, {b}) = {answer}"
        elif q_type == "lcm":
            a, b = random.randint(5, 20), random.randint(5, 20)
            from math import gcd
            answer = str((a * b) // gcd(a, b))
            question_text = f"Find the LCM of {a} and {b}."
            explanation = f"LCM is (a * b) / GCD(a, b). LCM({a}, {b}) = {answer}"
        else:
            num = random.randint(10, 100)
            is_prime = True
            for j in range(2, int(num**0.5) + 1):
                if num % j == 0:
                    is_prime = False
                    break
            answer = "Yes" if is_prime else "No"
            question_text = f"Is the number {num} a prime number?"
            explanation = f"{num} is {'only divisible by 1 and itself' if is_prime else 'divisible by other factors'}."
            options = ["Yes", "No", "Maybe", "Depends"]
            # fix correct_answer
            random.shuffle(options)
            questions.append({
                "question": question_text,
                "options": options,
                "correct_answer": options.index(answer),
                "answer_explanation": explanation,
                "topic": "Number System",
                "category": "Quantitative Aptitude",
                "difficulty": "easy"
            })
            continue

        options = [answer]
        while len(options) < 4:
            try:
                val = int(answer)
                wrong = str(val + random.randint(-10, 10))
            except ValueError:
                wrong = str(random.randint(1, 100))
            if wrong not in options:
                options.append(wrong)
        random.shuffle(options)
        questions.append({
            "question": question_text,
            "options": options,
            "correct_answer": options.index(answer),
            "answer_explanation": explanation,
            "topic": random.choice(["HCF and LCM", "Number System"]),
            "category": "Quantitative Aptitude",
            "difficulty": "medium"
        })
    return questions

def generate_test_category(count=100):
    questions = []
    for i in range(count):
        # Adaptive Logic patterns
        a = random.randint(1, 10)
        b = a * 2
        c = b * 2
        answer = str(c * 2)
        question_text = f"Adaptive Logic Test: 1:{a}, 2:{b}, 3:{c}, 4:?"
        explanation = f"The value is doubled each time. {c} * 2 = {answer}"
        
        options = [answer]
        while len(options) < 4:
            wrong = str(random.randint(1, 100))
            if wrong not in options:
                options.append(wrong)
        random.shuffle(options)
        questions.append({
            "question": question_text,
            "options": options,
            "correct_answer": options.index(answer),
            "answer_explanation": explanation,
            "topic": "AdaptiveLogicTest",
            "category": "TestCategory",
            "difficulty": "medium"
        })
    return questions

def main():
    db = SessionLocal()
    try:
        all_q = []
        print("Generating Data Interpretation...")
        data_int = generate_data_interpretation(100)
        print(f"Generated {len(data_int)} Data Interpretation questions.")
        all_q.extend(data_int)
        
        print("Generating Analytical Reasoning...")
        anal_reas = generate_analytical_reasoning(150)
        print(f"Generated {len(anal_reas)} Analytical Reasoning questions.")
        all_q.extend(anal_reas)
        
        print("Generating Verbal Reasoning...")
        verb_reas = generate_verbal_reasoning(150)
        print(f"Generated {len(verb_reas)} Verbal Reasoning questions.")
        all_q.extend(verb_reas)
        
        print("Generating Quantitative Aptitude...")
        quant_apt = generate_quantitative_aptitude(20)
        print(f"Generated {len(quant_apt)} Quantitative Aptitude questions.")
        all_q.extend(quant_apt)
        
        print("Generating TestCategory...")
        test_cat = generate_test_category(100)
        print(f"Generated {len(test_cat)} TestCategory questions.")
        all_q.extend(test_cat)
        
        print(f"Total to add: {len(all_q)}")
        added = 0
        for q_data in all_q:
            # Check for duplicates
            exists = db.query(AptitudeQuestion).filter(AptitudeQuestion.question == q_data["question"]).first()
            if not exists:
                new_q = AptitudeQuestion(**q_data)
                db.add(new_q)
                added += 1
        
        db.commit()
        print(f"Added {added} questions.")
        
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
