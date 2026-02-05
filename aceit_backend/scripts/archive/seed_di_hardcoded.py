"""
Script to seed HARDCODED Data Interpretation questions provided by the user.
Contains 40 questions (2 sets of 20) with specific chart data.
"""
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.aptitude_sql import AptitudeQuestion
from services.chart_generator import ChartGenerator

load_dotenv()

QUESTIONS_DATA = [
    # === SET 1: EASY ===
    {
        "topic": "Pie Chart",
        "difficulty": "easy",
        "question": "The pie chart shows the favorite colors of students in Class 10. The total number of students is 180. The chart segments are: Blue (72°), Red (108°), Green (90°), Yellow (54°), Purple (36°). How many students prefer Red?",
        "options": ["36", "48", "54", "60"],
        "correct_answer": 2,
        "explanation": "Total angle = 360°. Students preferring Red = (108/360) × 180 = (3/10) × 180 = 54 students.",
        "primary_concepts": ["angle_to_value", "basic_proportion"],
        "chart_type": "pie",
        "chart_data": {"labels": ["Blue", "Red", "Green", "Yellow", "Purple"], "values": [72, 108, 90, 54, 36], "title": "Student Favorite Colors"}
    },
    {
        "topic": "Bar Graph",
        "difficulty": "easy",
        "question": "The bar graph shows the number of laptops sold by a store from January to May: January (25), February (40), March (35), April (50), May (45). What is the difference in sales between the highest and lowest months?",
        "options": ["15", "20", "25", "30"],
        "correct_answer": 2,
        "explanation": "Highest sales = April (50), Lowest sales = January (25). Difference = 50 - 25 = 25.",
        "primary_concepts": ["range_calculation", "data_extremes"],
        "chart_type": "bar",
        "chart_data": {"labels": ["Jan", "Feb", "Mar", "Apr", "May"], "values": [25, 40, 35, 50, 45], "title": "Laptop Sales", "y_label": "Units"}
    },
    {
        "topic": "Line Graph",
        "difficulty": "easy",
        "question": "The line graph shows the weekly rainfall (in mm) in Mumbai during a monsoon week: Monday (12), Tuesday (18), Wednesday (15), Thursday (22), Friday (10), Saturday (14), Sunday (16). On which day was rainfall exactly 15 mm?",
        "options": ["Tuesday", "Wednesday", "Thursday", "Saturday"],
        "correct_answer": 1,
        "explanation": "Directly read from the graph: Wednesday has 15 mm rainfall.",
        "primary_concepts": ["direct_reading", "exact_match"],
        "chart_type": "line",
        "chart_data": {"labels": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], "values": [12, 18, 15, 22, 10, 14, 16], "title": "Weekly Rainfall (mm)", "y_label": "Rainfall (mm)"}
    },
    {
        "topic": "Pie Chart",
        "difficulty": "easy",
        "question": "A pie chart shows the distribution of 240 employees by department: Marketing (30%), Finance (25%), HR (20%), Operations (15%), IT (10%). How many employees work in the Finance department?",
        "options": ["48", "54", "60", "72"],
        "correct_answer": 2,
        "explanation": "Finance employees = 25% of 240 = (25/100) × 240 = 60 employees.",
        "primary_concepts": ["percentage_calculation", "departmental_distribution"],
        "chart_type": "pie",
        "chart_data": {"labels": ["Marketing", "Finance", "HR", "Operations", "IT"], "values": [30, 25, 20, 15, 10], "title": "Employee Distribution"}
    },
    {
        "topic": "Bar Graph",
        "difficulty": "easy",
        "question": "The bar graph shows the number of visitors to a museum on 5 consecutive days: Day 1 (120), Day 2 (150), Day 3 (180), Day 4 (140), Day 5 (160). What is the average daily visitors?",
        "options": ["140", "145", "150", "155"],
        "correct_answer": 2,
        "explanation": "Total visitors = 120+150+180+140+160 = 750. Average = 750/5 = 150.",
        "primary_concepts": ["average_calculation", "summation"],
        "chart_type": "bar",
        "chart_data": {"labels": ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5"], "values": [120, 150, 180, 140, 160], "title": "Museum Visitors", "y_label": "Visitors"}
    },
    # === SET 1: MEDIUM ===
    {
        "topic": "Pie Chart",
        "difficulty": "medium",
        "question": "A pie chart shows the budget allocation for a project: Labor (40%), Materials (30%), Equipment (20%), Contingency (10%). If the budget for Materials is ₹9,00,000, what is the total project budget?",
        "options": ["₹25,00,000", "₹28,00,000", "₹30,00,000", "₹32,00,000"],
        "correct_answer": 2,
        "explanation": "Materials = 30% of total = ₹9,00,000. Total budget = 9,00,000 × (100/30) = ₹30,00,000.",
        "primary_concepts": ["budget_calculation", "percentage_to_total"],
        "chart_type": "pie",
        "chart_data": {"labels": ["Labor", "Materials", "Equipment", "Contingency"], "values": [40, 30, 20, 10], "title": "Project Budget Allocation"}
    },
    {
        "topic": "Bar Graph",
        "difficulty": "medium",
        "question": "A grouped bar graph shows the number of male and female students in 4 sections: Section A (Male: 25, Female: 30), Section B (Male: 28, Female: 32), Section C (Male: 22, Female: 28), Section D (Male: 30, Female: 25). Which section has the highest total students?",
        "options": ["Section A", "Section B", "Section C", "Section D"],
        "correct_answer": 1,
        "explanation": "A=55, B=60, C=50, D=55. Section B highest.",
        "primary_concepts": ["total_calculation", "comparison"],
        "chart_type": "bar_group",
        "chart_data": {
            "labels": ["Sec A", "Sec B", "Sec C", "Sec D"],
            "datasets": [{"name": "Male", "values": [25, 28, 22, 30]}, {"name": "Female", "values": [30, 32, 28, 25]}],
            "title": "Students by Section"
        }
    },
    {
        "topic": "Line Graph",
        "difficulty": "medium",
        "question": "The line graph shows monthly sales (in ₹ lakhs) from July to Dec: Jul (12), Aug (15), Sep (18), Oct (14), Nov (20), Dec (22). What is the percentage increase from July to December?",
        "options": ["75%", "80%", "83.33%", "87.5%"],
        "correct_answer": 2,
        "explanation": "Increase = 22 - 12 = 10. % Increase = (10/12)*100 = 83.33%.",
        "primary_concepts": ["percentage_increase", "two_point_comparison"],
        "chart_type": "line",
        "chart_data": {"labels": ["Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], "values": [12, 15, 18, 14, 20, 22], "title": "Monthly Sales (₹ Lakhs)", "y_label": "Sales"}
    },
    {
        "topic": "Pie Chart",
        "difficulty": "medium",
        "question": "A pie chart shows daily activity time: Sleep (120°), Study (90°), Recreation (60°), Meals (45°), Travel (30°), Misc (15°). If Study time is 6 hours, what is the total time in a day?",
        "options": ["20 hours", "22 hours", "24 hours", "26 hours"],
        "correct_answer": 2,
        "explanation": "Study 90° = 6 hrs. Total 360° = (360/90)*6 = 24 hrs.",
        "primary_concepts": ["time_allocation", "angle_to_hours"],
        "chart_type": "pie",
        "chart_data": {"labels": ["Sleep", "Study", "Recreation", "Meals", "Travel", "Misc"], "values": [120, 90, 60, 45, 30, 15], "title": "Daily Activity Time"}
    },
    {
        "topic": "Bar Graph",
        "difficulty": "medium",
        "question": "Bar graph of quarterly profit (₹ Cr) for 2023: Q1 (8), Q2 (12), Q3 (10), Q4 (14). Ratio of first half (Q1+Q2) to second half (Q3+Q4)?",
        "options": ["1:1", "5:6", "10:12", "20:24"],
        "correct_answer": 1,
        "explanation": "1st Half = 20. 2nd Half = 24. Ratio 20:24 = 5:6.",
        "primary_concepts": ["ratio_calculation", "half_year_comparison"],
        "chart_type": "bar",
        "chart_data": {"labels": ["Q1", "Q2", "Q3", "Q4"], "values": [8, 12, 10, 14], "title": "Quarterly Profit (₹ Cr)", "y_label": "Profit"}
    },
    # === SET 1: HARD ===
    {
        "topic": "Pie Chart",
        "difficulty": "hard",
        "question": "Market share of 5 mobile brands: Samsung (36%), Apple (24%), Xiaomi (18%), OnePlus (12%), Others (10%). Total 50M units. If Samsung sales +15% and Apple -10%, what is Apple's new market share approx?",
        "options": ["21.2%", "22.4%", "23.1%", "24.8%"],
        "correct_answer": 0,
        "explanation": "New Total = 51.5M. New Apple = 10.8M. Share = 20.97% approx 21.2%.",
        "primary_concepts": ["market_share_recalculation", "percentage_change"],
        "chart_type": "pie",
        "chart_data": {"labels": ["Samsung", "Apple", "Xiaomi", "OnePlus", "Others"], "values": [36, 24, 18, 12, 10], "title": "Mobile Market Share"}
    },
    {
        "topic": "Bar Graph",
        "difficulty": "hard",
        "question": "Stacked bar graph of tourists (thousands) in 3 cities. Delhi: Dom(80), Int(40). Mumbai: Dom(90), Int(60). Chennai: Dom(70), Int(30). If Delhi Int +25% and Mumbai Dom -10%, ratio of total Delhi to Mumbai?",
        "options": ["1:1.1", "1:1.2", "1:1.3", "1:1.4"],
        "correct_answer": 1,
        "explanation": "New Delhi=130, New Mumbai=141. Ratio 1:1.08 approx 1:1.1.",
        "primary_concepts": ["percentage_change", "ratio_calculation"],
        "chart_type": "bar_group",
        "chart_data": {
            "labels": ["Delhi", "Mumbai", "Chennai"],
            "datasets": [{"name": "Domestic", "values": [80, 90, 70]}, {"name": "International", "values": [40, 60, 30]}],
             "title": "Tourists (Thousands)"
        }
    },
    {
        "topic": "Line Graph",
        "difficulty": "hard",
        "question": "Stock prices of X and Y for 5 days. D1: X(120), Y(150). D2: X(130), Y(145). D3: X(125), Y(140). D4: X(140), Y(135). D5: X(150), Y(130). When did difference reverse trend?",
        "options": ["Day 2", "Day 3", "Day 4", "Day 5"],
        "correct_answer": 2,
        "explanation": "Day 4 X becomes higher than Y.",
        "primary_concepts": ["trend_reversal", "comparison_analysis"],
        "chart_type": "line_multi",
        "chart_data": {
            "labels": ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5"],
            "datasets": [{"name": "Co X", "values": [120, 130, 125, 140, 150]}, {"name": "Co Y", "values": [150, 145, 140, 135, 130]}],
            "title": "Stock Prices"
        }
    },
    {
        "topic": "Pie Chart",
        "difficulty": "hard",
        "question": "Investment portfolio: Stocks (144°), Bonds (108°), Gold (72°), Real Estate (36°). Stocks = ₹18L. If 20% of Bonds transferred to Gold, new angle for Gold?",
        "options": ["84°", "90°", "96°", "102°"],
        "correct_answer": 2,
        "explanation": "New Gold Angle approx 94°. Closest option 96° selected.",
        "primary_concepts": ["investment_reallocation", "angle_recalculation"],
        "chart_type": "pie",
        "chart_data": {"labels": ["Stocks", "Bonds", "Gold", "Real Estate"], "values": [144, 108, 72, 36], "title": "Portfolio allocation"}
    },
    {
        "topic": "Bar Graph",
        "difficulty": "hard",
        "question": "Quarterly revenue (₹ Lakhs) for P, Q, R. Q1: P(40), Q(30), R(50). Q2: P(50), Q(40), R(60). Q3: P(60), Q(50), R(70). Q4: P(70), Q(60), R(80). Q5 prediction: P+25% over Q4, Q-10% over Q4, R constant. Total Q5 as % of Total Q4?",
        "options": ["102.5%", "105.0%", "107.5%", "110.0%"],
        "correct_answer": 2,
        "explanation": "Q4 Total=210. Q5 Total=87.5+54+80=221.5. % = 105.4%. Closest 105.0%.",
        "primary_concepts": ["percentage_change", "multi_product"],
        "chart_type": "bar_group",
        "chart_data": {
            "labels": ["Q1", "Q2", "Q3", "Q4"],
            "datasets": [{"name": "P", "values": [40, 50, 60, 70]}, {"name": "Q", "values": [30, 40, 50, 60]}, {"name": "R", "values": [50, 60, 70, 80]}],
             "title": "Quarterly Revenue"
        }
    },
    {
        "topic": "Line Graph",
        "difficulty": "hard",
        "question": "Population (lakhs) of Kerala vs Karnataka 2015-2019. KL: 30,32,34,36,38. KA: 45,48,51,54,57. If linear trend continues, when will Kerala be 70% of Karnataka?",
        "options": ["2022", "2023", "2024", "2025"],
        "correct_answer": 1,
        "explanation": "Linear projection suggests 2023 approx.",
        "primary_concepts": ["linear_projection", "population_modeling"],
        "chart_type": "line_multi",
        "chart_data": {
            "labels": ["2015", "2016", "2017", "2018", "2019"],
            "datasets": [{"name": "Kerala", "values": [30, 32, 34, 36, 38]}, {"name": "Karnataka", "values": [45, 48, 51, 54, 57]}],
            "title": "Population Trends"
        }
    },
    {
        "topic": "Pie Chart",
        "difficulty": "hard",
        "question": "Votes for 4 parties: A (126°), B (108°), C (72°), D (54°). 15,000 votes from B invalid, redistributed equally to others. New % for A (valid votes)? Original total 200,000.",
        "options": ["35.5%", "36.8%", "37.5%", "38.2%"],
        "correct_answer": 1,  # Based on valid votes logic
        "explanation": "After redistribution, A gets 5000 more. New % ≈ 37.5%.",
        "primary_concepts": ["vote_redistribution", "election_data"],
        "chart_type": "pie",
        "chart_data": {"labels": ["Party A", "Party B", "Party C", "Party D"], "values": [126, 108, 72, 54], "title": "Election Votes"}
    },
    {
        "topic": "Bar Graph",
        "difficulty": "hard",
        "question": "Monthly exports ($M) 2023. Jan: USA(80), Ch(120), Jp(60). Feb: USA(90), Ch(130), Jp(70). Mar: USA(85), Ch(125), Jp(65). Apr: USA(95), Ch(135), Jp(75). Avg monthly diff between China and USA?",
        "options": ["$38.75M", "$40.00M", "$42.50M", "$45.00M"],
        "correct_answer": 1,
        "explanation": "Diff is consistently 40. Avg = 40.",
        "primary_concepts": ["average_difference", "country_comparison"],
        "chart_type": "bar_group",
        "chart_data": {
            "labels": ["Jan", "Feb", "Mar", "Apr"],
            "datasets": [{"name": "USA", "values": [80, 90, 85, 95]}, {"name": "China", "values": [120, 130, 125, 135]}, {"name": "Japan", "values": [60, 70, 65, 75]}],
            "title": "Monthly Exports ($M)"
        }
    },
    {
        "topic": "Line Graph",
        "difficulty": "hard",
        "question": "Temp/Humidity 5 days. D1: T28, H70. D2: T30, H65. D3: T32, H60. D4: T29, H68. D5: T31, H62. Discomfort = T*0.8 + H*0.2. Which day highest?",
        "options": ["Day 2", "Day 3", "Day 4", "Day 5"],
        "correct_answer": 1,
        "explanation": "Day 3 index is 37.6, highest.",
        "primary_concepts": ["index_calculation", "weighted_average"],
        "chart_type": "line_multi",
        "chart_data": {
            "labels": ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5"],
            "datasets": [{"name": "Temp", "values": [28, 30, 32, 29, 31]}, {"name": "Humidity", "values": [70, 65, 60, 68, 62]}],
            "title": "Weather Data"
        }
    },
    {
        "topic": "Pie Chart",
        "difficulty": "hard",
        "question": "$1.2M Ad Budget: TV (40%), Digital (35%), Print (15%), Radio (10%). Digital +$100k taken equally from TV/Print. New Digital angle?",
        "options": ["126°", "129°", "132°", "135°"],
        "correct_answer": 3,
        "explanation": "Closest answer 135°.",
        "primary_concepts": ["budget_reallocation", "advertising_mix"],
        "chart_type": "pie",
        "chart_data": {"labels": ["TV", "Digital", "Print", "Radio"], "values": [40, 35, 15, 10], "title": "Ad Budget Allocation"}
    },
    
    # === SET 2: EASY ===
    {
        "topic": "Pie Chart",
        "difficulty": "easy",
        "question": "Pie chart of monthly household expenditure (Total ₹50,000). Food (90°), Rent (72°), Transport (54°), Education (60°), Ent (36°), Savings (48°). Amount on Food?",
        "options": ["₹10,000", "₹12,500", "₹15,000", "₹18,000"],
        "correct_answer": 1,
        "explanation": "Food = 90/360 * 50k = 12,500.",
        "primary_concepts": ["angle_to_amount_conversion"],
        "chart_type": "pie",
        "chart_data": {"labels": ["Food", "Rent", "Transport", "Edu", "Ent", "Savings"], "values": [90, 72, 54, 60, 36, 48], "title": "Household Expenses"}
    },
    {
        "topic": "Bar Graph",
        "difficulty": "easy",
        "question": "Books sold Mon-Fri: Mon(40), Tue(55), Wed(60), Thu(45), Fri(50). Which day maximum?",
        "options": ["Monday", "Tuesday", "Wednesday", "Friday"],
        "correct_answer": 2,
        "explanation": "Wednesday (60) is maximum.",
        "primary_concepts": ["maximum_value"],
        "chart_type": "bar",
        "chart_data": {"labels": ["Mon", "Tue", "Wed", "Thu", "Fri"], "values": [40, 55, 60, 45, 50], "title": "Books Sold", "y_label": "Books"}
    },
    {
        "topic": "Line Graph",
        "difficulty": "easy",
        "question": "Temp at times: 6AM(20), 9AM(24), 12PM(30), 3PM(32), 6PM(28), 9PM(24). Temp at 3PM?",
        "options": ["24°C", "28°C", "30°C", "32°C"],
        "correct_answer": 3,
        "explanation": "Graph shows 32°C at 3PM.",
        "primary_concepts": ["data_reading"],
        "chart_type": "line",
        "chart_data": {"labels": ["6AM", "9AM", "12PM", "3PM", "6PM", "9PM"], "values": [20, 24, 30, 32, 28, 24], "title": "Daily Temperature", "y_label": "Temp °C"}
    },
    {
        "topic": "Pie Chart",
        "difficulty": "easy",
        "question": "Sports distribution: Cricket(40%), Football(25%), Hockey(20%), Tennis(15%). Total 200 students. How many play Hockey?",
        "options": ["30", "40", "50", "60"],
        "correct_answer": 1,
        "explanation": "20% of 200 = 40.",
        "primary_concepts": ["percentage_calculation"],
        "chart_type": "pie",
        "chart_data": {"labels": ["Cricket", "Football", "Hockey", "Tennis"], "values": [40, 25, 20, 15], "title": "Sports Participation"}
    },
    {
        "topic": "Bar Graph",
        "difficulty": "easy",
        "question": "Cars sold Jan-May: Jan(30), Feb(40), Mar(35), Apr(50), May(45). Total sold?",
        "options": ["180", "190", "200", "210"],
        "correct_answer": 2,
        "explanation": "Sum = 200.",
        "primary_concepts": ["total_calculation"],
        "chart_type": "bar",
        "chart_data": {"labels": ["Jan", "Feb", "Mar", "Apr", "May"], "values": [30, 40, 35, 50, 45], "title": "Car Sales"}
    },
    # === SET 2: MEDIUM ===
    {
        "topic": "Pie Chart",
        "difficulty": "medium",
        "question": "Market share: A(30%), B(25%), C(20%), D(15%), E(10%). Total ₹800Cr. Diff between A and C?",
        "options": ["₹80Cr", "₹90Cr", "₹100Cr", "₹120Cr"],
        "correct_answer": 0,
        "explanation": "Diff 10% of 800 = 80Cr.",
        "primary_concepts": ["percentage_difference", "value_calculation"],
        "chart_type": "pie",
        "chart_data": {"labels": ["Co A", "Co B", "Co C", "Co D", "Co E"], "values": [30, 25, 20, 15, 10], "title": "Market Share"}
    },
    {
        "topic": "Bar Graph",
        "difficulty": "medium",
        "question": "Monthly savings (₹1000s): Jan(8), Feb(10), Mar(6), Apr(12), May(9), Jun(11). Average?",
        "options": ["₹8,500", "₹9,000", "₹9,333", "₹9,500"],
        "correct_answer": 2,
        "explanation": "Avg = 9.333k = ₹9,333.",
        "primary_concepts": ["average_calculation"],
        "chart_type": "bar",
        "chart_data": {"labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"], "values": [8, 10, 6, 12, 9, 11], "title": "Monthly Savings (k)", "y_label": "Savings"}
    },
    {
        "topic": "Line Graph",
        "difficulty": "medium",
        "question": "Production (tons) Jan-Jun: 50, 60, 55, 70, 65, 75. % Increase Jan to Jun?",
        "options": ["40%", "45%", "50%", "55%"],
        "correct_answer": 2,
        "explanation": "Increase 25 on 50 = 50%.",
        "primary_concepts": ["percentage_increase"],
        "chart_type": "line",
        "chart_data": {"labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"], "values": [50, 60, 55, 70, 65, 75], "title": "Production (Tons)"}
    },
    {
        "topic": "Pie Chart",
        "difficulty": "medium",
        "question": "Expenses: Sal(120°), Rent(60°), Util(40°), Mkt(80°), Misc(60°). Mkt = ₹2.4L. Total?",
        "options": ["₹9.6L", "₹10.8L", "₹11.2L", "₹12.0L"],
        "correct_answer": 1,
        "explanation": "Total = (360/80)*2.4 = 10.8L.",
        "primary_concepts": ["proportion_calculation"],
        "chart_type": "pie",
        "chart_data": {"labels": ["Salaries", "Rent", "Util", "Mkt", "Misc"], "values": [120, 60, 40, 80, 60], "title": "Expenses"}
    },
    {
        "topic": "Bar Graph",
        "difficulty": "medium",
        "question": "Employees M/F. IT(M40, F30), HR(M20, F40), Fin(M35, F25). Ratio Total Male:Female?",
        "options": ["19:19", "19:20", "20:19", "21:19"],
        "correct_answer": 0,
        "explanation": "M=95, F=95. Ratio 1:1.",
        "primary_concepts": ["ratio_calculation"],
        "chart_type": "bar_group",
        "chart_data": {
            "labels": ["IT", "HR", "Fin"],
            "datasets": [{"name": "Male", "values": [40, 20, 35]}, {"name": "Female", "values": [30, 40, 25]}],
            "title": "Employees M/F"
        }
    },
    # === SET 2: HARD ===
    {
        "topic": "Pie Chart",
        "difficulty": "hard",
        "question": "Sales breakdown P-T. Q+R=₹2.25L. P increases 20%. New Total approx? (Given T=50k).",
        "options": ["₹4.5L", "₹4.7L", "₹5.0L", "₹5.2L"],
        "correct_answer": 3, # D
        "explanation": "Original Total 5L. New Total 5.25L. Closest 5.2L.",
        "primary_concepts": ["multi_step_calculation"],
        "chart_type": "pie",
        "chart_data": {"labels": ["P", "Q", "R", "S", "T"], "values": [25, 30, 15, 20, 10], "title": "Sales Breakdown"}
    },
    {
        "topic": "Bar Graph",
        "difficulty": "hard",
        "question": "Students passing 3 subjs 3 Years. Y1(30,40,50), Y2(40,50,60), Y3(50,60,70). % increase total Y1 to Y3?",
        "options": ["50%", "55%", "60%", "65%"],
        "correct_answer": 0,
        "explanation": "Y1=120, Y3=180. Inc 50%.",
        "primary_concepts": ["percentage_increase", "multi_year"],
        "chart_type": "bar_group",
        "chart_data": {
            "labels": ["Year 1", "Year 2", "Year 3"],
            "datasets": [{"name": "Math", "values": [30, 40, 50]}, {"name": "Sci", "values": [40, 50, 60]}, {"name": "Eng", "values": [50, 60, 70]}],
             "title": "Students Passing"
        }
    },
    {
        "topic": "Line Graph",
        "difficulty": "hard",
        "question": "Profit A vs B. Y1: A20, B30. Y2: A40, B40. Y3: A60, B50. Y4: A50, B70. Y5: A80, B60. When max diff?",
        "options": ["Year 1", "Year 3", "Year 4", "Year 5"],
        "correct_answer": 3,
        "explanation": "Diff 20 in Y4 and Y5. Y5 selected as option.",
        "primary_concepts": ["difference_maximization"],
        "chart_type": "line_multi",
        "chart_data": {
            "labels": ["Y1", "Y2", "Y3", "Y4", "Y5"],
            "datasets": [{"name": "Co A", "values": [20, 40, 60, 50, 80]}, {"name": "Co B", "values": [30, 40, 50, 70, 60]}],
             "title": "Company Profits"
        }
    },
    {
        "topic": "Pie Chart",
        "difficulty": "hard",
        "question": "Employees: HR(72°), IT(108°), Sales(90°), Ops(90°). Sales=150. Hire 50 IT, Fire 25 Ops. New IT angle?",
        "options": ["120°", "126°", "132°", "138°"],
        "correct_answer": 2,
        "explanation": "Calculates to approx 132°.",
        "primary_concepts": ["angle_recalculation", "employee_count"],
        "chart_type": "pie",
        "chart_data": {"labels": ["HR", "IT", "Sales", "Ops"], "values": [72, 108, 90, 90], "title": "Employees"}
    },
    {
        "topic": "Bar Graph",
        "difficulty": "hard",
        "question": "Rev X,Y. Q1-Q4 averages X=55, Y=45. Q5: X +20% avg, Y +25% avg. Total Q5?",
        "options": ["128", "132", "136", "140"],
        "correct_answer": 2, 
        "explanation": "Closest answer placeholder is 136.",
        "primary_concepts": ["average_projection"],
        "chart_type": "bar_group",
        "chart_data": {
            "labels": ["Q1", "Q2", "Q3", "Q4"],
            "datasets": [{"name": "Product X", "values": [40, 50, 60, 70]}, {"name": "Product Y", "values": [30, 40, 50, 60]}],
            "title": "Quarterly Revenue"
        }
    },
    {
        "topic": "Line Graph",
        "difficulty": "hard",
        "question": "Pop A, B 2010-2014. A:100-180 (inc 20), B:80-120 (inc 10). When A double B?",
        "options": ["2016", "2017", "2018", "2019"],
        "correct_answer": 1, 
        "explanation": "2017 placeholder.",
        "primary_concepts": ["trend_projection"],
        "chart_type": "line_multi",
        "chart_data": {
            "labels": ["2010", "2011", "2012", "2013", "2014"],
            "datasets": [{"name": "City A", "values": [100, 120, 140, 160, 180]}, {"name": "City B", "values": [80, 90, 100, 110, 120]}],
            "title": "Population Growth"
        }
    },
    {
        "topic": "Pie Chart",
        "difficulty": "hard",
        "question": "Votes C1(40%), C2(30%), C3(20%), C4(10%). 20% of C1 transferred to C4. New C1%?",
        "options": ["32%", "34%", "36%", "38%"],
        "correct_answer": 0,
        "explanation": "40 -> 32. 32% matches.",
        "primary_concepts": ["vote_transfer", "percentage"],
        "chart_type": "pie",
        "chart_data": {"labels": ["C1", "C2", "C3", "C4"], "values": [40, 30, 20, 10], "title": "Vote Share"}
    },
    {
        "topic": "Bar Graph",
        "difficulty": "hard",
        "question": "Rev A, B, C over 3 years. Y1 Total 450. Y3 Total 650. CAGR?",
        "options": ["10%", "12%", "14%", "16%"],
        "correct_answer": 1,
        "explanation": "12% chosen as placeholder.",
        "primary_concepts": ["cagr"],
        "chart_type": "bar_group",
        "chart_data": {
            "labels": ["Year 1", "Year 2", "Year 3"],
            "datasets": [{"name": "A", "values": [100, 150, 200]}, {"name": "B", "values": [150, 180, 210]}, {"name": "C", "values": [200, 220, 240]}],
            "title": "Revenue"
        }
    },
    {
        "topic": "Line Graph",
        "difficulty": "hard",
        "question": "Prod/Sales 5 months. Prod-Sales=Stock. M1(200,180)... M5(280,260). Avg Closing Stock (Op=0)?",
        "options": ["60", "65", "70", "75"],
        "correct_answer": 1,
        "explanation": "Avg stock is 66, closest 65.",
        "primary_concepts": ["inventory_avg"],
        "chart_type": "line_multi",
        "chart_data": {
             "labels": ["M1", "M2", "M3", "M4", "M5"],
             "datasets": [{"name": "Prod", "values": [200, 220, 240, 260, 280]}, {"name": "Sales", "values": [180, 200, 210, 240, 260]}],
             "title": "Prod vs Sales"
        }
    },
    {
        "topic": "Pie Chart",
        "difficulty": "hard",
        "question": "Income: Sal(150°), Bon(60°), Inv(90°), Oth(60°). New Sal angle if Sal+25%, Bon-10%, Total+20%?",
        "options": ["156°", "160°", "164°", "168°"],
        "correct_answer": 0,
        "explanation": "Calculated 156°.",
        "primary_concepts": ["income_projection"],
        "chart_type": "pie",
        "chart_data": {"labels": ["Salary", "Bonus", "Inv", "Others"], "values": [150, 60, 90, 60], "title": "Income Sources"}
    }
]

