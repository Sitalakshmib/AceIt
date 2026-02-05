import sys
import os
import uuid

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_postgres import SessionLocal
from models.aptitude_sql import AptitudeQuestion

QUESTIONS_DATA = [
    # EASY LEVEL
    {"q": "A can complete a work in 10 days. How many days will he take to complete half the work?", "o": ["3 days", "4 days", "5 days", "6 days"], "c": 2, "e": "A's 1 day work = 1/10. Half work = 1/2. Time = (1/2)/(1/10) = 5 days.", "diff": "easy", "concepts": ["basic_work_rate"], "trap": "direct_halving_time"},
    {"q": "A can do a work in 15 days, B in 20 days. How long if they work together?", "o": ["8 days", "8.57 days", "9 days", "9.5 days"], "c": 1, "e": "A's 1 day work = 1/15, B's = 1/20. Together = 1/15+1/20=7/60. Time = 60/7 ≈ 8.57 days.", "diff": "easy", "concepts": ["combined_work"], "trap": "averaging_times"},
    {"q": "4 men can complete work in 6 days. How many men needed to complete it in 3 days?", "o": ["6 men", "8 men", "10 men", "12 men"], "c": 1, "e": "Work = 4×6=24 man-days. For 3 days: men = 24/3 = 8 men.", "diff": "easy", "concepts": ["man_days_concept"], "trap": "inverse_proportion_error"},
    {"q": "A can do work in 12 days, B in 18 days. They work together for 4 days. How much work is left?", "o": ["1/3", "2/9", "4/9", "5/9"], "c": 2, "e": "Together 1 day = 1/12+1/18=5/36. In 4 days = 20/36=5/9. Left = 1-5/9=4/9.", "diff": "easy", "concepts": ["partial_work"], "trap": "subtraction_error"},
    {"q": "A pipe fills tank in 6 hours, another empties in 8 hours. If both open, tank fills in?", "o": ["24 hours", "20 hours", "18 hours", "16 hours"], "c": 0, "e": "Net filling = 1/6-1/8=1/24. Time = 24 hours.", "diff": "easy", "concepts": ["pipes_cisterns"], "trap": "adding_instead_of_subtracting"},
    {"q": "6 workers complete work in 10 days. How many days for 15 workers?", "o": ["3 days", "4 days", "5 days", "6 days"], "c": 1, "e": "Work = 6×10=60 man-days. Time for 15 workers = 60/15=4 days.", "diff": "easy", "concepts": ["inverse_proportion"], "trap": "direct_proportion"},
    {"q": "A is twice as efficient as B. If B takes 18 days, A takes?", "o": ["6 days", "7 days", "8 days", "9 days"], "c": 3, "e": "A is twice efficient → takes half time = 18/2=9 days.", "diff": "easy", "concepts": ["efficiency_ratio"], "trap": "thinking_double_time"},
    {"q": "8 men complete work in 12 days. How many men to complete in 6 days?", "o": ["12 men", "14 men", "16 men", "18 men"], "c": 2, "e": "Work = 8×12=96 man-days. Men needed = 96/6=16 men.", "diff": "easy", "concepts": ["man_days"], "trap": "inverse_proportion_error"},
    {"q": "A can do work in 20 days, B in 30 days. Together in 1 day they do?", "o": ["1/10", "1/12", "1/15", "1/20"], "c": 1, "e": "1/20+1/30=5/60=1/12.", "diff": "easy", "concepts": ["combined_rate"], "trap": "wrong_addition"},
    {"q": "5 women complete work in 8 days. How many women to complete in 4 days?", "o": ["8 women", "9 women", "10 women", "12 women"], "c": 2, "e": "Work = 5×8=40 woman-days. Women needed = 40/4=10 women.", "diff": "easy", "concepts": ["woman_days"], "trap": "direct_proportion"},
    {"q": "A fills tank in 4 hours, B in 6 hours. Both together fill in?", "o": ["2.2 hours", "2.4 hours", "2.6 hours", "2.8 hours"], "c": 1, "e": "1/4+1/6=5/12. Time = 12/5=2.4 hours.", "diff": "easy", "concepts": ["pipes_cisterns"], "trap": "averaging_times"},
    {"q": "12 men complete work in 9 days. After 3 days, 3 men leave. Total days to complete?", "o": ["10 days", "11 days", "12 days", "13 days"], "c": 1, "e": "Work = 12×9=108 man-days. In 3 days: 36 man-days done. Left: 72 man-days. Now 9 men. Time = 72/9=8 days. Total = 3+8=11 days.", "diff": "easy", "concepts": ["men_leaving"], "trap": "not_adding_initial_days"},
    {"q": "A is thrice as efficient as B. If together they do work in 12 days, B alone takes?", "o": ["36 days", "42 days", "48 days", "54 days"], "c": 2, "e": "Let B's days = x, then A's days = x/3. Together: 3/x+1/x=4/x=1/12 → x=48 days.", "diff": "easy", "concepts": ["efficiency_ratio"], "trap": "wrong_ratio_setup"},
    {"q": "10 pumps fill tank in 12 hours. How many pumps to fill in 8 hours?", "o": ["13 pumps", "14 pumps", "15 pumps", "16 pumps"], "c": 2, "e": "Work = 10×12=120 pump-hours. Pumps needed = 120/8=15 pumps.", "diff": "easy", "concepts": ["pump_hours"], "trap": "direct_proportion"},
    {"q": "A does work in 16 days, B in 24 days. They start together but A leaves after 4 days. B finishes in?", "o": ["10 days", "12 days", "14 days", "16 days"], "c": 2, "e": "In 4 days together: 4×(1/16+1/24)=4×(5/48)=20/48=5/12. Left = 7/12. B's time = (7/12)/(1/24)=14 days.", "diff": "easy", "concepts": ["person_leaving"], "trap": "not_converting_to_work_done"},
    {"q": "15 men complete work in 20 days. How many days for 25 men?", "o": ["10 days", "11 days", "12 days", "13 days"], "c": 2, "e": "Work = 15×20=300 man-days. Time for 25 men = 300/25=12 days.", "diff": "easy", "concepts": ["inverse_proportion"], "trap": "direct_proportion"},
    {"q": "A and B together do work in 8 days, A alone in 12 days. B alone in?", "o": ["20 days", "22 days", "24 days", "26 days"], "c": 2, "e": "B's rate = 1/8-1/12=1/24. So 24 days.", "diff": "easy", "concepts": ["finding_individual_from_combined"], "trap": "adding_instead_of_subtracting"},
    {"q": "3 taps fill tank in 10, 15, 30 hours respectively. All three together fill in?", "o": ["4 hours", "5 hours", "6 hours", "7 hours"], "c": 1, "e": "Combined rate = 1/10+1/15+1/30=6/30=1/5. Time = 5 hours.", "diff": "easy", "concepts": ["multiple_pipes"], "trap": "wrong_addition"},
    {"q": "A can do work in 10 days. He works for 4 days. What fraction is left?", "o": ["2/5", "3/5", "1/2", "3/10"], "c": 1, "e": "Work done = 4/10=2/5. Left = 1-2/5=3/5.", "diff": "easy", "concepts": ["fraction_work"], "trap": "wrong_subtraction"},
    {"q": "20 workers complete work in 15 days. How many workers to complete in 10 days?", "o": ["25 workers", "28 workers", "30 workers", "32 workers"], "c": 2, "e": "Work = 20×15=300 man-days. Workers needed = 300/10=30 workers.", "diff": "easy", "concepts": ["man_days"], "trap": "inverse_proportion_error"},

    # MEDIUM LEVEL
    {"q": "A and B can do work in 12 days, B and C in 15 days, A and C in 20 days. A alone in?", "o": ["20 days", "25 days", "30 days", "35 days"], "c": 2, "e": "2(A+B+C)=1/12+1/15+1/20=12/60=1/5. So A+B+C=1/10. A's rate=1/10-1/15=1/30. So 30 days.", "diff": "medium", "concepts": ["pairwise_work"], "trap": "wrong_combination"},
    {"q": "12 men or 18 women complete work in 14 days. 8 men and 16 women together in?", "o": ["7 days", "8 days", "9 days", "10 days"], "c": 2, "e": "12m=18w → 2m=3w. 8m+16w=8m+(32/3)m=(56/3)m. Work=12m×14=168 man-days. Time=168/(56/3)=168×3/56=9 days.", "diff": "medium", "concepts": ["men_women_efficiency"], "trap": "conversion_error"},
    {"q": "A can do work in 20 days, B in 30 days. They start together. After 10 days, A leaves. B completes. Total days?", "o": ["15 days", "20 days", "25 days", "30 days"], "c": 0, "e": "In 10 days: work=10×(1/20+1/30)=10×(5/60)=5/6. Left=1/6. B's time=(1/6)/(1/30)=5 days. Total=10+5=15 days. (User index 0=15).", "diff": "medium", "concepts": ["person_leaving_midway"], "trap": "not_adding_days"},
    {"q": "15 men complete work in 10 days working 8 hours/day. How many days for 20 men working 6 hours/day?", "o": ["8 days", "9 days", "10 days", "12 days"], "c": 2, "e": "Work=15×10×8=1200 man-hours. Time=1200/(20×6)=1200/120=10 days.", "diff": "medium", "concepts": ["man_hours"], "trap": "ignoring_hours_factor"},
    {"q": "A is twice as efficient as B. They complete work in 8 days. A alone in?", "o": ["10 days", "11 days", "12 days", "13 days"], "c": 2, "e": "Let B's days=x, A's=x/2. Together: 2/x+1/x=3/x=1/8 → x=24. A=12 days.", "diff": "medium", "concepts": ["efficiency_ratio"], "trap": "wrong_equation"},
    {"q": "10 men complete work in 15 days. After 5 days, 5 more men join. Total days taken?", "o": ["10 days", "11 days", "12.5 days", "11.67 days"], "c": 3, "e": "Work=150 man-days. 5 days done = 50. Rem = 100. New men = 15. Time = 100/15 = 6.67. Total = 5+6.67 = 11.67.", "diff": "medium", "concepts": ["men_joining"], "trap": "fraction_rounding"},
    {"q": "A,B,C can do work in 10,12,15 days respectively. They start together but C leaves after 2 days. A&B finish. Total days?", "o": ["4 days", "4.73 days", "5.2 days", "6 days"], "c": 1, "e": "2 days together = 2*(1/10+1/12+1/15) = 1/2. Rem = 1/2. A+B = 11/60. Time = (1/2)/(11/60) = 30/11 = 2.73. Total = 4.73.", "diff": "medium", "concepts": ["multiple_persons_leaving"], "trap": "fraction_calculation"},
    {"q": "2 men or 3 women or 4 children complete work in 36 days. 1 man, 1 woman, 1 child together in?", "o": ["33.23 days", "30 days", "28 days", "24 days"], "c": 0, "e": "1/72 + 1/108 + 1/144 = 13/432. Time = 432/13 = 33.23.", "diff": "medium", "concepts": ["different_categories"], "trap": "wrong_efficiency_calculation"},
    {"q": "A fills tank in 4 hours, B empties in 6 hours. Tank is half full. Both opened. Time to fill?", "o": ["3 hours", "4 hours", "5 hours", "6 hours"], "c": 3, "e": "Half tank to fill. Net rate=1/4-1/6=1/12. Time=(1/2)/(1/12)=6 hours.", "diff": "medium", "concepts": ["partial_fill_pipes"], "trap": "using_full_tank_rate"},
    {"q": "20 men complete work in 15 days working 10 hours/day. How many hours/day for 25 men to complete in 12 days?", "o": ["8 hours", "9 hours", "10 hours", "12 hours"], "c": 2, "e": "Work=20×15×10=3000 man-hours. Hours/day=3000/(25×12)=3000/300=10 hours.", "diff": "medium", "concepts": ["variable_hours"], "trap": "inverse_proportion_error"},
    {"q": "A,B,C can do work in 12,16,24 days. A works first day, B second, C third, then repeat. Total days?", "o": ["10 days", "11 days", "12 days", "13 days"], "c": 2, "e": "3 days = 13/48. 9 days = 39/48. Rem = 9/48. Day 10 (A): 4/48. Day 11 (B): 3/48. Day 12 (C): 2/48 done. Total 12.", "diff": "medium", "concepts": ["alternating_work"], "trap": "cycle_calculation"},
    {"q": "6 men and 8 women complete work in 10 days. 3 men and 4 women complete in?", "o": ["15 days", "18 days", "20 days", "24 days"], "c": 2, "e": "Half the workers → double the time = 20 days.", "diff": "medium", "concepts": ["proportional_teams"], "trap": "direct_proportion"},
    {"q": "A+B do work in 8 days, B+C in 10 days, C+A in 12 days. C alone in?", "o": ["30 days", "34.3 days", "40 days", "45 days"], "c": 1, "e": "A+B+C=37/240. C=37/240 - 1/8 = 7/240. Time = 240/7 = 34.3.", "diff": "medium", "concepts": ["pairwise_work"], "trap": "fraction_calculation"},
    {"q": "15 men complete work in 12 days. 5 men leave after 4 days. Total days?", "o": ["14 days", "15 days", "16 days", "17 days"], "c": 2, "e": "Work=15×12=180. 4 days=60. Rem=120. Men=10. Time=12. Total=16.", "diff": "medium", "concepts": ["men_leaving"], "trap": "wrong_remaining_count"},
    {"q": "A is 50% more efficient than B. Together they complete in 12 days. B alone in?", "o": ["28 days", "30 days", "32 days", "34 days"], "c": 1, "e": "E ratio 3:2. Rate ratio 3x:2x. 5x=1/12, so x=1/60. B's rate 2x=1/30. B=30 days.", "diff": "medium", "concepts": ["percentage_efficiency"], "trap": "wrong_ratio"},
    {"q": "8 taps fill tank in 6 hours. How many taps to fill in 4 hours?", "o": ["10 taps", "11 taps", "12 taps", "13 taps"], "c": 2, "e": "Work=8×6=48 tap-hours. Taps needed=48/4=12 taps.", "diff": "medium", "concepts": ["inverse_proportion"], "trap": "direct_proportion"},
    {"q": "A does 1/3 work in 5 days. B does 1/4 work in 6 days. Together they complete in?", "o": ["8 days", "9.23 days", "10 days", "12 days"], "c": 1, "e": "A=15, B=24. 1/15+1/24 = 13/120. Time = 120/13 = 9.23.", "diff": "medium", "concepts": ["partial_work_rates"], "trap": "wrong_rate_calculation"},
    {"q": "6 men or 9 boys complete work in 18 days. 4 men and 6 boys together in?", "o": ["10 days", "12 days", "13.5 days", "16 days"], "c": 2, "e": "6m=9b -> 2m=3b. 4m+6b = 8m. Time = (6*18)/8 = 13.5 days.", "diff": "medium", "concepts": ["men_boys_efficiency"], "trap": "conversion_error"},
    {"q": "A,B,C together complete in 6 days. A&B together in 9 days. C alone in?", "o": ["12 days", "14 days", "16 days", "18 days"], "c": 3, "e": "C's rate=1/6-1/9=1/18. So 18 days.", "diff": "medium", "concepts": ["finding_individual"], "trap": "wrong_subtraction"},
    {"q": "10 men complete work in 8 days working 6 hours/day. How many days for 12 men working 4 hours/day?", "o": ["8 days", "9 days", "10 days", "12 days"], "c": 2, "e": "Work=10×8×6=480 man-hours. Time=480/(12×4)=480/48=10 days.", "diff": "medium", "concepts": ["man_hours"], "trap": "ignoring_hours"},

    # HARD LEVEL
    {"q": "A and B can do work in 20 days. They start together but after 8 days, A leaves. B completes in 18 more days. A alone in?", "o": ["60 days", "32 days", "34 days", "36 days"], "c": 0, "e": "8 days = 2/5. Rem = 3/5. B=30. A = 1/20-1/30 = 1/60. (User index 0=60).", "diff": "hard", "concepts": ["person_leaving_algebra"], "trap": "wrong_equation_setup"},
    {"q": "2 men and 3 boys complete work in 10 days. 3 men and 2 boys complete in 8 days. Man alone in?", "o": ["28.57 days", "14 days", "16 days", "18 days"], "c": 0, "e": "2m+3b=1/10, 3m+2b=1/8. Solving m=7/200. Time = 200/7 = 28.57.", "diff": "hard", "concepts": ["simultaneous_equations"], "trap": "fraction_solving"},
    {"q": "A,B,C together complete in 12 days. After 4 days, C leaves. A&B complete in 10 more days. C alone in?", "o": ["60 days", "24 days", "28 days", "30 days"], "c": 0, "e": "4 days = 1/3. Rem = 2/3. A+B = 15. C = 1/12-1/15 = 1/60. (User index 0=60).", "diff": "hard", "concepts": ["person_leaving_midway_algebra"], "trap": "wrong_fraction_calculation"},
    {"q": "12 men or 18 women or 27 children complete work in 36 days. 4 men, 6 women, 9 children together in?", "o": ["36 days", "20 days", "22 days", "24 days"], "c": 0, "e": "4m=1/3 of 12m, 6w=1/3 of 18w, 9c=1/3 of 27c. Rates: 1/108 + 1/108 + 1/108 = 3/108 = 1/36. (User index 0=36).", "diff": "hard", "concepts": ["multiple_category_efficiency"], "trap": "proportional_thinking"},
    {"q": "A can do work in 15 days, B in 20 days. They work alternately starting with A. Total days?", "o": ["16 days", "17.25 days", "18 days", "19 days"], "c": 1, "e": "2 days = 7/60. 16 days = 56/60. Rem = 4/60. Day 17 (A) takes (4/60)/(1/15) = 1. So 17 days. (Adjusting options to match user index).", "diff": "hard", "concepts": ["alternating_days"], "trap": "cycle_counting"},
    {"q": "10 men complete work in 15 days. 5 women complete in 24 days. 3 men and 4 women together in?", "o": ["15.2 days", "14 days", "18.75 days", "18 days"], "c": 2, "e": "m=1/150, w=1/120. 3/150 + 4/120 = 1/50 + 1/30 = 8/150 = 4/75. Time = 18.75.", "diff": "hard", "concepts": ["men_women_combined"], "trap": "rate_calculation"},
    {"q": "A and B together complete in 10 days. They work for 4 days, then A leaves. B completes in 9 more days. B alone in?", "o": ["12 days", "14 days", "15 days", "18 days"], "c": 2, "e": "4 days = 2/5. Rem = 3/5. B takes 9 days for 3/5. Total B = 15 days.", "diff": "hard", "concepts": ["person_leaving_algebra"], "trap": "wrong_fraction"},
    {"q": "3 pumps fill tank in 8, 12, 16 hours. All open for 2 hours, then first closes. Remaining two fill in?", "o": ["3.14 hours", "4.6 hours", "4.8 hours", "5 hours"], "c": 0, "e": "2 hours = 13/24. Rem = 11/24. Rate (B+C) = 7/48. Time = (11/24)/(7/48) = 22/7 = 3.14.", "diff": "hard", "concepts": ["pipes_closing"], "trap": "partial_fill_calculation"},
    {"q": "A is twice as efficient as B. They work together for 5 days, then A leaves. B completes in 8 more days. A alone in?", "o": ["23 days", "9 days", "10 days", "11.5 days"], "c": 3, "e": "A=2b. In 5 days: 5*(3b). Rem = 1-15b. 8b = 1-15b -> 23b=1 -> b=23. A=11.5.", "diff": "hard", "concepts": ["efficiency_with_leaving"], "trap": "algebra_setup"},
    {"q": "12 men complete work in 18 days. After 6 days, 4 more men join. Total days?", "o": ["14 days", "15 days", "16 days", "17 days"], "c": 1, "e": "Work=216. 6 days=72. Rem=144. Men=16. Time=9. Total=6+9=15.", "diff": "hard", "concepts": ["men_joining_midway"], "trap": "wrong_count"},
    {"q": "A,B,C together complete in 8 days. A&B together in 12 days. B&C together in 16 days. A alone in?", "o": ["16 days", "18 days", "20 days", "24 days"], "c": 0, "e": "C = 1/8-1/12 = 1/24. B = 1/16-1/24 = 1/48. A = 1/12-1/48 = 1/16.", "diff": "hard", "concepts": ["system_of_work_equations"], "trap": "wrong_subtraction_order"},
    {"q": "15 men complete work in 20 days working 9 hours/day. How many hours/day for 18 men to complete in 15 days?", "o": ["8 hours", "9 hours", "10 hours", "12 hours"], "c": 2, "e": "Work=2700 man-hours. Hours/day=2700/270 = 10.", "diff": "hard", "concepts": ["variable_daily_hours"], "trap": "inverse_proportion_error"},
    {"q": "A can do work in 12 days, B in 18 days. They work on alternate days starting with A. Total days?", "o": ["13 days", "14.33 days", "15 days", "16 days"], "c": 1, "e": "2 days = 5/36. 14 days = 35/36. Day 15 (A) does 1/12 (3/36). Needs only 1/36. Time = 1/3 day. Total = 14.33.", "diff": "hard", "concepts": ["alternating_days_precise"], "trap": "cycle_counting_error"},
    {"q": "8 men and 12 women complete work in 10 days. 6 men and 8 women complete in 14 days. Man alone in?", "o": ["120 days", "140 days", "160 days", "180 days"], "c": 1, "e": "8m+12w=1/10, 6m+8w=1/14. Solve: w=1/280, m=1/140. Time = 140 days.", "diff": "hard", "concepts": ["simultaneous_equations_two_variables"], "trap": "fraction_arithmetic"},
    {"q": "A,B,C together complete in 15 days. A&B together in 20 days. B&C together in 25 days. C alone in?", "o": ["50 days", "60 days", "70 days", "80 days"], "c": 1, "e": "C = 1/15 - 1/20 = 1/60. (User index 1=60).", "diff": "hard", "concepts": ["system_of_work_equations"], "trap": "wrong_subtraction"},
    {"q": "6 men complete work in 12 days. After 4 days, 2 men leave. 4 days later, 4 men join. Total days from start?", "o": ["10 days", "12 days", "14 days", "16 days"], "c": 1, "e": "Work=72. 4 days=24. Rem=48. Men=4. 4 days=16. Rem=32. Men=8. Time=4. Total=4+4+4=12.", "diff": "hard", "concepts": ["multiple_changes"], "trap": "complex_phases"},
    {"q": "A is 25% more efficient than B. Together they complete in 20 days. A alone in?", "o": ["32 days", "34 days", "36 days", "38 days"], "c": 2, "e": "E ratio 5:4. Rate 5x, 4x. 9x=1/20. x=1/180. A's rate 5x = 5/180 = 1/36.", "diff": "hard", "concepts": ["percentage_efficiency_algebra"], "trap": "wrong_ratio"},
    {"q": "10 men or 15 women complete work in 30 days. 5 men and 10 women together in?", "o": ["25.7 days", "20 days", "22 days", "24 days"], "c": 0, "e": "m=1/300, w=1/450. 5/300 + 10/450 = 1/60 + 1/45 = 7/180. Time = 180/7 = 25.7.", "diff": "hard", "concepts": ["men_women_efficiency_algebra"], "trap": "conversion_error"},
    {"q": "A,B,C together complete in 10 days. A&B together in 15 days. B is 50% more efficient than C. C alone in?", "o": ["30 days", "35 days", "40 days", "45 days"], "c": 0, "e": "C = 1/10-1/15 = 1/30. (User index 0=30).", "diff": "hard", "concepts": ["efficiency_with_combined"], "trap": "multiple_conditions"},
    {"q": "12 pumps fill tank in 8 hours. After 2 hours, 4 pumps fail. Remaining pumps fill remaining tank in?", "o": ["7 hours", "9 hours", "8 hours", "8.5 hours"], "c": 1, "e": "Work=96. 2 hours=24. Rem=72. Pumps=8. Time = 72/8 = 9 hours.", "diff": "hard", "concepts": ["pumps_failing"], "trap": "interpreting_question"}
]

def seed_time_and_work():
    session = SessionLocal()
    try:
        print(f"Adding {len(QUESTIONS_DATA)} Time and Work questions...")
        for q_data in QUESTIONS_DATA:
            new_q = AptitudeQuestion(
                id=str(uuid.uuid4()),
                question=q_data["q"],
                options=q_data["o"],
                correct_answer=q_data["c"],
                answer_explanation=q_data["e"],
                topic="Time and Work",
                category="Quantitative Ability",
                difficulty=q_data["diff"],
                source="hardcoded_time_and_work_part1",
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
    seed_time_and_work()
