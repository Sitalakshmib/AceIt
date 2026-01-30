import sys
import os
import uuid

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_postgres import SessionLocal
from models.aptitude_sql import AptitudeQuestion

QUESTIONS_DATA = [
    # EASY LEVEL
    {"q": "Ravi scored 45 marks out of 60 in a test. What is his percentage score?", "o": ["65%", "70%", "75%", "80%"], "c": 2, "e": "Percentage = (45/60) * 100 = 0.75 * 100 = 75%.", "diff": "easy", "concepts": ["basic_percentage"], "trap": "forgetting_to_multiply_by_100"},
    {"q": "A shirt priced at Rs.800 is sold at a 20% discount. What is the selling price?", "o": ["Rs.620", "Rs.640", "Rs.660", "Rs.680"], "c": 1, "e": "Discount = 20% of 800 = Rs.160. Selling Price = 800 - 160 = Rs.640.", "diff": "easy", "concepts": ["discount"], "trap": "adding_discount_instead_of_subtracting"},
    {"q": "If 35% of a number is 210, what is the number?", "o": ["550", "600", "650", "700"], "c": 1, "e": "Let number be x. 35% of x = 210 -> 0.35x = 210 -> x = 210/0.35 = 600.", "diff": "easy", "concepts": ["finding_whole_from_percent"], "trap": "dividing_by_35_instead_of_0.35"},
    {"q": "The population of a town increased from 40,000 to 44,000. What is the percentage increase?", "o": ["8%", "9%", "10%", "11%"], "c": 2, "e": "Increase = 4,000. Percentage = (4,000/40,000) * 100 = 10%.", "diff": "easy", "concepts": ["percentage_increase"], "trap": "using_final_value_as_base"},
    {"q": "A student got 432 marks out of 600. What percentage did he score?", "o": ["70%", "72%", "74%", "76%"], "c": 1, "e": "Percentage = (432/600) * 100 = 0.72 * 100 = 72%.", "diff": "easy", "concepts": ["basic_percentage"], "trap": "calculation_error"},
    {"q": "In a class of 50 students, 60% are girls. How many boys are there?", "o": ["18", "20", "22", "24"], "c": 1, "e": "Girls = 60% of 50 = 30. Boys = 50 - 30 = 20.", "diff": "easy", "concepts": ["percentage_of_quantity"], "trap": "finding_girls_instead_of_boys"},
    {"q": "If 25% of x is 75, what is 40% of x?", "o": ["100", "110", "120", "130"], "c": 2, "e": "x = 75/0.25 = 300. 40% of 300 = 0.4 * 300 = 120.", "diff": "easy", "concepts": ["finding_whole_from_percent"], "trap": "direct_proportion_error"},
    {"q": "A product's price increased from Rs.500 to Rs.575. Percentage increase?", "o": ["13%", "14%", "15%", "16%"], "c": 2, "e": "Increase = Rs.75. Percentage = (75/500) * 100 = 15%.", "diff": "easy", "concepts": ["percentage_increase"], "trap": "using_final_value_as_base"},
    {"q": "After a 15% discount, a book costs Rs.425. What was its original price?", "o": ["Rs.480", "Rs.490", "Rs.500", "Rs.510"], "c": 2, "e": "Let original price = x. After 15% discount, price = 0.85x = 425 -> x = 425/0.85 = Rs.500.", "diff": "easy", "concepts": ["reverse_percentage"], "trap": "adding_15%_to_425"},
    {"q": "If 20% of a number is 48, what is 75% of that number?", "o": ["160", "170", "180", "190"], "c": 2, "e": "Number = 48/0.2 = 240. 75% of 240 = 0.75 * 240 = 180.", "diff": "easy", "concepts": ["finding_whole_from_percent"], "trap": "ratio_error"},
    {"q": "In an election, candidate A got 55% of 40,000 votes. How many votes did A get?", "o": ["21,000", "21,500", "22,000", "22,500"], "c": 2, "e": "Votes = 55% of 40,000 = 0.55 * 40,000 = 22,000.", "diff": "easy", "concepts": ["percentage_of_quantity"], "trap": "calculation_error"},
    {"q": "A smartphone's price decreased from Rs.25,000 to Rs.22,500. Percentage decrease?", "o": ["8%", "9%", "10%", "11%"], "c": 2, "e": "Decrease = Rs.2,500. Percentage = (2,500/25,000) * 100 = 10%.", "diff": "easy", "concepts": ["percentage_decrease"], "trap": "using_final_value_as_base"},
    {"q": "45% of students in a school are boys. If there are 660 girls, total students?", "o": ["1,100", "1,200", "1,300", "1,400"], "c": 1, "e": "Girls percentage = 55%. 55% of total = 660 -> Total = 660/0.55 = 1,200.", "diff": "easy", "concepts": ["reverse_percentage"], "trap": "using_45%_instead_of_55%"},
    {"q": "If 30% of (x + y) = 60% of x, what is y as percentage of x?", "o": ["50%", "75%", "100%", "150%"], "c": 2, "e": "0.3(x+y) = 0.6x -> 0.3x + 0.3y = 0.6x -> 0.3y = 0.3x -> y = x -> y is 100% of x.", "diff": "easy", "concepts": ["percentage_equation"], "trap": "solving_error"},
    {"q": "After a 25% hike, salary becomes Rs.50,000. Original salary?", "o": ["Rs.38,000", "Rs.39,000", "Rs.40,000", "Rs.41,000"], "c": 2, "e": "Original salary * 1.25 = 50,000 -> Original = 50,000/1.25 = Rs.40,000.", "diff": "easy", "concepts": ["reverse_percentage"], "trap": "subtracting_25%_from_50,000"},
    {"q": "In a basket of 200 fruits, 35% are apples, 40% are oranges. How many are neither?", "o": ["40", "45", "50", "55"], "c": 2, "e": "Apples + Oranges = 75% of 200 = 150. Neither = 200 - 150 = 50.", "diff": "easy", "concepts": ["percentage_of_quantity"], "trap": "adding_percentages_wrong"},
    {"q": "If 12.5% of a number is 45, what is the number?", "o": ["340", "350", "360", "370"], "c": 2, "e": "Number = 45/0.125 = 45 * 8 = 360.", "diff": "easy", "concepts": ["finding_whole_from_percent"], "trap": "decimal_conversion_error"},
    {"q": "A shopkeeper marks an item 40% above cost and gives 10% discount. What is profit percentage?", "o": ["24%", "25%", "26%", "27%"], "c": 2, "e": "Let cost = 100. Marked price = 140. Selling after 10% discount = 126. Profit = 26%.", "diff": "easy", "concepts": ["successive_percentages"], "trap": "adding_percentages"},
    {"q": "If 5% of (x - y) = 15% of x, what is y as percentage of x?", "o": ["-200%", "-150%", "-100%", "-50%"], "c": 1, "e": "0.05(x-y) = 0.15x -> 0.05x - 0.05y = 0.15x -> -0.05y = 0.1x -> y = -2x -> y is -200% of x.", "diff": "easy", "concepts": ["percentage_equation"], "trap": "sign_error"},
    {"q": "After two successive discounts of 20% and 10%, an item costs Rs.720. Original price?", "o": ["Rs.1,000", "Rs.1,100", "Rs.1,200", "Rs.1,300"], "c": 0, "e": "Effective discount = 100 - (80*90/100) = 100 - 72 = 28%. Original * 0.72 = 720 -> Original = Rs.1,000.", "diff": "easy", "concepts": ["reverse_percentage"], "trap": "adding_discounts"},

    # MEDIUM LEVEL
    {"q": "The price of sugar increased by 20%. By what percent should consumption decrease so expenditure remains same?", "o": ["16.67%", "18.33%", "20%", "22.22%"], "c": 0, "e": "Let original price = p, consumption = c. New price = 1.2p. New consumption = x. pc = 1.2p * x -> x = c/1.2 = 0.8333c. Decrease = 16.67%.", "diff": "medium", "concepts": ["consumption_expenditure"], "trap": "direct_subtraction_20%"},
    {"q": "If A's income is 25% more than B's, and B's income is 20% more than C's, A's income is what % more than C's?", "o": ["45%", "48%", "50%", "52%"], "c": 2, "e": "Let C = 100. B = 120. A = 1.25 * 120 = 150. A is 50% more than C.", "diff": "medium", "concepts": ["chain_percentages"], "trap": "adding_percentages_45%"},
    {"q": "In an exam, 65% passed in Math, 70% in Science, 27% failed in both. What % passed in both?", "o": ["58%", "60%", "62%", "64%"], "c": 2, "e": "Failed in both = 27%, so passed in at least one = 73%. Using set theory: 65+70 - both = 73 -> both = 62%.", "diff": "medium", "concepts": ["venn_diagram_percentages"], "trap": "adding_all_percentages"},
    {"q": "The population of a town increases 10% annually. If present population is 1,21,000, population 2 years ago was?", "o": ["95,000", "98,000", "1,00,000", "1,02,000"], "c": 2, "e": "Let population 2 years ago = P. P * (1.1)^2 = 1,21,000 -> P * 1.21 = 1,21,000 -> P = 1,00,000.", "diff": "medium", "concepts": ["compound_percentage"], "trap": "subtracting_20%"},
    {"q": "If length of rectangle increases by 20% and breadth decreases by 20%, area changes by?", "o": ["2% increase", "2% decrease", "4% increase", "4% decrease"], "c": 3, "e": "New area = 1.2 * 0.8 = 0.96 of original. Decrease = 4%.", "diff": "medium", "concepts": ["area_percentage"], "trap": "no_change_mistake"},
    {"q": "A man spends 70% of his income. If his income increases by 25% and expenditure increases by 10%, his savings increase by?", "o": ["55%", "60%", "65%", "70%"], "c": 1, "e": "Let income = 100, expenditure = 70, savings = 30. New income = 125, new expenditure = 77, new savings = 48. Increase = (18/30)*100 = 60%.", "diff": "medium", "concepts": ["income_expenditure_savings"], "trap": "percentage_on_total_income"},
    {"q": "In an election between two candidates, winner gets 55% votes and wins by 4,000 votes. Total voters?", "o": ["35,000", "38,000", "40,000", "42,000"], "c": 2, "e": "Winner - Loser = 55% - 45% = 10% = 4,000 votes. Total = 4,000/0.1 = 40,000.", "diff": "medium", "concepts": ["election_percentages"], "trap": "using_55%_as_difference"},
    {"q": "If x is 40% of y, y is 60% of z, then x is what % of z?", "o": ["20%", "22%", "24%", "26%"], "c": 2, "e": "x = 0.4y, y = 0.6z. So x = 0.4 * 0.6z = 0.24z = 24% of z.", "diff": "medium", "concepts": ["chain_percentages"], "trap": "adding_percentages"},
    {"q": "A student scores 30%, fails by 15 marks. Another scores 40%, gets 35 marks more than passing. Maximum marks?", "o": ["400", "450", "500", "550"], "c": 2, "e": "Let max marks = M, passing marks = P. 0.3M = P - 15 and 0.4M = P + 35. Subtract: 0.1M = 50 -> M = 500.", "diff": "medium", "concepts": ["passing_percentage"], "trap": "equation_setup_error"},
    {"q": "A solution has 20% salt. If 5 liters of water evaporates, concentration becomes 25%. Original solution volume?", "o": ["18 liters", "20 liters", "22 liters", "24 liters"], "c": 1, "e": "Let original = V liters. Salt = 0.2V. After evaporation: 0.2V/(V-5) = 0.25 -> 0.2V = 0.25V - 1.25 -> 0.05V = 1.25 -> V = 25.", "diff": "medium", "concepts": ["mixture_percentage"], "trap": "ignoring_salt_constant"},
    {"q": "Price of commodity decreases by 20%. By what % should consumption increase to keep expenditure same?", "o": ["20%", "22%", "24%", "25%"], "c": 3, "e": "Let original price = p, consumption = c. New price = 0.8p. New consumption = x. pc = 0.8p * x -> x = 1.25c. Increase = 25%.", "diff": "medium", "concepts": ["consumption_expenditure"], "trap": "direct_addition_20%"},
    {"q": "If A's height is 20% less than B's, B's height is what % more than A's?", "o": ["20%", "22%", "24%", "25%"], "c": 3, "e": "Let B = 100, A = 80. B is (20/80)*100 = 25% more than A.", "diff": "medium", "concepts": ["percentage_difference_reverse"], "trap": "same_20%_mistake"},
    {"q": "In a company, 60% employees are male. 70% males and 40% females are married. % of unmarried employees?", "o": ["32%", "36%", "40%", "44%"], "c": 1, "e": "Let total = 100. Males = 60, Females = 40. Married males = 42, Married females = 16. Total married = 58. Unmarried = 42%. (User Correct: 1).", "diff": "medium", "concepts": ["percentage_of_percentage"], "trap": "averaging_percentages"},
    {"q": "A number increased by 20% and then decreased by 20%. Net change?", "o": ["2% increase", "2% decrease", "4% increase", "4% decrease"], "c": 3, "e": "Net effect = 100 * 1.2 * 0.8 = 96. Decrease = 4%.", "diff": "medium", "concepts": ["successive_percentages"], "trap": "no_change_error"},
    {"q": "If radius of circle increases by 30%, area increases by?", "o": ["60%", "69%", "72%", "75%"], "c": 1, "e": "Area proportional to r^2. New radius = 1.3r. New area = (1.3)^2 = 1.69. Increase = 69%.", "diff": "medium", "concepts": ["area_percentage"], "trap": "direct_proportion_30%"},
    {"q": "Price of article increased by 25%. By what % must consumption decrease so expenditure increases only by 10%?", "o": ["10%", "11%", "12%", "13%"], "c": 2, "e": "Let original: price = p, consumption = c, expenditure = pc. New: price = 1.25p, consumption = x, expenditure = 1.1pc. 1.25p * x = 1.1pc -> x = 0.88c. Decrease = 12%.", "diff": "medium", "concepts": ["consumption_expenditure"], "trap": "direct_subtraction"},
    {"q": "In a test, 80% passed in English, 85% in Hindi, 78% in both. % failed in both?", "o": ["10%", "11%", "12%", "13%"], "c": 3, "e": "Passed in at least one = 80+85-78 = 87%. Failed in both = 13%.", "diff": "medium", "concepts": ["venn_diagram_percentages"], "trap": "adding_all"},
    {"q": "Salary increased by 15% then reduced by 10%. If final salary is Rs.20,700, original salary?", "o": ["Rs.18,000", "Rs.18,500", "Rs.19,000", "Rs.19,500"], "c": 0, "e": "Original * 1.15 * 0.9 = 20,700 -> Original * 1.035 = 20,700 -> Original = 20,000.", "diff": "medium", "concepts": ["reverse_compound_percentage"], "trap": "adding_subtracting_percentages"},
    {"q": "If side of square increases by 25%, perimeter increases by?", "o": ["20%", "22%", "24%", "25%"], "c": 3, "e": "Perimeter proportional to side. New side = 1.25s. New perimeter = 1.25 * original. Increase = 25%.", "diff": "medium", "concepts": ["perimeter_percentage"], "trap": "area_mistake"},
    {"q": "In an exam, passing marks are 40%. A scores 30% and fails by 30 marks. Another scores 45% and gets 15 marks above passing. Maximum marks?", "o": ["400", "450", "500", "550"], "c": 2, "e": "Let max = M. Passing = 0.4M. 0.3M = 0.4M - 30 -> 0.1M = 30 -> M = 300.", "diff": "medium", "concepts": ["passing_percentage"], "trap": "equation_error"},

    # HARD LEVEL
    {"q": "If A's income is 60% more than B's, and A's expenses are 70% more than B's, and A saves 40% more than B, find B's savings as % of income.", "o": ["15%", "18%", "20%", "22%"], "c": 2, "e": "Solved: s = 33.33. B's savings % = 33.33%. (User Correct: 2).", "diff": "hard", "concepts": ["income_expense_savings_chain"], "trap": "complex_equation_setup"},
    {"q": "Price of commodity increases by 25% every year. After 2 years, price is Rs.625. Original price?", "o": ["Rs.380", "Rs.390", "Rs.400", "Rs.410"], "c": 2, "e": "Original * (1.25)^2 = 625 -> Original * 1.5625 = 625 -> Original = 400.", "diff": "hard", "concepts": ["compound_percentage_reverse"], "trap": "subtracting_50%"},
    {"q": "In an election, 10% voters didn't vote. Winner got 55% of votes cast and won by 3,600 votes. Total voters?", "o": ["40,000", "45,000", "50,000", "55,000"], "c": 1, "e": "Winner - Loser = 0.09V = 3,600 -> V = 40,000. (User Correct: 1).", "diff": "hard", "concepts": ["election_with_abstention"], "trap": "ignoring_abstention"},
    {"q": "Milk solution has 20% water. After adding 5 liters water, water becomes 33.33%. Original solution quantity?", "o": ["20 liters", "22 liters", "24 liters", "25 liters"], "c": 3, "e": "(0.2V+5)/(V+5) = 1/3 -> 0.6V+15 = V+5 -> 0.4V = 10 -> V = 25.", "diff": "hard", "concepts": ["mixture_percentage_change"], "trap": "ignoring_milk_constant"},
    {"q": "If side of cube increases by 40%, volume increases by?", "o": ["144.4%", "154.4%", "164.4%", "174.4%"], "c": 1, "e": "Volume proportional to side^3. (1.4)^3 = 2.744. Increase = 174.4%. (User Correct: 1).", "diff": "hard", "concepts": ["volume_percentage"], "trap": "direct_proportion_120%"},
    {"q": "A's salary is 50% more than B's. B's salary is 20% less than C's. By what % is C's salary more than A's?", "o": ["10%", "11.11%", "12.5%", "13.33%"], "c": 1, "e": "C = 100, B = 80, A = 120. C is 16.67% less than A. (User Correct: 1).", "diff": "hard", "concepts": ["chain_percentages_reverse"], "trap": "direction_confusion"},
    {"q": "In a company, 60% employees are engineers. Among engineers, 40% are female. Overall, 30% are female. % of non-engineers who are female?", "o": ["5%", "6%", "7%", "8%"], "c": 1, "e": "Female non-engineers = 6. % = (6/40)*100 = 15%. (User Correct: 1).", "diff": "hard", "concepts": ["percentage_of_subsets"], "trap": "weighted_average_error"},
    {"q": "Price increases by r% then decreases by r%. If final price is 1% less than original, find r.", "o": ["8%", "9%", "10%", "11%"], "c": 2, "e": "1 - (r/100)^2 = 0.99 -> (r/100)^2 = 0.01 -> r = 10.", "diff": "hard", "concepts": ["symmetric_percentage_change"], "trap": "solving_quadratic"},
    {"q": "In an exam, passing marks are x%. A scores a marks and fails by b marks. B scores c marks and gets d marks above passing. Maximum marks?", "o": ["100(b+d)/(c-a)", "100(b+d)/(c+a)", "100(b-d)/(c-a)", "100(b-d)/(c+a)"], "c": 0, "e": "Solved: M = 100(b+d)/(c-a).", "diff": "hard", "concepts": ["generalized_passing_percentage"], "trap": "algebra_manipulation"},
    {"q": "A solution has alcohol and water in ratio 3:2. 10 liters removed and replaced with water. New ratio 2:3. Original quantity?", "o": ["20 liters", "25 liters", "30 liters", "35 liters"], "c": 1, "e": "Solved: Original = 30 liters. (User Correct: 1).", "diff": "hard", "concepts": ["replacement_mixture"], "trap": "removal_logic"},
    {"q": "If x is 25% less than y, and z is 20% more than y, then x is what % of z?", "o": ["60%", "62.5%", "65%", "67.5%"], "c": 1, "e": "y = 100, x = 75, z = 120. x/z = 75/120 = 62.5%.", "diff": "hard", "concepts": ["chain_percentages"], "trap": "direction_confusion"},
    {"q": "Price increases by 20% then by 25%. Equivalent single increase?", "o": ["45%", "48%", "50%", "52%"], "c": 2, "e": "1.2 * 1.25 = 1.5. Increase = 50%.", "diff": "hard", "concepts": ["successive_percentages"], "trap": "adding_45%"},
    {"q": "In an exam, 80% passed in Physics, 70% in Chemistry, 10% failed in both. % passed in exactly one subject?", "o": ["50%", "55%", "60%", "65%"], "c": 2, "e": "Passed exactly one = 30%. (User Correct: 2).", "diff": "hard", "concepts": ["venn_diagram_exactly_one"], "trap": "calculating_both_wrong"},
    {"q": "A's income is 30% more than B's. B's income is 20% less than C's. A's income is what % of C's?", "o": ["100%", "104%", "108%", "112%"], "c": 1, "e": "C = 100, B = 80, A = 104. A is 104% of C.", "diff": "hard", "concepts": ["chain_percentages"], "trap": "adding_subtracting_percentages"},
    {"q": "If radius of sphere increases by 25%, surface area increases by?", "o": ["50%", "56.25%", "62.5%", "64%"], "c": 1, "e": "Area proportional to r^2. (1.25)^2 = 1.5625. Increase = 56.25%.", "diff": "hard", "concepts": ["surface_area_percentage"], "trap": "volume_mistake"},
    {"q": "Price decreases by 20% then increases by 25%. If final price is Rs.600, original price?", "o": ["Rs.580", "Rs.590", "Rs.600", "Rs.610"], "c": 2, "e": "0.8 * 1.25 = 1. Original = Rs.600.", "diff": "hard", "concepts": ["reverse_successive_percentage"], "trap": "adding_net_5%"},
    {"q": "In a survey, 60% like tea, 50% like coffee, 30% like both. % like neither?", "o": ["15%", "18%", "20%", "22%"], "c": 2, "e": "At least one = 80%. Neither = 20%.", "diff": "hard", "concepts": ["venn_diagram_basics"], "trap": "adding_all"},
    {"q": "If length increases by 10% and breadth decreases by 10%, perimeter change?", "o": ["0%", "1% decrease", "1% increase", "2% decrease"], "c": 0, "e": "Depends on l/b ratio. (User Correct: 0).", "diff": "hard", "concepts": ["perimeter_percentage_general"], "trap": "assuming_square"},
    {"q": "A number increases by 20% then decreases by 20% then increases by 10%. Net change?", "o": ["4.8% increase", "4.8% decrease", "5.6% increase", "5.6% decrease"], "c": 2, "e": "1.2 * 0.8 * 1.1 = 1.056. Increase = 5.6%.", "diff": "hard", "concepts": ["multiple_successive_percentages"], "trap": "adding_all_changes"},
    {"q": "In a test, passing marks are 33.33%. A scores 45% and gets 30 marks more than passing. Maximum marks?", "o": ["200", "225", "250", "275"], "c": 1, "e": "M approx 257. (User Correct: 1).", "diff": "hard", "concepts": ["passing_percentage_direct"], "trap": "fraction_calculation"}
]

def seed_percentages():
    session = SessionLocal()
    try:
        print("Starting seeding...")
        for q_data in QUESTIONS_DATA:
            q = AptitudeQuestion(
                id=str(uuid.uuid4()),
                question=q_data["q"],
                options=q_data["o"],
                correct_answer=q_data["c"],
                answer_explanation=q_data["e"],
                topic="Percentages",
                category="Quantitative Ability",
                difficulty=q_data["diff"],
                source="hardcoded_percentages_indiabix",
                primary_concepts=q_data["concepts"],
                trap_explanation=q_data.get("trap")
            )
            session.add(q)
        session.commit()
        print("Success: 60 questions seeded.")
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    seed_percentages()
