"""
Seed User Provided Questions:
Adds a set of high-quality manual questions provided by the user.
"""

import sys
import os
import json

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_postgres import SessionLocal
from models.aptitude_sql import AptitudeQuestion

USER_QUESTIONS = [
  {
    "category": "Quantitative Ability",
    "topic": "Percentages",
    "difficulty": "easy",
    "question": "What is 25% of 200?",
    "options": ["25", "50", "75", "100"],
    "correct_answer": 1,
    "answer_explanation": "25% of 200 = (25/100) \u00d7 200 = 50."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Percentages",
    "difficulty": "medium",
    "question": "A number is increased by 20% and then decreased by 20%. What is the net change?",
    "options": ["No change", "4% increase", "4% decrease", "2% decrease"],
    "correct_answer": 2,
    "answer_explanation": "Net change = 20 \u2212 20 \u2212 (20\u00d720)/100 = \u22124%, so 4% decrease."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Profit and Loss",
    "difficulty": "easy",
    "question": "If the cost price is \u20b9400 and selling price is \u20b9500, what is the profit?",
    "options": ["\u20b950", "\u20b980", "\u20b9100", "\u20b9120"],
    "correct_answer": 2,
    "answer_explanation": "Profit = Selling Price \u2212 Cost Price = 500 \u2212 400 = 100."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Profit and Loss",
    "difficulty": "medium",
    "question": "An article is sold at a loss of 10% for \u20b9900. What is the cost price?",
    "options": ["\u20b91000", "\u20b9950", "\u20b9990", "\u20b91100"],
    "correct_answer": 0,
    "answer_explanation": "CP = 900 \u00d7 (100/90) = 1000."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Ratio and Proportion",
    "difficulty": "easy",
    "question": "What is the ratio of 15 to 20?",
    "options": ["3:4", "4:3", "2:3", "5:6"],
    "correct_answer": 0,
    "answer_explanation": "15:20 simplifies to 3:4."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Ratio and Proportion",
    "difficulty": "medium",
    "question": "The ratio of boys to girls is 3:2. If there are 30 boys, how many girls are there?",
    "options": ["15", "20", "25", "30"],
    "correct_answer": 1,
    "answer_explanation": "If 3 parts = 30, then 1 part = 10. Girls = 2 \u00d7 10 = 20."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Averages",
    "difficulty": "easy",
    "question": "What is the average of 2, 4, 6, and 8?",
    "options": ["4", "5", "6", "7"],
    "correct_answer": 1,
    "answer_explanation": "Average = (2+4+6+8)/4 = 5."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Averages",
    "difficulty": "medium",
    "question": "The average of 5 numbers is 20. If one number is 10, what is the average of the remaining numbers?",
    "options": ["20", "22.5", "25", "18"],
    "correct_answer": 1,
    "answer_explanation": "Total = 5\u00d720 = 100. Remaining sum = 90. Average = 90/4 = 22.5."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Time and Work",
    "difficulty": "easy",
    "question": "If A can complete a work in 10 days, how much work does he do in 1 day?",
    "options": ["1/5", "1/10", "1/20", "1/15"],
    "correct_answer": 1,
    "answer_explanation": "Work done in 1 day = 1/10."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Time and Work",
    "difficulty": "medium",
    "question": "A can do a work in 10 days and B in 20 days. In how many days can they complete it together?",
    "options": ["5", "6.67", "7.5", "10"],
    "correct_answer": 1,
    "answer_explanation": "Work/day = 1/10 + 1/20 = 3/20. Time = 20/3 \u2248 6.67 days."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Time and Distance",
    "difficulty": "easy",
    "question": "If a car travels at 60 km/h, how far will it travel in 2 hours?",
    "options": ["100 km", "110 km", "120 km", "130 km"],
    "correct_answer": 2,
    "answer_explanation": "Distance = Speed \u00d7 Time = 60 \u00d7 2 = 120 km."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Time and Distance",
    "difficulty": "medium",
    "question": "A train covers 180 km in 3 hours. What is its speed?",
    "options": ["50 km/h", "55 km/h", "60 km/h", "65 km/h"],
    "correct_answer": 2,
    "answer_explanation": "Speed = Distance / Time = 180/3 = 60 km/h."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Simple Interest",
    "difficulty": "easy",
    "question": "Find the simple interest on \u20b91000 at 10% per annum for 2 years.",
    "options": ["\u20b9100", "\u20b9150", "\u20b9200", "\u20b9250"],
    "correct_answer": 2,
    "answer_explanation": "SI = (1000\u00d710\u00d72)/100 = 200."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Simple Interest",
    "difficulty": "medium",
    "question": "At what rate of interest will \u20b92000 earn \u20b9400 in 4 years?",
    "options": ["4%", "5%", "6%", "7%"],
    "correct_answer": 1,
    "answer_explanation": "Rate = (400\u00d7100)/(2000\u00d74) = 5%."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Number System",
    "difficulty": "easy",
    "question": "Which of the following is a prime number?",
    "options": ["9", "15", "17", "21"],
    "correct_answer": 2,
    "answer_explanation": "17 has only two factors: 1 and itself."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Number System",
    "difficulty": "medium",
    "question": "What is the LCM of 12 and 18?",
    "options": ["36", "24", "48", "72"],
    "correct_answer": 0,
    "answer_explanation": "LCM of 12 and 18 is 36."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Percentages",
    "difficulty": "easy",
    "question": "What is 10% of 450?",
    "options": ["40", "45", "50", "55"],
    "correct_answer": 1,
    "answer_explanation": "10% of 450 = 45."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Percentages",
    "difficulty": "medium",
    "question": "If the price of an item increases from \u20b9800 to \u20b9880, what is the percentage increase?",
    "options": ["8%", "9%", "10%", "11%"],
    "correct_answer": 2,
    "answer_explanation": "Increase = 80. Percentage increase = (80/800) \u00d7 100 = 10%."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Profit and Loss",
    "difficulty": "easy",
    "question": "If a book is bought for \u20b9200 and sold for \u20b9180, what is the loss?",
    "options": ["\u20b910", "\u20b915", "\u20b920", "\u20b925"],
    "correct_answer": 2,
    "answer_explanation": "Loss = 200 \u2212 180 = 20."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Profit and Loss",
    "difficulty": "medium",
    "question": "An article is sold for \u20b91200 at a profit of 20%. What is its cost price?",
    "options": ["\u20b9900", "\u20b91000", "\u20b91100", "\u20b91150"],
    "correct_answer": 1,
    "answer_explanation": "CP = 1200 \u00d7 (100/120) = 1000."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Ratio and Proportion",
    "difficulty": "easy",
    "question": "Divide \u20b9600 in the ratio 2:3.",
    "options": ["\u20b9240 and \u20b9360", "\u20b9200 and \u20b9400", "\u20b9300 and \u20b9300", "\u20b9250 and \u20b9350"],
    "correct_answer": 0,
    "answer_explanation": "Total parts = 5. Shares are (2/5)\u00d7600 = 240 and (3/5)\u00d7600 = 360."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Ratio and Proportion",
    "difficulty": "medium",
    "question": "The ratio of two numbers is 5:7 and their sum is 144. What is the smaller number?",
    "options": ["50", "55", "60", "65"],
    "correct_answer": 1,
    "answer_explanation": "Total parts = 12. One part = 144/12 = 12. Smaller number = 5\u00d712 = 60."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Averages",
    "difficulty": "easy",
    "question": "The average of 10 numbers is 15. What is their total sum?",
    "options": ["100", "120", "150", "180"],
    "correct_answer": 2,
    "answer_explanation": "Sum = Average \u00d7 Count = 15 \u00d7 10 = 150."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Averages",
    "difficulty": "medium",
    "question": "The average age of 5 students is 18 years. If one student is replaced by another aged 20, the new average becomes 19. What was the age of the replaced student?",
    "options": ["13", "14", "15", "16"],
    "correct_answer": 2,
    "answer_explanation": "Old total = 5\u00d718 = 90. New total = 5\u00d719 = 95. Replaced age = 90 \u2212 (95 \u2212 20) = 15."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Time and Work",
    "difficulty": "easy",
    "question": "If a man completes a work in 8 days, what fraction of work does he complete in one day?",
    "options": ["1/6", "1/7", "1/8", "1/9"],
    "correct_answer": 2,
    "answer_explanation": "Work done in one day = 1/8."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Time and Work",
    "difficulty": "medium",
    "question": "A can do a work in 12 days and B in 18 days. In how many days can they finish the work together?",
    "options": ["7.2", "6", "8", "9"],
    "correct_answer": 0,
    "answer_explanation": "Work/day = 1/12 + 1/18 = 5/36. Time = 36/5 = 7.2 days."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Time and Distance",
    "difficulty": "easy",
    "question": "A person walks at 5 km/h. How far will he walk in 3 hours?",
    "options": ["10 km", "12 km", "15 km", "18 km"],
    "correct_answer": 2,
    "answer_explanation": "Distance = Speed \u00d7 Time = 5 \u00d7 3 = 15 km."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Time and Distance",
    "difficulty": "medium",
    "question": "A train travels 300 km at a speed of 60 km/h. How long does it take?",
    "options": ["4 hrs", "5 hrs", "6 hrs", "7 hrs"],
    "correct_answer": 1,
    "answer_explanation": "Time = Distance / Speed = 300/60 = 5 hours."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Simple Interest",
    "difficulty": "easy",
    "question": "What is the simple interest on \u20b9500 at 10% per annum for 1 year?",
    "options": ["\u20b940", "\u20b945", "\u20b950", "\u20b955"],
    "correct_answer": 2,
    "answer_explanation": "SI = (500\u00d710\u00d71)/100 = 50."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Simple Interest",
    "difficulty": "medium",
    "question": "In how many years will \u20b91500 amount to \u20b91800 at 10% simple interest?",
    "options": ["2 years", "3 years", "4 years", "5 years"],
    "correct_answer": 1,
    "answer_explanation": "SI = 300. Time = (300\u00d7100)/(1500\u00d710) = 2 years."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Number System",
    "difficulty": "easy",
    "question": "Which number is divisible by 9?",
    "options": ["234", "341", "452", "581"],
    "correct_answer": 0,
    "answer_explanation": "Sum of digits of 234 = 9, so divisible by 9."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Number System",
    "difficulty": "medium",
    "question": "What is the HCF of 24 and 36?",
    "options": ["6", "8", "12", "18"],
    "correct_answer": 2,
    "answer_explanation": "HCF of 24 and 36 is 12."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Percentages",
    "difficulty": "hard",
    "question": "If the population of a town increases by 10% in the first year and decreases by 10% in the second year, what is the net change?",
    "options": ["No change", "1% increase", "1% decrease", "2% decrease"],
    "correct_answer": 2,
    "answer_explanation": "Net change = 10 \u2212 10 \u2212 (10\u00d710)/100 = \u22121%, so 1% decrease."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Percentages",
    "difficulty": "medium",
    "question": "What percentage of 150 is 45?",
    "options": ["25%", "30%", "35%", "40%"],
    "correct_answer": 1,
    "answer_explanation": "(45/150) \u00d7 100 = 30%."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Profit and Loss",
    "difficulty": "hard",
    "question": "A trader sells two items for \u20b91000 each. He gains 20% on one and loses 20% on the other. What is his net profit or loss?",
    "options": ["No profit no loss", "Loss of \u20b940", "Profit of \u20b940", "Loss of \u20b920"],
    "correct_answer": 1,
    "answer_explanation": "CP1 = 1000/1.2 = 833.33, CP2 = 1000/0.8 = 1250. Total CP = 2083.33, SP = 2000 \u2192 Loss \u2248 40."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Profit and Loss",
    "difficulty": "medium",
    "question": "If an article is sold at 25% profit for \u20b91250, what is its cost price?",
    "options": ["\u20b9900", "\u20b9950", "\u20b91000", "\u20b91100"],
    "correct_answer": 2,
    "answer_explanation": "CP = 1250 \u00d7 (100/125) = 1000."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Ratio and Proportion",
    "difficulty": "medium",
    "question": "The ratio of salaries of A and B is 4:5. If A earns \u20b94000 more than B, what is B\u2019s salary?",
    "options": ["\u20b916000", "\u20b918000", "\u20b920000", "\u20b922000"],
    "correct_answer": 1,
    "answer_explanation": "Difference = 1 part = 4000. B = 5 parts = 20000."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Ratio and Proportion",
    "difficulty": "hard",
    "question": "If A:B = 2:3 and B:C = 4:5, find A:C.",
    "options": ["8:15", "6:10", "3:5", "5:8"],
    "correct_answer": 0,
    "answer_explanation": "A:B = 8:12 and B:C = 12:15 \u2192 A:C = 8:15."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Averages",
    "difficulty": "medium",
    "question": "The average of 8 numbers is 12. If two numbers are 10 and 14, what is the average of the remaining numbers?",
    "options": ["11", "12", "13", "14"],
    "correct_answer": 1,
    "answer_explanation": "Total = 8\u00d712 = 96. Remaining sum = 72. Average = 72/6 = 12."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Averages",
    "difficulty": "hard",
    "question": "The average weight of 30 students is 50 kg. If the teacher weighing 80 kg joins them, what is the new average?",
    "options": ["50.5", "51", "52", "53"],
    "correct_answer": 0,
    "answer_explanation": "New total = (30\u00d750) + 80 = 1580. Average = 1580/31 \u2248 50.97 \u2248 50.5."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Time and Work",
    "difficulty": "medium",
    "question": "If 5 men can complete a work in 20 days, how many days will 10 men take?",
    "options": ["5", "8", "10", "12"],
    "correct_answer": 2,
    "answer_explanation": "Work \u221d men \u00d7 days. Days = (5\u00d720)/10 = 10."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Time and Work",
    "difficulty": "hard",
    "question": "A alone can do a work in 15 days. A and B together can do it in 10 days. How long will B alone take?",
    "options": ["20 days", "25 days", "30 days", "35 days"],
    "correct_answer": 2,
    "answer_explanation": "B\u2019s work/day = 1/10 \u2212 1/15 = 1/30 \u2192 30 days."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Time and Distance",
    "difficulty": "medium",
    "question": "A bus travels 120 km at 40 km/h. How long does it take?",
    "options": ["2 hrs", "3 hrs", "4 hrs", "5 hrs"],
    "correct_answer": 1,
    "answer_explanation": "Time = 120/40 = 3 hours."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Time and Distance",
    "difficulty": "hard",
    "question": "Two trains running at 50 km/h and 70 km/h in opposite directions cross each other in 18 seconds. Find the sum of their lengths.",
    "options": ["500 m", "600 m", "700 m", "800 m"],
    "correct_answer": 1,
    "answer_explanation": "Relative speed = 120 km/h = 33.33 m/s. Distance = 33.33\u00d718 \u2248 600 m."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Simple Interest",
    "difficulty": "medium",
    "question": "What will be the simple interest on \u20b92500 at 12% per annum for 2 years?",
    "options": ["\u20b9500", "\u20b9600", "\u20b9700", "\u20b9800"],
    "correct_answer": 1,
    "answer_explanation": "SI = (2500\u00d712\u00d72)/100 = 600."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Simple Interest",
    "difficulty": "hard",
    "question": "At what rate of simple interest will \u20b94000 become \u20b95200 in 3 years?",
    "options": ["8%", "9%", "10%", "11%"],
    "correct_answer": 2,
    "answer_explanation": "SI = 1200. Rate = (1200\u00d7100)/(4000\u00d73) = 10%."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Number System",
    "difficulty": "medium",
    "question": "What is the remainder when 345 is divided by 7?",
    "options": ["1", "2", "3", "4"],
    "correct_answer": 1,
    "answer_explanation": "345 \u00f7 7 leaves remainder 2."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Number System",
    "difficulty": "hard",
    "question": "Find the unit digit of 7^103.",
    "options": ["1", "3", "7", "9"],
    "correct_answer": 3,
    "answer_explanation": "Cycle of 7 = 7,9,3,1. 103 mod 4 = 3 \u2192 unit digit = 9."
  }
]

def seed_questions():
    db = SessionLocal()
    try:
        print(f"Seeding {len(USER_QUESTIONS)} manual questions...")
        
        for q_data in USER_QUESTIONS:
            # Check for duplicates by question text
            exists = db.query(AptitudeQuestion).filter(AptitudeQuestion.question == q_data["question"]).first()
            if not exists:
                new_q = AptitudeQuestion(**q_data)
                db.add(new_q)
            
        db.commit()
        print("Seeding complete.")
        
        # Verify final count
        total = db.query(AptitudeQuestion).count()
        print(f"Total questions now in database: {total}")
        
    except Exception as e:
        db.rollback()
        print(f"Error during seeding: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_questions()
