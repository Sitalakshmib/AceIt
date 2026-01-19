"""
Seed User Provided Questions (Set 2):
Adds a set of high-quality manual questions provided by the user.
"""

import sys
import os
import json

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_postgres import SessionLocal
from models.aptitude_sql import AptitudeQuestion

NEW_USER_QUESTIONS = [
  {
    "category": "Quantitative Ability",
    "topic": "Percentages",
    "difficulty": "easy",
    "question": "What is 15% of 300?",
    "options": ["30", "45", "50", "60"],
    "correct_answer": 1,
    "answer_explanation": "15% of 300 = (15/100) \u00d7 300 = 45."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Percentages",
    "difficulty": "medium",
    "question": "If a number is increased by 25%, by what percentage should it be decreased to get the original number?",
    "options": ["20%", "22%", "25%", "30%"],
    "correct_answer": 0,
    "answer_explanation": "Required decrease = (25/125) \u00d7 100 = 20%."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Profit and Loss",
    "difficulty": "easy",
    "question": "An article is sold for \u20b9750 at a profit of \u20b9150. What is the cost price?",
    "options": ["\u20b9500", "\u20b9550", "\u20b9600", "\u20b9650"],
    "correct_answer": 2,
    "answer_explanation": "Cost Price = Selling Price \u2212 Profit = 750 \u2212 150 = 600."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Profit and Loss",
    "difficulty": "medium",
    "question": "If an article is sold at 10% loss for \u20b9900, what would be the selling price at 10% profit?",
    "options": ["\u20b91100", "\u20b91000", "\u20b9990", "\u20b9950"],
    "correct_answer": 1,
    "answer_explanation": "CP = 900 \u00d7 (100/90) = 1000. New SP = 1000 \u00d7 1.1 = 1100."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Ratio and Proportion",
    "difficulty": "easy",
    "question": "What is the ratio of 24 to 36?",
    "options": ["2:3", "3:4", "4:5", "5:6"],
    "correct_answer": 0,
    "answer_explanation": "24:36 simplifies to 2:3."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Ratio and Proportion",
    "difficulty": "medium",
    "question": "The ratio of ages of A and B is 5:7. If B is 28 years old, what is A\u2019s age?",
    "options": ["18", "20", "22", "24"],
    "correct_answer": 1,
    "answer_explanation": "One part = 28/7 = 4. A = 5\u00d74 = 20."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Averages",
    "difficulty": "easy",
    "question": "Find the average of the first 10 natural numbers.",
    "options": ["4.5", "5", "5.5", "6"],
    "correct_answer": 2,
    "answer_explanation": "Sum = 55. Average = 55/10 = 5.5."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Averages",
    "difficulty": "medium",
    "question": "The average marks of 40 students is 60. If the marks of the teacher (80) are included, what is the new average?",
    "options": ["60.5", "61", "62", "63"],
    "correct_answer": 0,
    "answer_explanation": "New total = (40\u00d760)+80 = 2480. Average = 2480/41 \u2248 60.5."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Time and Work",
    "difficulty": "easy",
    "question": "If a person completes a work in 5 days, how much work does he do in one day?",
    "options": ["1/3", "1/4", "1/5", "1/6"],
    "correct_answer": 2,
    "answer_explanation": "Work done per day = 1/5."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Time and Work",
    "difficulty": "medium",
    "question": "A can do a work in 20 days and B in 30 days. In how many days will they complete it together?",
    "options": ["10", "12", "15", "18"],
    "correct_answer": 1,
    "answer_explanation": "Work/day = 1/20 + 1/30 = 5/60. Time = 60/5 = 12 days."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Time and Distance",
    "difficulty": "easy",
    "question": "A cyclist travels at 12 km/h for 2 hours. What distance does he cover?",
    "options": ["20 km", "22 km", "24 km", "26 km"],
    "correct_answer": 2,
    "answer_explanation": "Distance = 12 \u00d7 2 = 24 km."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Time and Distance",
    "difficulty": "medium",
    "question": "A car covers 360 km in 6 hours. What is its speed?",
    "options": ["50 km/h", "55 km/h", "60 km/h", "65 km/h"],
    "correct_answer": 2,
    "answer_explanation": "Speed = 360/6 = 60 km/h."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Simple Interest",
    "difficulty": "easy",
    "question": "What is the simple interest on \u20b9800 at 5% per annum for 2 years?",
    "options": ["\u20b960", "\u20b970", "\u20b980", "\u20b990"],
    "correct_answer": 2,
    "answer_explanation": "SI = (800\u00d75\u00d72)/100 = 80."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Simple Interest",
    "difficulty": "medium",
    "question": "In how many years will \u20b91000 amount to \u20b91400 at 10% simple interest?",
    "options": ["2 years", "3 years", "4 years", "5 years"],
    "correct_answer": 3,
    "answer_explanation": "SI = 400. Time = (400\u00d7100)/(1000\u00d710) = 4 years."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Number System",
    "difficulty": "easy",
    "question": "Which of the following is an even number?",
    "options": ["15", "21", "28", "35"],
    "correct_answer": 2,
    "answer_explanation": "28 is divisible by 2."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Number System",
    "difficulty": "medium",
    "question": "What is the smallest prime number?",
    "options": ["0", "1", "2", "3"],
    "correct_answer": 2,
    "answer_explanation": "2 is the smallest and only even prime number."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Percentages",
    "difficulty": "easy",
    "question": "What is 40% of 250?",
    "options": ["80", "90", "100", "110"],
    "correct_answer": 2,
    "answer_explanation": "40% of 250 = (40/100) \u00d7 250 = 100."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Percentages",
    "difficulty": "medium",
    "question": "If a salary is increased from \u20b920,000 to \u20b924,000, what is the percentage increase?",
    "options": ["15%", "18%", "20%", "25%"],
    "correct_answer": 2,
    "answer_explanation": "Increase = 4000. Percentage increase = (4000/20000) \u00d7 100 = 20%."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Percentages",
    "difficulty": "hard",
    "question": "If the price of an item is reduced by 20%, by what percentage must it be increased to regain the original price?",
    "options": ["20%", "22%", "25%", "30%"],
    "correct_answer": 2,
    "answer_explanation": "Required increase = (20/80) \u00d7 100 = 25%."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Profit and Loss",
    "difficulty": "easy",
    "question": "If the cost price of an item is \u20b9600 and selling price is \u20b9660, what is the profit percentage?",
    "options": ["8%", "9%", "10%", "12%"],
    "correct_answer": 2,
    "answer_explanation": "Profit = 60. Profit% = (60/600) \u00d7 100 = 10%."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Profit and Loss",
    "difficulty": "medium",
    "question": "An article is sold for \u20b9720 at a loss of 10%. What is its cost price?",
    "options": ["\u20b9780", "\u20b9800", "\u20b9820", "\u20b9840"],
    "correct_answer": 1,
    "answer_explanation": "CP = 720 \u00d7 (100/90) = 800."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Profit and Loss",
    "difficulty": "hard",
    "question": "A shopkeeper marks an article 25% above cost price and allows a discount of 10%. What is his profit percentage?",
    "options": ["10%", "12.5%", "15%", "20%"],
    "correct_answer": 1,
    "answer_explanation": "Net SP = 1.25 \u00d7 0.9 = 1.125 \u2192 Profit = 12.5%."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Ratio and Proportion",
    "difficulty": "easy",
    "question": "Find the ratio of 45 minutes to 1 hour.",
    "options": ["3:4", "4:5", "2:3", "1:2"],
    "correct_answer": 0,
    "answer_explanation": "45 min : 60 min = 3:4."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Ratio and Proportion",
    "difficulty": "medium",
    "question": "The ratio of two numbers is 7:9. If their difference is 18, find the larger number.",
    "options": ["54", "63", "72", "81"],
    "correct_answer": 3,
    "answer_explanation": "Difference = 2 parts = 18 \u2192 1 part = 9. Larger = 9\u00d79 = 81."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Ratio and Proportion",
    "difficulty": "hard",
    "question": "If A:B = 3:4 and B:C = 6:5, find A:C.",
    "options": ["9:10", "18:20", "12:15", "15:16"],
    "correct_answer": 0,
    "answer_explanation": "A:B = 9:12, B:C = 12:10 \u2192 A:C = 9:10."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Averages",
    "difficulty": "easy",
    "question": "What is the average of 5, 10, 15, 20?",
    "options": ["10", "12.5", "15", "17.5"],
    "correct_answer": 1,
    "answer_explanation": "Average = (5+10+15+20)/4 = 12.5."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Averages",
    "difficulty": "medium",
    "question": "The average of 9 numbers is 30. If one number is removed, the average becomes 28. What is the removed number?",
    "options": ["42", "44", "46", "48"],
    "correct_answer": 2,
    "answer_explanation": "Original sum = 270. New sum = 224. Removed number = 46."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Averages",
    "difficulty": "hard",
    "question": "The average age of a group of 10 persons is 25 years. If one person aged 35 leaves, what is the new average?",
    "options": ["23", "24", "26", "27"],
    "correct_answer": 1,
    "answer_explanation": "Original sum = 250. New sum = 215. Average = 215/9 \u2248 24."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Time and Work",
    "difficulty": "easy",
    "question": "If a work is completed in 4 days, what part of the work is done in one day?",
    "options": ["1/2", "1/3", "1/4", "1/5"],
    "correct_answer": 2,
    "answer_explanation": "Work done per day = 1/4."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Time and Work",
    "difficulty": "medium",
    "question": "A can do a work in 16 days and B in 24 days. How long will they take together?",
    "options": ["8", "9.6", "10", "12"],
    "correct_answer": 1,
    "answer_explanation": "Work/day = 1/16 + 1/24 = 5/48. Time = 48/5 = 9.6 days."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Percentages",
    "difficulty": "hard",
    "question": "If the price of sugar is increased by 25%, by what percentage must the consumption be reduced so that the expenditure remains the same?",
    "options": ["15%", "18%", "20%", "25%"],
    "correct_answer": 2,
    "answer_explanation": "Required reduction = (25 / (100 + 25)) \u00d7 100 = 20%."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Percentages",
    "difficulty": "hard",
    "question": "A number is first increased by 30% and then decreased by 20%. What is the net percentage change?",
    "options": ["4% increase", "6% increase", "4% decrease", "10% increase"],
    "correct_answer": 0,
    "answer_explanation": "Net change = 30 \u2212 20 \u2212 (30\u00d720)/100 = 4% increase."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Profit and Loss",
    "difficulty": "hard",
    "question": "A trader marks his goods 40% above cost price and allows a discount of 25%. What is his profit percentage?",
    "options": ["5%", "8%", "10%", "15%"],
    "correct_answer": 0,
    "answer_explanation": "Net SP = 1.4 \u00d7 0.75 = 1.05 \u2192 Profit = 5%."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Profit and Loss",
    "difficulty": "hard",
    "question": "By selling an article at \u20b9540, a man incurs a loss of 10%. At what price should he sell it to gain 10%?",
    "options": ["\u20b9600", "\u20b9660", "\u20b9720", "\u20b9750"],
    "correct_answer": 1,
    "answer_explanation": "CP = 540 \u00d7 (100/90) = 600. New SP = 600 \u00d7 1.1 = 660."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Ratio and Proportion",
    "difficulty": "hard",
    "question": "The ratio of incomes of A and B is 3:5 and their expenditures are in the ratio 2:3. If both save \u20b91000, find A\u2019s income.",
    "options": ["\u20b93000", "\u20b94000", "\u20b95000", "\u20b96000"],
    "correct_answer": 0,
    "answer_explanation": "Let incomes = 3x, 5x and expenditures = 2y, 3y. Savings equal \u21d2 3x\u22122y = 5x\u22123y = 1000 \u21d2 x = 1000. A\u2019s income = 3\u00d71000 = 3000."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Ratio and Proportion",
    "difficulty": "hard",
    "question": "If A:B:C = 2:3:5 and A+B = 20, find C.",
    "options": ["20", "25", "30", "35"],
    "correct_answer": 0,
    "answer_explanation": "A+B = 5 parts = 20 \u2192 1 part = 4 \u2192 C = 5\u00d74 = 20."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Averages",
    "difficulty": "hard",
    "question": "The average of 20 numbers is 30. If two numbers 10 and 20 are removed, what is the new average?",
    "options": ["31", "32", "33", "34"],
    "correct_answer": 1,
    "answer_explanation": "Original sum = 600. New sum = 570. New average = 570/18 \u2248 31.7 \u2248 32."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Averages",
    "difficulty": "hard",
    "question": "The average age of a class of 40 students is 15 years. If the teacher aged 35 joins, what is the new average?",
    "options": ["15.2", "15.5", "16", "16.5"],
    "correct_answer": 1,
    "answer_explanation": "New total = (40\u00d715)+35 = 635. Average = 635/41 \u2248 15.5."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Time and Work",
    "difficulty": "hard",
    "question": "A can complete a work in 12 days, B in 18 days. They work together for 4 days, then A leaves. How many more days will B take to finish the work?",
    "options": ["5", "6", "7", "8"],
    "correct_answer": 1,
    "answer_explanation": "Work done in 4 days = 4\u00d7(1/12+1/18)=10/36=5/18. Remaining = 13/18. Time by B = (13/18)/(1/18)=6 days."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Time and Work",
    "difficulty": "hard",
    "question": "If 6 men can do a work in 10 days, how many days will 15 men take to do the same work?",
    "options": ["3", "4", "5", "6"],
    "correct_answer": 1,
    "answer_explanation": "Work \u221d men\u00d7days \u2192 Days = (6\u00d710)/15 = 4 days."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Time and Distance",
    "difficulty": "hard",
    "question": "A train passes a pole in 10 seconds and a platform 110 m long in 21 seconds. Find the length of the train.",
    "options": ["100 m", "110 m", "120 m", "130 m"],
    "correct_answer": 0,
    "answer_explanation": "Difference time = 11 s \u2192 Distance = 110 m \u2192 Speed = 10 m/s \u2192 Train length = 10\u00d710 = 100 m."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Time and Distance",
    "difficulty": "hard",
    "question": "Two trains of equal length cross each other in 12 seconds at speeds 54 km/h and 36 km/h. Find the length of each train.",
    "options": ["120 m", "135 m", "150 m", "180 m"],
    "correct_answer": 2,
    "answer_explanation": "Relative speed = 90 km/h = 25 m/s. Distance = 25\u00d712 = 300 \u2192 Each train = 150 m."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Simple Interest",
    "difficulty": "hard",
    "question": "At what rate of simple interest will a sum double itself in 10 years?",
    "options": ["5%", "8%", "10%", "12%"],
    "correct_answer": 2,
    "answer_explanation": "SI = P \u2192 Rate = (100/10) = 10%."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Simple Interest",
    "difficulty": "hard",
    "question": "A sum amounts to \u20b96000 in 4 years and \u20b97200 in 7 years at simple interest. Find the principal.",
    "options": ["\u20b93000", "\u20b93600", "\u20b94000", "\u20b94800"],
    "correct_answer": 2,
    "answer_explanation": "Difference = 1200 for 3 years \u2192 SI per year = 400 \u2192 Principal = 4000."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Number System",
    "difficulty": "hard",
    "question": "Find the smallest number which when divided by 6, 8, and 12 leaves remainder 1 in each case.",
    "options": ["25", "49", "73", "97"],
    "correct_answer": 0,
    "answer_explanation": "LCM(6,8,12)=24 \u2192 Required number = 24+1 = 25."
  },
  {
    "category": "Quantitative Ability",
    "topic": "Number System",
    "difficulty": "hard",
    "question": "What is the greatest number that will divide 120, 180 and 240 leaving the same remainder?",
    "options": ["20", "30", "40", "60"],
    "correct_answer": 3,
    "answer_explanation": "HCF of differences = HCF(60,60) = 60."
  }
]

def seed_questions():
    db = SessionLocal()
    try:
        print(f"Seeding {len(NEW_USER_QUESTIONS)} manual questions...")
        added = 0
        for q_data in NEW_USER_QUESTIONS:
            # Check for duplicates by question text
            exists = db.query(AptitudeQuestion).filter(AptitudeQuestion.question == q_data["question"]).first()
            if not exists:
                new_q = AptitudeQuestion(**q_data)
                db.add(new_q)
                added += 1
            
        db.commit()
        print(f"Seeding complete. Added {added} new questions.")
        
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
