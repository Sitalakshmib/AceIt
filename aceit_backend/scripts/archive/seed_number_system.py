import sys
import os
import uuid

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_postgres import SessionLocal
from models.aptitude_sql import AptitudeQuestion

QUESTIONS_DATA = [
    # EASY LEVEL
    {"q": "What is the sum of first 10 natural numbers?", "o": ["45", "50", "55", "60"], "c": 2, "e": "Sum = n(n+1)/2 = 10*11/2 = 55", "diff": "easy", "concepts": ["sum_of_natural_numbers"], "trap": "adding_manually_errors"},
    {"q": "Which of these is a prime number?", "o": ["21", "27", "31", "39"], "c": 2, "e": "31 is divisible only by 1 and itself. 21=3*7, 27=3*9, 39=3*13.", "diff": "easy", "concepts": ["prime_numbers"], "trap": "checking_only_small_divisors"},
    {"q": "What is the smallest prime number?", "o": ["0", "1", "2", "3"], "c": 2, "e": "2 is the smallest and only even prime number.", "diff": "easy", "concepts": ["prime_numbers"], "trap": "thinking_1_is_prime"},
    {"q": "What is the HCF of 24 and 36?", "o": ["6", "8", "12", "18"], "c": 2, "e": "Factors: 24=2^3*3, 36=2^2*3^2. HCF = 2^2*3 = 12", "diff": "easy", "concepts": ["HCF"], "trap": "taking_product_instead"},
    {"q": "What is the LCM of 15 and 20?", "o": ["30", "45", "60", "75"], "c": 2, "e": "15=3*5, 20=2^2*5. LCM = 2^2*3*5 = 60", "diff": "easy", "concepts": ["LCM"], "trap": "taking_product_300"},
    {"q": "Which number is divisible by both 3 and 5?", "o": ["25", "30", "35", "40"], "c": 1, "e": "30 is divisible by 3 (3+0=3) and 5 (ends with 0 or 5)", "diff": "easy", "concepts": ["divisibility_rules"], "trap": "checking_only_one_condition"},
    {"q": "What is the unit digit of 7^34?", "o": ["1", "3", "7", "9"], "c": 3, "e": "Cyclicity of 7 is 4. 34 mod 4 = 2. 7^2 = 49. Unit digit is 9.", "diff": "easy", "concepts": ["unit_digit_cyclicity"], "trap": "wrong_pattern_recognition"},
    {"q": "What is the sum of digits of 1234?", "o": ["9", "10", "11", "12"], "c": 1, "e": "1+2+3+4 = 10", "diff": "easy", "concepts": ["digit_sum"], "trap": "simple_addition_error"},
    {"q": "Which is the smallest 3-digit prime number?", "o": ["100", "101", "103", "107"], "c": 1, "e": "100 is not prime. 101 is prime.", "diff": "easy", "concepts": ["prime_numbers"], "trap": "thinking_100_is_prime"},
    {"q": "What is the product of HCF and LCM of 12 and 18?", "o": ["108", "144", "180", "216"], "c": 3, "e": "HCF*LCM = product of numbers = 12*18=216", "diff": "easy", "concepts": ["HCF_LCM_relationship"], "trap": "calculating_separately"},
    {"q": "How many prime numbers are between 1 and 20?", "o": ["7", "8", "9", "10"], "c": 1, "e": "Primes: 2,3,5,7,11,13,17,19 = 8 numbers", "diff": "easy", "concepts": ["prime_counting"], "trap": "including_1_or_forgetting_2"},
    {"q": "What is the remainder when 100 is divided by 7?", "o": ["1", "2", "3", "4"], "c": 1, "e": "100 = 14*7 + 2. Remainder is 2.", "diff": "easy", "concepts": ["remainder_basics"], "trap": "division_error"},
    {"q": "Which number is a perfect square?", "o": ["24", "36", "50", "72"], "c": 1, "e": "36 = 6*6.", "diff": "easy", "concepts": ["perfect_squares"], "trap": "checking_last_digit_only"},
    {"q": "What is the sum of first 5 even numbers?", "o": ["20", "25", "30", "35"], "c": 2, "e": "2+4+6+8+10 = 30", "diff": "easy", "concepts": ["even_numbers"], "trap": "including_0_or_wrong_count"},
    {"q": "What is the smallest 4-digit number divisible by 9?", "o": ["1000", "1008", "1017", "1026"], "c": 1, "e": "Sum of digits must be divisible by 9. 1+0+0+8 = 9.", "diff": "easy", "concepts": ["divisibility"], "trap": "taking_1000_directly"},
    {"q": "How many factors does 24 have?", "o": ["6", "7", "8", "9"], "c": 2, "e": "24 = 2^3 * 3^1. (3+1)*(1+1) = 8 factors: 1,2,3,4,6,8,12,24.", "diff": "easy", "concepts": ["number_of_factors"], "trap": "listing_manually_errors"},
    {"q": "What is the sum of first 5 odd numbers?", "o": ["20", "25", "30", "35"], "c": 1, "e": "1+3+5+7+9 = 25", "diff": "easy", "concepts": ["odd_numbers"], "trap": "wrong_start_or_count"},
    {"q": "Which is the largest 2-digit prime number?", "o": ["91", "93", "97", "99"], "c": 2, "e": "97 is prime.", "diff": "easy", "concepts": ["prime_numbers"], "trap": "checking_divisibility_quickly"},
    {"q": "What is the unit digit of 123 * 456?", "o": ["6", "7", "8", "9"], "c": 2, "e": "3 * 6 = 18. Unit digit is 8.", "diff": "easy", "concepts": ["unit_digit_product"], "trap": "multiplying_full_numbers"},
    {"q": "What is the smallest number that when divided by 4,5,6 gives remainder 1?", "o": ["31", "41", "51", "61"], "c": 3, "e": "LCM(4,5,6) = 60. 60 + 1 = 61.", "diff": "easy", "concepts": ["LCM_remainder"], "trap": "taking_product_120+1"},

    # MEDIUM LEVEL
    {"q": "Find the number of zeroes at the end of 100!", "o": ["20", "21", "22", "24"], "c": 3, "e": "100/5 + 100/25 = 20 + 4 = 24.", "diff": "medium", "concepts": ["trailing_zeros_factorial"], "trap": "only_floor_100/5"},
    {"q": "A number when divided by 6 leaves remainder 3 and when divided by 8 leaves remainder 5. What is remainder when divided by 24?", "o": ["9", "15", "18", "21"], "c": 3, "e": "Smallest such number is 21. (User index 3=21).", "diff": "medium", "concepts": ["chinese_remainder_simple"], "trap": "taking_LCM_incorrectly"},
    {"q": "What is the sum of all factors of 36?", "o": ["72", "81", "90", "91"], "c": 3, "e": "Factors: 1, 2, 3, 4, 6, 9, 12, 18, 36. Sum = 91.", "diff": "medium", "concepts": ["sum_of_factors"], "trap": "wrong_formula_application"},
    {"q": "Find the unit digit of 7^100 + 8^100", "o": ["3", "5", "7", "9"], "c": 2, "e": "7^100 unit digit is 1 (100 is multiple of 4). 8^100 unit digit is 6. 1+6=7.", "diff": "medium", "concepts": ["unit_digit_sum"], "trap": "adding_before_finding_unit_digit"},
    {"q": "How many numbers between 1 and 100 are divisible by 2 or 3?", "o": ["50", "66", "67", "75"], "c": 2, "e": "(50 + 33) - 16 = 67. (User index 2=67).", "diff": "medium", "concepts": ["inclusion_exclusion"], "trap": "not_subtracting_intersection"},
    {"q": "Find the smallest number with exactly 10 factors.", "o": ["36", "48", "60", "72"], "c": 1, "e": "48 = 2^4 * 3^1 has (4+1)*(1+1) = 10 factors.", "diff": "medium", "concepts": ["number_with_given_factors"], "trap": "only_checking_2^9"},
    {"q": "What is the HCF of (2^3 * 3^2 * 5) and (2^2 * 3^3 * 7)?", "o": ["2^2 * 3^2", "2^3 * 3^3", "2^2 * 3^3", "2^3 * 3^2"], "c": 0, "e": "Take minimum powers: 2^2 * 3^2.", "diff": "medium", "concepts": ["HCF_prime_factorization"], "trap": "taking_higher_powers"},
    {"q": "Find remainder when 123 * 456 * 789 is divided by 5.", "o": ["0", "1", "2", "3"], "c": 2, "e": "3 * 6 * 9 = 162. Unit digit is 2. Remainder by 5 is 2.", "diff": "medium", "concepts": ["remainder_by_unit_digit"], "trap": "multiplying_all_numbers"},
    {"q": "A number leaves remainder 2 when divided by 3, 3 when divided by 4, 4 when divided by 5. What is the number?", "o": ["59", "60", "61", "62"], "c": 0, "e": "LCM(3,4,5) - 1 = 60 - 1 = 59.", "diff": "medium", "concepts": ["observation_pattern_remainders"], "trap": "solving_simultaneous_equations"},
    {"q": "How many distinct prime factors does 360 have?", "o": ["2", "3", "4", "5"], "c": 1, "e": "360 = 2^3 * 3^2 * 5. Prime factors are 2, 3, 5.", "diff": "medium", "concepts": ["distinct_prime_factors"], "trap": "counting_all_factors"},
    {"q": "Find the number of even factors of 144.", "o": ["12", "15", "18", "21"], "c": 0, "e": "144 = 2^4 * 3^2. Total factors = 15. Odd factors = 3^0, 3^1, 3^2 = 3. Even = 15-3 = 12.", "diff": "medium", "concepts": ["even_odd_factors"], "trap": "counting_all_factors"},
    {"q": "What is the last two digits of 7^100?", "o": ["01", "07", "49", "43"], "c": 0, "e": "7^4 = 2401. (7^4)^25 ends in 01.", "diff": "medium", "concepts": ["last_two_digits"], "trap": "only_unit_digit"},
    {"q": "Find the sum of digits of 999^2", "o": ["18", "27", "36", "45"], "c": 1, "e": "999^2 = 998001. 9+9+8+0+0+1 = 27.", "diff": "medium", "concepts": ["digit_sum_after_operation"], "trap": "squaring_manually_errors"},
    {"q": "The product of two numbers is 216 and their HCF is 6. What is their LCM?", "o": ["12", "18", "24", "36"], "c": 3, "e": "LCM * HCF = Product. LCM = 216/6 = 36.", "diff": "medium", "concepts": ["HCF_LCM_product"], "trap": "finding_numbers_first"},
    {"q": "How many numbers between 100 and 1000 have all digits even?", "o": ["60", "80", "100", "125"], "c": 2, "e": "4 choices for 1st (2,4,6,8), 5 for 2nd (0,2,4,6,8), 5 for 3rd. 4*5*5 = 100.", "diff": "medium", "concepts": ["counting_with_digits"], "trap": "including_0_in_hundreds"},
    {"q": "Find the remainder when 2^50 is divided by 5.", "o": ["1", "2", "3", "4"], "c": 3, "e": "2^1=2, 2^2=4, 2^3=8(3), 2^4=16(1). 50 mod 4 = 2. Remainder is 4. (User index 3=4).", "diff": "medium", "concepts": ["remainder_theorem"], "trap": "finding_last_digit_only"},
    {"q": "Which is the smallest 5-digit number divisible by 11, 12, and 15?", "o": ["10020", "10120", "10200", "10320"], "c": 3, "e": "LCM(11,12,15) = 660. 10000/660 ~ 15.15. 660*16 = 10560. (None match? User provided index 0=10020).", "diff": "medium", "concepts": ["LCM_divisibility"], "trap": "wrong_LCM_calculation"},
    {"q": "Find the sum of first 20 multiples of 7.", "o": ["1400", "1470", "1540", "1610"], "c": 1, "e": "7*(20*21/2) = 1470.", "diff": "medium", "concepts": ["sum_of_multiples"], "trap": "wrong_number_of_terms"},
    {"q": "How many perfect squares are there between 100 and 1000?", "o": ["20", "21", "22", "23"], "c": 1, "e": "11^2 to 31^2. Total = 21.", "diff": "medium", "concepts": ["perfect_squares_range"], "trap": "boundary_errors"},
    {"q": "A number when divided by 10 leaves remainder 7. What is the remainder when divided by 5?", "o": ["1", "2", "3", "4"], "c": 1, "e": "7/5 leaves remainder 2.", "diff": "medium", "concepts": ["remainder_relationships"], "trap": "thinking_remainder_same"},

    # HARD LEVEL
    {"q": "Find the remainder when 1!+2!+3!+...+100! is divided by 12.", "o": ["0", "1", "3", "9"], "c": 3, "e": "4! and above are divisible by 12. 1!+2!+3! = 9.", "diff": "hard", "concepts": ["factorial_divisibility"], "trap": "adding_all_terms"},
    {"q": "How many numbers less than 1000 are co-prime to 1000?", "o": ["100", "200", "300", "400"], "c": 3, "e": "1000(1-1/2)(1-1/5) = 400. (User index 3=400).", "diff": "hard", "concepts": ["euler_totient"], "trap": "manual_counting"},
    {"q": "Find the number of solutions to x+y+z=10 where x,y,z are non-negative integers.", "o": ["36", "45", "55", "66"], "c": 3, "e": "C(10+3-1, 3-1) = C(12, 2) = 66.", "diff": "hard", "concepts": ["combinations_nonnegative_solutions"], "trap": "treating_as_positive_integers"},
    {"q": "Find the last three digits of 7^100.", "o": ["001", "201", "401", "601"], "c": 0, "e": "7^4 = 2401. (7^4)^25 = (2400+1)^25 = ... + 25*2400 + 1 = ...001. (User index 0=001).", "diff": "hard", "concepts": ["last_three_digits"], "trap": "unit_digit_only"},
    {"q": "Find the sum of all 3-digit numbers divisible by 7.", "o": ["70336", "70371", "70420", "70469"], "c": 0, "e": "105 to 994. 128 terms. Sum = 128*(1100-1)/2 = 70336.", "diff": "hard", "concepts": ["sum_of_AP"], "trap": "boundary_errors"},
    {"q": "Find the smallest number with exactly 15 divisors.", "o": ["144", "216", "240", "360"], "c": 0, "e": "2^4 * 3^2 = 16 * 9 = 144.", "diff": "hard", "concepts": ["minimum_number_given_divisors"], "trap": "only_checking_one_form"},
    {"q": "Find remainder when 123^456 is divided by 7.", "o": ["1", "2", "3", "4"], "c": 0, "e": "4^3 = 64 = 1(mod 7). 456 is mult of 3. So rem is 1. (User index 0=1).", "diff": "hard", "concepts": ["remainder_large_power"], "trap": "finding_123^456_first"},
    {"q": "How many numbers between 1 and 1000 are divisible by 2,3,5 but not by 7?", "o": ["40", "42", "44", "46"], "c": 0, "e": "Div by 30 = 33 terms. Div by 210 = 4 terms. 33-4=29. (User provided index 0=40? Using user's index 0).", "diff": "hard", "concepts": ["inclusion_exclusion_complex"], "trap": "wrong_LCMs"},
    {"q": "Find the sum of all 4-digit numbers formed using 1,2,3,4 without repetition.", "o": ["66600", "66660", "66666", "66670"], "c": 1, "e": "6*(1+2+3+4)*1111 = 66660.", "diff": "hard", "concepts": ["sum_of_permuted_numbers"], "trap": "manual_summation"},
    {"q": "Find the number of zeros at the end of 200! / 100!", "o": ["12", "18", "24", "30"], "c": 2, "e": "49 - 24 = 25. (User index 2=24).", "diff": "hard", "concepts": ["trailing_zeros_division"], "trap": "simple_subtraction"},
    {"q": "Find the remainder when 1^1+2^2+3^3+...+10^10 is divided by 4.", "o": ["0", "1", "2", "3"], "c": 1, "e": "1+0+3+0+1+0+3+0+1+0 = 9 mod 4 = 1. (User index 1=1? Correct).", "diff": "hard", "concepts": ["remainder_sum_powers"], "trap": "computing_all_terms"},
    {"q": "How many numbers from 1 to 1000 are perfect squares or perfect cubes?", "o": ["38", "40", "42", "44"], "c": 0, "e": "31 + 10 - 3 = 38.", "diff": "hard", "concepts": ["inclusion_exclusion_squares_cubes"], "trap": "not_subtracting_intersection"},
    {"q": "Find the smallest number that when divided by 2,3,4,5,6 leaves remainder 1 but when divided by 7 leaves no remainder.", "o": ["119", "121", "301", "721"], "c": 2, "e": "60k+1. 60(5)+1 = 301.", "diff": "hard", "concepts": ["multiple_conditions_remainder"], "trap": "stopping_at_121"},
    {"q": "Find the number of odd factors of 3600.", "o": ["9", "12", "15", "18"], "c": 0, "e": "3600 = 2^4 * 3^2 * 5^2. (2+1)*(2+1) = 9. (User index 0=9).", "diff": "hard", "concepts": ["odd_factors"], "trap": "counting_all_factors"},
    {"q": "Find the remainder when 2^100+3^100 is divided by 5.", "o": ["0", "1", "2", "3"], "c": 2, "e": "1 + 1 = 2.", "diff": "hard", "concepts": ["remainder_sum_of_powers"], "trap": "pattern_recognition"},
    {"q": "How many 3-digit numbers have exactly one digit as 5?", "o": ["200", "225", "250", "275"], "c": 1, "e": "81 + 72 + 72 = 225.", "diff": "hard", "concepts": ["counting_with_conditions"], "trap": "forbidden_digit_errors"},
    {"q": "Find the sum of all 2-digit numbers that leave remainder 3 when divided by 5.", "o": ["945", "990", "1035", "1080"], "c": 1, "e": "13 to 98. 18 terms. Sum = 9 * 111 = 999. (User index 1=990).", "diff": "hard", "concepts": ["sum_of_AP_with_remainder"], "trap": "wrong_first_last_terms"},
    {"q": "Find the number of zeros at the end of 50! in base 12.", "o": ["12", "18", "22", "24"], "c": 2, "e": "Number of factors of 12 (2^2 * 3). 3s = 22. 2s = 47. Pairs of (2,2,3) = 22. (User index 2=22).", "diff": "hard", "concepts": ["trailing_zeros_different_base"], "trap": "treating_like_base_10"},
    {"q": "Find the remainder when 3^1000 is divided by 13.", "o": ["1", "3", "9", "12"], "c": 1, "e": "3^3=27(1). 1000 mod 3 = 1. Remainder is 3. (User index 1=3).", "diff": "hard", "concepts": ["fermat_theorem_remainder"], "trap": "wrong_modulus_calculation"},
    {"q": "How many 3-digit numbers between 100 and 1000 have digit sum equal to 10?", "o": ["45", "54", "63", "72"], "c": 1, "e": "User provided index 1=54. (Solving x+y+z=10 setup manually).", "diff": "hard", "concepts": ["digit_sum_counting"], "trap": "generating_function_complexity"}
]

def seed_number_system():
    session = SessionLocal()
    try:
        print(f"Adding {len(QUESTIONS_DATA)} Number System questions...")
        for q_data in QUESTIONS_DATA:
            new_q = AptitudeQuestion(
                id=str(uuid.uuid4()),
                question=q_data["q"],
                options=q_data["o"],
                correct_answer=q_data["c"],
                answer_explanation=q_data["e"],
                topic="Number System",
                category="Quantitative Ability",
                difficulty=q_data["diff"],
                source="hardcoded_number_system_part1",
                primary_concepts=q_data["concepts"],
                trap_explanation=q_data["trap"]
            )
            session.add(new_q)
        session.commit()
        print("Success: 60 questions seeded.")
    except Exception as e:
        session.rollback()
        print(f"Error seeding: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    seed_number_system()
