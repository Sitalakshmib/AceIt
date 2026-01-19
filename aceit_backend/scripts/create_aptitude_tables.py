"""
Create aptitude tables and seed with comprehensive question data.
Run this script from the aceit_backend directory:
    python scripts/create_aptitude_tables.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_postgres import engine, Base, SessionLocal
from models.aptitude_sql import AptitudeQuestion, UserAptitudeProgress
from models.user_sql import User  # Required for foreign key relationship

# Create all tables
print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")

# Seed data
APTITUDE_QUESTIONS = [
    # ========== LOGICAL ABILITY ==========
    # Number Series
    {
        "question": "What comes next in the series: 2, 6, 12, 20, 30, ?",
        "options": ["42", "40", "38", "44"],
        "correct_answer": 0,
        "answer_explanation": "The pattern is: +4, +6, +8, +10, +12. So 30 + 12 = 42",
        "topic": "Number Series",
        "category": "Logical Ability",
        "difficulty": "easy"
    },
    {
        "question": "Find the next number: 1, 4, 9, 16, 25, ?",
        "options": ["30", "36", "49", "35"],
        "correct_answer": 1,
        "answer_explanation": "These are perfect squares: 1², 2², 3², 4², 5², 6² = 36",
        "topic": "Number Series",
        "category": "Logical Ability",
        "difficulty": "easy"
    },
    {
        "question": "What is the next number in the series: 3, 9, 27, 81, ?",
        "options": ["162", "243", "324", "189"],
        "correct_answer": 1,
        "answer_explanation": "Each number is multiplied by 3: 81 × 3 = 243",
        "topic": "Number Series",
        "category": "Logical Ability",
        "difficulty": "easy"
    },
    {
        "question": "Find the missing number: 2, 5, 11, 23, 47, ?",
        "options": ["94", "95", "96", "97"],
        "correct_answer": 1,
        "answer_explanation": "Pattern: ×2+1. So 47×2+1 = 95",
        "topic": "Number Series",
        "category": "Logical Ability",
        "difficulty": "medium"
    },
    {
        "question": "What comes next: 1, 2, 4, 7, 11, 16, ?",
        "options": ["22", "21", "23", "24"],
        "correct_answer": 0,
        "answer_explanation": "Differences are +1, +2, +3, +4, +5, +6. So 16+6 = 22",
        "topic": "Number Series",
        "category": "Logical Ability",
        "difficulty": "medium"
    },
    {
        "question": "Find the next: 1, 1, 2, 3, 5, 8, 13, ?",
        "options": ["18", "20", "21", "19"],
        "correct_answer": 2,
        "answer_explanation": "Fibonacci series: each number is sum of previous two. 8+13 = 21",
        "topic": "Number Series",
        "category": "Logical Ability",
        "difficulty": "medium"
    },
    {
        "question": "What is the next number: 2, 3, 5, 7, 11, 13, ?",
        "options": ["15", "17", "19", "21"],
        "correct_answer": 1,
        "answer_explanation": "These are prime numbers. Next prime after 13 is 17",
        "topic": "Number Series",
        "category": "Logical Ability",
        "difficulty": "hard"
    },
    {
        "question": "Find the pattern: 8, 27, 64, 125, ?",
        "options": ["196", "216", "256", "225"],
        "correct_answer": 1,
        "answer_explanation": "These are cubes: 2³, 3³, 4³, 5³, 6³ = 216",
        "topic": "Number Series",
        "category": "Logical Ability",
        "difficulty": "hard"
    },
    
    # Coding-Decoding
    {
        "question": "If APPLE is coded as ELPPA, how is BANANA coded?",
        "options": ["ANANAB", "NANABA", "NAANAB", "BANANA"],
        "correct_answer": 0,
        "answer_explanation": "The word is reversed. BANANA reversed is ANANAB",
        "topic": "Coding-Decoding",
        "category": "Logical Ability",
        "difficulty": "easy"
    },
    {
        "question": "If CAT = 24, DOG = 26, then RAT = ?",
        "options": ["27", "37", "39", "33"],
        "correct_answer": 2,
        "answer_explanation": "C(3)+A(1)+T(20)=24, D(4)+O(15)+G(7)=26, R(18)+A(1)+T(20)=39",
        "topic": "Coding-Decoding",
        "category": "Logical Ability",
        "difficulty": "medium"
    },
    {
        "question": "If 'COMPUTER' is coded as 'RETUPMOC', then 'KEYBOARD' is coded as?",
        "options": ["DRAOBYEK", "DRAOYEKB", "YEKBOARD", "DRAOBKEY"],
        "correct_answer": 0,
        "answer_explanation": "The letters are reversed. KEYBOARD reversed is DRAOBYEK",
        "topic": "Coding-Decoding",
        "category": "Logical Ability",
        "difficulty": "easy"
    },
    {
        "question": "If A=1, B=2, C=3, what is the code for HELLO?",
        "options": ["8-5-12-12-15", "7-5-12-12-15", "8-6-12-12-15", "8-5-11-12-15"],
        "correct_answer": 0,
        "answer_explanation": "H=8, E=5, L=12, L=12, O=15",
        "topic": "Coding-Decoding",
        "category": "Logical Ability",
        "difficulty": "easy"
    },
    {
        "question": "In a certain code, PENCIL is written as QFODKM. How is MOTHER written?",
        "options": ["NPUIFS", "NPUIRF", "NQUJFS", "NPVIFS"],
        "correct_answer": 0,
        "answer_explanation": "Each letter is replaced by next letter. M+1=N, O+1=P, T+1=U, H+1=I, E+1=F, R+1=S",
        "topic": "Coding-Decoding",
        "category": "Logical Ability",
        "difficulty": "hard"
    },
    
    # Blood Relations
    {
        "question": "Pointing to a photograph, a man said 'She is the daughter of my grandfather's only son.' How is the woman in the photograph related to the man?",
        "options": ["Sister", "Mother", "Cousin", "Aunt"],
        "correct_answer": 0,
        "answer_explanation": "Grandfather's only son is the man's father. His daughter is the man's sister.",
        "topic": "Blood Relations",
        "category": "Logical Ability",
        "difficulty": "medium"
    },
    {
        "question": "If A is the brother of B, B is the sister of C, and C is the father of D, how is A related to D?",
        "options": ["Uncle", "Father", "Grandfather", "Brother"],
        "correct_answer": 0,
        "answer_explanation": "A is brother of B, B is sister of C, so A is brother of C. C is father of D, so A is Uncle of D.",
        "topic": "Blood Relations",
        "category": "Logical Ability",
        "difficulty": "medium"
    },
    {
        "question": "A's mother is B's sister. B has a daughter C. How is A related to C?",
        "options": ["Cousin", "Nephew", "Niece", "Uncle"],
        "correct_answer": 0,
        "answer_explanation": "A's mother and B are siblings. So A and C (B's daughter) are cousins.",
        "topic": "Blood Relations",
        "category": "Logical Ability",
        "difficulty": "medium"
    },
    {
        "question": "Pointing to a man in a photograph, a woman said, 'He is the only son of my mother's mother.' How is the man related to the woman?",
        "options": ["Father", "Uncle", "Brother", "Grandfather"],
        "correct_answer": 1,
        "answer_explanation": "Woman's mother's mother is her grandmother. The only son of grandmother is woman's uncle.",
        "topic": "Blood Relations",
        "category": "Logical Ability",
        "difficulty": "hard"
    },
    
    # Direction Sense
    {
        "question": "A man walks 5 km South, then turns left and walks 3 km. In which direction is he now from his starting point?",
        "options": ["South-East", "North-East", "South-West", "North-West"],
        "correct_answer": 0,
        "answer_explanation": "Starting South, then turning left means going East. From start, he is South-East.",
        "topic": "Direction Sense",
        "category": "Logical Ability",
        "difficulty": "easy"
    },
    {
        "question": "Ram starts from his house and walks 4 km North, then 3 km East. How far is he from his starting point?",
        "options": ["5 km", "7 km", "6 km", "4 km"],
        "correct_answer": 0,
        "answer_explanation": "Using Pythagoras: √(4² + 3²) = √(16+9) = √25 = 5 km",
        "topic": "Direction Sense",
        "category": "Logical Ability",
        "difficulty": "medium"
    },
    {
        "question": "A person faces North, turns 90° clockwise, then 180°. Which direction is he facing now?",
        "options": ["South", "West", "North", "East"],
        "correct_answer": 1,
        "answer_explanation": "North → 90° clockwise → East → 180° → West",
        "topic": "Direction Sense",
        "category": "Logical Ability",
        "difficulty": "easy"
    },
    {
        "question": "Ravi walks 10 km towards North. From there, he walks 6 km towards South. Then, he walks 3 km towards East. How far and in which direction is he with reference to his starting point?",
        "options": ["5 km North-East", "5 km North", "7 km East", "7 km North-East"],
        "correct_answer": 0,
        "answer_explanation": "Net North = 10-6 = 4 km, East = 3 km. Distance = √(16+9) = 5 km North-East",
        "topic": "Direction Sense",
        "category": "Logical Ability",
        "difficulty": "hard"
    },
    
    # Logical Puzzles
    {
        "question": "If all roses are flowers, and some flowers fade quickly, which statement must be true?",
        "options": ["All roses fade quickly", "Some roses fade quickly", "No roses fade quickly", "Cannot be determined"],
        "correct_answer": 3,
        "answer_explanation": "We only know some flowers fade quickly, not which ones. Cannot determine if roses are among them.",
        "topic": "Logical Puzzles",
        "category": "Logical Ability",
        "difficulty": "medium"
    },
    {
        "question": "Five friends A, B, C, D, E are sitting in a row. A is to the left of B. C is to the right of D. E is between A and D. Who is in the middle?",
        "options": ["A", "E", "D", "B"],
        "correct_answer": 1,
        "answer_explanation": "Arrangement: A-E-D-B-C or similar. E is between A and D, making E in middle.",
        "topic": "Logical Puzzles",
        "category": "Logical Ability",
        "difficulty": "hard"
    },
    
    # ========== QUANTITATIVE ABILITY ==========
    # Percentages
    {
        "question": "What is 25% of 200?",
        "options": ["40", "50", "60", "45"],
        "correct_answer": 1,
        "answer_explanation": "25% of 200 = (25/100) × 200 = 50",
        "topic": "Percentages",
        "category": "Quantitative Ability",
        "difficulty": "easy"
    },
    {
        "question": "If a number is increased by 20% and then decreased by 20%, what is the net change?",
        "options": ["No change", "4% decrease", "4% increase", "2% decrease"],
        "correct_answer": 1,
        "answer_explanation": "Let number = 100. After 20% increase = 120. After 20% decrease = 120 × 0.8 = 96. Net change = 4% decrease",
        "topic": "Percentages",
        "category": "Quantitative Ability",
        "difficulty": "medium"
    },
    {
        "question": "A student scores 450 marks out of 600. What is the percentage?",
        "options": ["70%", "75%", "80%", "72%"],
        "correct_answer": 1,
        "answer_explanation": "(450/600) × 100 = 75%",
        "topic": "Percentages",
        "category": "Quantitative Ability",
        "difficulty": "easy"
    },
    {
        "question": "The price of an item increased from ₹80 to ₹100. Find the percentage increase.",
        "options": ["20%", "25%", "15%", "30%"],
        "correct_answer": 1,
        "answer_explanation": "Increase = 20, Percentage = (20/80) × 100 = 25%",
        "topic": "Percentages",
        "category": "Quantitative Ability",
        "difficulty": "easy"
    },
    {
        "question": "If 40% of a number is 80, what is the number?",
        "options": ["160", "200", "180", "220"],
        "correct_answer": 1,
        "answer_explanation": "40% × x = 80, so x = 80 × (100/40) = 200",
        "topic": "Percentages",
        "category": "Quantitative Ability",
        "difficulty": "medium"
    },
    {
        "question": "Two successive discounts of 10% and 20% are equivalent to a single discount of:",
        "options": ["30%", "28%", "27%", "25%"],
        "correct_answer": 1,
        "answer_explanation": "Net discount = 100 - (90% of 80%) = 100 - 72 = 28%",
        "topic": "Percentages",
        "category": "Quantitative Ability",
        "difficulty": "hard"
    },
    
    # Profit & Loss
    {
        "question": "A shopkeeper buys an article for ₹400 and sells it for ₹500. What is his profit percentage?",
        "options": ["20%", "25%", "30%", "15%"],
        "correct_answer": 1,
        "answer_explanation": "Profit = 100, Profit% = (100/400) × 100 = 25%",
        "topic": "Profit & Loss",
        "category": "Quantitative Ability",
        "difficulty": "easy"
    },
    {
        "question": "An item is sold at a 10% loss. If the cost price is ₹500, what is the selling price?",
        "options": ["₹450", "₹470", "₹440", "₹460"],
        "correct_answer": 0,
        "answer_explanation": "Selling price = Cost price - 10% of Cost price = 500 - 50 = ₹450",
        "topic": "Profit & Loss",
        "category": "Quantitative Ability",
        "difficulty": "easy"
    },
    {
        "question": "If selling price is ₹600 and profit is 20%, what is the cost price?",
        "options": ["₹480", "₹500", "₹520", "₹550"],
        "correct_answer": 1,
        "answer_explanation": "SP = CP × 1.2, so CP = 600/1.2 = ₹500",
        "topic": "Profit & Loss",
        "category": "Quantitative Ability",
        "difficulty": "medium"
    },
    {
        "question": "A man sells two items at ₹990 each. On one he gains 10% and on the other loses 10%. What is the overall result?",
        "options": ["No profit, no loss", "1% loss", "1% gain", "2% loss"],
        "correct_answer": 1,
        "answer_explanation": "When SP is same and percentage is same, there's always a loss = (common %)²/100 = 1%",
        "topic": "Profit & Loss",
        "category": "Quantitative Ability",
        "difficulty": "hard"
    },
    
    # Time & Work
    {
        "question": "A can do a work in 10 days. How much of the work can A do in 1 day?",
        "options": ["1/10", "1/5", "1/8", "1/12"],
        "correct_answer": 0,
        "answer_explanation": "If complete work takes 10 days, 1 day's work = 1/10",
        "topic": "Time & Work",
        "category": "Quantitative Ability",
        "difficulty": "easy"
    },
    {
        "question": "A can do a work in 12 days and B can do it in 15 days. In how many days can they finish it together?",
        "options": ["6 2/3 days", "6.5 days", "7 days", "5 days"],
        "correct_answer": 0,
        "answer_explanation": "Combined rate = 1/12 + 1/15 = 9/60 = 3/20. Time = 20/3 = 6 2/3 days",
        "topic": "Time & Work",
        "category": "Quantitative Ability",
        "difficulty": "medium"
    },
    {
        "question": "If 6 men can complete a work in 8 days, how many days will 4 men take?",
        "options": ["10 days", "12 days", "14 days", "16 days"],
        "correct_answer": 1,
        "answer_explanation": "6 × 8 = 4 × x, so x = 48/4 = 12 days (inverse proportion)",
        "topic": "Time & Work",
        "category": "Quantitative Ability",
        "difficulty": "medium"
    },
    {
        "question": "A and B together can complete work in 8 days. A alone can complete it in 12 days. How long will B alone take?",
        "options": ["20 days", "24 days", "18 days", "16 days"],
        "correct_answer": 1,
        "answer_explanation": "1/B = 1/8 - 1/12 = (3-2)/24 = 1/24. So B takes 24 days.",
        "topic": "Time & Work",
        "category": "Quantitative Ability",
        "difficulty": "hard"
    },
    
    # Time, Speed & Distance
    {
        "question": "A car travels 120 km in 2 hours. What is its speed?",
        "options": ["50 km/h", "55 km/h", "60 km/h", "65 km/h"],
        "correct_answer": 2,
        "answer_explanation": "Speed = Distance/Time = 120/2 = 60 km/h",
        "topic": "Time Speed Distance",
        "category": "Quantitative Ability",
        "difficulty": "easy"
    },
    {
        "question": "A train 200m long crosses a pole in 10 seconds. What is its speed in km/h?",
        "options": ["72 km/h", "60 km/h", "80 km/h", "54 km/h"],
        "correct_answer": 0,
        "answer_explanation": "Speed = 200/10 = 20 m/s = 20 × (18/5) = 72 km/h",
        "topic": "Time Speed Distance",
        "category": "Quantitative Ability",
        "difficulty": "medium"
    },
    {
        "question": "If a person walks at 5 km/h, he misses a train by 7 minutes. If he walks at 6 km/h, he reaches 5 minutes early. What is the distance?",
        "options": ["5 km", "6 km", "7 km", "4 km"],
        "correct_answer": 1,
        "answer_explanation": "Time difference = 12 min = 1/5 hour. d/5 - d/6 = 1/5. d(6-5)/30 = 1/5. d = 6 km",
        "topic": "Time Speed Distance",
        "category": "Quantitative Ability",
        "difficulty": "hard"
    },
    
    # Simple & Compound Interest
    {
        "question": "What is the simple interest on ₹5000 at 10% per annum for 2 years?",
        "options": ["₹800", "₹900", "₹1000", "₹1100"],
        "correct_answer": 2,
        "answer_explanation": "SI = P × R × T / 100 = 5000 × 10 × 2 / 100 = ₹1000",
        "topic": "Simple & Compound Interest",
        "category": "Quantitative Ability",
        "difficulty": "easy"
    },
    {
        "question": "Find compound interest on ₹1000 at 10% for 2 years compounded annually.",
        "options": ["₹200", "₹210", "₹220", "₹205"],
        "correct_answer": 1,
        "answer_explanation": "A = 1000(1.1)² = 1210. CI = 1210 - 1000 = ₹210",
        "topic": "Simple & Compound Interest",
        "category": "Quantitative Ability",
        "difficulty": "medium"
    },
    {
        "question": "At what rate of simple interest will ₹800 amount to ₹920 in 3 years?",
        "options": ["4%", "5%", "6%", "7%"],
        "correct_answer": 1,
        "answer_explanation": "SI = 920-800 = 120. R = (SI × 100)/(P × T) = 12000/2400 = 5%",
        "topic": "Simple & Compound Interest",
        "category": "Quantitative Ability",
        "difficulty": "medium"
    },
    {
        "question": "The difference between CI and SI on a sum for 2 years at 10% is ₹50. Find the sum.",
        "options": ["₹4000", "₹5000", "₹6000", "₹4500"],
        "correct_answer": 1,
        "answer_explanation": "Difference = P(R/100)² = P × 0.01 = 50. So P = ₹5000",
        "topic": "Simple & Compound Interest",
        "category": "Quantitative Ability",
        "difficulty": "hard"
    },
    
    # Permutations & Combinations
    {
        "question": "In how many ways can 3 books be arranged on a shelf?",
        "options": ["3", "6", "9", "12"],
        "correct_answer": 1,
        "answer_explanation": "3! = 3 × 2 × 1 = 6 ways",
        "topic": "Permutations & Combinations",
        "category": "Quantitative Ability",
        "difficulty": "easy"
    },
    {
        "question": "How many 3-digit numbers can be formed using digits 1, 2, 3, 4, 5 without repetition?",
        "options": ["60", "120", "20", "125"],
        "correct_answer": 0,
        "answer_explanation": "5P3 = 5 × 4 × 3 = 60",
        "topic": "Permutations & Combinations",
        "category": "Quantitative Ability",
        "difficulty": "medium"
    },
    {
        "question": "In how many ways can a committee of 3 be formed from 5 people?",
        "options": ["10", "60", "15", "20"],
        "correct_answer": 0,
        "answer_explanation": "5C3 = 5!/(3!×2!) = 10",
        "topic": "Permutations & Combinations",
        "category": "Quantitative Ability",
        "difficulty": "medium"
    },
    {
        "question": "How many words can be formed by rearranging letters of MISSISSIPPI?",
        "options": ["34650", "39916800", "11", "4620"],
        "correct_answer": 0,
        "answer_explanation": "11!/(4!×4!×2!) = 34650 (M=1, I=4, S=4, P=2)",
        "topic": "Permutations & Combinations",
        "category": "Quantitative Ability",
        "difficulty": "hard"
    },
    
    # ========== VERBAL ABILITY ==========
    # Synonyms & Antonyms
    {
        "question": "Choose the synonym of 'BENEVOLENT':",
        "options": ["Kind", "Cruel", "Angry", "Lazy"],
        "correct_answer": 0,
        "answer_explanation": "Benevolent means kind and generous.",
        "topic": "Synonyms & Antonyms",
        "category": "Verbal Ability",
        "difficulty": "easy"
    },
    {
        "question": "Choose the antonym of 'TRANSPARENT':",
        "options": ["Clear", "Opaque", "Visible", "Obvious"],
        "correct_answer": 1,
        "answer_explanation": "Transparent means clear; opaque means not clear/not transparent.",
        "topic": "Synonyms & Antonyms",
        "category": "Verbal Ability",
        "difficulty": "easy"
    },
    {
        "question": "Find the synonym of 'ELOQUENT':",
        "options": ["Silent", "Fluent", "Confused", "Boring"],
        "correct_answer": 1,
        "answer_explanation": "Eloquent means fluent and persuasive in speaking or writing.",
        "topic": "Synonyms & Antonyms",
        "category": "Verbal Ability",
        "difficulty": "medium"
    },
    {
        "question": "Choose the antonym of 'ARDUOUS':",
        "options": ["Difficult", "Easy", "Tiring", "Complex"],
        "correct_answer": 1,
        "answer_explanation": "Arduous means difficult and tiring; easy is the opposite.",
        "topic": "Synonyms & Antonyms",
        "category": "Verbal Ability",
        "difficulty": "medium"
    },
    {
        "question": "Select the synonym of 'EPHEMERAL':",
        "options": ["Eternal", "Temporary", "Important", "Beautiful"],
        "correct_answer": 1,
        "answer_explanation": "Ephemeral means lasting for a very short time; same as temporary.",
        "topic": "Synonyms & Antonyms",
        "category": "Verbal Ability",
        "difficulty": "hard"
    },
    {
        "question": "Choose the antonym of 'UBIQUITOUS':",
        "options": ["Rare", "Common", "Present", "Available"],
        "correct_answer": 0,
        "answer_explanation": "Ubiquitous means present everywhere; rare is the opposite.",
        "topic": "Synonyms & Antonyms",
        "category": "Verbal Ability",
        "difficulty": "hard"
    },
    
    # Reading Comprehension
    {
        "question": "Passage: 'The sun is essential for life on Earth. It provides light and warmth.' What is the main idea?",
        "options": ["The sun is hot", "The sun is essential for Earth", "Light is important", "Earth is warm"],
        "correct_answer": 1,
        "answer_explanation": "The passage emphasizes the sun's essential role for life on Earth.",
        "topic": "Reading Comprehension",
        "category": "Verbal Ability",
        "difficulty": "easy"
    },
    {
        "question": "Passage: 'Despite the rain, the match continued. The players showed great determination.' What can be inferred?",
        "options": ["Players dislike rain", "The match was cancelled", "Players were dedicated", "Rain stopped the match"],
        "correct_answer": 2,
        "answer_explanation": "Continuing despite rain shows the players' dedication.",
        "topic": "Reading Comprehension",
        "category": "Verbal Ability",
        "difficulty": "medium"
    },
    
    # Sentence Correction
    {
        "question": "Choose the correct sentence:",
        "options": ["He don't know the answer", "He doesn't knows the answer", "He doesn't know the answer", "He don't knows the answer"],
        "correct_answer": 2,
        "answer_explanation": "Third person singular (He) uses 'doesn't' + base verb 'know'.",
        "topic": "Sentence Correction",
        "category": "Verbal Ability",
        "difficulty": "easy"
    },
    {
        "question": "Choose the grammatically correct sentence:",
        "options": ["Neither of them were present", "Neither of them was present", "Neither of them are present", "Neither of them is being present"],
        "correct_answer": 1,
        "answer_explanation": "'Neither' takes singular verb 'was'.",
        "topic": "Sentence Correction",
        "category": "Verbal Ability",
        "difficulty": "medium"
    },
    {
        "question": "Identify the correct sentence:",
        "options": ["Each of the students have submitted their work", "Each of the students has submitted his work", "Each of the students have submitted his work", "Each of the students has submitted their work"],
        "correct_answer": 1,
        "answer_explanation": "'Each' is singular, takes 'has' and traditionally 'his' (though 'their' is becoming acceptable).",
        "topic": "Sentence Correction",
        "category": "Verbal Ability",
        "difficulty": "hard"
    },
    
    # Fill in the Blanks
    {
        "question": "She is ___ honest person.",
        "options": ["a", "an", "the", "no article"],
        "correct_answer": 1,
        "answer_explanation": "Use 'an' before words starting with vowel sounds. 'Honest' starts with vowel sound.",
        "topic": "Fill in the Blanks",
        "category": "Verbal Ability",
        "difficulty": "easy"
    },
    {
        "question": "The committee ___ divided on the issue.",
        "options": ["is", "are", "was", "were"],
        "correct_answer": 1,
        "answer_explanation": "When committee members are divided (acting individually), use plural verb 'are'.",
        "topic": "Fill in the Blanks",
        "category": "Verbal Ability",
        "difficulty": "medium"
    },
    {
        "question": "He walked ___ the bridge to cross the river.",
        "options": ["across", "through", "along", "into"],
        "correct_answer": 0,
        "answer_explanation": "'Across' means from one side to the other, appropriate for crossing a bridge.",
        "topic": "Fill in the Blanks",
        "category": "Verbal Ability",
        "difficulty": "easy"
    },
    
    # Error Spotting
    {
        "question": "Find the error: 'One of my friend (A)/ has gone (B)/ to London. (C)/ No error (D)'",
        "options": ["One of my friend", "has gone", "to London", "No error"],
        "correct_answer": 0,
        "answer_explanation": "'One of' is followed by plural noun: 'One of my friends'.",
        "topic": "Error Spotting",
        "category": "Verbal Ability",
        "difficulty": "easy"
    },
    {
        "question": "Find the error: 'The sceneries (A)/ of Kashmir (B)/ are very beautiful. (C)/ No error (D)'",
        "options": ["The sceneries", "of Kashmir", "are very beautiful", "No error"],
        "correct_answer": 0,
        "answer_explanation": "'Scenery' is uncountable. Should be 'The scenery of Kashmir is...'",
        "topic": "Error Spotting",
        "category": "Verbal Ability",
        "difficulty": "medium"
    },
    {
        "question": "Spot the error: 'He is one of those (A)/ who always helps (B)/ others in need. (C)/ No error (D)'",
        "options": ["He is one of those", "who always helps", "others in need", "No error"],
        "correct_answer": 1,
        "answer_explanation": "'Who' refers to 'those' (plural), so it should be 'who always help'.",
        "topic": "Error Spotting",
        "category": "Verbal Ability",
        "difficulty": "hard"
    },
    
    # ========== DATA INTERPRETATION ==========
    {
        "question": "If a pie chart shows 90° for Category A out of 360°, what percentage does A represent?",
        "options": ["20%", "25%", "30%", "35%"],
        "correct_answer": 1,
        "answer_explanation": "(90/360) × 100 = 25%",
        "topic": "Data Interpretation",
        "category": "Data Interpretation",
        "difficulty": "easy"
    },
    {
        "question": "Bar chart shows sales: Jan-100, Feb-120, Mar-150. What is the average monthly sales?",
        "options": ["115", "120", "123.33", "130"],
        "correct_answer": 2,
        "answer_explanation": "Average = (100+120+150)/3 = 370/3 = 123.33",
        "topic": "Data Interpretation",
        "category": "Data Interpretation",
        "difficulty": "easy"
    },
    {
        "question": "If production in Year 1 was 1000 units and Year 2 was 1200 units, what is the percentage increase?",
        "options": ["15%", "20%", "25%", "30%"],
        "correct_answer": 1,
        "answer_explanation": "Increase = 200, Percentage = (200/1000) × 100 = 20%",
        "topic": "Data Interpretation",
        "category": "Data Interpretation",
        "difficulty": "medium"
    },
    {
        "question": "A line graph shows values 50, 60, 75, 95. What is the highest percentage increase between consecutive values?",
        "options": ["20%", "25%", "26.67%", "33.33%"],
        "correct_answer": 2,
        "answer_explanation": "50→60: 20%, 60→75: 25%, 75→95: 26.67%. Highest is 26.67%",
        "topic": "Data Interpretation",
        "category": "Data Interpretation",
        "difficulty": "hard"
    },
    
    # ========== ANALYTICAL REASONING ==========
    {
        "question": "All cats are animals. All animals need food. Therefore:",
        "options": ["All cats need food", "All food is for cats", "Some animals are cats", "None of the above"],
        "correct_answer": 0,
        "answer_explanation": "This is a valid syllogism: Cats ⊂ Animals, Animals need food → Cats need food",
        "topic": "Analytical Reasoning",
        "category": "Analytical Reasoning",
        "difficulty": "easy"
    },
    {
        "question": "If A > B, B > C, and C > D, which is the smallest?",
        "options": ["A", "B", "C", "D"],
        "correct_answer": 3,
        "answer_explanation": "A > B > C > D, so D is the smallest.",
        "topic": "Analytical Reasoning",
        "category": "Analytical Reasoning",
        "difficulty": "easy"
    },
    {
        "question": "Statement: All doctors are professionals. Some professionals are teachers. Conclusion: Some doctors are teachers.",
        "options": ["Definitely true", "Probably true", "Definitely false", "Cannot be determined"],
        "correct_answer": 3,
        "answer_explanation": "We cannot conclude that the teachers who are professionals are also doctors.",
        "topic": "Analytical Reasoning",
        "category": "Analytical Reasoning",
        "difficulty": "medium"
    },
    {
        "question": "In a certain code, if PLAY is QMBZ, then what is the code for GAME?",
        "options": ["HBNF", "GBNF", "FAME", "HAME"],
        "correct_answer": 0,
        "answer_explanation": "Each letter moved +1: P→Q, L→M, A→B, Y→Z. So G→H, A→B, M→N, E→F = HBNF",
        "topic": "Analytical Reasoning",
        "category": "Analytical Reasoning",
        "difficulty": "medium"
    },
    
    # ========== VERBAL REASONING ==========
    {
        "question": "Statement: Smoking is injurious to health. Conclusion: One should not smoke.",
        "options": ["Conclusion follows", "Conclusion does not follow", "Data inadequate", "None of these"],
        "correct_answer": 0,
        "answer_explanation": "If something is injurious to health, avoiding it is logical.",
        "topic": "Verbal Reasoning",
        "category": "Verbal Reasoning",
        "difficulty": "easy"
    },
    {
        "question": "Choose the odd one out: Apple, Orange, Carrot, Banana",
        "options": ["Apple", "Orange", "Carrot", "Banana"],
        "correct_answer": 2,
        "answer_explanation": "Carrot is a vegetable; others are fruits.",
        "topic": "Verbal Reasoning",
        "category": "Verbal Reasoning",
        "difficulty": "easy"
    },
    {
        "question": "Arrange in logical order: 1. Seed 2. Plant 3. Flower 4. Fruit 5. Germination",
        "options": ["1,5,2,3,4", "1,2,5,3,4", "5,1,2,3,4", "1,5,3,2,4"],
        "correct_answer": 0,
        "answer_explanation": "Seed → Germination → Plant → Flower → Fruit",
        "topic": "Verbal Reasoning",
        "category": "Verbal Reasoning",
        "difficulty": "medium"
    },
    {
        "question": "Statement: The best way to escape from a problem is to solve it. Conclusion: Escaping from problems is impossible.",
        "options": ["Conclusion follows", "Conclusion does not follow", "Data inadequate", "Both follow"],
        "correct_answer": 1,
        "answer_explanation": "The statement suggests solving is the best way, not that escaping is impossible.",
        "topic": "Verbal Reasoning",
        "category": "Verbal Reasoning",
        "difficulty": "hard"
    }
]

def seed_questions():
    """Seed the database with aptitude questions"""
    db = SessionLocal()
    
    try:
        # Check if questions already exist
        existing_count = db.query(AptitudeQuestion).count()
        if existing_count > 0:
            print(f"Database already has {existing_count} questions. Skipping seeding.")
            return
            
        # Add all questions
        for q_data in APTITUDE_QUESTIONS:
            question = AptitudeQuestion(**q_data)
            db.add(question)
            
        db.commit()
        print(f"Seeded {len(APTITUDE_QUESTIONS)} aptitude questions!")
        
        # Print summary
        categories = {}
        for q in APTITUDE_QUESTIONS:
            cat = q["category"]
            topic = q["topic"]
            if cat not in categories:
                categories[cat] = set()
            categories[cat].add(topic)
            
        print("\n📊 Question Summary:")
        for cat, topics in categories.items():
            print(f"  {cat}: {len(topics)} topics")
            for topic in sorted(topics):
                count = sum(1 for q in APTITUDE_QUESTIONS if q["topic"] == topic)
                print(f"    - {topic}: {count} questions")
                
    except Exception as e:
        db.rollback()
        print(f"Error seeding questions: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_questions()
