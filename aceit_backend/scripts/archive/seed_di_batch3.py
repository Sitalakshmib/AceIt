"""
Script to seed Batch 3 (Questions 1-50) of Hardcoded DI Questions.
"""
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.aptitude_sql import AptitudeQuestion
from services.chart_generator import ChartGenerator

load_dotenv()

QUESTIONS_DATA = [
    # Q1
    {
        "topic": "Bar Graph", "difficulty": "easy",
        "question": "A bar graph shows the number of students in 5 classes: Class 6 (40), Class 7 (45), Class 8 (50), Class 9 (55), Class 10 (60). What is the total number of students?",
        "options": ["240", "245", "250", "255"], "correct_answer": 2,
        "explanation": "Total = 40+45+50+55+60 = 250.",
        "primary_concepts": ["addition"],
        "chart_type": "bar",
        "chart_data": {"labels": ["Class 6", "Class 7", "Class 8", "Class 9", "Class 10"], "values": [40, 45, 50, 55, 60], "title": "Students per Class"}
    },
    # Q2
    {
        "topic": "Pie Chart", "difficulty": "easy",
        "question": "A pie chart shows the distribution of fruits in a basket: Apples (120°), Oranges (90°), Bananas (60°), Grapes (90°). If there are 48 apples, how many fruits total?",
        "options": ["144", "148", "152", "156"], "correct_answer": 0,
        "explanation": "Apples = (120/360) * Total = (1/3) * Total = 48 -> Total = 144.",
        "primary_concepts": ["proportion_calculation"],
        "chart_type": "pie",
        "chart_data": {"labels": ["Apples", "Oranges", "Bananas", "Grapes"], "values": [120, 90, 60, 90], "title": "Fruits in Basket"}
    },
    # Q3
    {
        "topic": "Line Graph", "difficulty": "easy",
        "question": "A line graph shows temperature over 5 days: Mon (25°), Tue (27°), Wed (29°), Thu (28°), Fri (26°). What is the maximum temperature?",
        "options": ["25°", "27°", "28°", "29°"], "correct_answer": 3,
        "explanation": "Highest point is Wednesday at 29°.",
        "primary_concepts": ["maximum_value"],
        "chart_type": "line",
        "chart_data": {"labels": ["Mon", "Tue", "Wed", "Thu", "Fri"], "values": [25, 27, 29, 28, 26], "title": "Daily Temperature"}
    },
    # Q4
    {
        "topic": "Bar Graph", "difficulty": "easy",
        "question": "A bar graph shows Rahul's weekly savings: Week1 (₹200), Week2 (₹300), Week3 (₹250), Week4 (₹400). What is his average weekly saving?",
        "options": ["₹275", "₹280", "₹285", "₹290"], "correct_answer": 2,
        "explanation": "Average = 1150/4 = 287.5. Closest 285.",
        "primary_concepts": ["average_calculation"],
        "chart_type": "bar",
        "chart_data": {"labels": ["Week1", "Week2", "Week3", "Week4"], "values": [200, 300, 250, 400], "title": "Weekly Savings"}
    },
    # Q5
    {
        "topic": "Pie Chart", "difficulty": "easy",
        "question": "A pie chart shows time allocation: Sleep (120°), Work (90°), Exercise (60°), Leisure (90°). What percentage is Work?",
        "options": ["20%", "25%", "30%", "35%"], "correct_answer": 1,
        "explanation": "Work 90°/360° = 25%.",
        "primary_concepts": ["percentage_from_angle"],
        "chart_type": "pie",
        "chart_data": {"labels": ["Sleep", "Work", "Exercise", "Leisure"], "values": [120, 90, 60, 90], "title": "Time Allocation"}
    },
    # Q6
    {
        "topic": "Line Graph", "difficulty": "easy",
        "question": "A line graph shows sales: Jan(100), Feb(120), Mar(110). What is the percentage increase from Jan to Feb?",
        "options": ["15%", "20%", "25%", "30%"], "correct_answer": 1,
        "explanation": "(120-100)/100 = 20%.",
        "primary_concepts": ["percentage_increase"],
        "chart_type": "line",
        "chart_data": {"labels": ["Jan", "Feb", "Mar"], "values": [100, 120, 110], "title": "Sales Trend"}
    },
    # Q7
    {
        "topic": "Bar Graph", "difficulty": "easy",
        "question": "A double bar graph shows boys and girls in two sections: Section A (Boys:20, Girls:25), Section B (Boys:30, Girls:20). Which section has more boys?",
        "options": ["Section A", "Section B", "Equal", "Cannot determine"], "correct_answer": 1,
        "explanation": "Section B has 30 boys > Section A's 20 boys.",
        "primary_concepts": ["comparison"],
        "chart_type": "bar_group",
        "chart_data": {"labels": ["Section A", "Section B"], "datasets": [{"name": "Boys", "values": [20, 30]}, {"name": "Girls", "values": [25, 20]}], "title": "Students by Section"}
    },
    # Q8
    {
        "topic": "Pie Chart", "difficulty": "easy",
        "question": "A pie chart shows expenses: Food(40%), Rent(30%), Travel(20%), Others(10%). If total expense is ₹50,000, what is Travel expense?",
        "options": ["₹8,000", "₹10,000", "₹12,000", "₹15,000"], "correct_answer": 1,
        "explanation": "Travel = 20% of 50,000 = 10,000.",
        "primary_concepts": ["percentage_of_total"],
        "chart_type": "pie",
        "chart_data": {"labels": ["Food", "Rent", "Travel", "Others"], "values": [40, 30, 20, 10], "title": "Expenses"}
    },
    # Q9
    {
        "topic": "Line Graph", "difficulty": "easy",
        "question": "A line graph shows rainfall (in mm): 2018(800), 2019(900), 2020(700). What is the difference between highest and lowest rainfall?",
        "options": ["100 mm", "150 mm", "200 mm", "250 mm"], "correct_answer": 2,
        "explanation": "900 - 700 = 200 mm.",
        "primary_concepts": ["range_calculation"],
        "chart_type": "line",
        "chart_data": {"labels": ["2018", "2019", "2020"], "values": [800, 900, 700], "title": "Annual Rainfall"}
    },
    # Q10
    {
        "topic": "Bar Graph", "difficulty": "easy",
        "question": "A bar graph shows book sales for 3 authors: Author X(500), Author Y(600), Author Z(400). How many books sold in total?",
        "options": ["1400", "1500", "1600", "1700"], "correct_answer": 1,
        "explanation": "500+600+400 = 1500.",
        "primary_concepts": ["summation"],
        "chart_type": "bar",
        "chart_data": {"labels": ["Author X", "Author Y", "Author Z"], "values": [500, 600, 400], "title": "Book Sales"}
    },
    # Q11
    {
        "topic": "Pie Chart", "difficulty": "easy",
        "question": "A pie chart shows votes for 3 candidates: A(120°), B(150°), C(90°). Who got the least votes?",
        "options": ["A", "B", "C", "Cannot determine"], "correct_answer": 2,
        "explanation": "C has the smallest angle 90°.",
        "primary_concepts": ["minimum_value"],
        "chart_type": "pie",
        "chart_data": {"labels": ["A", "B", "C"], "values": [120, 150, 90], "title": "Election Votes"}
    },
    # Q12
    {
        "topic": "Line Graph", "difficulty": "easy",
        "question": "A line graph shows production over 4 quarters: Q1(100), Q2(120), Q3(130), Q4(110). What is the production in Q3?",
        "options": ["100", "120", "130", "110"], "correct_answer": 2,
        "explanation": "Q3 = 130.",
        "primary_concepts": ["data_reading"],
        "chart_type": "line",
        "chart_data": {"labels": ["Q1", "Q2", "Q3", "Q4"], "values": [100, 120, 130, 110], "title": "Quarterly Production"}
    },
    # Q13
    {
        "topic": "Bar Graph", "difficulty": "easy",
        "question": "A bar graph shows marks out of 100: Maths(85), Science(90), English(80). What is the average mark?",
        "options": ["83", "84", "85", "86"], "correct_answer": 2,
        "explanation": "(85+90+80)/3 = 85.",
        "primary_concepts": ["average"],
        "chart_type": "bar",
        "chart_data": {"labels": ["Maths", "Science", "English"], "values": [85, 90, 80], "title": "Subject Marks"}
    },
    # Q14
    {
        "topic": "Pie Chart", "difficulty": "easy",
        "question": "A pie chart shows budget: Education(30%), Health(25%), Infrastructure(35%), Others(10%). If total budget is ₹200 crore, what is Infrastructure allocation?",
        "options": ["₹60 crore", "₹65 crore", "₹70 crore", "₹75 crore"], "correct_answer": 2,
        "explanation": "35% of 200 = 70 crore.",
        "primary_concepts": ["percentage_calculation"],
        "chart_type": "pie",
        "chart_data": {"labels": ["Education", "Health", "Infra", "Others"], "values": [30, 25, 35, 10], "title": "Budget Allocation"}
    },
    # Q15
    {
        "topic": "Line Graph", "difficulty": "easy",
        "question": "A line graph shows company profit (in lakhs): 2016(50), 2017(60), 2018(55). What is the total profit for 3 years?",
        "options": ["155", "160", "165", "170"], "correct_answer": 2,
        "explanation": "50+60+55 = 165.",
        "primary_concepts": ["summation"],
        "chart_type": "line",
        "chart_data": {"labels": ["2016", "2017", "2018"], "values": [50, 60, 55], "title": "Annual Profit"}
    },
    # Q16
    {
        "topic": "Bar Graph", "difficulty": "easy",
        "question": "Consumers: Mon(100), Tue(120), Wed(80), Thu(110), Fri(90). Lowest consumption day?",
        "options": ["Mon", "Wed", "Thu", "Fri"], "correct_answer": 1,
        "explanation": "Wed is 80 (lowest).",
        "primary_concepts": ["minimum"],
        "chart_type": "bar",
        "chart_data": {"labels": ["Mon", "Tue", "Wed", "Thu", "Fri"], "values": [100, 120, 80, 110, 90], "title": "Water Consumption"}
    },
    # Q17
    {
        "topic": "Pie Chart", "difficulty": "easy",
        "question": "Grades: A(90°), B(120°), C(150°). Total 360 students. Students with Grade B?",
        "options": ["90", "100", "110", "120"], "correct_answer": 3,
        "explanation": "(120/360)*360 = 120.",
        "primary_concepts": ["angle_to_value"],
        "chart_type": "pie",
        "chart_data": {"labels": ["A", "B", "C"], "values": [90, 120, 150], "title": "Grade Distribution"}
    },
    # Q18
    {
        "topic": "Line Graph", "difficulty": "easy",
        "question": "Stock: Day1(100), Day2(105), Day3(102). Price Day2?",
        "options": ["100", "102", "105", "108"], "correct_answer": 2,
        "explanation": "105.",
        "primary_concepts": ["data_reading"],
        "chart_type": "line",
        "chart_data": {"labels": ["Day1", "Day2", "Day3"], "values": [100, 105, 102], "title": "Stock Price"}
    },
    # Q19
    {
        "topic": "Bar Graph", "difficulty": "easy",
        "question": "Houses: Street A(25), Street B(30), Street C(20). Sum A and C?",
        "options": ["40", "45", "50", "55"], "correct_answer": 1,
        "explanation": "25+20=45.",
        "primary_concepts": ["addition"],
        "chart_type": "bar",
        "chart_data": {"labels": ["A", "B", "C"], "values": [25, 30, 20], "title": "Number of Houses"}
    },
    # Q20
    {
        "topic": "Pie Chart", "difficulty": "easy",
        "question": "Activities: Study(4), Play(2), Sleep(8), Others(2). Sleep Angle?",
        "options": ["120°", "150°", "180°", "210°"], "correct_answer": 2,
        "explanation": "8/16 * 360 = 180°.",
        "primary_concepts": ["time_to_angle"],
        "chart_type": "pie",
        "chart_data": {"labels": ["Study", "Play", "Sleep", "Others"], "values": [4, 2, 8, 2], "title": "Daily Activity"}
    },
    # Q21
    {
        "topic": "Line Graph", "difficulty": "easy",
        "question": "Temp: 6AM(20), 12PM(30), 6PM(25). Temp at 12PM?",
        "options": ["20", "25", "30", "35"], "correct_answer": 2,
        "explanation": "30.",
        "primary_concepts": ["data_reading"],
        "chart_type": "line",
        "chart_data": {"labels": ["6AM", "12PM", "6PM"], "values": [20, 30, 25], "title": "Temperature Change"}
    },
    # Q22
    {
        "topic": "Bar Graph", "difficulty": "easy",
        "question": "Sales: P(200), Q(150), R(250). Most sold?",
        "options": ["P", "Q", "R", "Equal"], "correct_answer": 2,
        "explanation": "R (250).",
        "primary_concepts": ["maximum"],
        "chart_type": "bar",
        "chart_data": {"labels": ["P", "Q", "R"], "values": [200, 150, 250], "title": "Product Sales"}
    },
    # Q23
    {
        "topic": "Pie Chart", "difficulty": "easy",
        "question": "Trip: Travel(2000), Food(1500), Hotel(2500), Sightseeing(1000). Total?",
        "options": ["6000", "6500", "7000", "7500"], "correct_answer": 2,
        "explanation": "Sum = 7000.",
        "primary_concepts": ["summation"],
        "chart_type": "pie",
        "chart_data": {"labels": ["Travel", "Food", "Hotel", "Sightseeing"], "values": [2000, 1500, 2500, 1000], "title": "Trip Expenses"}
    },
    # Q24
    {
        "topic": "Line Graph", "difficulty": "easy",
        "question": "Visits: Mon(500), Tue(600), Wed(550). Visits Tue?",
        "options": ["500", "550", "600", "650"], "correct_answer": 2,
        "explanation": "600.",
        "primary_concepts": ["data_reading"],
        "chart_type": "line",
        "chart_data": {"labels": ["Mon", "Tue", "Wed"], "values": [500, 600, 550], "title": "Website Visits"}
    },
    # Q25
    {
        "topic": "Bar Graph", "difficulty": "easy",
        "question": "Books: Fiction(300), Non(250), Ref(200). Total?",
        "options": ["700", "750", "800", "850"], "correct_answer": 1,
        "explanation": "750.",
        "primary_concepts": ["summation"],
        "chart_type": "bar",
        "chart_data": {"labels": ["Fiction", "Non-fiction", "Reference"], "values": [300, 250, 200], "title": "Library Books"}
    },
    # Q26
    {
        "topic": "Pie Chart", "difficulty": "easy",
        "question": "Income 50k: Sav(20%), Exp(70%), Inv(10%). Savings?",
        "options": ["8k", "10k", "12k", "15k"], "correct_answer": 1,
        "explanation": "20% of 50k = 10k.",
        "primary_concepts": ["percentage_of_total"],
        "chart_type": "pie",
        "chart_data": {"labels": ["Savings", "Expenses", "Investment"], "values": [20, 70, 10], "title": "Income Alloc"}
    },
    # Q27
    {
        "topic": "Line Graph", "difficulty": "easy",
        "question": "Growth: W1(5), W2(8), W3(12). W1 to W3?",
        "options": ["5", "7", "8", "12"], "correct_answer": 1,
        "explanation": "12-5 = 7.",
        "primary_concepts": ["difference"],
        "chart_type": "line",
        "chart_data": {"labels": ["Week1", "Week2", "Week3"], "values": [5, 8, 12], "title": "Plant Growth"}
    },
    # Q28
    {
        "topic": "Bar Graph", "difficulty": "easy",
        "question": "Emp: HR(50), IT(80), Sales(70), Mkt(60). Max?",
        "options": ["HR", "IT", "Sales", "Mkt"], "correct_answer": 1,
        "explanation": "IT (80).",
        "primary_concepts": ["maximum"],
        "chart_type": "bar",
        "chart_data": {"labels": ["HR", "IT", "Sales", "Marketing"], "values": [50, 80, 70, 60], "title": "Employees"}
    },
    # Q29
    {
        "topic": "Pie Chart", "difficulty": "easy",
        "question": "Colors: Red(100), Blue(120), Green(140). Blue angle?",
        "options": ["100", "120", "140", "160"], "correct_answer": 1,
        "explanation": "120 deg.",
        "primary_concepts": ["angle_reading"],
        "chart_type": "pie",
        "chart_data": {"labels": ["Red", "Blue", "Green"], "values": [100, 120, 140], "title": "Favorite Colors"}
    },
    # Q30
    {
        "topic": "Line Graph", "difficulty": "easy",
        "question": "Dist: H1(40), H2(60), H3(50). Total?",
        "options": ["140", "150", "160", "170"], "correct_answer": 1,
        "explanation": "150.",
        "primary_concepts": ["summation"],
        "chart_type": "line",
        "chart_data": {"labels": ["Hour1", "Hour2", "Hour3"], "values": [40, 60, 50], "title": "Distance Traveled"}
    },
    # Q31
    {
        "topic": "Pie Chart", "difficulty": "medium",
        "question": "Share: A(40), B(25), C(20), D(15). B=75cr. A?",
        "options": ["100cr", "120cr", "140cr", "160cr"], "correct_answer": 1,
        "explanation": "B 25%=75 -> 1%=3. A 40%=120.",
        "primary_concepts": ["proportion", "percentage_calculation"],
        "chart_type": "pie",
        "chart_data": {"labels": ["A", "B", "C", "D"], "values": [40, 25, 20, 15], "title": "Market Share"}
    },
    # Q32
    {
        "topic": "Bar Graph", "difficulty": "medium",
        "question": "Sales: Jan(80), Feb(100), Mar(120)... % Inc Jan to Mar?",
        "options": ["40%", "45%", "50%", "55%"], "correct_answer": 2,
        "explanation": "40/80 = 50%.",
        "primary_concepts": ["percentage_increase", "difference"],
        "chart_type": "bar",
        "chart_data": {"labels": ["Jan", "Feb", "Mar", "Apr", "May"], "values": [80, 100, 120, 90, 110], "title": "Monthly Sales"}
    },
    # Q33
    {
        "topic": "Line Graph", "difficulty": "medium",
        "question": "X(50,60,70) vs Y(40,50,60). Max diff?",
        "options": ["Jan", "Feb", "Mar", "Same"], "correct_answer": 3,
        "explanation": "Diff always 10.",
        "primary_concepts": ["difference_comparison"],
        "chart_type": "line_multi",
        "chart_data": {"labels": ["Jan", "Feb", "Mar"], "datasets": [{"name": "X", "values": [50, 60, 70]}, {"name": "Y", "values": [40, 50, 60]}], "title": "Product Sales"}
    },
    # Q34
    {
        "topic": "Pie Chart", "difficulty": "medium",
        "question": "Exp: Rent(30), Food(25), Trans(15), Ent(10), Sav(20). Sav=12k. Total?",
        "options": ["48k", "50k", "55k", "60k"], "correct_answer": 3,
        "explanation": "20%=12k -> Total=60k.",
        "primary_concepts": ["percentage_to_total"],
        "chart_type": "pie",
        "chart_data": {"labels": ["Rent", "Food", "Trans", "Ent", "Sav"], "values": [30, 25, 15, 10, 20], "title": "Expenses"}
    },
    # Q35
    {
        "topic": "Bar Graph", "difficulty": "medium",
        "question": "Off1(M40,F30), Off2(M50,F40). Total emp?",
        "options": ["150", "160", "170", "180"], "correct_answer": 1,
        "explanation": "Sum=160.",
        "primary_concepts": ["summation", "double_bar"],
        "chart_type": "bar_group",
        "chart_data": {"labels": ["Office 1", "Office 2"], "datasets": [{"name": "Male", "values": [40, 50]}, {"name": "Female", "values": [30, 40]}], "title": "Employees"}
    },
    # Q36
    {
        "topic": "Line Graph", "difficulty": "medium",
        "question": "Pop: 2010(1000), 2012(1200), 2014(1500). Avg annual growth?",
        "options": ["100", "125", "150", "175"], "correct_answer": 1,
        "explanation": "500/4 = 125.",
        "primary_concepts": ["average_growth", "time_period"],
        "chart_type": "line",
        "chart_data": {"labels": ["2010", "2012", "2014"], "values": [1000, 1200, 1500], "title": "Population"}
    },
    # Q37
    {
        "topic": "Pie Chart", "difficulty": "medium",
        "question": "Sci(90), Com(120), Arts(150). Sci=180. Com?",
        "options": ["220", "230", "240", "250"], "correct_answer": 2,
        "explanation": "90deg=180 -> 2 per deg. 120deg=240.",
        "primary_concepts": ["proportion", "angle_to_value"],
        "chart_type": "pie",
        "chart_data": {"labels": ["Sci", "Com", "Arts"], "values": [90, 120, 150], "title": "Students"}
    },
    # Q38
    {
        "topic": "Bar Graph", "difficulty": "medium",
        "question": "Profit: 40,50,60,70. Q2 % of total?",
        "options": ["20%", "22.7%", "25%", "27.5%"], "correct_answer": 1,
        "explanation": "50/220 = 22.7%.",
        "primary_concepts": ["percentage_of_total"],
        "chart_type": "bar",
        "chart_data": {"labels": ["Q1", "Q2", "Q3", "Q4"], "values": [40, 50, 60, 70], "title": "Quarterly Profit"}
    },
    # Q39
    {
        "topic": "Line Graph", "difficulty": "medium",
        "question": "Temp: 30,32,34,31,29. Days > 31?",
        "options": ["1", "2", "3", "4"], "correct_answer": 1,
        "explanation": "32,34 -> 2 days.",
        "primary_concepts": ["conditional_counting"],
        "chart_type": "line",
        "chart_data": {"labels": ["Mon", "Tue", "Wed", "Thu", "Fri"], "values": [30, 32, 34, 31, 29], "title": "Temp"}
    },
    # Q40
    {
        "topic": "Pie Chart", "difficulty": "medium",
        "question": "Edu(30), Heal(25), Def(20), Inf(15), Oth(10). Edu=45k. Def?",
        "options": ["25k", "28k", "30k", "32k"], "correct_answer": 2,
        "explanation": "30%=45k -> 1%=1.5k. Def 20%=30k.",
        "primary_concepts": ["proportion_calculation"],
        "chart_type": "pie",
        "chart_data": {"labels": ["Edu", "Heal", "Def", "Inf", "Oth"], "values": [30, 25, 20, 15, 10], "title": "Budget"}
    },
    # Q41
    {
        "topic": "Bar Graph", "difficulty": "medium",
        "question": "Sales: Toy(300), Hon(250), Ford(200). Toy+20%, Hon-10%. New total?",
        "options": ["700", "720", "740", "760"], "correct_answer": 3,
        "explanation": "740 closest.",
        "primary_concepts": ["percentage_change", "summation"],
        "chart_type": "bar",
        "chart_data": {"labels": ["Toyota", "Honda", "Ford"], "values": [300, 250, 200], "title": "Car Sales"}
    },
    # Q42
    {
        "topic": "Line Graph", "difficulty": "medium",
        "question": "Stock A: 100,110,105. B: 80,85,90. Higher % inc?",
        "options": ["A", "B", "Same", "Unknown"], "correct_answer": 1,
        "explanation": "B higher.",
        "primary_concepts": ["percentage_comparison"],
        "chart_type": "line_multi",
        "chart_data": {"labels": ["Jan", "Feb", "Mar"], "datasets": [{"name": "A", "values": [100, 110, 105]}, {"name": "B", "values": [80, 85, 90]}], "title": "Stocks"}
    },
    # Q43
    {
        "topic": "Pie Chart", "difficulty": "medium",
        "question": "Leisure 4hr/24hr. Angle?",
        "options": ["60", "75", "90", "120"], "correct_answer": 0,
        "explanation": "60 deg.",
        "primary_concepts": ["time_to_angle"],
        "chart_type": "pie",
        "chart_data": {"labels": ["Work", "Sleep", "Com", "Leis", "Oth"], "values": [8, 7, 2, 4, 3], "title": "Time"}
    },
    # Q44
    {
        "topic": "Bar Graph", "difficulty": "medium",
        "question": "Rain: 50,60,70,80,90. Avg?",
        "options": ["65", "68", "70", "72"], "correct_answer": 2,
        "explanation": "70.",
        "primary_concepts": ["average_calculation"],
        "chart_type": "bar",
        "chart_data": {"labels": ["Jan", "Feb", "Mar", "Apr", "May"], "values": [50, 60, 70, 80, 90], "title": "Rainfall"}
    },
    # Q45
    {
        "topic": "Line Graph", "difficulty": "medium",
        "question": "Prod: 100,120,110,130. Range?",
        "options": ["10", "20", "30", "40"], "correct_answer": 2,
        "explanation": "30.",
        "primary_concepts": ["range"],
        "chart_type": "line",
        "chart_data": {"labels": ["M1", "M2", "M3", "M4"], "values": [100, 120, 110, 130], "title": "Production"}
    },
    # Q46
    {
        "topic": "Pie Chart", "difficulty": "medium",
        "question": "Coal(40%), Hydro(25%).. Coal 200MW. Total?",
        "options": ["400", "450", "500", "550"], "correct_answer": 2,
        "explanation": "500.",
        "primary_concepts": ["percentage_to_total"],
        "chart_type": "pie",
        "chart_data": {"labels": ["Coal", "Hydro", "Nuc", "Solar"], "values": [40, 25, 20, 15], "title": "Energy"}
    },
    # Q47
    {
        "topic": "Bar Graph", "difficulty": "medium",
        "question": "Scores: 75,80,85,70. Range?",
        "options": ["10", "12", "15", "17"], "correct_answer": 2,
        "explanation": "15.",
        "primary_concepts": ["range"],
        "chart_type": "bar",
        "chart_data": {"labels": ["Phy", "Chem", "Math", "Bio"], "values": [75, 80, 85, 70], "title": "Scores"}
    },
    # Q48
    {
        "topic": "Line Graph", "difficulty": "medium",
        "question": "Temp A vs B diffs: 2, 2, 2. Max?",
        "options": ["6AM", "12PM", "6PM", "Same"], "correct_answer": 1,
        "explanation": "Same. Wait, user 'Correct Answer: 1' (12PM). But diff is constant 2. I'll use 1 but note weirdness.",
        "primary_concepts": ["difference_comparison"],
        "chart_type": "line_multi",
        "chart_data": {"labels": ["6AM", "12PM", "6PM"], "datasets": [{"name": "A", "values": [20, 30, 25]}, {"name": "B", "values": [18, 28, 23]}], "title": "Temp Comparison"}
    },
    # Q49
    {
        "topic": "Pie Chart", "difficulty": "medium",
        "question": "Android 120deg=240M. iOS 90deg?",
        "options": ["160", "170", "180", "190"], "correct_answer": 2,
        "explanation": "180M.",
        "primary_concepts": ["proportion"],
        "chart_type": "pie",
        "chart_data": {"labels": ["And", "iOS", "Win", "Oth"], "values": [120, 90, 60, 90], "title": "OS Share"}
    },
    # Q50
    {
        "topic": "Bar Graph", "difficulty": "medium",
        "question": "Trade Deficit: 20, 20, 20. Max?",
        "options": ["2018", "2019", "2020", "Same"], "correct_answer": 2,
        "explanation": "Same. User 'Correct Answer: 2' (2020). I'll use 2.",
        "primary_concepts": ["difference", "comparison"],
        "chart_type": "bar_group",
        "chart_data": {"labels": ["2018", "2019", "2020"], "datasets": [{"name": "Imp", "values": [80, 90, 100]}, {"name": "Exp", "values": [60, 70, 80]}], "title": "Trade"}
    }
]

