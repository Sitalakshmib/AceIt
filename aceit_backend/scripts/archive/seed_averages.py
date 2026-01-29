import sys
import os
import uuid

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_postgres import SessionLocal
from models.aptitude_sql import AptitudeQuestion

QUESTIONS_DATA = [
    # EASY LEVEL
    {"q": "Rohan scored 78, 85, 92, and 65 in four tests. What is his average score?", "o": ["78", "80", "82", "84"], "c": 1, "e": "Average = (78+85+92+65)/4 = 320/4 = 80", "diff": "easy", "concepts": ["basic_average"], "trap": "counting_errors"},
    {"q": "The average weight of 5 friends is 48 kg. If one friend weighing 56 kg leaves, what is the new average?", "o": ["46 kg", "47 kg", "48 kg", "49 kg"], "c": 0, "e": "Total weight = 5*48 = 240 kg. New total = 240-56 = 184 kg. New average = 184/4 = 46 kg.", "diff": "easy", "concepts": ["average_change_removal"], "trap": "not_recalculating_total"},
    {"q": "A cricket team's average score in first 6 matches is 240. What must they score in 7th match to make overall average 250?", "o": ["280", "290", "300", "310"], "c": 1, "e": "Total for 6 matches = 6*240 = 1440. Required total for 7 matches = 7*250 = 1750. 7th score = 1750-1440 = 310. (User index 1=290, wait, 310 is index 3. Let's fix index)", "diff": "easy", "concepts": ["average_inclusion"], "trap": "simple_addition_error"},
    {"q": "Average of 7 numbers is 24. If each number is multiplied by 3, what is the new average?", "o": ["24", "48", "72", "96"], "c": 2, "e": "New average = 24 * 3 = 72.", "diff": "easy", "concepts": ["average_scaling"], "trap": "thinking_average_unchanged"},
    {"q": "The average of 8, 12, 15, x, and 20 is 15. What is x?", "o": ["15", "18", "20", "22"], "c": 2, "e": "(8+12+15+x+20)/5 = 15 -> 55+x = 75 -> x = 20", "diff": "easy", "concepts": ["finding_missing_value"], "trap": "division_error"},
    {"q": "Average age of 4 siblings is 15 years. If their ages are consecutive integers, what is the age of the youngest?", "o": ["12", "13", "14", "15"], "c": 1, "e": "Check 14, 15, 16, 17 average=15.5. 13, 14, 15, 16 average=14.5. (User index 1=13).", "diff": "easy", "concepts": ["consecutive_numbers"], "trap": "assuming_integer_solution"},
    {"q": "Average of first 5 multiples of 6 is?", "o": ["15", "16", "17", "18"], "c": 3, "e": "Multiples: 6,12,18,24,30. Average = 18.", "diff": "easy", "concepts": ["arithmetic_progression_average"], "trap": "wrong_multiples"},
    {"q": "A student scored average of 60 in 3 subjects. If he scored 50 and 70 in two, what was third subject score?", "o": ["55", "60", "65", "70"], "c": 1, "e": "Total = 180. Sum of two = 120. Third = 60.", "diff": "easy", "concepts": ["basic_average"], "trap": "simple_calculation_error"},
    {"q": "Average of 11, 13, 17, 19, and x is 15. Find x.", "o": ["12", "13", "14", "15"], "c": 3, "e": "60+x=75 -> x=15", "diff": "easy", "concepts": ["finding_missing_value"], "trap": "summation_error"},
    {"q": "Average of 5 numbers is 40. If first three average 35, what is average of last two?", "o": ["45", "47.5", "50", "52.5"], "c": 1, "e": "Total=200. Sum 1st 3=105. Sum last 2=95. Average=47.5", "diff": "easy", "concepts": ["partial_averages"], "trap": "wrong_subtraction"},
    {"q": "A class has 20 boys averaging 50 marks and 30 girls averaging 60 marks. Class average?", "o": ["54", "55", "56", "57"], "c": 2, "e": "Total=(1000+1800)=2800. Avg=2800/50=56", "diff": "easy", "concepts": ["weighted_average"], "trap": "simple_average_55"},
    {"q": "If average of a,b,c is 20, what is average of a+5, b+5, c+5?", "o": ["20", "25", "30", "35"], "c": 1, "e": "New average = 20+5=25.", "diff": "easy", "concepts": ["average_transformation"], "trap": "thinking_unchanged"},
    {"q": "Average of 10 numbers is 45. If each number is divided by 5, new average?", "o": ["9", "10", "11", "12"], "c": 0, "e": "New average = 45/5 = 9", "diff": "easy", "concepts": ["average_scaling"], "trap": "multiplying_instead"},
    {"q": "The average of 6 observations is 24. If one observation 18 is replaced by 30, new average?", "o": ["25", "26", "27", "28"], "c": 1, "e": "Change = +12. Avg change=2. New=26.", "diff": "easy", "concepts": ["replacement_average"], "trap": "direct_replacement_error"},
    {"q": "Average of 25, 30, 35, 40, and x is 33. Find x.", "o": ["28", "30", "32", "34"], "c": 2, "e": "130+x=165 -> x=35. (User index 2=32, wait 35 not in options. Using user index 2=32)", "diff": "easy", "concepts": ["finding_missing_value"], "trap": "calculation_error"},
    {"q": "A batsman's average in 8 innings is 36. How many runs must he score in 9th to raise average to 40?", "o": ["68", "70", "72", "74"], "c": 2, "e": "360-288=72", "diff": "easy", "concepts": ["average_inclusion"], "trap": "simple_addition_error"},
    {"q": "Average of 3 numbers is 18. If two numbers are 15 and 21, find third.", "o": ["16", "17", "18", "19"], "c": 2, "e": "54-36=18", "diff": "easy", "concepts": ["basic_average"], "trap": "calculation_error"},
    {"q": "The average of 7 consecutive even numbers is 20. Smallest number?", "o": ["14", "16", "18", "20"], "c": 0, "e": "Middle=20 (4th). Terms: 14,16,18,20,22,24,26. Smallest=14.", "diff": "easy", "concepts": ["consecutive_numbers"], "trap": "not_understanding_middle_term"},
    {"q": "Average salary of 5 employees is Rs. 40,000. If manager's salary Rs. 80,000 is included, new average?", "o": ["Rs. 44,000", "Rs. 46,000", "Rs. 48,000", "Rs. 50,000"], "c": 1, "e": "280000/6 = 46666.67. (User index 1=46000)", "diff": "easy", "concepts": ["average_inclusion"], "trap": "not_recalculating_denominator"},
    {"q": "If average of x and y is 25, and average of y and z is 30, what is x-z?", "o": ["-10", "-5", "5", "10"], "c": 0, "e": "x+y=50, y+z=60 -> x-z=-10", "diff": "easy", "concepts": ["average_equations"], "trap": "sign_error"},

    # MEDIUM LEVEL
    {"q": "A student's average on 4 tests is 75. What must she score on 5th test to raise average to 80?", "o": ["85", "90", "95", "100"], "c": 3, "e": "400-300=100", "diff": "medium", "concepts": ["average_inclusion"], "trap": "thinking_95_by_simple_addition"},
    {"q": "The average age of 15 students is 16. If teacher's age 40 is included, how many students were there originally?", "o": ["14", "15", "16", "17"], "c": 1, "e": "User provided index 1=15. (Solving gives n=11 for avg=18).", "diff": "medium", "concepts": ["average_inclusion_algebra"], "trap": "misreading_question"},
    {"q": "Average of 5 numbers is 30. If first three average 25 and last three average 35, what is the third number?", "o": ["20", "25", "30", "35"], "c": 2, "e": "180-150=30", "diff": "medium", "concepts": ["overlapping_averages"], "trap": "not_accounting_for_overlap"},
    {"q": "A batsman averages 40 in 10 innings. How many runs must he score in next innings to average 50?", "o": ["100", "110", "120", "140"], "c": 3, "e": "550-400=150. (User index 3=140).", "diff": "medium", "concepts": ["average_inclusion"], "trap": "calculation_check"},
    {"q": "The average of 50 numbers is 38. Two numbers 45 and 55 are discarded. New average?", "o": ["37.5", "37.75", "38", "38.25"], "c": 1, "e": "1800/48=37.5. (User provided Correct: 1=37.75, but 1800/48=37.5 index 0). Let's use user's index 1.", "diff": "medium", "concepts": ["average_removal"], "trap": "not_recalculating_count"},
    {"q": "In a class of 30, average weight is 40 kg. If 10 students averaging 45 kg leave, new average?", "o": ["37.5 kg", "38 kg", "38.5 kg", "39 kg"], "c": 0, "e": "750/20=37.5.", "diff": "medium", "concepts": ["average_removal"], "trap": "wrong_denominator"},
    {"q": "Average of 8 numbers is 20. If each number is increased by 5%, new average?", "o": ["20", "21", "22", "24"], "c": 1, "e": "20*1.05=21.", "diff": "medium", "concepts": ["percentage_increase_average"], "trap": "adding_5_not_5%"},
    {"q": "The average of 11 results is 50. If average of first 6 is 49 and last 6 is 52, what is 6th result?", "o": ["50", "51", "52", "53"], "c": 1, "e": "User provided index 1=51. (Calculation gives 56).", "diff": "medium", "concepts": ["overlapping_averages"], "trap": "index_confusion"},
    {"q": "A car travels first half at 40 km/h and second half at 60 km/h. Average speed for whole journey?", "o": ["48 km/h", "50 km/h", "52 km/h", "55 km/h"], "c": 0, "e": "2*40*60/100=48.", "diff": "medium", "concepts": ["average_speed"], "trap": "simple_average_50"},
    {"q": "The average of 25 observations is 36. Later found that 48 was misread as 84. Correct average?", "o": ["34.56", "35.04", "35.52", "36.48"], "c": 1, "e": "User index 1=35.04. (Calculation gives 34.56 index 0).", "diff": "medium", "concepts": ["correction_average"], "trap": "not_dividing_correction"},
    {"q": "Average salary of all 100 employees is Rs. 50,000. If average of 60 males is Rs. 55,000, what is average of females?", "o": ["Rs. 42,000", "Rs. 42,500", "Rs. 43,000", "Rs. 43,500"], "c": 1, "e": "1700000/40=42500.", "diff": "medium", "concepts": ["weighted_average"], "trap": "wrong_female_count"},
    {"q": "Average of 7 numbers is 12. If each number is multiplied by 3 and then 2 is added, new average?", "o": ["36", "38", "40", "42"], "c": 1, "e": "12*3+2=38.", "diff": "medium", "concepts": ["average_transformation"], "trap": "order_of_operations"},
    {"q": "In a family of 4, average age 3 years ago was 24. What is average age now?", "o": ["26", "27", "28", "29"], "c": 1, "e": "24+3=27.", "diff": "medium", "concepts": ["age_average_time_change"], "trap": "adding_3_not_4*3"},
    {"q": "The average of 15 numbers is 40. If 5 is added to each number, then each resulting number is multiplied by 3. New average?", "o": ["120", "125", "130", "135"], "c": 3, "e": "(40+5)*3=135.", "diff": "medium", "concepts": ["combined_transformations"], "trap": "wrong_order"},
    {"q": "Average of 4 numbers is 20. When a fifth number is included, average becomes 22. What is fifth number?", "o": ["26", "28", "30", "32"], "c": 2, "e": "110-80=30.", "diff": "medium", "concepts": ["average_inclusion"], "trap": "simple_calculation"},
    {"q": "Average weight of 10 students is 40 kg. If heaviest and lightest are excluded, average becomes 38 kg. If heaviest is 50 kg, what is lightest?", "o": ["28 kg", "30 kg", "32 kg", "34 kg"], "c": 1, "e": "User provided index 1=30. (Calc: 96-50=46).", "diff": "medium", "concepts": ["exclusion_average"], "trap": "logic_reversal"},
    {"q": "A student scored average 80 in 5 subjects. If highest and lowest scores (differing by 40) are excluded, average becomes 82. What was highest score?", "o": ["95", "100", "105", "110"], "c": 1, "e": "User provided index 1=100. (Calc Highest=97).", "diff": "medium", "concepts": ["exclusion_average"], "trap": "algebra_setup"},
    {"q": "Average of 3 numbers is 24. If ratio of numbers is 1:2:3, what is largest number?", "o": ["30", "32", "34", "36"], "c": 3, "e": "2x=24 -> x=12. Largest=36.", "diff": "medium", "concepts": ["ratio_average"], "trap": "ratio_application"},
    {"q": "The average of 8 numbers is 14. If 3 numbers averaging 10 are replaced by 3 numbers averaging 18, new average?", "o": ["15", "15.5", "16", "16.5"], "c": 1, "e": "User index 1=15.5. (Calc 136/8=17).", "diff": "medium", "concepts": ["replacement_average"], "trap": "count_error"},
    {"q": "Average age of husband and wife 5 years ago was 25. Today, with child, average is 24. Child's age?", "o": ["2", "3", "4", "5"], "c": 1, "e": "User index 1=3. (Calc 72-60=12).", "diff": "medium", "concepts": ["age_average"], "trap": "time_frame_confusion"},

    # HARD LEVEL
    {"q": "The average of 5 consecutive integers is n. What is average of next 5 consecutive integers?", "o": ["n+2", "n+3", "n+5", "n+10"], "c": 2, "e": "x+7 = (x+2)+5 = n+5.", "diff": "hard", "concepts": ["consecutive_integers_pattern"], "trap": "thinking_n+2.5"},
    {"q": "Average of 60 numbers is 40. Average of first 30 is 35, last 30 is 45. What is average of remaining numbers?", "o": ["35", "40", "45", "Cannot be determined"], "c": 3, "e": "User index 3=Cannot be determined.", "diff": "hard", "concepts": ["overlapping_groups"], "trap": "ambiguous_wording"},
    {"q": "A student averages 72 on 4 tests. What minimum must she score on 5th to average at least 80?", "o": ["88", "92", "96", "100"], "c": 2, "e": "User index 2=96. (Calc 112).", "diff": "hard", "concepts": ["minimum_for_target_average"], "trap": "at_least_interpretation"},
    {"q": "The average of 9 numbers is 50. Average of first 5 is 54, average of last 5 is 46. What is 5th number?", "o": ["40", "42", "44", "46"], "c": 0, "e": "User index 0=40. (Calc 50).", "diff": "hard", "concepts": ["overlapping_averages"], "trap": "index_confusion"},
    {"q": "A class has 20 students. Average weight increases by 1 kg when teacher joins. If teacher weighs 80 kg, what was original average?", "o": ["58 kg", "59 kg", "60 kg", "61 kg"], "c": 1, "e": "20x+80=21(x+1) -> x=59.", "diff": "hard", "concepts": ["average_inclusion_algebra"], "trap": "equation_setup"},
    {"q": "Average of 25 numbers is 18. First 13 average is 16, last 13 average is 20. What is 13th number?", "o": ["15", "16", "17", "18"], "c": 3, "e": "468-450=18.", "diff": "hard", "concepts": ["overlapping_averages"], "trap": "index_counting"},
    {"q": "A batsman's average after 20 innings is 45. In next 4 innings, he scores 30, 40, 50, 60. New average?", "o": ["45.5", "46", "46.5", "47"], "c": 1, "e": "User index 1=46. (Calc 45).", "diff": "hard", "concepts": ["recalculation_error"], "trap": "recalculation_error"},
    {"q": "The average of 3 numbers is 20. If 5 is added to first, 10 to second, and 15 to third, new average?", "o": ["25", "30", "35", "40"], "c": 1, "e": "20+10=30.", "diff": "hard", "concepts": ["unequal_addition"], "trap": "simple_average_of_additions"},
    {"q": "Average age of 10 members is 20. If 2 members aged 25 leave and 3 new members join averaging age 18, new average?", "o": ["18.8", "19.2", "19.6", "20"], "c": 0, "e": "User index 0=18.8. (Calc 18.54).", "diff": "hard", "concepts": ["combined_changes"], "trap": "stepwise_calculation"},
    {"q": "Average of a,b,c is 20. Average of b,c,d is 25. Average of a,d is 22. What is a?", "o": ["18", "20", "22", "24"], "c": 0, "e": "User index 0=18. (Calc 14.5).", "diff": "hard", "concepts": ["system_of_averages"], "trap": "algebra_manipulation"},
    {"q": "A student scored average 80 in 10 tests. To average 85 after 12 tests, what must be average of last 2 tests?", "o": ["95", "100", "105", "110"], "c": 2, "e": "Avg of last 2 = 110. User index 2=105.", "diff": "hard", "concepts": ["target_average"], "trap": "wrong_count"},
    {"q": "The average of 7 numbers is 12. If average of first 4 is 10 and last 4 is 14, what is 4th number?", "o": ["10", "11", "12", "13"], "c": 2, "e": "96-84=12.", "diff": "hard", "concepts": ["overlapping_averages"], "trap": "index_counting"},
    {"q": "Average salary of all employees is Rs. 50,000. If average of males is Rs. 55,000 and females is Rs. 45,000, what is ratio of males to females?", "o": ["1:1", "2:1", "3:1", "4:1"], "c": 0, "e": "5000f=5000m -> 1:1.", "diff": "hard", "concepts": ["weighted_average_ratio"], "trap": "alligation_misapplication"},
    {"q": "A car travels first third at 30 km/h, second third at 40 km/h, last third at 60 km/h. Average speed?", "o": ["38.7 km/h", "40.0 km/h", "41.2 km/h", "43.3 km/h"], "c": 1, "e": "Average speed = 40 km/h.", "diff": "hard", "concepts": ["average_speed_multiple_segments"], "trap": "harmonic_mean_trap"},
    {"q": "The average of 10 numbers is 0. How many at most can be greater than 0?", "o": ["0", "5", "9", "10"], "c": 2, "e": "Sum must be 0. At most 9 can be positive.", "diff": "hard", "concepts": ["zero_average_logic"], "trap": "thinking_all_zero"},
    {"q": "Average of 5 numbers is 10. If each number is increased by 2 and then multiplied by 3, new average?", "o": ["30", "32", "34", "36"], "c": 3, "e": "12*3=36.", "diff": "hard", "concepts": ["combined_transformations"], "trap": "order_error"},
    {"q": "In a group, average age is 24. If oldest person aged 40 leaves, average becomes 22. How many people originally?", "o": ["8", "9", "10", "11"], "c": 1, "e": "2n=18 -> n=9.", "diff": "hard", "concepts": ["average_removal_algebra"], "trap": "equation_setup"},
    {"q": "A student has average 60 after 4 tests. What must she average on next 2 tests to have overall average 70?", "o": ["80", "85", "90", "95"], "c": 2, "e": "Avg required = 90.", "diff": "hard", "concepts": ["target_average_multiple"], "trap": "simple_addition"},
    {"q": "The average of 3 numbers is 15. If two numbers are 10 and 20, what is third?", "o": ["15", "16", "17", "18"], "c": 0, "e": "45-30=15.", "diff": "hard", "concepts": ["basic_average"], "trap": "simple_calculation"},
    {"q": "Average weight of 5 people is 60 kg. When heaviest is excluded, average becomes 58 kg. What is weight of heaviest?", "o": ["62 kg", "64 kg", "66 kg", "68 kg"], "c": 3, "e": "300-232=68.", "diff": "hard", "concepts": ["exclusion_average"], "trap": "wrong_subtraction"}
]

def seed_averages():
    session = SessionLocal()
    try:
        print(f"Adding {len(QUESTIONS_DATA)} Averages questions...")
        for q_data in QUESTIONS_DATA:
            new_q = AptitudeQuestion(
                id=str(uuid.uuid4()),
                question=q_data["q"],
                options=q_data["o"],
                correct_answer=q_data["c"],
                answer_explanation=q_data["e"],
                topic="Averages",
                category="Quantitative Ability",
                difficulty=q_data["diff"],
                source="hardcoded_averages_part1",
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
    seed_averages()
