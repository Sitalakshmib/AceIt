from sqlalchemy.orm import sessionmaker
import sys
import os

# Add the parent directory to sys.path to import models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database_postgres import engine
from models.aptitude_sql import AptitudeQuestion
import uuid

Session = sessionmaker(bind=engine)
session = Session()

questions = [
    # EASY (20)
    {
        "question": "Rohan deposits \u20b95,000 at 8% simple interest for 3 years. What is the interest earned?",
        "options": ["\u20b91,000", "\u20b91,100", "\u20b91,200", "\u20b91,300"],
        "correct_answer": 2,
        "explanation": "SI = P\u00d7R\u00d7T/100 = 5000\u00d78\u00d73/100 = \u20b91,200",
        "difficulty": "easy",
        "concepts": ["basic_si_formula"],
        "traps": ["forgetting_divide_by_100", "wrong_time_unit"]
    },
    {
        "question": "What sum of money will earn \u20b9600 as simple interest at 5% per annum in 4 years?",
        "options": ["\u20b92,000", "\u20b92,500", "\u20b93,000", "\u20b93,500"],
        "correct_answer": 2,
        "explanation": "P = (SI\u00d7100)/(R\u00d7T) = (600\u00d7100)/(5\u00d74) = 60,000/20 = \u20b93,000",
        "difficulty": "easy",
        "concepts": ["finding_principal"],
        "traps": ["wrong_formula_rearrangement"]
    },
    {
        "question": "At what rate percent will \u20b92,000 amount to \u20b92,600 in 5 years at simple interest?",
        "options": ["5%", "6%", "7%", "8%"],
        "correct_answer": 1,
        "explanation": "SI = 2600-2000 = \u20b9600. R = (SI\u00d7100)/(P\u00d7T) = (600\u00d7100)/(2000\u00d75) = 60,000/10,000 = 6%",
        "difficulty": "easy",
        "concepts": ["finding_rate"],
        "traps": ["using_amount_instead_of_interest"]
    },
    {
        "question": "In what time will \u20b98,000 at 10% simple interest per annum double itself?",
        "options": ["8 years", "9 years", "10 years", "11 years"],
        "correct_answer": 2,
        "explanation": "To double, SI = P = \u20b98,000. T = (SI\u00d7100)/(P\u00d7R) = (8000\u00d7100)/(8000\u00d710) = 100/10 = 10 years",
        "difficulty": "easy",
        "concepts": ["doubling_time"],
        "traps": ["confusing_with_compound_interest"]
    },
    {
        "question": "The simple interest on \u20b94,000 for 2 years at 6% per annum is?",
        "options": ["\u20b9420", "\u20b9440", "\u20b9460", "\u20b9480"],
        "correct_answer": 3,
        "explanation": "SI = 4000\u00d76\u00d72/100 = \u20b9480",
        "difficulty": "easy",
        "concepts": ["basic_si_formula"],
        "traps": ["calculation_error"]
    },
    {
        "question": "A sum of \u20b91,500 amounts to \u20b91,800 in 2 years at simple interest. The rate percent per annum is?",
        "options": ["8%", "9%", "10%", "11%"],
        "correct_answer": 2,
        "explanation": "SI = 1800-1500 = \u20b9300. R = (300\u00d7100)/(1500\u00d72) = 30,000/3,000 = 10%",
        "difficulty": "easy",
        "concepts": ["finding_rate"],
        "traps": ["wrong_subtraction"]
    },
    {
        "question": "What principal will amount to \u20b95,600 in 3 years at 4% simple interest?",
        "options": ["\u20b94,800", "\u20b95,000", "\u20b95,200", "\u20b95,400"],
        "correct_answer": 1,
        "explanation": "A = P[1 + RT/100]. P = 5600/[1 + (4\u00d73)/100] = 5600/1.12 = \u20b95,000",
        "difficulty": "easy",
        "concepts": ["finding_principal_from_amount"],
        "traps": ["directly_subtracting_interest"]
    },
    {
        "question": "The simple interest on \u20b96,000 at 5% per annum for 9 months is?",
        "options": ["\u20b9200", "\u20b9225", "\u20b9250", "\u20b9275"],
        "correct_answer": 1,
        "explanation": "T = 9/12 = 3/4 years. SI = 6000\u00d75\u00d7(3/4)/100 = \u20b9225",
        "difficulty": "easy",
        "concepts": ["fractional_time"],
        "traps": ["using_months_as_years"]
    },
    {
        "question": "In how many years will \u20b93,000 yield \u20b9900 as simple interest at 5% per annum?",
        "options": ["5 years", "6 years", "7 years", "8 years"],
        "correct_answer": 1,
        "explanation": "T = (SI\u00d7100)/(P\u00d7R) = (900\u00d7100)/(3000\u00d75) = 90,000/15,000 = 6 years",
        "difficulty": "easy",
        "concepts": ["finding_time"],
        "traps": ["calculation_error"]
    },
    {
        "question": "A sum of \u20b92,400 amounts to \u20b92,640 in 2 years at simple interest. What is the rate?",
        "options": ["4%", "5%", "6%", "7%"],
        "correct_answer": 1,
        "explanation": "SI = 2640-2400 = \u20b9240. R = (240\u00d7100)/(2400\u00d72) = 24,000/4,800 = 5%",
        "difficulty": "easy",
        "concepts": ["finding_rate"],
        "traps": ["wrong_denominator"]
    },
    {
        "question": "At what rate will \u20b95,000 amount to \u20b96,500 in 6 years at simple interest?",
        "options": ["4%", "5%", "6%", "7%"],
        "correct_answer": 1,
        "explanation": "SI = 6500-5000 = \u20b91500. R = (1500\u00d7100)/(5000\u00d76) = 150,000/30,000 = 5%",
        "difficulty": "easy",
        "concepts": ["finding_rate"],
        "traps": ["using_total_amount_in_formula"]
    },
    {
        "question": "What is the simple interest on \u20b97,500 at 8% per annum for 2 years 6 months?",
        "options": ["\u20b91,400", "\u20b91,500", "\u20b91,600", "\u20b91,700"],
        "correct_answer": 1,
        "explanation": "T = 2.5 years. SI = 7500\u00d78\u00d72.5/100 = \u20b91,500",
        "difficulty": "easy",
        "concepts": ["mixed_time_units"],
        "traps": ["time_conversion_error"]
    },
    {
        "question": "A sum doubles itself in 8 years at simple interest. What is the rate percent per annum?",
        "options": ["10.5%", "11.5%", "12.5%", "13.5%"],
        "correct_answer": 2,
        "explanation": "When sum doubles, SI = P. R = (P\u00d7100)/(P\u00d7T) = 100/8 = 12.5%",
        "difficulty": "easy",
        "concepts": ["doubling_rate"],
        "traps": ["formula_misapplication"]
    },
    {
        "question": "The simple interest on a sum for 5 years at 6% per annum is \u20b91,200. The sum is?",
        "options": ["\u20b93,500", "\u20b93,800", "\u20b94,000", "\u20b94,200"],
        "correct_answer": 2,
        "explanation": "P = (SI\u00d7100)/(R\u00d7T) = (1200\u00d7100)/(6\u00d75) = 120,000/30 = \u20b94,000",
        "difficulty": "easy",
        "concepts": ["finding_principal"],
        "traps": ["wrong_multiplication"]
    },
    {
        "question": "In what time will \u20b910,000 at 12.5% simple interest per annum become \u20b915,000?",
        "options": ["3 years", "4 years", "5 years", "6 years"],
        "correct_answer": 1,
        "explanation": "SI = 15000-10000 = \u20b95,000. T = (5000\u00d7100)/(10000\u00d712.5) = 4 years",
        "difficulty": "easy",
        "concepts": ["finding_time"],
        "traps": ["decimal_rate_handling"]
    },
    {
        "question": "At simple interest, a sum becomes 5/4 of itself in 5 years. The rate percent per annum is?",
        "options": ["4%", "5%", "6%", "7%"],
        "correct_answer": 1,
        "explanation": "Let P = 4, then A = 5, SI = 1. R = (1\u00d7100)/(4\u00d75) = 100/20 = 5%",
        "difficulty": "easy",
        "concepts": ["fractional_amount"],
        "traps": ["fraction_interpretation"]
    },
    {
        "question": "The simple interest on \u20b98,000 at 7.5% per annum for 8 months is?",
        "options": ["\u20b9350", "\u20b9400", "\u20b9450", "\u20b9500"],
        "correct_answer": 1,
        "explanation": "T = 8/12 = 2/3 years. SI = 8000\u00d77.5\u00d7(2/3)/100 = \u20b9400",
        "difficulty": "easy",
        "concepts": ["fractional_time"],
        "traps": ["decimal_rate_with_fractional_time"]
    },
    {
        "question": "A sum of \u20b99,000 amounts to \u20b910,350 in 3 years at simple interest. Find the rate.",
        "options": ["4%", "5%", "6%", "7%"],
        "correct_answer": 1,
        "explanation": "SI = 10350-9000 = \u20b91,350. R = (1350\u00d7100)/(9000\u00d73) = 135,000/27,000 = 5%",
        "difficulty": "easy",
        "concepts": ["finding_rate"],
        "traps": ["calculation_error"]
    },
    {
        "question": "How much time will \u20b96,000 take to earn \u20b91,440 as simple interest at 6% per annum?",
        "options": ["3 years", "4 years", "5 years", "6 years"],
        "correct_answer": 1,
        "explanation": "T = (1440\u00d7100)/(6000\u00d76) = 144,000/36,000 = 4 years",
        "difficulty": "easy",
        "concepts": ["finding_time"],
        "traps": ["wrong_division"]
    },
    {
        "question": "A sum triples itself in 20 years at simple interest. What is the rate?",
        "options": ["8%", "10%", "12%", "15%"],
        "correct_answer": 1,
        "explanation": "When sum triples, SI = 2P. R = (2P\u00d7100)/(P\u00d720) = 200/20 = 10%",
        "difficulty": "easy",
        "concepts": ["tripling_time_rate"],
        "traps": ["thinking_si=3p"]
    },
    # MEDIUM (20)
    {
        "question": "A sum of money becomes \u20b98,800 in 4 years and \u20b99,600 in 6 years at simple interest. The sum is?",
        "options": ["\u20b96,500", "\u20b96,800", "\u20b97,000", "\u20b97,200"],
        "correct_answer": 3,
        "explanation": "Interest for 2 years = \u20b9800. Annual interest = \u20b9400. SI for 4y = \u20b91,600. P = 8800-1600 = \u20b97,200",
        "difficulty": "medium",
        "concepts": ["difference_method"],
        "traps": ["subtracting_wrong_values"]
    },
    {
        "question": "A certain sum amounts to \u20b97,200 in 2 years and to \u20b98,000 in 3 years at simple interest. Find the sum.",
        "options": ["\u20b95,400", "\u20b95,600", "\u20b95,800", "\u20b96,000"],
        "correct_answer": 1,
        "explanation": "Int for 1y = 8000-7200 = \u20b9800. Int for 2y = \u20b91,600. P = 7200-1600 = \u20b95,600",
        "difficulty": "medium",
        "concepts": ["difference_method"],
        "traps": ["equation_setup"]
    },
    {
        "question": "Simple interest on a certain sum at 8% per annum for 3 years is \u20b9200 more than interest on same sum at 5% per annum for 4 years. The sum is?",
        "options": ["\u20b94,000", "\u20b95,000", "\u20b96,000", "\u20b97,000"],
        "correct_answer": 1,
        "explanation": "Diff = (24% - 20%)P = 4%P. 0.04P=200 -> P=5000",
        "difficulty": "medium",
        "concepts": ["comparative_interest"],
        "traps": ["identical_interest_scenario"]
    },
    {
        "question": "A sum was put at simple interest at a certain rate for 3 years. Had it been put at 1% higher rate, it would have fetched \u20b918 more. The sum is?",
        "options": ["\u20b9500", "\u20b9600", "\u20b9700", "\u20b9800"],
        "correct_answer": 1,
        "explanation": "Extra interest = (P\u00d71\u00d73)/100 = 18 -> 3P/100 = 18 -> P = \u20b9600",
        "difficulty": "medium",
        "concepts": ["rate_change_effect"],
        "traps": ["time_not_included"]
    },
    {
        "question": "Mr. Sharma borrowed \u20b912,000 at 8% simple interest and lent it to Mr. Verma at 10% simple interest. His gain in 2 years is?",
        "options": ["\u20b9360", "\u20b9420", "\u20b9480", "\u20b9540"],
        "correct_answer": 2,
        "explanation": "Int diff per year = 2% of 12000 = \u20b9240. Gain in 2y = 240\u00d72 = \u20b9480",
        "difficulty": "medium",
        "concepts": ["borrow_lend_difference"],
        "traps": ["calculating_only_one_interest"]
    },
    {
        "question": "The simple interest on a sum of money is 1/9 of the principal, and the number of years is equal to the rate percent per annum. The rate is?",
        "options": ["3%", "3.33%", "4%", "4.33%"],
        "correct_answer": 1,
        "explanation": "SI = P/9, T=R. P/9 = P\u00d7R\u00d7R/100 -> R^2 = 100/9 -> R = 10/3 = 3.33%",
        "difficulty": "medium",
        "concepts": ["time_rate_relationship"],
        "traps": ["square_root_calculation"]
    },
    {
        "question": "A sum of money at simple interest amounts to \u20b91,073.50 in 2 years and to \u20b91,197 in 4 years. The sum and rate are?",
        "options": ["\u20b9900, 6%", "\u20b9950, 6.5%", "\u20b91,000, 6%", "\u20b91,000, 6.5%"],
        "correct_answer": 1,
        "explanation": "Int for 2y = 1197 - 1073.5 = \u20b9123.5. Int for 1y = \u20b961.75. P = 1073.5 - 123.5 = \u20b9950. R = (61.75\u00d7100)/950 = 6.5%",
        "difficulty": "medium",
        "concepts": ["multiple_time_periods"],
        "traps": ["compound_interest_confusion"]
    },
    {
        "question": "A sum was invested at simple interest at a certain rate for 4 years. Had it been invested at 2% higher rate, it would have fetched \u20b9160 more. The sum is?",
        "options": ["\u20b91,500", "\u20b92,000", "\u20b92,500", "\u20b93,000"],
        "correct_answer": 1,
        "explanation": "Extra interest = (P\u00d72\u00d74)/100 = 160 -> 8P/100 = 160 -> P = \u20b92,000",
        "difficulty": "medium",
        "concepts": ["rate_change_effect"],
        "traps": ["wrong_time_multiplier"]
    },
    {
        "question": "The simple interest on a sum of money at 5% per annum for 10 years is half the sum. The rate must be?",
        "options": ["4%", "5%", "6%", "7%"],
        "correct_answer": 1,
        "explanation": "SI = P/2. P/2 = P\u00d7R\u00d710/100 -> 1/2 = R/10 -> R=5%",
        "difficulty": "medium",
        "concepts": ["proportional_interest"],
        "traps": ["impossible_condition"]
    },
    {
        "question": "A sum of \u20b915,000 is lent out at simple interest in two parts at 8% and 10% per annum. If total annual interest is \u20b91,400, find money lent at 8%.",
        "options": ["\u20b95,000", "\u20b96,000", "\u20b97,000", "\u20b98,000"],
        "correct_answer": 0,
        "explanation": "Let x at 8%. 0.08x + 0.1(15000-x) = 1400 -> -0.02x = -100 -> x=5000",
        "difficulty": "medium",
        "concepts": ["split_investment"],
        "traps": ["equation_solving_error"]
    },
    {
        "question": "A sum of money amounts to \u20b95,200 in 2 years and to \u20b95,800 in 4 years at simple interest. Find the sum.",
        "options": ["\u20b94,200", "\u20b94,400", "\u20b94,600", "\u20b94,800"],
        "correct_answer": 2,
        "explanation": "Int for 2y = \u20b9600. P = 5200 - 600 = \u20b94,600",
        "difficulty": "medium",
        "concepts": ["difference_method"],
        "traps": ["wrong_subtraction"]
    },
    {
        "question": "A man invests \u20b910,000 in two parts at simple interest. First at 5% and second at 8%. If total interest after one year is \u20b9620, find amount invested at 5%.",
        "options": ["\u20b94,000", "\u20b95,000", "\u20b96,000", "\u20b97,000"],
        "correct_answer": 2,
        "explanation": "0.05x + 0.08(10000-x) = 620 -> -0.03x = -180 -> x=6000",
        "difficulty": "medium",
        "concepts": ["split_investment"],
        "traps": ["decimal_calculation"]
    },
    {
        "question": "The difference between simple interest on a sum for 3 years at 5% and for 2 years at 6% is \u20b930. Find the sum.",
        "options": ["\u20b91,000", "\u20b91,200", "\u20b91,500", "\u20b92,000"],
        "correct_answer": 0,
        "explanation": "(15% - 12%)P = 3%P. 0.03P=30 -> P=1000",
        "difficulty": "medium",
        "concepts": ["interest_difference"],
        "traps": ["sign_error"]
    },
    {
        "question": "A sum of \u20b98,000 is divided into two parts such that simple interest on first part at 6% for 4 years equals interest on second part at 8% for 2 years. First part is?",
        "options": ["\u20b93,200", "\u20b93,600", "\u20b94,000", "\u20b94,400"],
        "correct_answer": 0,
        "explanation": "24x = 16(8000-x) -> 40x=128000 -> x=3200",
        "difficulty": "medium",
        "concepts": ["equal_interest_split"],
        "traps": ["cross_multiplication_error"]
    },
    {
        "question": "A sum was put at simple interest at a certain rate for 4 years. Had it been put at 3% higher rate, it would have fetched \u20b9360 more. The sum is?",
        "options": ["\u20b92,000", "\u20b92,500", "\u20b93,000", "\u20b93,500"],
        "correct_answer": 2,
        "explanation": "12%P = 360 -> P = \u20b93,000",
        "difficulty": "medium",
        "concepts": ["rate_change_effect"],
        "traps": ["time_not_included"]
    },
    {
        "question": "Simple interest on a sum for 5 years at 12% per annum is \u20b9600 less than the simple interest on the same sum for 7 years at 10% per annum. The sum is?",
        "options": ["\u20b95,000", "\u20b95,500", "\u20b96,000", "\u20b96,500"],
        "correct_answer": 2,
        "explanation": "(70% - 60%)P = 10%P. 0.1P=600 -> P=6000",
        "difficulty": "medium",
        "concepts": ["comparative_interest"],
        "traps": ["which_is_larger_confusion"]
    },
    {
        "question": "A sum of \u20b916,000 amounts to \u20b918,400 in 2 years at simple interest. If rate is increased by 2%, what would it amount to in same time?",
        "options": ["\u20b918,800", "\u20b919,040", "\u20b919,200", "\u20b919,360"],
        "correct_answer": 1,
        "explanation": "Orig SI=2400 in 2y, R=7.5%. New R=9.5%. New SI=16000\u00d70.095\u00d72 = 3040. Amt = 19040",
        "difficulty": "medium",
        "concepts": ["rate_increase_effect"],
        "traps": ["finding_original_rate_first"]
    },
    {
        "question": "The simple interest on a certain sum for 2.5 years at 12% per annum is \u20b9600 less than simple interest on same sum for 4.5 years at 8% per annum. The sum is?",
        "options": ["\u20b98,000", "\u20b99,000", "\u20b910,000", "\u20b911,000"],
        "correct_answer": 2,
        "explanation": "(36% - 30%)P = 6%P. 0.06P=600 -> P=10000",
        "difficulty": "medium",
        "concepts": ["fractional_time_comparison"],
        "traps": ["decimal_time_calculation"]
    },
    {
        "question": "A sum of money becomes \u20b97,200 in 2 years and \u20b98,400 in 4 years at simple interest. Find the sum and rate.",
        "options": ["\u20b96,000, 10%", "\u20b96,200, 9.68%", "\u20b96,400, 10%", "\u20b96,600, 9.09%"],
        "correct_answer": 0,
        "explanation": "Int for 2y = \u20b91200. P = 7200 - 1200 = \u20b96000. R = (600\u00d7100)/6000 = 10%",
        "difficulty": "medium",
        "concepts": ["difference_method"],
        "traps": ["time_period_confusion"]
    },
    {
        "question": "A certain sum amounts to \u20b94,800 in 3 years and to \u20b95,200 in 5 years at simple interest. Find the sum.",
        "options": ["\u20b94,000", "\u20b94,200", "\u20b94,400", "\u20b94,600"],
        "correct_answer": 1,
        "explanation": "Int for 2y = 400. Int for 1y = 200. P = 4800 - (3\u00d7200) = \u20b94200",
        "difficulty": "medium",
        "concepts": ["difference_method"],
        "traps": ["wrong_time_multiplier"]
    },
    # HARD (20)
    {
        "question": "A sum of money doubles itself in 10 years at simple interest. In how many years will it triple itself?",
        "options": ["15 years", "18 years", "20 years", "25 years"],
        "correct_answer": 2,
        "explanation": "Doubles in 10y -> SI=P in 10y. Triples -> SI=2P. Time = 20 years",
        "difficulty": "hard",
        "concepts": ["multiple_times_principal"],
        "traps": ["linear_extrapolation_error"]
    },
    {
        "question": "A sum of \u20b910,000 is lent in two parts such that simple interest on first part at 4% for 5 years equals interest on second part at 5% for 4 years. Find the first part.",
        "options": ["\u20b94,500", "\u20b95,000", "\u20b95,500", "\u20b96,000"],
        "correct_answer": 1,
        "explanation": "20%x = 20%(10000-x) -> x = 5000",
        "difficulty": "hard",
        "concepts": ["equal_interest_split"],
        "traps": ["cancellation_error"]
    },
    {
        "question": "The simple interest on a sum for 8 months at 6% per annum is \u20b9180 less than simple interest on same sum for 15 months at 5% per annum. The sum is?",
        "options": ["\u20b96,000", "\u20b97,000", "\u20b98,000", "\u20b99,000"],
        "correct_answer": 2,
        "explanation": "8m@6% = 4%. 15m@5% = 6.25%. Diff = 2.25%. 0.0225P=180 -> P=8000",
        "difficulty": "hard",
        "concepts": ["fractional_time_comparison"],
        "traps": ["fraction_arithmetic"]
    },
    {
        "question": "A sum of money becomes \u20b91,440 in 2 years and \u20b91,560 in 3 years at simple interest. Find the sum.",
        "options": ["\u20b91,150", "\u20b91,180", "\u20b91,200", "\u20b91,220"],
        "correct_answer": 2,
        "explanation": "Int for 1y = 120. P = 1440 - 240 = \u20b91200",
        "difficulty": "hard",
        "concepts": ["difference_method"],
        "traps": ["calculation_verification"]
    },
    {
        "question": "A man invests equal sums at 5% and 6% simple interest respectively. After 3 years, the difference between interests is \u20b945. Find each sum.",
        "options": ["\u20b91,200", "\u20b91,300", "\u20b91,400", "\u20b91,500"],
        "correct_answer": 3,
        "explanation": "Diff per year = 1% of P. In 3y, 3% of P = 45 -> P = 1500",
        "difficulty": "hard",
        "concepts": ["equal_principal_different_rates"],
        "traps": ["sign_confusion"]
    },
    {
        "question": "A sum of money at simple interest amounts to \u20b914,400 in 3 years and to \u20b916,000 in 5 years. Find the sum and rate.",
        "options": ["\u20b912,000, 6.67%", "\u20b912,400, 6.45%", "\u20b912,800, 6.25%", "\u20b913,000, 6%"],
        "correct_answer": 0,
        "explanation": "Int for 2y = 1600. P = 14400 - 2400 = 12000. R = 800/12000 = 6.67%",
        "difficulty": "hard",
        "concepts": ["difference_method"],
        "traps": ["percentage_calculation"]
    },
    {
        "question": "A sum was put at simple interest at a certain rate for 2 years. Had it been put at 3% higher rate, it would have fetched \u20b9300 more. What is the sum?",
        "options": ["\u20b95,000", "\u20b95,500", "\u20b96,000", "\u20b96,500"],
        "correct_answer": 0,
        "explanation": "6%P = 300 -> P=5000",
        "difficulty": "hard",
        "concepts": ["rate_change_effect"],
        "traps": ["simple_calculation"]
    },
    {
        "question": "A person borrows \u20b95,000 at 4% simple interest and \u20b98,000 at 5% simple interest. After how many years will the total interest be \u20b91,800?",
        "options": ["3 years", "4 years", "5 years", "6 years"],
        "correct_answer": 0,
        "explanation": "Annual interest = 200 + 400 = 600. Time = 1800/600 = 3 years",
        "difficulty": "hard",
        "concepts": ["multiple_loans"],
        "traps": ["averaging_rates"]
    },
    {
        "question": "The simple interest on a sum of money at 4% per annum for 2 years is \u20b980. The compound interest on same sum at same rate for same time is?",
        "options": ["\u20b980.80", "\u20b981.60", "\u20b982.40", "\u20b983.20"],
        "correct_answer": 1,
        "explanation": "P=1000. CI = 1000[(1.04)^2 - 1] = 81.60",
        "difficulty": "hard",
        "concepts": ["si_ci_relationship"],
        "traps": ["si_ci_difference_calculation"]
    },
    {
        "question": "A sum of \u20b915,000 is divided into two parts such that simple interest on first at 8% for 4 years equals interest on second at 12% for 4 years. Find first part.",
        "options": ["\u20b98,000", "\u20b99,000", "\u20b910,000", "\u20b911,000"],
        "correct_answer": 1,
        "explanation": "32%x = 48%(15000-x) -> 80x = 720000 -> x=9000",
        "difficulty": "hard",
        "concepts": ["equal_interest_split"],
        "traps": ["cross_multiplication"]
    },
    {
        "question": "A certain sum amounts to \u20b97,200 in 2 years and to \u20b99,600 in 5 years at simple interest. Find the sum.",
        "options": ["\u20b95,200", "\u20b95,400", "\u20b95,600", "\u20b95,800"],
        "correct_answer": 2,
        "explanation": "Int for 3y = 2400. P = 7200 - 1600 = 5600",
        "difficulty": "hard",
        "concepts": ["difference_method"],
        "traps": ["time_interval_calculation"]
    },
    {
        "question": "The simple interest on a sum for 4 years at 8% per annum is \u20b91,920. What would be the simple interest on same sum at 10% per annum for 3 years?",
        "options": ["\u20b91,600", "\u20b91,700", "\u20b91,800", "\u20b91,900"],
        "correct_answer": 2,
        "explanation": "P = 6000. New SI = 6000\u00d70.1\u00d73 = 1800",
        "difficulty": "hard",
        "concepts": ["changing_parameters"],
        "traps": ["finding_principal_first"]
    },
    {
        "question": "A sum was invested at simple interest at a certain rate for 5 years. Had it been invested at 2% higher rate, it would have fetched \u20b91,000 more. The sum is?",
        "options": ["\u20b98,000", "\u20b99,000", "\u20b910,000", "\u20b911,000"],
        "correct_answer": 2,
        "explanation": "10%P = 1000 -> P=10000",
        "difficulty": "hard",
        "concepts": ["rate_change_effect"],
        "traps": ["simple_calculation"]
    },
    {
        "question": "A sum of money becomes 3 times in 20 years at simple interest. In how many years will it become 5 times?",
        "options": ["30 years", "35 years", "40 years", "45 years"],
        "correct_answer": 2,
        "explanation": "SI=2P in 20y. SI=4P requires 40 years",
        "difficulty": "hard",
        "concepts": ["multiple_times_principal"],
        "traps": ["linear_progression_thinking"]
    },
    {
        "question": "A person invests \u20b912,000 at 5% simple interest and \u20b915,000 at 6% simple interest. After how many years will total interest be \u20b99,000?",
        "options": ["5 years", "6 years", "7 years", "8 years"],
        "correct_answer": 1,
        "explanation": "Annual interest = 600 + 900 = 1500. Time = 9000/1500 = 6 years",
        "difficulty": "hard",
        "concepts": ["multiple_investments"],
        "traps": ["weighted_average_rate"]
    },
    {
        "question": "The difference between simple interest on a sum for 4 years at 5% and for 3 years at 6% is \u20b920. Find the sum.",
        "options": ["\u20b91,000", "\u20b91,200", "\u20b91,500", "\u20b92,000"],
        "correct_answer": 0,
        "explanation": "(20% - 18%)P = 2%P = 20 -> P=1000",
        "difficulty": "hard",
        "concepts": ["interest_difference"],
        "traps": ["sign_setup"]
    },
    {
        "question": "A sum of \u20b920,000 is lent in two parts such that simple interest on first at 4% for 6 years equals interest on second at 6% for 4 years. Find second part.",
        "options": ["\u20b910,000", "\u20b912,000", "\u20b913,000", "\u20b915,000"],
        "correct_answer": 0,
        "explanation": "24%x = 24%(20000-x) -> x=10000",
        "difficulty": "hard",
        "concepts": ["equal_interest_split"],
        "traps": ["identical_coefficients"]
    },
    {
        "question": "Simple interest on a sum for 9 months at 8% per annum is \u20b9180. Find the sum.",
        "options": ["\u20b92,800", "\u20b93,000", "\u20b93,200", "\u20b93,400"],
        "correct_answer": 1,
        "explanation": "T=3/4y. SI = P\u00d78\u00d70.75/100 = 6%P = 180 -> P=3000",
        "difficulty": "hard",
        "concepts": ["fractional_time"],
        "traps": ["fraction_handling"]
    },
    {
        "question": "A sum of money becomes \u20b912,000 in 4 years and \u20b914,400 in 6 years at simple interest. Find the sum.",
        "options": ["\u20b97,000", "\u20b97,200", "\u20b97,400", "\u20b97,600"],
        "correct_answer": 1,
        "explanation": "Int for 2y = 2400. P = 12000 - 4800 = 7200",
        "difficulty": "hard",
        "concepts": ["difference_method"],
        "traps": ["verification_omission"]
    },
    {
        "question": "A man invests equal sums at 4% and 5% simple interest. After 4 years, total interest is \u20b9900. Find each sum.",
        "options": ["\u20b92,000", "\u20b92,250", "\u20b92,500", "\u20b92,750"],
        "correct_answer": 2,
        "explanation": "(16% + 20%)P = 36%P = 900 -> P=2500",
        "difficulty": "hard",
        "concepts": ["equal_investments"],
        "traps": ["interpretation_of_equal_sums"]
    }
]

for q_data in questions:
    q = AptitudeQuestion(
        id=str(uuid.uuid4()),
        question=q_data["question"],
        options=q_data["options"],
        correct_answer=q_data["correct_answer"],
        answer_explanation=q_data["explanation"],
        topic="Simple Interest",
        category="Quantitative Ability",
        difficulty=q_data["difficulty"],
        source="hardcoded",
        primary_concepts=q_data["concepts"],
        trap_explanation=f"Common traps: {', '.join(q_data['traps'])}" if q_data["traps"] else None
    )
    session.add(q)

session.commit()
print(f"Successfully seeded {len(questions)} Simple Interest questions.")
session.close()
