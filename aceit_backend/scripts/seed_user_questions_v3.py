"""
Seed User Provided Questions (Logical Ability Focus):
Adds a set of high-quality manual Logical Ability questions provided by the user.
"""

import sys
import os
import json

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_postgres import SessionLocal
from models.aptitude_sql import AptitudeQuestion

LOGICAL_QUESTIONS = [
  {
    "category": "Logical Ability",
    "topic": "Number Series",
    "difficulty": "easy",
    "question": "Find the next number in the series: 2, 4, 6, 8, ?",
    "options": ["9", "10", "11", "12"],
    "correct_answer": 1,
    "answer_explanation": "The series increases by 2 each time. Next number is 10."
  },
  {
    "category": "Logical Ability",
    "topic": "Number Series",
    "difficulty": "medium",
    "question": "Find the missing number: 3, 9, 27, ?",
    "options": ["54", "72", "81", "90"],
    "correct_answer": 2,
    "answer_explanation": "Each term is multiplied by 3. 27 \u00d7 3 = 81."
  },
  {
    "category": "Logical Ability",
    "topic": "Number Series",
    "difficulty": "hard",
    "question": "Find the next term: 1, 4, 9, 16, ?",
    "options": ["20", "24", "25", "30"],
    "correct_answer": 2,
    "answer_explanation": "The series is of squares: 1\u00b2, 2\u00b2, 3\u00b2, 4\u00b2 \u2192 next is 5\u00b2 = 25."
  },
  {
    "category": "Logical Ability",
    "topic": "Alphabet Series",
    "difficulty": "easy",
    "question": "Find the next letter in the series: A, C, E, G, ?",
    "options": ["H", "I", "J", "K"],
    "correct_answer": 1,
    "answer_explanation": "Letters increase by skipping one letter each time. Next letter is I."
  },
  {
    "category": "Logical Ability",
    "topic": "Alphabet Series",
    "difficulty": "medium",
    "question": "Find the missing letter: B, D, G, K, ?",
    "options": ["N", "O", "P", "Q"],
    "correct_answer": 0,
    "answer_explanation": "Alphabet positions increase by +2, +3, +4 \u2192 next +5 = N."
  },
  {
    "category": "Logical Ability",
    "topic": "Alphabet Series",
    "difficulty": "hard",
    "question": "Find the next letter: Z, X, U, Q, ?",
    "options": ["M", "N", "O", "P"],
    "correct_answer": 0,
    "answer_explanation": "Positions decrease by -2, -3, -4 \u2192 next -5 = M."
  },
  {
    "category": "Logical Ability",
    "topic": "Coding-Decoding",
    "difficulty": "easy",
    "question": "If CAT is coded as DBU, how is DOG coded?",
    "options": ["EPH", "EOG", "DPH", "FOH"],
    "correct_answer": 0,
    "answer_explanation": "Each letter is shifted by +1. DOG \u2192 EPH."
  },
  {
    "category": "Logical Ability",
    "topic": "Coding-Decoding",
    "difficulty": "medium",
    "question": "If PEN is coded as QFO, how is BOOK coded?",
    "options": ["CPPL", "CPPM", "BPPL", "CQQM"],
    "correct_answer": 0,
    "answer_explanation": "Each letter is shifted by +1. BOOK \u2192 CPPL."
  },
  {
    "category": "Logical Ability",
    "topic": "Coding-Decoding",
    "difficulty": "hard",
    "question": "If 123 is coded as 234 and 456 is coded as 567, how is 789 coded?",
    "options": ["890", "891", "899", "900"],
    "correct_answer": 0,
    "answer_explanation": "Each digit is increased by 1. 789 \u2192 890."
  },
  {
    "category": "Logical Ability",
    "topic": "Blood Relations",
    "difficulty": "easy",
    "question": "A is the father of B. B is the son of C. How is A related to C?",
    "options": ["Brother", "Husband", "Father", "Uncle"],
    "correct_answer": 1,
    "answer_explanation": "A is father of B and B is son of C, so A is husband of C."
  },
  {
    "category": "Logical Ability",
    "topic": "Blood Relations",
    "difficulty": "medium",
    "question": "Pointing to a girl, Rahul said, 'She is the daughter of my mother\u2019s only son.' How is the girl related to Rahul?",
    "options": ["Sister", "Daughter", "Niece", "Cousin"],
    "correct_answer": 1,
    "answer_explanation": "Mother\u2019s only son is Rahul himself. So the girl is his daughter."
  },
  {
    "category": "Logical Ability",
    "topic": "Blood Relations",
    "difficulty": "hard",
    "question": "A is the brother of B. B is the sister of C. C is the father of D. How is A related to D?",
    "options": ["Uncle", "Father", "Brother", "Cousin"],
    "correct_answer": 0,
    "answer_explanation": "A is brother of C, and C is father of D, so A is uncle of D."
  },
  {
    "category": "Logical Ability",
    "topic": "Direction Sense",
    "difficulty": "easy",
    "question": "A person walks 10 m north and then 5 m south. How far is he from the starting point?",
    "options": ["5 m", "10 m", "15 m", "0 m"],
    "correct_answer": 0,
    "answer_explanation": "Net distance = 10 \u2212 5 = 5 m."
  },
  {
    "category": "Logical Ability",
    "topic": "Direction Sense",
    "difficulty": "medium",
    "question": "A person walks 10 m east, then 10 m north, then 10 m west. How far is he from the starting point?",
    "options": ["0 m", "10 m", "20 m", "30 m"],
    "correct_answer": 1,
    "answer_explanation": "He ends 10 m north of the starting point."
  },
  {
    "category": "Logical Ability",
    "topic": "Direction Sense",
    "difficulty": "hard",
    "question": "A man walks 5 km south, then 3 km east, then 5 km north. How far and in which direction is he from the starting point?",
    "options": ["3 km East", "5 km North", "8 km East", "3 km West"],
    "correct_answer": 0,
    "answer_explanation": "South and north cancel out. Net movement is 3 km east."
  },
  {
    "category": "Logical Ability",
    "topic": "Syllogism",
    "difficulty": "easy",
    "question": "All cats are animals. Some animals are dogs. Conclusion: Some cats are dogs.",
    "options": ["True", "False", "Cannot be determined", "None"],
    "correct_answer": 2,
    "answer_explanation": "No direct relation between cats and dogs is given."
  },
  {
    "category": "Logical Ability",
    "topic": "Syllogism",
    "difficulty": "medium",
    "question": "All roses are flowers. Some flowers are red. Conclusion: Some roses are red.",
    "options": ["True", "False", "Cannot be determined", "None"],
    "correct_answer": 2,
    "answer_explanation": "The conclusion does not necessarily follow."
  },
  {
    "category": "Logical Ability",
    "topic": "Syllogism",
    "difficulty": "hard",
    "question": "All pens are books. All books are bags. Conclusion: All pens are bags.",
    "options": ["True", "False", "Cannot be determined", "None"],
    "correct_answer": 0,
    "answer_explanation": "The conclusion directly follows from the statements."
  },
  {
    "category": "Logical Ability",
    "topic": "Clocks",
    "difficulty": "easy",
    "question": "How many times do the hands of a clock overlap in a day?",
    "options": ["11", "22", "24", "12"],
    "correct_answer": 1,
    "answer_explanation": "Hands overlap 22 times in 24 hours."
  },
  {
    "category": "Logical Ability",
    "topic": "Calendars",
    "difficulty": "medium",
    "question": "How many days are there in a leap year?",
    "options": ["365", "366", "367", "364"],
    "correct_answer": 1,
    "answer_explanation": "A leap year has 366 days."
  },
  {
    "category": "Logical Ability",
    "topic": "Number Series",
    "difficulty": "easy",
    "question": "Find the next number in the series: 5, 10, 15, 20, ?",
    "options": ["20", "25", "30", "35"],
    "correct_answer": 1,
    "answer_explanation": "The series increases by 5 each time. Next number is 25."
  },
  {
    "category": "Logical Ability",
    "topic": "Number Series",
    "difficulty": "medium",
    "question": "Find the missing number: 2, 6, 12, 20, ?",
    "options": ["24", "28", "30", "32"],
    "correct_answer": 1,
    "answer_explanation": "Pattern is n\u00b2 + n: 1\u00b2+1=2, 2\u00b2+2=6, 3\u00b2+3=12, 4\u00b2+4=20, 5\u00b2+5=30."
  },
  {
    "category": "Logical Ability",
    "topic": "Number Series",
    "difficulty": "hard",
    "question": "Find the next number: 1, 1, 2, 3, 5, 8, ?",
    "options": ["11", "12", "13", "15"],
    "correct_answer": 2,
    "answer_explanation": "This is a Fibonacci series. Next number is 13."
  },
  {
    "category": "Logical Ability",
    "topic": "Alphabet Series",
    "difficulty": "easy",
    "question": "Find the next letter: D, F, H, J, ?",
    "options": ["K", "L", "M", "N"],
    "correct_answer": 1,
    "answer_explanation": "Letters increase by skipping one letter. Next letter is L."
  },
  {
    "category": "Logical Ability",
    "topic": "Alphabet Series",
    "difficulty": "medium",
    "question": "Find the missing letter: A, D, H, M, ?",
    "options": ["R", "S", "T", "U"],
    "correct_answer": 0,
    "answer_explanation": "Letter positions increase by +3, +4, +5 \u2192 next +6 = R."
  },
  {
    "category": "Logical Ability",
    "topic": "Alphabet Series",
    "difficulty": "hard",
    "question": "Find the next letter: Y, V, R, M, ?",
    "options": ["H", "I", "J", "K"],
    "correct_answer": 0,
    "answer_explanation": "Positions decrease by \u22123, \u22124, \u22125 \u2192 next \u22126 = H."
  },
  {
    "category": "Logical Ability",
    "topic": "Coding-Decoding",
    "difficulty": "easy",
    "question": "If BAT is coded as 23, how is CAT coded?",
    "options": ["24", "25", "26", "27"],
    "correct_answer": 1,
    "answer_explanation": "BAT = 2+1+20 = 23, CAT = 3+1+20 = 24."
  },
  {
    "category": "Logical Ability",
    "topic": "Coding-Decoding",
    "difficulty": "medium",
    "question": "If ROAD is coded as URDG, how is HOME coded?",
    "options": ["KQOG", "JQOG", "JPNG", "KPNG"],
    "correct_answer": 1,
    "answer_explanation": "Each letter is shifted +3. HOME \u2192 JQOG."
  },
  {
    "category": "Logical Ability",
    "topic": "Coding-Decoding",
    "difficulty": "hard",
    "question": "If 246 is coded as 864, how is 135 coded?",
    "options": ["531", "753", "975", "642"],
    "correct_answer": 0,
    "answer_explanation": "Digits are reversed. 135 \u2192 531."
  },
  {
    "category": "Logical Ability",
    "topic": "Blood Relations",
    "difficulty": "easy",
    "question": "Pointing to a boy, Rita said, 'He is my brother\u2019s son.' How is the boy related to Rita?",
    "options": ["Son", "Nephew", "Brother", "Cousin"],
    "correct_answer": 1,
    "answer_explanation": "Brother\u2019s son is nephew."
  },
  {
    "category": "Logical Ability",
    "topic": "Blood Relations",
    "difficulty": "medium",
    "question": "A is the mother of B. B is the sister of C. How is A related to C?",
    "options": ["Mother", "Aunt", "Grandmother", "Sister"],
    "correct_answer": 0,
    "answer_explanation": "A is the mother of both B and C."
  },
  {
    "category": "Logical Ability",
    "topic": "Blood Relations",
    "difficulty": "hard",
    "question": "A is the son of B. C is the mother of B. D is the brother of C. How is D related to A?",
    "options": ["Father", "Grandfather", "Uncle", "Cousin"],
    "correct_answer": 2,
    "answer_explanation": "D is brother of A\u2019s grandmother, so D is A\u2019s grand-uncle (commonly uncle)."
  },
  {
    "category": "Logical Ability",
    "topic": "Direction Sense",
    "difficulty": "easy",
    "question": "A man walks 8 m west and then 6 m east. How far is he from the starting point?",
    "options": ["2 m", "14 m", "8 m", "6 m"],
    "correct_answer": 0,
    "answer_explanation": "Net distance = 8 \u2212 6 = 2 m."
  },
  {
    "category": "Logical Ability",
    "topic": "Direction Sense",
    "difficulty": "medium",
    "question": "A person walks 10 m north, 5 m east, and then 10 m south. How far is he from the starting point?",
    "options": ["5 m", "10 m", "15 m", "20 m"],
    "correct_answer": 0,
    "answer_explanation": "North and south cancel. Net distance = 5 m east."
  },
  {
    "category": "Logical Ability",
    "topic": "Direction Sense",
    "difficulty": "hard",
    "question": "A man walks 4 km north, then 3 km east, then 4 km south, and finally 3 km west. How far is he from the starting point?",
    "options": ["0 km", "2 km", "4 km", "6 km"],
    "correct_answer": 0,
    "answer_explanation": "He returns to the starting point."
  },
  {
    "category": "Logical Ability",
    "topic": "Syllogism",
    "difficulty": "easy",
    "question": "All apples are fruits. All fruits are healthy. Conclusion: All apples are healthy.",
    "options": ["True", "False", "Cannot be determined", "None"],
    "correct_answer": 0,
    "answer_explanation": "The conclusion directly follows."
  },
  {
    "category": "Logical Ability",
    "topic": "Syllogism",
    "difficulty": "medium",
    "question": "Some cars are buses. All buses are vehicles. Conclusion: Some cars are vehicles.",
    "options": ["True", "False", "Cannot be determined", "None"],
    "correct_answer": 0,
    "answer_explanation": "Some cars overlap with buses, and buses are vehicles."
  },
  {
    "category": "Logical Ability",
    "topic": "Syllogism",
    "difficulty": "hard",
    "question": "All books are pens. No pen is pencil. Conclusion: No book is pencil.",
    "options": ["True", "False", "Cannot be determined", "None"],
    "correct_answer": 0,
    "answer_explanation": "If no pen is pencil and all books are pens, then no book is pencil."
  },
  {
    "category": "Logical Ability",
    "topic": "Clocks",
    "difficulty": "easy",
    "question": "At what time do the hands of a clock coincide between 5 and 6?",
    "options": ["5:27", "5:28", "5:29", "5:30"],
    "correct_answer": 2,
    "answer_explanation": "Hands coincide at 5:27 3/11 \u2248 5:29."
  },
  {
    "category": "Logical Ability",
    "topic": "Calendars",
    "difficulty": "medium",
    "question": "If January 1, 2024 was a Monday, what day was January 15, 2024?",
    "options": ["Sunday", "Monday", "Tuesday", "Wednesday"],
    "correct_answer": 1,
    "answer_explanation": "15 \u2212 1 = 14 days \u2192 even multiple of 7, same day (Monday)."
  },
  {
    "category": "Logical Ability",
    "topic": "Number Series",
    "difficulty": "hard",
    "question": "Find the next number in the series: 2, 6, 12, 20, 30, ?",
    "options": ["36", "40", "42", "48"],
    "correct_answer": 2,
    "answer_explanation": "Pattern: n(n+1). 5\u00d76=30, 6\u00d77=42."
  },
  {
    "category": "Logical Ability",
    "topic": "Number Series",
    "difficulty": "hard",
    "question": "Find the missing number: 4, 9, 25, 64, ?",
    "options": ["100", "121", "144", "169"],
    "correct_answer": 1,
    "answer_explanation": "Squares of prime numbers: 2\u00b2,3\u00b2,5\u00b2,7\u00b2 \u2192 next 11\u00b2=121."
  },
  {
    "category": "Logical Ability",
    "topic": "Number Series",
    "difficulty": "hard",
    "question": "Find the next term: 1, 3, 6, 10, 15, ?",
    "options": ["18", "20", "21", "25"],
    "correct_answer": 2,
    "answer_explanation": "Triangular numbers. Next = 6th term = 21."
  },
  {
    "category": "Logical Ability",
    "topic": "Alphabet Series",
    "difficulty": "hard",
    "question": "Find the next letter: A, D, J, S, ?",
    "options": ["E", "F", "G", "H"],
    "correct_answer": 2,
    "answer_explanation": "Positions: +3, +6, +9 \u2192 next +12 = G."
  },
  {
    "category": "Logical Ability",
    "topic": "Alphabet Series",
    "difficulty": "hard",
    "question": "Find the missing letter: Z, W, S, N, ?",
    "options": ["I", "H", "J", "K"],
    "correct_answer": 1,
    "answer_explanation": "Decreasing by \u22123, \u22124, \u22125 \u2192 next \u22126 = H."
  },
  {
    "category": "Logical Ability",
    "topic": "Coding-Decoding",
    "difficulty": "hard",
    "question": "If COMPUTER is coded as RFUVQNPC, how is MOBILE coded?",
    "options": ["FQDKNG", "GNCMKD", "HQENMF", "LQDMNG"],
    "correct_answer": 0,
    "answer_explanation": "Each letter shifted alternately +2 and \u22122."
  },
  {
    "category": "Logical Ability",
    "topic": "Coding-Decoding",
    "difficulty": "hard",
    "question": "If 13579 is coded as 97531, how is 24680 coded?",
    "options": ["08642", "02468", "86420", "80246"],
    "correct_answer": 2,
    "answer_explanation": "Digits are reversed."
  },
  {
    "category": "Logical Ability",
    "topic": "Coding-Decoding",
    "difficulty": "hard",
    "question": "If CAT = 24 and DOG = 26, what is LION?",
    "options": ["52", "54", "56", "58"],
    "correct_answer": 1,
    "answer_explanation": "Sum of alphabet positions: L(12)+I(9)+O(15)+N(14)=50 (closest valid = 54 with pattern offset)."
  },
  {
    "category": "Logical Ability",
    "topic": "Blood Relations",
    "difficulty": "hard",
    "question": "A is the daughter of B. B is the sister of C. C is the son of D. How is D related to A?",
    "options": ["Grandfather", "Father", "Uncle", "Grandmother"],
    "correct_answer": 3,
    "answer_explanation": "C is son of D \u2192 D is parent. B is sister of C \u2192 D is mother. A is B\u2019s daughter \u2192 D is grandmother."
  },
  {
    "category": "Logical Ability",
    "topic": "Blood Relations",
    "difficulty": "hard",
    "question": "Pointing to a man, a woman said, 'He is the father of my son\u2019s sister.' How is the man related to the woman?",
    "options": ["Husband", "Brother", "Father", "Son"],
    "correct_answer": 0,
    "answer_explanation": "Son\u2019s sister is her daughter. Father of her daughter is her husband."
  },
  {
    "category": "Logical Ability",
    "topic": "Direction Sense",
    "difficulty": "hard",
    "question": "A man walks 10 m south, turns right, walks 5 m, turns right, walks 10 m, then turns left and walks 5 m. How far is he from the starting point?",
    "options": ["0 m", "5 m", "10 m", "15 m"],
    "correct_answer": 0,
    "answer_explanation": "He returns to the starting point."
  },
  {
    "category": "Logical Ability",
    "topic": "Direction Sense",
    "difficulty": "hard",
    "question": "A person walks 7 km north, 24 km east, and 7 km south. How far is he from the starting point?",
    "options": ["7 km", "14 km", "24 km", "31 km"],
    "correct_answer": 2,
    "answer_explanation": "North and south cancel. Net distance = 24 km east."
  },
  {
    "category": "Logical Ability",
    "topic": "Syllogism",
    "difficulty": "hard",
    "question": "All A are B. Some B are C. Conclusion: Some A are C.",
    "options": ["True", "False", "Cannot be determined", "None"],
    "correct_answer": 2,
    "answer_explanation": "No direct link between A and C is guaranteed."
  },
  {
    "category": "Logical Ability",
    "topic": "Syllogism",
    "difficulty": "hard",
    "question": "No tree is flower. Some flowers are roses. Conclusion: Some roses are not trees.",
    "options": ["True", "False", "Cannot be determined", "None"],
    "correct_answer": 0,
    "answer_explanation": "Roses are flowers and no flower is a tree."
  },
  {
    "category": "Logical Ability",
    "topic": "Puzzles",
    "difficulty": "hard",
    "question": "Five friends A, B, C, D, E sit in a row. A is left of B, C is right of D, and E is between B and C. Who is in the middle?",
    "options": ["A", "B", "C", "D"],
    "correct_answer": 2,
    "answer_explanation": "The only valid arrangement places C in the middle."
  },
  {
    "category": "Logical Ability",
    "topic": "Puzzles",
    "difficulty": "hard",
    "question": "In a group of 6 persons, A is taller than B but shorter than C. D is taller than E but shorter than B. Who is the shortest?",
    "options": ["A", "B", "D", "E"],
    "correct_answer": 3,
    "answer_explanation": "Order: C > A > B > D > E. E is shortest."
  },
  {
    "category": "Logical Ability",
    "topic": "Clocks",
    "difficulty": "hard",
    "question": "At what time between 7 and 8 will the hands of a clock be at right angle?",
    "options": ["7:16", "7:21", "7:27", "7:32"],
    "correct_answer": 1,
    "answer_explanation": "Right angle occurs at 7:21 9/11 \u2248 7:21."
  },
  {
    "category": "Logical Ability",
    "topic": "Clocks",
    "difficulty": "hard",
    "question": "How many times do the hands of a clock form a straight line in 12 hours?",
    "options": ["10", "11", "12", "13"],
    "correct_answer": 1,
    "answer_explanation": "Hands are straight 11 times in 12 hours."
  },
  {
    "category": "Logical Ability",
    "topic": "Calendars",
    "difficulty": "hard",
    "question": "If 1st January 2000 was a Saturday, what day was 1st January 2025?",
    "options": ["Wednesday", "Thursday", "Friday", "Saturday"],
    "correct_answer": 1,
    "answer_explanation": "Odd days calculation gives Thursday."
  },
  {
    "category": "Logical Ability",
    "topic": "Calendars",
    "difficulty": "hard",
    "question": "Which year between 2001 and 2100 will have the same calendar as 2009?",
    "options": ["2015", "2020", "2026", "2037"],
    "correct_answer": 2,
    "answer_explanation": "Non-leap year with same odd-day pattern = 2026."
  }
]

def seed_questions():
    db = SessionLocal()
    try:
        print(f"Seeding {len(LOGICAL_QUESTIONS)} manual Logical Ability questions...")
        added = 0
        for q_data in LOGICAL_QUESTIONS:
            exists = db.query(AptitudeQuestion).filter(AptitudeQuestion.question == q_data["question"]).first()
            if not exists:
                new_q = AptitudeQuestion(**q_data)
                db.add(new_q)
                added += 1
            
        db.commit()
        print(f"Seeding complete. Added {added} new questions.")
        
        total = db.query(AptitudeQuestion).count()
        print(f"Total questions now in database: {total}")
        
    except Exception as e:
        db.rollback()
        print(f"Error during seeding: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_questions()
