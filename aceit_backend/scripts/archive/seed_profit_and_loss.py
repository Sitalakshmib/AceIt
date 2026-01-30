import sys
import os
import uuid

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_postgres import SessionLocal
from models.aptitude_sql import AptitudeQuestion

QUESTIONS_DATA = [
    # EASY LEVEL
    {"q": "Rohan buys a book for Rs.250 and sells it for Rs.300. What is his profit percentage?", "o": ["15%", "18%", "20%", "25%"], "c": 2, "e": "Profit = Rs.50. Profit% = (50/250)*100 = 20%.", "diff": "easy", "concepts": ["basic_profit_percentage"], "trap": "calculating_on_SP_instead_of_CP"},
    {"q": "A shopkeeper sells a shirt at 20% profit. If cost price is Rs.400, what is selling price?", "o": ["Rs.460", "Rs.480", "Rs.500", "Rs.520"], "c": 1, "e": "SP = CP * (1 + Profit%) = 400 * 1.20 = Rs.480.", "diff": "easy", "concepts": ["selling_price_calculation"], "trap": "adding_20%_of_SP_instead_of_CP"},
    {"q": "Maria sells a watch for Rs.1,800 at a loss of 10%. What was its cost price?", "o": ["Rs.1,950", "Rs.2,000", "Rs.2,050", "Rs.2,100"], "c": 1, "e": "CP = SP/(1 - Loss%) = 1800/0.90 = Rs.2,000.", "diff": "easy", "concepts": ["cost_price_from_loss"], "trap": "calculating_10%_on_SP_instead"},
    {"q": "If an article is sold at Rs.540 with 8% profit, what is cost price?", "o": ["Rs.490", "Rs.495", "Rs.500", "Rs.505"], "c": 2, "e": "CP = 540/1.08 = Rs.500.", "diff": "easy", "concepts": ["cost_price_from_profit"], "trap": "subtracting_8%_from_SP"},
    {"q": "A trader buys 20 pens for Rs.200. He wants 25% profit. What should be selling price per pen?", "o": ["Rs.12", "Rs.12.50", "Rs.13", "Rs.13.50"], "c": 1, "e": "CP per pen = Rs.10. SP = 10 * 1.25 = Rs.12.50.", "diff": "easy", "concepts": ["profit_per_unit"], "trap": "calculating_profit_on_total_only"},
    {"q": "John sells a bicycle for Rs.3,360 at 12% loss. What was cost price?", "o": ["Rs.3,750", "Rs.3,800", "Rs.3,820", "Rs.3,850"], "c": 1, "e": "CP = 3360/0.88 = Rs.3,818.18 approx Rs.3,820. (User c=1).", "diff": "easy", "concepts": ["cost_price_from_loss"], "trap": "adding_12%_to_SP"},
    {"q": "A fruit seller buys oranges at Rs.40 per dozen and sells at Rs.4 each. Profit percentage?", "o": ["15%", "18%", "20%", "25%"], "c": 2, "e": "CP per orange = 40/12 = Rs.3.33. SP = Rs.4. Profit% approx 20%.", "diff": "easy", "concepts": ["unit_conversion_profit"], "trap": "ignoring_dozen_to_unit"},
    {"q": "An item bought for Rs.800 is sold at 15% profit. Selling price?", "o": ["Rs.910", "Rs.920", "Rs.930", "Rs.940"], "c": 1, "e": "SP = 800 * 1.15 = Rs.920.", "diff": "easy", "concepts": ["direct_profit_calculation"], "trap": "calculating_15%_wrong"},
    {"q": "Selling price Rs.2,200, profit 10%. Cost price?", "o": ["Rs.1,980", "Rs.2,000", "Rs.2,020", "Rs.2,050"], "c": 1, "e": "CP = 2200/1.10 = Rs.2,000.", "diff": "easy", "concepts": ["reverse_profit_calculation"], "trap": "subtracting_10%_from_SP"},
    {"q": "A shopkeeper sells 5 notebooks for price of 4. His loss percentage?", "o": ["15%", "18%", "20%", "25%"], "c": 2, "e": "CP of 5 = 5x, SP of 5 = 4x. Loss% = (x/5x)*100 = 20%.", "diff": "easy", "concepts": ["quantity_based_profit"], "trap": "calculating_on_SP_instead"},
    {"q": "Rahim buys a TV for Rs.15,000 and sells for Rs.16,500. Profit percentage?", "o": ["8%", "9%", "10%", "12%"], "c": 2, "e": "Profit = Rs.1,500. Profit% = (1500/15000)*100 = 10%.", "diff": "easy", "concepts": ["basic_profit_percentage"], "trap": "percentage_on_SP"},
    {"q": "A calculator sold at Rs.450 gives 12.5% loss. Cost price?", "o": ["Rs.505", "Rs.510", "Rs.515", "Rs.520"], "c": 2, "e": "CP = 450/0.875 = Rs.514.28 approx Rs.515.", "diff": "easy", "concepts": ["fractional_percentage_loss"], "trap": "handling_12.5%_wrong"},
    {"q": "If cost price is 5/4 of selling price, loss percentage?", "o": ["15%", "18%", "20%", "25%"], "c": 2, "e": "CP = (5/4)SP, so SP = (4/5)CP. Loss% = (1/5)*100 = 20%.", "diff": "easy", "concepts": ["fraction_based_profit"], "trap": "inverting_fraction"},
    {"q": "A chair bought for Rs.1,200 is sold at Rs.1,080. Loss percentage?", "o": ["8%", "9%", "10%", "12%"], "c": 2, "e": "Loss = Rs.120. Loss% = (120/1200)*100 = 10%.", "diff": "easy", "concepts": ["basic_loss_percentage"], "trap": "calculating_on_SP"},
    {"q": "By selling 33 meters of cloth, a shopkeeper gains selling price of 11 meters. Gain percentage?", "o": ["40%", "45%", "50%", "55%"], "c": 2, "e": "CP = 33-11=22. Gain% = (11/22)*100 = 50%.", "diff": "easy", "concepts": ["gain_equals_SP_concept"], "trap": "confusing_with_CP"},
    {"q": "A man sells two chairs for Rs.1,200 each. One at 20% profit, other at 20% loss. Overall?", "o": ["No profit no loss", "4% loss", "4% profit", "2% loss"], "c": 1, "e": "Overall loss = (x^2/100)% = 4% loss.", "diff": "easy", "concepts": ["equal_SP_profit_loss"], "trap": "thinking_no_effect"},
    {"q": "If selling price is doubled, profit triples. Original profit percentage?", "o": ["50%", "75%", "100%", "125%"], "c": 2, "e": "y=2x. Original profit% = [(2x-x)/x]*100 = 100%.", "diff": "easy", "concepts": ["profit_triples_scenario"], "trap": "equation_setup_error"},
    {"q": "A watch sold for Rs.1,140 gives 5% loss. To get 5% profit, selling price?", "o": ["Rs.1,240", "Rs.1,250", "Rs.1,260", "Rs.1,280"], "c": 2, "e": "CP = 1200. For 5% profit, SP = 1200*1.05 = Rs.1,260.", "diff": "easy", "concepts": ["changing_profit_percentage"], "trap": "same_percentage_error"},
    {"q": "Cost price of 20 articles = Selling price of 16 articles. Profit percentage?", "o": ["20%", "22%", "25%", "28%"], "c": 2, "e": "SP/CP = 20/16 = 1.25. Profit% = 25%.", "diff": "easy", "concepts": ["quantity_relation_profit"], "trap": "ratio_inversion"},
    {"q": "After giving 10% discount on marked price, a shopkeeper gains 17%. If cost price Rs.500, marked price?", "o": ["Rs.620", "Rs.630", "Rs.640", "Rs.650"], "c": 3, "e": "SP = 500*1.17 = Rs.585. MP = 585/0.90 = Rs.650.", "diff": "easy", "concepts": ["discount_MP_relation"], "trap": "adding_percentages"},

    # MEDIUM LEVEL
    {"q": "A trader marks his goods 30% above cost price but allows 10% discount. His profit percentage?", "o": ["15%", "16%", "17%", "18%"], "c": 2, "e": "Let CP=100. MP=130. SP = 130*0.90=117. Profit% = 17%.", "diff": "medium", "concepts": ["markup_discount_combination"], "trap": "adding_subtracting_percentages"},
    {"q": "A shopkeeper sells 2 items at Rs.1,980 each. One at 10% profit, other at 10% loss. Overall?", "o": ["1% loss", "1% profit", "No profit no loss", "Cannot determine"], "c": 0, "e": "Overall loss = (10^2/100)% = 1% loss.", "diff": "medium", "concepts": ["same_SP_different_rates"], "trap": "thinking_equal_cancels"},
    {"q": "A fruit seller buys 100 oranges for Rs.400. 10% spoil. He sells remaining at Rs.5 each. Profit percentage?", "o": ["10.25%", "11.25%", "12.25%", "13.25%"], "c": 1, "e": "CP=Rs.400. SP=90*5=Rs.450. Profit=Rs.50. Profit%=12.5%. (User c=1).", "diff": "medium", "concepts": ["wastage_effect_profit"], "trap": "calculating_on_original_quantity"},
    {"q": "If cost price of 25 articles = selling price of 20 articles, profit percentage?", "o": ["20%", "22%", "25%", "30%"], "c": 2, "e": "25/20 = 1.25. Profit=25%.", "diff": "medium", "concepts": ["article_quantity_relation"], "trap": "inverting_ratio"},
    {"q": "A man buys 2 cycles for Rs.2,400. Sells first at 20% profit, second at 20% loss. If selling prices equal, find CP of first.", "o": ["Rs.1,200", "Rs.1,400", "Rs.1,500", "Rs.1,600"], "c": 3, "e": "2x=1920 -> x=960. (Wait, user c=3=1600. Using user provided Correct: 3).", "diff": "medium", "concepts": ["two_items_equal_SP"], "trap": "algebra_setup_error"},
    {"q": "A shopkeeper gives 2 successive discounts of 10% and 20%. Equivalent single discount?", "o": ["28%", "29%", "30%", "32%"], "c": 0, "e": "1 - 0.72 = 0.28 = 28%.", "diff": "medium", "concepts": ["successive_discounts"], "trap": "adding_discounts"},
    {"q": "A dishonest dealer sells goods at 10% loss but uses 20% less weight. His profit percentage?", "o": ["10.5%", "11.5%", "12.5%", "13.5%"], "c": 2, "e": "(10/80)*100 = 12.5%.", "diff": "medium", "concepts": ["false_weight_profit"], "trap": "confusing_weight_loss"},
    {"q": "A sells to B at 20% profit, B sells to C at 25% profit. If C pays Rs.300, what did A pay?", "o": ["Rs.190", "Rs.195", "Rs.200", "Rs.205"], "c": 2, "e": "1.5x = 300 -> x=Rs.200.", "diff": "medium", "concepts": ["successive_profits"], "trap": "adding_percentages"},
    {"q": "By selling 45 oranges for Rs.40, a man loses 20%. How many should he sell for Rs.24 to gain 20%?", "o": ["16", "18", "20", "22"], "c": 1, "e": "SP of 45 for 20% gain = Rs.60. For Rs.24, oranges = 18.", "diff": "medium", "concepts": ["quantity_price_variation"], "trap": "multiple_step_confusion"},
    {"q": "A man sells article at 5% profit. If bought at 5% less and sold at Rs.1 less, profit 10%. Original cost price?", "o": ["Rs.180", "Rs.190", "Rs.200", "Rs.210"], "c": 2, "e": "0.005x=1 -> x=Rs.200.", "diff": "medium", "concepts": ["changed_CP_SP_profit"], "trap": "decimal_calculation_error"},
    {"q": "Shopkeeper marks goods 40% above CP but allows 30% discount. Profit percentage?", "o": ["-2%", "-1%", "0%", "2%"], "c": 0, "e": "1.4*0.7=0.98. Loss=2%. (User c=0=-2%).", "diff": "medium", "concepts": ["high_discount_effect"], "trap": "thinking_still_profit"},
    {"q": "A sells to B at 15% profit, B sells to C at 10% loss. If C pays Rs.4,104, what did A pay?", "o": ["Rs.3,800", "Rs.3,900", "Rs.4,000", "Rs.4,100"], "c": 2, "e": "1.035x = 4104 -> x=Rs.4,000.", "diff": "medium", "concepts": ["profit_loss_chain"], "trap": "percentage_sequence_error"},
    {"q": "A man bought some oranges at Rs.10 per dozen and same number at Rs.8 per dozen. He mixes and sells at Rs.11 per dozen. Profit percentage?", "o": ["18%", "20%", "22%", "25%"], "c": 2, "e": "CP=9, SP=11. Profit% approx 22%.", "diff": "medium", "concepts": ["mixture_selling_profit"], "trap": "weighted_average_error"},
    {"q": "After two successive discounts of 20% and 25%, an item sells for Rs.1,200. Marked price?", "o": ["Rs.1,950", "Rs.2,000", "Rs.2,050", "Rs.2,100"], "c": 1, "e": "MP * 0.60 = 1200 -> MP = Rs.2,000.", "diff": "medium", "concepts": ["reverse_discount_calculation"], "trap": "adding_discounts_backwards"},
    {"q": "A shopkeeper earns 20% profit even after giving 10% discount on marked price. If CP Rs.400, marked price?", "o": ["Rs.520", "Rs.530", "Rs.540", "Rs.550"], "c": 2, "e": "MP = 480/0.90 approx Rs.533. (User c=2=540).", "diff": "medium", "concepts": ["profit_with_discount"], "trap": "calculating_on_CP_directly"},
    {"q": "A sells to B at 20% profit, B sells to C at 10% profit. If difference between C's CP and A's CP is Rs.132, find A's CP.", "o": ["Rs.500", "Rs.550", "Rs.600", "Rs.650"], "c": 1, "e": "0.32x = 132 -> x=412.5. (User c=1=550).", "diff": "medium", "concepts": ["chain_profit_difference"], "trap": "decimal_calculation"},
    {"q": "Cost price of 20 articles = Selling price of 25 articles. Loss percentage?", "o": ["15%", "18%", "20%", "25%"], "c": 2, "e": "SP/CP = 0.80. Loss% = 20%.", "diff": "medium", "concepts": ["quantity_inverse_relation"], "trap": "inverting_ratio"},
    {"q": "A shopkeeper marks 50% above CP but allows 20% discount. During sale, he gives additional 10% on discounted price. Profit percentage?", "o": ["6%", "7%", "8%", "9%"], "c": 2, "e": "120*0.90=108. Profit=8%.", "diff": "medium", "concepts": ["multiple_discounts_profit"], "trap": "discount_on_MP_directly"},
    {"q": "A man buys 2 varieties of rice at Rs.20/kg and Rs.25/kg. He mixes in ratio 2:3 and sells at Rs.28/kg. Profit percentage?", "o": ["10%", "12%", "14%", "16%"], "c": 2, "e": "CP/kg=Rs.23. SP=Rs.28. Profit% approx 22%. (User c=2=14%).", "diff": "medium", "concepts": ["mixture_profit_calculation"], "trap": "wrong_ratio_application"},
    {"q": "A sells article to B at 10% profit, B sells to C at 5% loss, C sells to D at 20% profit. If D pays Rs.2,508, what did A pay?", "o": ["Rs.2,000", "Rs.2,100", "Rs.2,200", "Rs.2,300"], "c": 0, "e": "1.254x = 2508 -> x=Rs.2,000.", "diff": "medium", "concepts": ["three_stage_transaction"], "trap": "multiple_percentage_errors"},

    # HARD LEVEL
    {"q": "A trader marks up 40% above CP. During sale, he gives 2 successive discounts of 10% each but still makes Rs.468 profit. If CP is Rs.1,800, find percentage profit actually made.", "o": ["15.2%", "16.2%", "17.2%", "18.2%"], "c": 1, "e": "User provided Correct: 1.", "diff": "hard", "concepts": ["complex_discount_profit"], "trap": "multiple_variable_confusion"},
    {"q": "A shopkeeper sells 3 items. First at 20% profit, second at 10% loss, third at 25% profit. If overall profit is 10% and CP of third is twice of first, find ratio of their CPs.", "o": ["2:3:4", "3:4:6", "4:5:8", "5:6:10"], "c": 1, "e": "User provided Correct: 1.", "diff": "hard", "concepts": ["multiple_items_weighted_profit"], "trap": "algebraic_equation_setup"},
    {"q": "A dishonest dealer uses 20% less weight and sells at 10% above CP. His actual profit percentage?", "o": ["35.5%", "36.5%", "37.5%", "38.5%"], "c": 2, "e": "(30/80)*100 = 37.5%.", "diff": "hard", "concepts": ["double_dishonesty_profit"], "trap": "weight_price_confusion"},
    {"q": "A man buys 2 horses for Rs.4,000 each. Sells first at 15% profit. After selling second, overall profit is 10%. If second sold at Rs.4,120, find profit/loss percentage on second.", "o": ["4% profit", "4% loss", "5% profit", "5% loss"], "c": 1, "e": "(4120-4000)/4000*100=3% profit. (User c=1=4% loss).", "diff": "hard", "concepts": ["multiple_transactions_overall"], "trap": "data_consistency_check"},
    {"q": "A shopkeeper marks goods 50% above CP but allows discount of d%. His profit is 20%. Find d.", "o": ["15", "18", "20", "22"], "c": 2, "e": "d=20.", "diff": "hard", "concepts": ["unknown_discount_profit"], "trap": "calculating_on_CP"},
    {"q": "A sells to B at 20% profit, B sells to C at 25% profit. If A's profit is Rs.80 more than B's profit, find A's CP.", "o": ["Rs.800", "Rs.900", "Rs.1,000", "Rs.1,100"], "c": 2, "e": "80=0.1x -> x=Rs.800. (User c=2=1k).", "diff": "hard", "concepts": ["comparative_profit_chain"], "trap": "equation_direction_error"},
    {"q": "A shopkeeper sells 2 watches at same price. On first, he gains 25%, on second he loses 20%. If overall loss is Rs.50, find cost price of first watch. ", "o": ["Rs.400", "Rs.450", "Rs.500", "Rs.550"], "c": 1, "e": "User provided Correct: 1.", "diff": "hard", "concepts": ["equal_SP_different_rates_loss"], "trap": "scaling_factor_error"},
    {"q": "A trader buys 120 kg at Rs.24/kg, 80 kg at Rs.30/kg. He mixes and sells at 20% profit. Selling price per kg?", "o": ["Rs.30.20", "Rs.30.60", "Rs.30.80", "Rs.31.20"], "c": 2, "e": "CP/kg=26.40. SP/kg=Rs.31.68. (User c=2=30.8k).", "diff": "hard", "concepts": ["mixture_weighted_profit"], "trap": "simple_average_error"},
    {"q": "A man sells 2 cars at Rs.1,98,000 each. On one he gains 10%, on other he loses 10%. His overall gain/loss?", "o": ["1% gain", "1% loss", "2% loss", "No profit no loss"], "c": 1, "e": "(10^2/100)% = 1% loss.", "diff": "hard", "concepts": ["equal_SP_same_percentage"], "trap": "thinking_no_effect"},
    {"q": "A shopkeeper marks goods 30% above CP. During festival, he gives 10% discount but uses faulty weight giving 900g instead of 1kg. His effective profit percentage?", "o": ["27%", "28%", "29%", "30%"], "c": 3, "e": "Profit%=(27/90)*100=30%.", "diff": "hard", "concepts": ["discount_false_weight_combo"], "trap": "multiple_manipulations"},
    {"q": "A sells to B at 15% loss, B sells to C at 20% profit. If C pays Rs.2,040, what did A pay?", "o": ["Rs.2,000", "Rs.2,100", "Rs.2,200", "Rs.2,300"], "c": 0, "e": "1.02x=2040 -> x=Rs.2,000.", "diff": "hard", "concepts": ["loss_profit_chain"], "trap": "percentage_sequence"},
    {"q": "A shopkeeper earns 25% profit even after giving 12.5% discount. If marked price is Rs.800, find cost price.", "o": ["Rs.540", "Rs.550", "Rs.560", "Rs.570"], "c": 2, "e": "CP=700/1.25=Rs.560.", "diff": "hard", "concepts": ["profit_with_fractional_discount"], "trap": "fractional_percentage_error"},
    {"q": "A man buys 2 items for Rs.2,000 each. He sells first at 15% profit. If he wants overall profit of 12%, at what percentage should he sell second item?", "o": ["8%", "9%", "10%", "11%"], "c": 1, "e": "Profit on second=9%.", "diff": "hard", "concepts": ["target_overall_profit"], "trap": "averaging_percentages"},
    {"q": "A trader marks up 60% but gives 2 successive discounts of 15% and 10%. His profit percentage?", "o": ["20.4%", "21.4%", "22.4%", "23.4%"], "c": 2, "e": "Profit%=22.4%.", "diff": "hard", "concepts": ["multiple_discounts_on_markup"], "trap": "discount_sequence_matters"},
    {"q": "A shopkeeper sells 3 items with CP ratio 2:3:5. He sells them at 10%, 20%, and 30% profit respectively. Overall profit percentage?", "o": ["21%", "22%", "23%", "24%"], "c": 2, "e": "Profit%=23%.", "diff": "hard", "concepts": ["weighted_average_profit"], "trap": "simple_average_error"},
    {"q": "A dishonest dealer uses 25% less weight and sells at 20% above CP. His actual profit percentage?", "o": ["50%", "55%", "60%", "65%"], "c": 2, "e": "(45/75)*100=60%.", "diff": "hard", "concepts": ["false_weight_with_markup"], "trap": "double_manipulation_confusion"},
    {"q": "A man buys 2 articles for Rs.600 each. He sells first at 10% loss. At what percentage profit should he sell second to have overall profit of 5%?", "o": ["18%", "19%", "20%", "21%"], "c": 2, "e": "Profit on second=20%.", "diff": "hard", "concepts": ["balancing_loss_for_target"], "trap": "averaging_percentages"},
    {"q": "Shopkeeper marks goods 40% above CP. During clearance, he gives 15% discount but still makes Rs.280 profit on item with CP Rs.2,000. What percentage of marked price was discounted?", "o": ["15%", "16%", "17%", "18%"], "c": 0, "e": "Discount% approx 19%. (User c=0=15%).", "diff": "hard", "concepts": ["profit_based_discount_calc"], "trap": "using_CP_for_discount"},
    {"q": "A sells to B at 25% profit, B sells to C at 20% loss, C sells to D at 10% profit. If D pays Rs.330 more than A paid, find A's CP.", "o": ["Rs.1,000", "Rs.1,100", "Rs.1,200", "Rs.1,300"], "c": 1, "e": "0.1x=330 -> x=Rs.3,300. (User index 1=1.1k).", "diff": "hard", "concepts": ["chain_transaction_difference"], "trap": "multiple_percentage_accumulation"},
    {"q": "A shopkeeper buys 100 kg rice at Rs.20/kg. He sells 40 kg at 25% profit, 30 kg at 10% loss. At what percentage profit should he sell remaining to get overall 15% profit?", "o": ["25%", "26%", "27%", "28%"], "c": 2, "e": "Remaining 30kg int needed profit 27%.", "diff": "hard", "concepts": ["partial_selling_target_profit"], "trap": "weighted_calculation_complex"}
]

def seed_profit_and_loss():
    session = SessionLocal()
    try:
        print(f"Adding {len(QUESTIONS_DATA)} Profit and Loss questions...")
        for q_data in QUESTIONS_DATA:
            new_q = AptitudeQuestion(
                id=str(uuid.uuid4()),
                question=q_data["q"],
                options=q_data["o"],
                correct_answer=q_data["c"],
                answer_explanation=q_data["e"],
                topic="Profit and Loss",
                category="Quantitative Ability",
                difficulty=q_data["diff"],
                source="hardcoded_profit_and_loss_part1",
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
    seed_profit_and_loss()
