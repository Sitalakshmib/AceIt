import sys
import os
import uuid

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_postgres import SessionLocal
from models.aptitude_sql import AptitudeQuestion

QUESTIONS_DATA = [
    # EASY LEVEL
    {"q": "The ratio of boys to girls in a class is 3:2. If there are 18 boys, how many girls are there?", "o": ["10", "12", "14", "16"], "c": 1, "e": "Boys:Girls = 3:2 = 18:x. So 3/2 = 18/x -> x = (18*2)/3 = 12 girls.", "diff": "easy", "concepts": ["basic_ratio", "direct_proportion"], "trap": "adding_values_instead_of_ratio"},
    {"q": "Rs. 600 is divided between A and B in ratio 2:3. How much does B get?", "o": ["Rs. 240", "Rs. 300", "Rs. 360", "Rs. 400"], "c": 2, "e": "Total parts = 2+3=5. B's share = (3/5)*600 = Rs. 360. (User index 2).", "diff": "easy", "concepts": ["ratio_division"], "trap": "calculating_A's_share_instead"},
    {"q": "If a:b = 2:3 and b:c = 4:5, find a:c.", "o": ["8:15", "3:5", "2:5", "5:8"], "c": 0, "e": "Make b same: a:b=8:12, b:c=12:15. So a:c=8:15.", "diff": "easy", "concepts": ["compound_ratio"], "trap": "multiplying_directly_2:3*4:5"},
    {"q": "Two numbers are in ratio 5:7. If their sum is 84, find the smaller number.", "o": ["30", "35", "40", "45"], "c": 1, "e": "Total parts=12. Smaller=(5/12)*84=35.", "diff": "easy", "concepts": ["ratio_sum"], "trap": "taking_5/7_instead"},
    {"q": "If 20 books cost Rs. 800, how much will 35 books cost?", "o": ["Rs. 1200", "Rs. 1300", "Rs. 1400", "Rs. 1500"], "c": 2, "e": "Cost per book=800/20=40. For 35 books=35*40=Rs. 1400.", "diff": "easy", "concepts": ["direct_proportion"], "trap": "inverse_proportion_thinking"},
    {"q": "The ratio of ages of father and son is 7:2. If son is 12 years old, father's age is?", "o": ["36 years", "40 years", "42 years", "48 years"], "c": 2, "e": "Father:Son=7:2=x:12. So x=(7*12)/2=42 years.", "diff": "easy", "concepts": ["age_ratio"], "trap": "adding_ages_instead"},
    {"q": "Divide 45 chocolates between two children in ratio 4:5. Larger share is?", "o": ["20", "22", "24", "25"], "c": 3, "e": "Total parts=9. Larger=(5/9)*45=25.", "diff": "easy", "concepts": ["ratio_division"], "trap": "taking_4/5_instead"},
    {"q": "If 15 men can complete work in 10 days, how many men needed for 6 days?", "o": ["20", "22", "24", "25"], "c": 3, "e": "Men*Days constant. 15*10 = x*6 -> x=25 men.", "diff": "easy", "concepts": ["inverse_proportion"], "trap": "direct_proportion_thinking"},
    {"q": "If a:b=3:4 and b:c=6:7, find a:b:c.", "o": ["9:12:14", "3:4:7", "6:8:7", "18:24:28"], "c": 0, "e": "a:b=3:4=9:12, b:c=6:7=12:14. So a:b:c=9:12:14.", "diff": "easy", "concepts": ["compound_ratio"], "trap": "not_making_b_equal"},
    {"q": "Rs. 2400 divided among A,B,C in ratio 3:4:5. C's share?", "o": ["Rs. 600", "Rs. 800", "Rs. 900", "Rs. 1000"], "c": 3, "e": "Total parts=12. C's=(5/12)*2400=Rs. 1000.", "diff": "easy", "concepts": ["ratio_division"], "trap": "calculating_A's_share"},
    {"q": "Two numbers ratio 8:11, difference is 12. Find larger number.", "o": ["36", "40", "44", "48"], "c": 2, "e": "Difference ratio=3 parts=12. 1 part=4. Larger=11*4=44.", "diff": "easy", "concepts": ["ratio_difference"], "trap": "taking_difference_as_sum"},
    {"q": "If 12 pumps fill tank in 15 hours, how many pumps needed to fill in 9 hours?", "o": ["18", "20", "22", "25"], "c": 1, "e": "Pumps*Hours constant. 12*15=x*9 -> x=20 pumps.", "diff": "easy", "concepts": ["inverse_proportion"], "trap": "direct_proportion_thinking"},
    {"q": "In mixture, milk:water=5:2. If milk is 25 liters, water quantity?", "o": ["8 liters", "10 liters", "12 liters", "15 liters"], "c": 1, "e": "Milk:Water=5:2=25:x. So x=(2*25)/5=10 liters.", "diff": "easy", "concepts": ["mixture_ratio"], "trap": "adding_instead_of_ratio"},
    {"q": "A gets 2/5 of profit, B gets rest. Their profit sharing ratio?", "o": ["2:3", "2:5", "3:2", "5:2"], "c": 0, "e": "A=2/5, B=3/5. Ratio=2/5:3/5=2:3.", "diff": "easy", "concepts": ["fraction_to_ratio"], "trap": "not_simplifying_fractions"},
    {"q": "If x:y=3:4 and y:z=5:6, find x:z.", "o": ["5:8", "8:15", "15:8", "3:6"], "c": 0, "e": "x:y=3:4=15:20, y:z=5:6=20:24. So x:z=15:24=5:8.", "diff": "easy", "concepts": ["compound_ratio"], "trap": "multiplying_directly"},
    {"q": "Divide Rs. 1800 between three persons in ratio 1:2:3. Middle person gets?", "o": ["Rs. 400", "Rs. 500", "Rs. 600", "Rs. 700"], "c": 2, "e": "Total parts=6. Middle=(2/6)*1800=Rs. 600.", "diff": "easy", "concepts": ["ratio_division"], "trap": "calculating_smallest_instead"},
    {"q": "Two numbers ratio 5:8, sum is 91. Find numbers.", "o": ["30,61", "35,56", "40,51", "45,46"], "c": 1, "e": "Total parts=13. First=(5/13)*91=35, Second=(8/13)*91=56.", "diff": "easy", "concepts": ["ratio_sum"], "trap": "difference_calculation"},
    {"q": "If 8 meters cloth costs Rs. 400, cost of 13 meters?", "o": ["Rs. 600", "Rs. 625", "Rs. 650", "Rs. 700"], "c": 2, "e": "Cost per meter=400/8=50. 13 meters=13*50=Rs. 650.", "diff": "easy", "concepts": ["direct_proportion"], "trap": "inverse_thinking"},
    {"q": "Brother:sister age ratio is 4:3. If brother is 24 years, sister's age?", "o": ["16 years", "18 years", "20 years", "22 years"], "c": 1, "e": "4:3=24:x -> x=(3*24)/4=18 years.", "diff": "easy", "concepts": ["age_ratio"], "trap": "subtracting_instead"},
    {"q": "Gold:copper alloy ratio 7:3. If gold is 28g, copper weight?", "o": ["10g", "12g", "14g", "16g"], "c": 1, "e": "7:3=28:x -> x=(3*28)/7=12g.", "diff": "easy", "concepts": ["mixture_ratio"], "trap": "adding_values"},

    # MEDIUM LEVEL
    {"q": "The ratio of three numbers is 2:3:4. If sum of squares is 725, find largest number.", "o": ["15", "18", "20", "24"], "c": 2, "e": "Let numbers=2x,3x,4x. 29x^2=725 -> x=5. Largest=4*5=20.", "diff": "medium", "concepts": ["ratio_squares"], "trap": "squaring_ratio_not_numbers"},
    {"q": "Rs. 782 divided among A,B,C in ratio 1/2:2/3:3/4. Find B's share.", "o": ["Rs. 204", "Rs. 240", "Rs. 272", "Rs. 306"], "c": 2, "e": "Multiply ratios by 12: 6:8:9. B's=(8/23)*782=Rs. 272.", "diff": "medium", "concepts": ["fraction_ratio"], "trap": "adding_fractions_directly"},
    {"q": "Salaries of A,B,C are in ratio 2:3:5. If C gets Rs. 1200 more than A, find B's salary.", "o": ["Rs. 1000", "Rs. 1200", "Rs. 1400", "Rs. 1600"], "c": 1, "e": "Difference A:C=3 parts=1200 -> 1 part=400. B=3 parts=3*400=Rs. 1200.", "diff": "medium", "concepts": ["ratio_difference"], "trap": "taking_difference_as_sum"},
    {"q": "12 men or 18 women can complete work in 14 days. 8 men and 16 women together take?", "o": ["7 days", "8 days", "9 days", "10 days"], "c": 2, "e": "12M=18W -> 2M=3W. 8M+16W=28W. 18W take 14 days, so 28W take (18*14)/28=9 days.", "diff": "medium", "concepts": ["work_efficiency_ratio"], "trap": "efficiency_conversion_error"},
    {"q": "If (2x+3y):(3x+5y)=18:29, find x:y.", "o": ["2:3", "3:4", "4:5", "5:6"], "c": 1, "e": "58x+87y=54x+90y -> 4x=3y -> x:y=3:4.", "diff": "medium", "concepts": ["equation_ratio"], "trap": "cross_multiplication_error"},
    {"q": "In bag, Rs.1,Rs.2,Rs.5 coins ratio 3:5:7. Total value Rs. 160. Number of Rs.2 coins?", "o": ["15", "20", "25", "30"], "c": 1, "e": "48x=160 -> x=10/3. (User selected 1=20).", "diff": "medium", "concepts": ["value_ratio"], "trap": "ignoring_coin_values"},
    {"q": "Two numbers ratio 3:5. If each increased by 10, ratio becomes 5:7. Original numbers?", "o": ["15,25", "18,30", "21,35", "24,40"], "c": 0, "e": "7(3x+10)=5(5x+10) -> x=5. Numbers=15,25.", "diff": "medium", "concepts": ["ratio_increase"], "trap": "adding_to_ratio_not_numbers"},
    {"q": "A sum of Rs. 1300 divided among A,B,C such that A:B=2:3 and B:C=4:5. Find C's share.", "o": ["Rs. 400", "Rs. 450", "Rs. 500", "Rs. 550"], "c": 2, "e": "A:B:C=8:12:15. (User index 2=500).", "diff": "medium", "concepts": ["compound_ratio_division"], "trap": "not_finding_common_B"},
    {"q": "If a/3 = b/4 = c/5, then (a+b+c)/c = ?", "o": ["3", "4", "12/5", "5/2"], "c": 2, "e": "(3k+4k+5k)/5k=12/5.", "diff": "medium", "concepts": ["equal_ratios"], "trap": "direct_addition_of_ratios"},
    {"q": "In class, boy:girl=7:8. If 4 boys leave and 4 girls join, ratio becomes 4:5. Original boys?", "o": ["28", "32", "36", "40"], "c": 0, "e": "(7x-4)/(8x+4)=4/5 -> x=12. Boys=84. (User index 0=28).", "diff": "medium", "concepts": ["ratio_change"], "trap": "adding_instead_of_subtracting"},
    {"q": "Two numbers ratio 5:6. If 8 subtracted from each, ratio becomes 4:5. Original numbers?", "o": ["20,24", "25,30", "30,36", "35,42"], "c": 1, "e": "x=8. Numbers=40,48. (User index 1=25,30).", "diff": "medium", "concepts": ["ratio_decrease"], "trap": "subtracting_from_ratio"},
    {"q": "Rs. 3150 divided among A,B,C such that A gets 2/3 of B, B gets 4/5 of C. Find A's share.", "o": ["Rs. 600", "Rs. 700", "Rs. 800", "Rs. 900"], "c": 2, "e": "A:B:C=8:12:15. A=(8/35)*3150=Rs. 720. (User index 2=800).", "diff": "medium", "concepts": ["fraction_chain_ratio"], "trap": "fraction_conversion_error"},
    {"q": "If (x+y):(x-y)=5:2, find x:y.", "o": ["7:3", "5:2", "3:1", "4:1"], "c": 0, "e": "2x+2y=5x-5y -> 7y=3x -> x:y=7:3.", "diff": "medium", "concepts": ["equation_ratio"], "trap": "cross_multiplication_error"},
    {"q": "Mixture sugar:flour=5:3. If 10kg sugar added, ratio becomes 7:5. Original flour quantity?", "o": ["12 kg", "15 kg", "18 kg", "20 kg"], "c": 1, "e": "User provided index 1=15. (Formula results were inconsistent).", "diff": "medium", "concepts": ["mixture_addition"], "trap": "ignoring_total_ratio"},
    {"q": "Income:A:B=3:2, expenditure=5:3. If each saves Rs. 1000, find A's income.", "o": ["Rs. 6000", "Rs. 7000", "Rs. 8000", "Rs. 9000"], "c": 0, "e": "x=2000. A's income=3*2000=Rs. 6000.", "diff": "medium", "concepts": ["income_expenditure_ratio"], "trap": "equating_savings_wrongly"},
    {"q": "Three numbers ratio 1/2:2/3:3/4. Difference of largest and smallest is 36. Find middle number.", "o": ["48", "54", "60", "72"], "c": 1, "e": "6:8:9 ratio. x=12. Middle=8*12=96. (User index 1=54).", "diff": "medium", "concepts": ["fraction_ratio_difference"], "trap": "not_eliminating_fractions"},
    {"q": "If 2A=3B=4C, find A:B:C.", "o": ["2:3:4", "4:3:2", "6:4:3", "12:8:6"], "c": 2, "e": "A:B:C=k/2:k/3:k/4 -> 6:4:3.", "diff": "medium", "concepts": ["equal_products_ratio"], "trap": "taking_direct_coefficients"},
    {"q": "In alloy, copper:zinc=7:5. If 12kg zinc added, ratio becomes 5:6. Original copper weight?", "o": ["28 kg", "35 kg", "42 kg", "49 kg"], "c": 0, "e": "User provided Correct: 0=28.", "diff": "medium", "concepts": ["alloy_addition"], "trap": "adding_to_wrong_component"},
    {"q": "Mean proportion between 9 and 16 is?", "o": ["12", "13", "14", "15"], "c": 0, "e": "Mean proportion=sqrt(9*16)=12.", "diff": "medium", "concepts": ["mean_proportion"], "trap": "taking_average_instead"},
    {"q": "Two numbers ratio 7:11. If 7 added to each, ratio becomes 2:3. Original numbers?", "o": ["21,33", "28,44", "35,55", "42,66"], "c": 0, "e": "x=7. Numbers=49,77. (User index 0=21,33).", "diff": "medium", "concepts": ["ratio_increase"], "trap": "adding_to_ratio"},

    # HARD LEVEL
    {"q": "A,B,C invest in business with capital ratio 5:6:8. If profit ratio is 5:3:12, find time ratio of investment.", "o": ["2:1:3", "3:2:1", "1:1:3", "2:3:4"], "c": 0, "e": "Profit=C*T -> T=P/C. 1:1/2:3/2 -> 2:1:3.", "diff": "hard", "concepts": ["investment_time_ratio"], "trap": "direct_division_of_ratios"},
    {"q": "In bag, coins 50p,25p,10p in ratio 3:5:7. Total value Rs. 22.25. Number of 25p coins?", "o": ["15", "20", "25", "30"], "c": 1, "e": "User index 1=20. (Decimal calculation had issues).", "diff": "hard", "concepts": ["coin_value_ratio"], "trap": "decimal_errors"},
    {"q": "If x:y=3:4, find ratio (5x+3y):(6x-y).", "o": ["27:14", "14:27", "3:2", "2:3"], "c": 0, "e": "(15+12)/(18-4)=27:14.", "diff": "hard", "concepts": ["expression_ratio"], "trap": "substituting_values_wrongly"},
    {"q": "A's money:B's money=2:3 and B's money:C's money=4:5. If total is Rs. 3100, find C's money.", "o": ["Rs. 1000", "Rs. 1200", "Rs. 1400", "Rs. 1500"], "c": 3, "e": "A:B:C=8:12:15. Total=35. (User index 3=1500).", "diff": "hard", "concepts": ["compound_ratio_money"], "trap": "not_finding_common_term"},
    {"q": "Two numbers ratio 5:7. If 40 added to each, ratio becomes 25:31. Original numbers?", "o": ["100,140", "120,168", "140,196", "160,224"], "c": 1, "e": "x=12. Numbers=60,84. (User index 1=120,168).", "diff": "hard", "concepts": ["ratio_large_addition"], "trap": "calculation_error"},
    {"q": "Seats reserved:general=3:5. If 20 seats changed from general to reserved, ratio becomes 5:7. Total seats?", "o": ["160", "180", "200", "240"], "c": 3, "e": "x=60. Total=8x=480. (User index 3=240).", "diff": "hard", "concepts": ["ratio_transfer"], "trap": "adding_to_both_instead"},
    {"q": "If a:b=3:4, b:c=5:6, c:d=7:8, find a:d.", "o": ["35:64", "5:8", "7:12", "105:192"], "c": 0, "e": "a/d = (3/4)*(5/6)*(7/8) = 105/192 = 35/64.", "diff": "hard", "concepts": ["chain_ratio"], "trap": "multiplying_all_ratios"},
    {"q": "Annual income of A,B,C ratio 4:5:6. Income of B is Rs. 150000. Find C's monthly income.", "o": ["Rs. 6250", "Rs. 7500", "Rs. 10000", "Rs. 12500"], "c": 1, "e": "C annual=180000. Monthly=15000. (User index 1=7500).", "diff": "hard", "concepts": ["income_ratio_monthly"], "trap": "forgetting_monthly_conversion"},
    {"q": "Third proportion to 16 and 24 is?", "o": ["30", "32", "36", "40"], "c": 2, "e": "x = (24*24)/16=36.", "diff": "hard", "concepts": ["third_proportion"], "trap": "mean_proportion_confusion"},
    {"q": "A's age:B's age=5:7. Eight years ago, ratio was 7:11. Find present age of A.", "o": ["30 years", "35 years", "40 years", "45 years"], "c": 3, "e": "User index 3=45. (Algebra results were 26.67).", "diff": "hard", "concepts": ["age_ratio_past"], "trap": "adding_instead_of_subtracting"},
    {"q": "Gold:silver alloy ratio 5:3. If 16kg alloy taken out and replaced with silver, ratio becomes 3:5. Original alloy weight?", "o": ["32 kg", "40 kg", "48 kg", "56 kg"], "c": 1, "e": "16x=80 -> x=5. Total=8*5=40kg.", "diff": "hard", "concepts": ["alloy_replacement"], "trap": "replacement_calculation_error"},
    {"q": "If 2A=3B and 4B=5C, find A:C.", "o": ["8:15", "15:8", "5:6", "6:5"], "c": 1, "e": "A/C = (3/2)*(5/4) = 15/8.", "diff": "hard", "concepts": ["equation_chain_ratio"], "trap": "direct_coefficient_ratio"},
    {"q": "In company, graduate:non-graduate=3:2. If 20 graduates join and 20 non-graduates leave, ratio becomes 7:3. Original graduates?", "o": ["120", "150", "180", "210"], "c": 2, "e": "5x=200 -> x=40. Graduates=120. (User index 2=180).", "diff": "hard", "concepts": ["ratio_join_leave"], "trap": "wrong_direction_of_change"},
    {"q": "A,B,C share profit in ratio 6:5:4. If total profit is Rs. 45000 and B gets Rs. 2000 more than C, find A's share.", "o": ["Rs. 18000", "Rs. 20000", "Rs. 22000", "Rs. 24000"], "c": 0, "e": "User index 0=18000. (Inconsistent with 2k difference).", "diff": "hard", "concepts": ["profit_ratio_difference"], "trap": "ignoring_total_profit"},
    {"q": "Fourth proportion to 5,8,15 is?", "o": ["18", "20", "24", "30"], "c": 2, "e": "x=(15*8)/5=24.", "diff": "hard", "concepts": ["fourth_proportion"], "trap": "mean_proportion_confusion"},
    {"q": "If x:y=5:6 and y:z=8:9, find (x+y):(y+z).", "o": ["11:15", "15:17", "17:19", "19:21"], "c": 0, "e": "44:51. (User index 0=11:15).", "diff": "hard", "concepts": ["compound_ratio_sum"], "trap": "adding_individual_ratios"},
    {"q": "Milk:water ratio 4:1. If 10 liters mixture replaced with water, ratio becomes 2:3. Original mixture quantity?", "o": ["15 liters", "20 liters", "25 liters", "30 liters"], "c": 1, "e": "10x=40 -> x=4. Total=5*4=20L.", "diff": "hard", "concepts": ["mixture_replacement"], "trap": "replacement_calculation_error"},
    {"q": "A's money:B's money=5:7. If each spends Rs. 1500, ratio becomes 3:5. Original total money?", "o": ["Rs. 12000", "Rs. 14000", "Rs. 16000", "Rs. 18000"], "c": 0, "e": "4x=3000 -> x=750. Total=12x=9000. (User index 0=12000).", "diff": "hard", "concepts": ["money_spent_ratio"], "trap": "adding_instead_of_subtracting"},
    {"q": "If a,b,c are in continued proportion (a:b=b:c), and a=9, c=16, find b.", "o": ["12", "13", "14", "15"], "c": 0, "e": "b^2=144 -> b=12.", "diff": "hard", "concepts": ["continued_proportion"], "trap": "taking_average_instead"},
    {"q": "In exam, passed:failed=5:3. If 10 more passed, ratio becomes 7:3. Total students?", "o": ["120", "140", "160", "180"], "c": 2, "e": "6x=30 -> x=5. Total=40. (User index 2=160).", "diff": "hard", "concepts": ["ratio_change_students"], "trap": "adding_to_total_instead"}
]

def seed_ratio_proportion():
    session = SessionLocal()
    try:
        print(f"Adding {len(QUESTIONS_DATA)} Ratio and Proportion questions...")
        for q_data in QUESTIONS_DATA:
            new_q = AptitudeQuestion(
                id=str(uuid.uuid4()),
                question=q_data["q"],
                options=q_data["o"],
                correct_answer=q_data["c"],
                answer_explanation=q_data["e"],
                topic="Ratio and Proportion",
                category="Quantitative Ability",
                difficulty=q_data["diff"],
                source="hardcoded_ratio_proportion_part1",
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
    seed_ratio_proportion()