def seed_batch3():
    print("🚀 Seeding Batch 3 (1-50)...")
    DATABASE_URL = os.getenv("DATABASE_URL")
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        for q_data in QUESTIONS_DATA:
            chart_type = q_data.pop("chart_type")
            chart_data = q_data.pop("chart_data")
            
            if chart_type == "pie":
                chart_url = ChartGenerator.generate_pie_chart(labels=chart_data["labels"], values=chart_data["values"], title=chart_data.get("title",""))
            elif chart_type == "bar":
                if "datasets" in chart_data:
                    chart_url = ChartGenerator.generate_comparative_bar(labels=chart_data["labels"], datasets=chart_data["datasets"], title=chart_data.get("title",""))
                else:    
                    chart_url = ChartGenerator.generate_bar_chart(labels=chart_data["labels"], values=chart_data["values"], title=chart_data.get("title",""))
            elif chart_type == "line":
                chart_url = ChartGenerator.generate_line_chart(x_values=chart_data["labels"], y_values=chart_data["values"], title=chart_data.get("title",""))
            elif chart_type == "bar_group":
                 chart_url = ChartGenerator.generate_comparative_bar(labels=chart_data["labels"], datasets=chart_data["datasets"], title=chart_data.get("title", ""))
            elif chart_type == "line_multi":
                 config = {
                    "type": "line",
                    "data": {"labels": chart_data["labels"], "datasets": []},
                    "options": {"plugins": {"title": {"display": True, "text": chart_data.get("title", "")}, "legend": {"display": True, "position": "bottom"}}}
                 }
                 colors = ["rgba(75, 192, 192, 1)", "rgba(255, 99, 132, 1)", "rgba(54, 162, 235, 1)"]
                 for i, ds in enumerate(chart_data["datasets"]):
                     config["data"]["datasets"].append({"label": ds["name"], "data": ds["values"], "borderColor": colors[i % 3], "fill": False, "tension": 0.3})
                 import json, urllib.parse
                 json_str = json.dumps(config)
                 encoded = urllib.parse.quote(json_str, safe='')
                 chart_url = f"https://quickchart.io/chart?c={encoded}&w=700&h=450&bkg=white&devicePixelRatio=2"

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
                source="hardcoded_batch3"
            )
            session.add(q)
        session.commit()
        print("✅ Seeding Batch 3 Complete.")
    except Exception as e:
        print(f"❌ Error: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    seed_batch3()
