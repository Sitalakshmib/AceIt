import sys
import os
import uuid
import json

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_postgres import SessionLocal
from models.aptitude_sql import AptitudeQuestion

def seed_algebra():
    session = SessionLocal()
    
    questions_data = [
        # EASY (20)
        {"q": "If x + 5 = 12, what is the value of x?", "o": ["5", "6", "7", "8"], "c": 2, "e": "x = 12 - 5 = 7", "diff": "easy", "concepts": ["linear_equations"], "trap": "adding_instead_of_subtracting"},
        {"q": "Rohan is 3 years older than Sohan. If Sohan is 15 years old, how old is Rohan?", "o": ["16", "17", "18", "19"], "c": 2, "e": "Rohan = Sohan + 3 = 15 + 3 = 18", "diff": "easy", "concepts": ["linear_equations"], "trap": "subtracting_instead_of_adding"},
        {"q": "If 2x = 18, what is x?", "o": ["7", "8", "9", "10"], "c": 2, "e": "x = 18 ÷ 2 = 9", "diff": "easy", "concepts": ["linear_equations"], "trap": "multiplying_instead_of_dividing"},
        {"q": "The sum of two consecutive integers is 25. What are the numbers?", "o": ["11 and 12", "12 and 13", "13 and 14", "14 and 15"], "c": 1, "e": "Let numbers be x and x+1. x + (x+1) = 25 → 2x = 24 → x = 12. Numbers: 12 and 13", "diff": "easy", "concepts": ["consecutive_integers"], "trap": "forgetting_consecutive_means_+1"},
        {"q": "If 3x - 7 = 14, what is x?", "o": ["5", "6", "7", "8"], "c": 2, "e": "3x = 21 → x = 7", "diff": "easy", "concepts": ["linear_equations"], "trap": "sign_error_with_negative"},
        {"q": "A number multiplied by 5 gives 45. What is the number?", "o": ["8", "9", "10", "11"], "c": 1, "e": "5x = 45 → x = 9", "diff": "easy", "concepts": ["linear_equations"], "trap": "dividing_wrong_number"},
        {"q": "If y = 3x + 2 and x = 4, what is y?", "o": ["12", "13", "14", "15"], "c": 2, "e": "y = 3(4) + 2 = 12 + 2 = 14", "diff": "easy", "concepts": ["substitution"], "trap": "order_of_operations"},
        {"q": "Twice a number decreased by 5 equals 13. What is the number?", "o": ["7", "8", "9", "10"], "c": 2, "e": "2x - 5 = 13 → 2x = 18 → x = 9", "diff": "easy", "concepts": ["linear_equations"], "trap": "adding_5_to_13_instead"},
        {"q": "Simplify: 3(x + 4) - 2x", "o": ["x + 12", "x + 4", "5x + 12", "5x + 4"], "c": 0, "e": "3x + 12 - 2x = x + 12", "diff": "easy", "concepts": ["polynomials"], "trap": "distributive_property_error"},
        {"q": "If 4x + 8 = 36, what is x?", "o": ["6", "7", "8", "9"], "c": 1, "e": "4x = 28 → x = 7", "diff": "easy", "concepts": ["linear_equations"], "trap": "subtracting_wrong_number"},
        {"q": "The sum of a number and 7 is 19. What is the number?", "o": ["10", "11", "12", "13"], "c": 2, "e": "x + 7 = 19 → x = 12", "diff": "easy", "concepts": ["linear_equations"], "trap": "adding_instead"},
        {"q": "If 2(x - 3) = 10, what is x?", "o": ["6", "7", "8", "9"], "c": 2, "e": "2x - 6 = 10 → 2x = 16 → x = 8", "diff": "easy", "concepts": ["distributive_property"], "trap": "forgetting_to_distribute"},
        {"q": "Three times a number is 39. What is the number?", "o": ["11", "12", "13", "14"], "c": 2, "e": "3x = 39 → x = 13", "diff": "easy", "concepts": ["linear_equations"], "trap": "division_error"},
        {"q": "If 5x - 3 = 2x + 9, what is x?", "o": ["2", "3", "4", "5"], "c": 2, "e": "5x - 2x = 9 + 3 → 3x = 12 → x = 4", "diff": "easy", "concepts": ["variables_both_sides"], "trap": "sign_error_when_moving_terms"},
        {"q": "A number divided by 4 equals 6. What is the number?", "o": ["20", "22", "24", "26"], "c": 2, "e": "x/4 = 6 → x = 24", "diff": "easy", "concepts": ["linear_equations"], "trap": "multiplying_by_wrong_number"},
        {"q": "If x = 5, what is 2x^2?", "o": ["25", "40", "50", "100"], "c": 2, "e": "2 * (5^2) = 2 * 25 = 50", "diff": "easy", "concepts": ["polynomials"], "trap": "squaring_2x_first"},
        {"q": "The product of a number and 8 is 64. What is the number?", "o": ["6", "7", "8", "9"], "c": 2, "e": "8x = 64 → x = 8", "diff": "easy", "concepts": ["linear_equations"], "trap": "division_error"},
        {"q": "If 3x + 5 = 20, what is x?", "o": ["4", "5", "6", "7"], "c": 1, "e": "3x = 15 → x = 5", "diff": "easy", "concepts": ["linear_equations"], "trap": "subtracting_wrong_term"},
        {"q": "Simplify: 4x + 2x - 3x", "o": ["3x", "4x", "5x", "6x"], "c": 0, "e": "4x + 2x - 3x = 3x", "diff": "easy", "concepts": ["polynomials"], "trap": "adding_all_coefficients"},
        {"q": "If x/3 = 7, what is x?", "o": ["18", "20", "21", "24"], "c": 2, "e": "x = 7 * 3 = 21", "diff": "easy", "concepts": ["linear_equations"], "trap": "dividing_instead_of_multiplying"},

        # MEDIUM (20)
        {"q": "The sum of three consecutive even integers is 78. What is the smallest integer?", "o": ["22", "24", "26", "28"], "c": 1, "e": "Let numbers be x, x+2, x+4. Sum = 3x+6=78 → 3x=72 → x=24. Smallest = 24", "diff": "medium", "concepts": ["consecutive_even_integers"], "trap": "using_x,x+1,x+2_for_even"},
        {"q": "If 2(x+3) + 3(x-1) = 28, what is x?", "o": ["4", "5", "6", "7"], "c": 1, "e": "2x+6+3x-3=28 → 5x+3=28 → 5x=25 → x=5", "diff": "medium", "concepts": ["distributive_combining"], "trap": "sign_errors_in_distribution"},
        {"q": "A father is 3 times as old as his son. After 10 years, he will be twice as old. What is son's current age?", "o": ["8", "10", "12", "15"], "c": 1, "e": "Let son's age = x. Father's age = 3x. After 10 years: 3x+10=2(x+10) → 3x+10=2x+20 → x=10.", "diff": "medium", "concepts": ["age_problem_with_time"], "trap": "not_adding_10_to_both"},
        {"q": "Solve: (x+3)/2 = (x-1)/3", "o": ["-11", "-10", "-9", "-8"], "c": 0, "e": "Cross multiply: 3(x+3)=2(x-1) → 3x+9=2x-2 → x=-11", "diff": "medium", "concepts": ["fractional_equations"], "trap": "cross_multiplication_error"},
        {"q": "The difference between two numbers is 12. Their sum is 40. What is the larger number?", "o": ["24", "25", "26", "27"], "c": 2, "e": "x-y=12, x+y=40. Add: 2x=52 → x=26.", "diff": "medium", "concepts": ["system_of_equations"], "trap": "solving_for_wrong_variable"},
        {"q": "If 2x + 3y = 20 and x - y = 0, what is x?", "o": ["3", "4", "5", "6"], "c": 1, "e": "x = y. Substitute: 2x+3x=20 → 5x=20 → x=4", "diff": "medium", "concepts": ["substitution_method"], "trap": "not_recognizing_x=y"},
        {"q": "Expand: (x+4)(x-3)", "o": ["x^2 + x - 12", "x^2 - x - 12", "x^2 + 7x - 12", "x^2 - 7x - 12"], "c": 0, "e": "x^2 -3x +4x -12 = x^2 + x -12", "diff": "medium", "concepts": ["polynomials"], "trap": "middle_term_error"},
        {"q": "A number is multiplied by 4 and then 5 is added. The result is 29. What is the number?", "o": ["5", "6", "7", "8"], "c": 1, "e": "4x + 5 = 29 → 4x = 24 → x = 6", "diff": "medium", "concepts": ["linear_equations"], "trap": "reverse_order_error"},
        {"q": "Solve for x: 5 - 2(x+1) = 3x - 7", "o": ["2", "3", "4", "5"], "c": 0, "e": "5 - 2x - 2 = 3x - 7 → 3 - 2x = 3x - 7 → 10 = 5x → x = 2", "diff": "medium", "concepts": ["linear_equations"], "trap": "distributive_sign_error"},
        {"q": "The sum of two numbers is 45. One number is 9 more than the other. Find both numbers.", "o": ["18 and 27", "19 and 28", "20 and 29", "21 and 30"], "c": 0, "e": "x+(x+9)=45 → 2x=36 → x=18.", "diff": "medium", "concepts": ["linear_equations"], "trap": "using_x_and_9_instead_of_x+9"},
        {"q": "Factor: x^2 - 9", "o": ["(x-3)(x+3)", "(x-3)^2", "(x+3)^2", "(x-9)(x+1)"], "c": 0, "e": "Difference of squares: x^2 - 9 = (x-3)(x+3)", "diff": "medium", "concepts": ["identities"], "trap": "confusing_with_perfect_square"},
        {"q": "If 3x - 2y = 14 and x + y = 8, what is y?", "o": ["1", "2", "3", "4"], "c": 1, "e": "x=8-y → 3(8-y)-2y=14 → 24-5y=14 → 5y=10 → y=2", "diff": "medium", "concepts": ["linear_equations"], "trap": "algebraic_manipulation_error"},
        {"q": "A rectangle's length is 5 more than its width. Perimeter is 38. What is width?", "o": ["6", "7", "8", "9"], "c": 1, "e": "2(w + w+5) = 2(2w+5)=4w+10=38 → 4w=28 → w=7", "diff": "medium", "concepts": ["linear_equations"], "trap": "perimeter_formula_error"},
        {"q": "Simplify: (3x^2 - 2x + 5) + (2x^2 + 4x - 3)", "o": ["5x^2 + 2x + 2", "5x^2 + 2x + 8", "5x^2 - 2x + 2", "5x^2 + 6x + 2"], "c": 0, "e": "3x^2+2x^2=5x^2, -2x+4x=2x, 5-3=2.", "diff": "medium", "concepts": ["polynomials"], "trap": "sign_errors_with_negatives"},
        {"q": "If (x-3)/4 = 5, what is x?", "o": ["17", "19", "21", "23"], "c": 3, "e": "x-3 = 20 → x = 23", "diff": "medium", "concepts": ["linear_equations"], "trap": "multiplying_only_numerator"},
        {"q": "The product of two consecutive integers is 156. What is the smaller integer?", "o": ["11", "12", "13", "14"], "c": 1, "e": "x(x+1)=156 → x^2+x-156=0 → (x+13)(x-12)=0 → x=12", "diff": "medium", "concepts": ["quadratic_roots"], "trap": "not_forming_quadratic"},
        {"q": "If 5x - 3 = 3x + 11, what is x?", "o": ["6", "7", "8", "9"], "c": 1, "e": "2x=14 → x=7", "diff": "medium", "concepts": ["linear_equations"], "trap": "sign_error_collecting_terms"},
        {"q": "A number plus its double is 36. What is the number?", "o": ["10", "11", "12", "13"], "c": 2, "e": "x + 2x = 36 → 3x = 36 → x = 12", "diff": "medium", "concepts": ["linear_equations"], "trap": "using_half_instead_of_double"},
        {"q": "Solve: 2(3x-4) = 5x + 6", "o": ["12", "14", "16", "18"], "c": 1, "e": "6x-8=5x+6 → x=14", "diff": "medium", "concepts": ["linear_equations"], "trap": "distributing_only_to_first_term"},
        {"q": "The sum of three consecutive odd integers is 75. What is the middle integer?", "o": ["23", "24", "25", "26"], "c": 2, "e": "3x = 75 → x = 25", "diff": "medium", "concepts": ["consecutive_odd_integers"], "trap": "using_x,x+1,x+2_for_odd"},

        # HARD (20)
        {"q": "Solve: (x+2)/(x-3) = 3/2", "o": ["11", "12", "13", "14"], "c": 2, "e": "2(x+2)=3(x-3) → 2x+4=3x-9 → x=13", "diff": "hard", "concepts": ["linear_equations"], "trap": "cross_multiplying_incorrectly"},
        {"q": "A two-digit number is 4 times the sum of its digits. If 18 is added, digits reverse. What is the number?", "o": ["24", "36", "48", "72"], "c": 0, "e": "Let number = 10a+b. 10a+b=4(a+b) → 6a=3b → 2a=b. Also a+2=b. 2a=a+2 → a=2, b=4. Number=24", "diff": "hard", "concepts": ["linear_equations"], "trap": "setting_up_equations_incorrectly"},
        {"q": "If x^2 - 5x + 6 = 0, what are the roots?", "o": ["2 and 3", "-2 and -3", "1 and 6", "-1 and -6"], "c": 0, "e": "Factor: (x-2)(x-3)=0 → x=2 or 3", "diff": "hard", "concepts": ["quadratic_roots"], "trap": "sign_errors_in_factoring"},
        {"q": "Solve system: 2x+3y=13, 3x+2y=12", "o": ["x=2, y=3", "x=3, y=2", "x=2, y=2", "x=3, y=3"], "c": 0, "e": "Multiply 1st by 3, 2nd by 2. 6x+9y=39, 6x+4y=24. Sub: 5y=15 → y=3. 2x+9=13 → x=2", "diff": "hard", "concepts": ["linear_equations"], "trap": "arithmetic_errors_in_elimination"},
        {"q": "If 1/x + 1/y = 1/6 and x+y=30, what is xy?", "o": ["120", "140", "160", "180"], "c": 3, "e": "(x+y)/xy = 1/6. 30/xy = 1/6 → xy=180", "diff": "hard", "concepts": ["identities"], "trap": "not_combining_fractions_correctly"},
        {"q": "The sum of ages of father and son is 50. Five years ago, father was 7 times as old. Current ages?", "o": ["35 and 15", "40 and 10", "45 and 5", "30 and 20"], "c": 1, "e": "f+s=50. f-5=7(s-5) → f=7s-30. 8s=80 → s=10. f=40.", "diff": "hard", "concepts": ["age_problem_two_conditions"], "trap": "time_frame_error"},
        {"q": "Solve for x: 2/x + 3/(x+1) = 2", "o": ["x=1", "x=2", "x=3", "x=4"], "c": 1, "e": "If x=2: 2/2 + 3/3 = 1+1=2. Correct.", "diff": "hard", "concepts": ["linear_equations"], "trap": "common_denominator_error"},
        {"q": "If a+b=7 and ab=12, what is a^2+b^2?", "o": ["23", "24", "25", "26"], "c": 2, "e": "(a+b)^2 = a^2+b^2+2ab → 49 = a^2+b^2 + 24 → 25", "diff": "hard", "concepts": ["identities"], "trap": "not_using_identity"},
        {"q": "A fraction becomes 5/7 when 1 is added to numerator, and 2/3 when 1 is subtracted from denominator. Original fraction?", "o": ["3/7", "4/7", "5/7", "6/7"], "c": 1, "e": "Let fraction=x/y. (x+1)/7=5/7 → x=4. 4/(y-1)=2/3 → 12=2y-2 → 14=2y → y=7. Fraction=4/7", "diff": "hard", "concepts": ["linear_equations"], "trap": "setting_up_equations"},
        {"q": "Solve: sqrt(x+15) + sqrt(x) = 15", "o": ["36", "49", "64", "81"], "c": 1, "e": "Let sqrt(x)=a. sqrt(a^2+15)+a=15 → a^2+15=225-30a+a^2 → 30a=210 → a=7. x=49", "diff": "hard", "concepts": ["linear_equations"], "trap": "squaring_prematurely"},
        {"q": "If 2^(x-1) + 2^(x+1) = 40, what is x?", "o": ["2", "3", "4", "5"], "c": 2, "e": "2^x/2 + 2 * 2^x = 40 → 2.5 * 2^x = 40 → 2^x = 16 → x=4", "diff": "hard", "concepts": ["polynomials"], "trap": "exponent_rules_error"},
        {"q": "The sum of reciprocals of two numbers is 7/10. Their sum is 7. What are the numbers?", "o": ["2 and 5", "3 and 4", "1 and 6", "2.5 and 4.5"], "c": 0, "e": "1/x+1/y = (x+y)/xy = 7/10. 7/xy = 7/10 → xy=10. x+y=7. Roots: 2 and 5", "diff": "hard", "concepts": ["quadratic_roots"], "trap": "not_forming_quadratic"},
        {"q": "Solve: |x-3| = 7", "o": ["x=10 only", "x=-4 only", "x=10 or x=-4", "x=10 or x=4"], "c": 2, "e": "x-3=7 or x-3=-7 → x=10 or -4", "diff": "hard", "concepts": ["linear_equations"], "trap": "forgetting_negative_case"},
        {"q": "If log2(x) + log2(x+2) = 3, what is x?", "o": ["2", "4", "6", "8"], "c": 0, "e": "log2[x(x+2)]=3 → x(x+2)=8 → x=2", "diff": "hard", "concepts": ["polynomials"], "trap": "log_rules_error"},
        {"q": "A man buys 5 pens and 3 pencils for ₹115. Another time, 3 pens and 5 pencils cost ₹85. Cost of one pen?", "o": ["₹15", "₹18", "₹20", "₹22"], "c": 2, "e": "5p+3c=115, 3p+5c=85. Add: 8p+8c=200 → p+c=25. Sub: 2p-2c=30 → p-c=15. p=20", "diff": "hard", "concepts": ["linear_equations"], "trap": "arithmetic_error"},
        {"q": "If x+1/x=3, what is x^2+1/x^2?", "o": ["5", "6", "7", "8"], "c": 2, "e": "(x+1/x)^2 = x^2+2+1/x^2 = 9 → 7", "diff": "hard", "concepts": ["identities"], "trap": "not_squaring_correctly"},
        {"q": "Solve: 3^x = 27^(x-2)", "o": ["1", "2", "3", "4"], "c": 2, "e": "3^x = 3^(3x-6) → x = 3x-6 → x=3", "diff": "hard", "concepts": ["polynomials"], "trap": "exponent_distribution_error"},
        {"q": "The area of a rectangle is 60 sq units. Length is 4 more than width. Find dimensions.", "o": ["6 and 10", "5 and 12", "4 and 15", "8 and 7.5"], "c": 0, "e": "w(w+4)=60 → w^2+4w-60=0 → (w+10)(w-6)=0 → 6 and 10", "diff": "hard", "concepts": ["quadratic_roots"], "trap": "negative_solution_not_rejected"},
        {"q": "If 2x+3y=8 and 4x-ky=16 have infinite solutions, what is k?", "o": ["-3", "-6", "3", "6"], "c": 1, "e": "Ratios: 2/4 = 3/-k = 8/16. 1/2 = 3/-k → k=-6", "diff": "hard", "concepts": ["linear_equations"], "trap": "ratio_setup_error"},
        {"q": "Solve: (x-1)(x-2)(x-3)=0", "o": ["x=1 only", "x=1,2", "x=1,2,3", "x=1,2,3,4"], "c": 2, "e": "x=1, 2, or 3", "diff": "hard", "concepts": ["polynomials"], "trap": "multiplying_out_unnecessarily"}
    ]

    print(f"Adding {len(questions_data)} Algebra questions...")
    
    try:
        for q_data in questions_data:
            new_q = AptitudeQuestion(
                id=str(uuid.uuid4()),
                question=q_data["q"],
                options=q_data["o"],
                correct_answer=q_data["c"],
                answer_explanation=q_data["e"],
                topic="Algebra",
                category="Quantitative Ability",
                difficulty=q_data["diff"],
                source="hardcoded_algebra_part1",
                primary_concepts=q_data["concepts"],
                trap_explanation=q_data["trap"]
            )
            session.add(new_q)
        session.commit()
        print(f"Success: {len(questions_data)} questions seeded.")
    except Exception as e:
        session.rollback()
        print(f"Error seeding: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    seed_algebra()