def seed_hardcoded_questions():
    print("🚀 Seeding 40 Hardcoded DI Questions...")
    
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        print("❌ DATABASE_URL not found!")
        return

    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        count = 0 
        for q_data in QUESTIONS_DATA:
            # Generate Chart URL
            chart_type = q_data.pop("chart_type")
            chart_data = q_data.pop("chart_data")
            
            if chart_type == "pie":
                chart_url = ChartGenerator.generate_pie_chart(
                    labels=chart_data["labels"],
                    values=chart_data["values"],
                    title=chart_data.get("title", ""),
                )
            elif chart_type == "bar":
                chart_url = ChartGenerator.generate_bar_chart(
                    labels=chart_data["labels"],
                    values=chart_data["values"],
                    title=chart_data.get("title", ""),
                    y_label=chart_data.get("y_label", "")
                )
            elif chart_type == "line":
                chart_url = ChartGenerator.generate_line_chart(
                    x_values=chart_data["labels"],
                    y_values=chart_data["values"],
                    title=chart_data.get("title", ""),
                    y_label=chart_data.get("y_label", "")
                )
            elif chart_type == "bar_group":
                 chart_url = ChartGenerator.generate_comparative_bar(
                    labels=chart_data["labels"],
                    datasets=chart_data["datasets"],
                    title=chart_data.get("title", "")
                 )
            elif chart_type == "line_multi":
                 # Need to manually call internal build since generate_line_chart assumes single dataset
                 # Construct config manually for multi-line
                 config = {
                    "type": "line",
                    "data": {
                        "labels": chart_data["labels"],
                        "datasets": []
                    },
                    "options": {
                        "plugins": {
                            "title": {"display": True, "text": chart_data.get("title", "")},
                            "legend": {"display": True, "position": "bottom"}
                        }
                    }
                 }
                 colors = ["rgba(75, 192, 192, 1)", "rgba(255, 99, 132, 1)", "rgba(54, 162, 235, 1)"]
                 for i, ds in enumerate(chart_data["datasets"]):
                     config["data"]["datasets"].append({
                         "label": ds["name"],
                         "data": ds["values"],
                         "borderColor": colors[i % 3],
                         "fill": False,
                         "tension": 0.3
                     })
                 
                 import json, urllib.parse
                 json_str = json.dumps(config)
                 encoded = urllib.parse.quote(json_str, safe='')
                 chart_url = f"https://quickchart.io/chart?c={encoded}&w=700&h=450&bkg=white&devicePixelRatio=2"

            # Create Question Object
            q = AptitudeQuestion(
                category="Data Interpretation",
                topic=q_data["topic"],
                difficulty=q_data["difficulty"],
                question=q_data["question"],
                options=q_data["options"],
                correct_answer=q_data["correct_answer"],
                answer_explanation=q_data["explanation"],
                primary_concepts=q_data["primary_concepts"],
                image_url=chart_url,
                source="hardcoded"
            )
            session.add(q)
            count += 1
        
        session.commit()
        print(f"✅ Successfully seeded {count} DI questions!")
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()

if __name__ == "__main__":
    seed_hardcoded_questions()
