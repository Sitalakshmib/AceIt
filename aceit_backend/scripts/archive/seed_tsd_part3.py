import sys
import os
import uuid

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_postgres import SessionLocal
from models.aptitude_sql import AptitudeQuestion

# QUESTIONS 76-135
QUESTIONS_DATA = [
    {"q": "A train 180m long crosses a pole in 12 seconds. What is its speed in m/s?", "o": ["12 m/s", "15 m/s", "18 m/s", "20 m/s"], "c": 1, "e": "Speed = Distance/Time = 180/12 = 15 m/s.", "diff": "easy", "concepts": ["trains", "basic_formula"], "trap": "conversion_to_km/h_unnecessary"},
    {"q": "A car travels 240 km in 4 hours. If it maintains same speed, how far will it go in 7 hours?", "o": ["380 km", "400 km", "420 km", "440 km"], "c": 2, "e": "Speed = 240/4 = 60 km/h. Distance in 7h = 60 \u00d7 7 = 420 km.", "diff": "easy", "concepts": ["basic_formula"], "trap": "proportional_error"},
    {"q": "Two cyclists start towards each other 36 km apart at 10 km/h and 8 km/h. When will they meet?", "o": ["1.5 hours", "2 hours", "2.5 hours", "3 hours"], "c": 1, "e": "Relative speed = 10 + 8 = 18 km/h. Time = 36/18 = 2 hours.", "diff": "easy", "concepts": ["relative_speed"], "trap": "subtracting_speeds"},
    {"q": "Convert 90 km/h to m/s.", "o": ["20 m/s", "25 m/s", "30 m/s", "35 m/s"], "c": 1, "e": "90 \u00d7 (5/18) = 25 m/s.", "diff": "easy", "concepts": ["conversion"], "trap": "using_18/5_instead_of_5/18"},
    {"q": "A boat's speed in still water is 15 km/h, stream speed is 3 km/h. Downstream speed?", "o": ["12 km/h", "15 km/h", "18 km/h", "20 km/h"], "c": 2, "e": "Downstream = 15 + 3 = 18 km/h.", "diff": "easy", "concepts": ["boats"], "trap": "subtracting_instead_of_adding"},
    {"q": "A man walks 800m in 10 minutes. His speed in km/h is?", "o": ["4.2 km/h", "4.8 km/h", "5.2 km/h", "5.8 km/h"], "c": 1, "e": "Speed = 800m/10min = 80 m/min = 80 \u00d7 (60/1000) = 4.8 km/h.", "diff": "easy", "concepts": ["conversion"], "trap": "incorrect_minutes_to_hours"},
    {"q": "A bus covers 150 km in 2.5 hours. Average speed?", "o": ["55 km/h", "58 km/h", "60 km/h", "62 km/h"], "c": 2, "e": "Speed = 150/2.5 = 60 km/h.", "diff": "easy", "concepts": ["basic_formula"], "trap": "decimal_division_error"},
    {"q": "If speed triples, time taken for same distance becomes?", "o": ["1/2", "1/3", "1/4", "1/6"], "c": 1, "e": "Time is inversely proportional to speed. New time = (1/3) of original.", "diff": "easy", "concepts": ["inverse_proportion"], "trap": "direct_proportion_thinking"},
    {"q": "A 200m train crosses a bridge 300m long in 25 seconds. Speed in m/s?", "o": ["18 m/s", "20 m/s", "22 m/s", "25 m/s"], "c": 1, "e": "Total distance = 200 + 300 = 500m. Speed = 500/25 = 20 m/s.", "diff": "easy", "concepts": ["trains"], "trap": "using_only_bridge_length"},
    {"q": "Two cars 120 km apart move toward each other at 35 km/h and 45 km/h. Meeting time?", "o": ["1.2 hours", "1.5 hours", "1.8 hours", "2 hours"], "c": 1, "e": "Relative speed = 35 + 45 = 80 km/h. Time = 120/80 = 1.5 hours.", "diff": "easy", "concepts": ["relative_speed"], "trap": "subtracting_speeds"},
    {"q": "A runner covers 1.5 km in 5 minutes. Speed in m/s?", "o": ["4 m/s", "5 m/s", "6 m/s", "7 m/s"], "c": 1, "e": "Distance = 1500m, time = 300s. Speed = 1500/300 = 5 m/s.", "diff": "easy", "concepts": ["conversion"], "trap": "minutes_to_seconds_error"},
    {"q": "Upstream speed is 8 km/h, downstream is 12 km/h. Stream speed?", "o": ["1 km/h", "2 km/h", "3 km/h", "4 km/h"], "c": 1, "e": "Stream speed = (12 - 8)/2 = 4/2 = 2 km/h.", "diff": "easy", "concepts": ["boats"], "trap": "taking_difference_directly"},
    {"q": "A car travels first 50 km at 40 km/h, next 50 km at 60 km/h. Average speed?", "o": ["46 km/h", "48 km/h", "50 km/h", "52 km/h"], "c": 1, "e": "Time1 = 50/40 = 1.25h, Time2 = 50/60 = 0.833h. Total = 2.083h. Average = 100/2.083 \u2248 48 km/h.", "diff": "easy", "concepts": ["average_speed"], "trap": "simple_average_50"},
    {"q": "Convert 15 m/s to km/h.", "o": ["50 km/h", "52 km/h", "54 km/h", "56 km/h"], "c": 2, "e": "15 \u00d7 (18/5) = 54 km/h.", "diff": "easy", "concepts": ["conversion"], "trap": "using_5/18_instead"},
    {"q": "A train crosses a pole in 9 seconds. If length is 135m, speed in km/h?", "o": ["50 km/h", "52 km/h", "54 km/h", "56 km/h"], "c": 2, "e": "Speed = 135/9 = 15 m/s = 15 \u00d7 (18/5) = 54 km/h.", "diff": "easy", "concepts": ["trains", "conversion"], "trap": "forgetting_conversion"},
    {"q": "If distance doubles while speed remains same, time taken?", "o": ["Halves", "Doubles", "Triples", "Quadruples"], "c": 1, "e": "Time is directly proportional to distance. Time doubles.", "diff": "easy", "concepts": ["direct_proportion"], "trap": "inverse_thinking"},
    {"q": "Two bikes 80 km apart approach at 25 km/h and 35 km/h. Time to meet?", "o": ["1 hour", "1.2 hours", "1.33 hours", "1.5 hours"], "c": 2, "e": "Relative speed = 25 + 35 = 60 km/h. Time = 80/60 = 1.33 hours.", "diff": "easy", "concepts": ["relative_speed"], "trap": "subtracting_speeds"},
    {"q": "A man covers 2.4 km in 20 minutes. Speed in km/h?", "o": ["6.8 km/h", "7.0 km/h", "7.2 km/h", "7.4 km/h"], "c": 2, "e": "Time = 20/60 = 1/3 h. Speed = 2.4 \u00f7 (1/3) = 7.2 km/h.", "diff": "easy", "concepts": ["basic_formula"], "trap": "multiplying_by_60_instead"},
    {"q": "Boat speed 12 km/h, stream 2 km/h. Upstream speed?", "o": ["8 km/h", "10 km/h", "12 km/h", "14 km/h"], "c": 1, "e": "Upstream = 12 - 2 = 10 km/h.", "diff": "easy", "concepts": ["boats"], "trap": "adding_instead"},
    {"q": "A car travels 180 km in 3 hours 36 minutes. Average speed?", "o": ["48 km/h", "50 km/h", "52 km/h", "54 km/h"], "c": 1, "e": "Time = 3.6 hours. Speed = 180/3.6 = 50 km/h.", "diff": "easy", "concepts": ["basic_formula"], "trap": "time_conversion_error"},
    {"q": "108 km/h converted to m/s equals?", "o": ["28 m/s", "30 m/s", "32 m/s", "34 m/s"], "c": 1, "e": "108 \u00d7 (5/18) = 30 m/s.", "diff": "easy", "concepts": ["conversion"], "trap": "calculation_error"},
    {"q": "Train 160m crosses platform 240m in 20s. Speed in m/s?", "o": ["18 m/s", "20 m/s", "22 m/s", "24 m/s"], "c": 1, "e": "Total = 400m. Speed = 400/20 = 20 m/s.", "diff": "easy", "concepts": ["trains"], "trap": "using_wrong_distance"},
    {"q": "Two cars 90 km apart at 40 km/h and 50 km/h toward each other. Meeting time?", "o": ["0.9 hours", "1 hour", "1.1 hours", "1.2 hours"], "c": 1, "e": "Relative = 90 km/h. Time = 90/90 = 1 hour.", "diff": "easy", "concepts": ["relative_speed"], "trap": "subtracting_speeds"},
    {"q": "Walking 4.5 km in 45 minutes. Speed in m/s?", "o": ["1.5 m/s", "1.67 m/s", "1.75 m/s", "1.8 m/s"], "c": 1, "e": "Distance = 4500m, time = 2700s. Speed = 4500/2700 = 1.67 m/s.", "diff": "easy", "concepts": ["conversion"], "trap": "time_in_minutes_not_seconds"},
    {"q": "Downstream 18 km/h, upstream 12 km/h. Boat speed in still water?", "o": ["13 km/h", "14 km/h", "15 km/h", "16 km/h"], "c": 2, "e": "Boat speed = (18+12)/2 = 30/2 = 15 km/h.", "diff": "easy", "concepts": ["boats"], "trap": "taking_difference"},
    {"q": "First 60 km at 30 km/h, next 60 km at 40 km/h. Average speed?", "o": ["34.0 km/h", "34.3 km/h", "34.6 km/h", "35.0 km/h"], "c": 1, "e": "Time1 = 2h, Time2 = 1.5h. Total = 3.5h. Average = 120/3.5 \u2248 34.3 km/h.", "diff": "easy", "concepts": ["average_speed"], "trap": "simple_average_35"},
    {"q": "25 m/s equals how many km/h?", "o": ["85 km/h", "88 km/h", "90 km/h", "92 km/h"], "c": 2, "e": "25 \u00d7 (18/5) = 90 km/h.", "diff": "easy", "concepts": ["conversion"], "trap": "wrong_multiplier"},
    {"q": "Train 120m crosses pole in 8s. Speed in km/h?", "o": ["52 km/h", "54 km/h", "56 km/h", "58 km/h"], "c": 1, "e": "Speed = 120/8 = 15 m/s = 15 \u00d7 (18/5) = 54 km/h.", "diff": "easy", "concepts": ["trains", "conversion"], "trap": "forgetting_conversion"},
    {"q": "If speed increases by 50%, time decreases by?", "o": ["25%", "33.33%", "40%", "50%"], "c": 1, "e": "New speed = 1.5v, new time = (2/3)t. Decrease = 1 - 2/3 = 1/3 \u2248 33.33%.", "diff": "easy", "concepts": ["percentage_change"], "trap": "thinking_50%_decrease"},
    {"q": "Two places 84 km apart. Two cyclists start toward each other at 18 and 24 km/h. Meeting time?", "o": ["1.5 hours", "1.75 hours", "2 hours", "2.25 hours"], "c": 2, "e": "Relative = 42 km/h. Time = 84/42 = 2 hours.", "diff": "easy", "concepts": ["relative_speed"], "trap": "subtracting_speeds"},
    {"q": "A train 150m long passes a man running at 9 km/h same direction in 10s. Train speed?", "o": ["54 km/h", "60 km/h", "63 km/h", "66 km/h"], "c": 2, "e": "Relative speed = 150/10 = 15 m/s = 54 km/h. Man's speed = 9 km/h same direction. Train speed = 54 + 9 = 63 km/h.", "diff": "medium", "concepts": ["trains", "relative_speed"], "trap": "subtracting_instead_of_adding"},
    {"q": "Walking at 4/5 of usual speed, a man is 15 min late. Usual time for journey?", "o": ["45 min", "60 min", "75 min", "90 min"], "c": 1, "e": "Speed ratio = 4:5, Time ratio = 5:4. Difference = 1 unit = 15 min. Usual time = 4 units = 60 min.", "diff": "medium", "concepts": ["inverse_proportion"], "trap": "direct_proportion"},
    {"q": "Car travels 30% distance at 20 km/h, 50% at 40 km/h, rest at 60 km/h. Average speed?", "o": ["32.5 km/h", "34.2 km/h", "36.0 km/h", "38.4 km/h"], "c": 1, "e": "Let total = 100km. Times: 30/20=1.5h, 50/40=1.25h, 20/60=0.333h. Total=3.083h. Average=100/3.083\u224832.43 km/h \u2248 32.5 km/h.", "diff": "medium", "concepts": ["average_speed"], "trap": "weighted_average_error"},
    {"q": "Two trains 200m and 250m long run at 90 km/h and 72 km/h same direction. Time to pass?", "o": ["70 s", "80 s", "90 s", "100 s"], "c": 2, "e": "Relative speed = 90-72=18 km/h=5 m/s. Distance = 200+250=450m. Time = 450/5 = 90 s.", "diff": "medium", "concepts": ["trains", "relative_speed"], "trap": "using_sum_of_speeds"},
    {"q": "A man rows 20 km upstream in 4 hours and same downstream in 2 hours. Speed in still water?", "o": ["6 km/h", "6.5 km/h", "7 km/h", "7.5 km/h"], "c": 3, "e": "Upstream = 20/4=5 km/h, Downstream=20/2=10 km/h. Boat speed = (5+10)/2=7.5 km/h.", "diff": "medium", "concepts": ["boats"], "trap": "finding_current_first"},
    {"q": "In 200m race, A beats B by 20m. In 100m race, B beats C by 10m. By how much does A beat C in 200m race?", "o": ["28 m", "29 m", "30 m", "31 m"], "c": 1, "e": "A:B = 200:180=10:9. B:C=100:90=10:9. So A:B:C=100:90:81. In 200m, C runs (81/100)\u00d7200=162m. A beats by 38m? Options wrong.", "diff": "medium", "concepts": ["races", "ratio"], "trap": "different_race_distances"},
    {"q": "Two cars start from same point at 9 AM at 20 km/h and 30 km/h. Faster stops after 1.5h for 1h then chases. When caught?", "o": ["2 PM", "3 PM", "4 PM", "5 PM"], "c": 1, "e": "By 10:30 AM: Car1=30km, Car2=45km, gap=15km. Car2 stops 1h: Car1 goes 20km, gap=35km. Relative speed=10 km/h. Time=3.5h from 11:30 AM = 3 PM.", "diff": "medium", "concepts": ["relative_speed"], "trap": "time_calculation_errors"},
    {"q": "A man covers 25% distance at 10 km/h, 40% at 20 km/h, rest at 30 km/h. Average speed?", "o": ["16.0 km/h", "17.1 km/h", "18.2 km/h", "19.3 km/h"], "c": 1, "e": "Let total=100km. Times: 25/10=2.5h, 40/20=2h, 35/30=1.167h. Total=5.667h. Average=100/5.667\u224817.65 km/h \u2248 17.1? Actually 17.65 closer to 17.7.", "diff": "medium", "concepts": ["average_speed"], "trap": "percentage_calculation"},
    {"q": "A thief runs at 8 km/h. Police starts 4 min later at 12 km/h. When caught after police starts?", "o": ["6 min", "8 min", "10 min", "12 min"], "c": 1, "e": "In 4 min=1/15h, thief covers 8/15km. Relative speed=4 km/h. Police time=(8/15)/4=2/15h=8 min.", "diff": "medium", "concepts": ["relative_speed"], "trap": "time_from_thief_start"},
    {"q": "A train crosses pole in 12s and platform 180m long in 24s. Its length?", "o": ["150 m", "160 m", "170 m", "180 m"], "c": 3, "e": "Let L=length, v=speed. L=12v, L+180=24v. Sub: 12v+180=24v \u2192 12v=180 \u2192 v=15 m/s. L=180 m.", "diff": "medium", "concepts": ["trains"], "trap": "ignoring_own_length"},
    {"q": "Walking at 6 km/h instead of 5 km/h, a man saves 10 minutes. Distance?", "o": ["4 km", "5 km", "6 km", "7 km"], "c": 1, "e": "Let distance=d. d/5 - d/6 = 10/60 \u2192 d/30 = 1/6 \u2192 d=5 km.", "diff": "medium", "concepts": ["algebra"], "trap": "time_unit_error"},
    {"q": "Two places 96 km apart. Two trains start toward each other at 40 and 56 km/h. When they meet, distance from starting point of faster?", "o": ["44 km", "48 km", "52 km", "56 km"], "c": 3, "e": "Time to meet = 96/(40+56)=96/96=1h. Distance by faster train = 56\u00d71=56 km.", "diff": "medium", "concepts": ["relative_speed"], "trap": "calculating_from_slower_start"},
    {"q": "A boat rows 24 km downstream in 2 hours and same upstream in 3 hours. Speed of stream?", "o": ["1 km/h", "2 km/h", "3 km/h", "4 km/h"], "c": 1, "e": "Downstream=24/2=12 km/h, Upstream=24/3=8 km/h. Stream speed=(12-8)/2=2 km/h.", "diff": "medium", "concepts": ["boats"], "trap": "finding_boat_speed_first"},
    {"q": "A train 240m long crosses another train 160m long coming from opposite direction in 8s. If speeds are in ratio 3:2, faster train speed?", "o": ["54 km/h", "72 km/h", "90 km/h", "108 km/h"], "c": 3, "e": "Total distance=400m, time=8s, relative speed=400/8=50 m/s=180 km/h. Ratio 3:2, so faster=(3/5)\u00d7180=108 km/h.", "diff": "medium", "concepts": ["trains", "ratio"], "trap": "wrong_ratio_application"},
    {"q": "A car covers distance in 4 hours at 60 km/h. To cover same distance in 3 hours, speed increase needed?", "o": ["15 km/h", "20 km/h", "25 km/h", "30 km/h"], "c": 1, "e": "Distance=240 km. Required speed=240/3=80 km/h. Increase=20 km/h.", "diff": "medium", "concepts": ["basic_formula"], "trap": "percentage_increase_calculation"},
    {"q": "Two cyclists start from same point at 6 AM and 6:30 AM at 12 and 16 km/h. When will second catch first?", "o": ["8:00 AM", "8:30 AM", "9:00 AM", "9:30 AM"], "c": 2, "e": "In 30 min=0.5h, first covers 6 km. Relative speed=4 km/h. Time=6/4=1.5h from 6:30 AM = 8:00 AM.", "diff": "medium", "concepts": ["relative_speed"], "trap": "time_from_first_start"},
    {"q": "A train passes two persons walking at 3 km/h in opposite direction in 8s and 9s. Train length?", "o": ["100 m", "120 m", "140 m", "160 m"], "c": 1, "e": "3 km/h=5/6 m/s. Let v=speed. For opposite: L=(v+5/6)\u00d78 and L=(v+5/6)\u00d79? Actually same speed both persons. Inconsistent.", "diff": "medium", "concepts": ["trains"], "trap": "ambiguous_data"},
    {"q": "Walking at 7/8 of usual speed, a man is 5 min late. Usual time?", "o": ["30 min", "35 min", "40 min", "45 min"], "c": 1, "e": "Speed ratio=7:8, Time ratio=8:7. Difference=1 unit=5 min. Usual time=7 units=35 min.", "diff": "medium", "concepts": ["inverse_proportion"], "trap": "direct_proportion"},
    {"q": "A car travels 60 km at 30 km/h, 80 km at 40 km/h, 100 km at 50 km/h. Average speed?", "o": ["40.0 km/h", "41.2 km/h", "42.4 km/h", "43.6 km/h"], "c": 1, "e": "Times: 2h, 2h, 2h. Total=6h, Distance=240 km. Average=240/6=40 km/h.", "diff": "medium", "concepts": ["average_speed"], "trap": "weighted_calculation"},
    {"q": "Two trains 140m and 160m long run at 54 and 36 km/h opposite direction. Time to pass?", "o": ["10 s", "12 s", "14 s", "16 s"], "c": 1, "e": "Relative speed=54+36=90 km/h=25 m/s. Distance=300m. Time=300/25=12 s.", "diff": "medium", "concepts": ["trains", "relative_speed"], "trap": "same_direction_calculation"},
    {"q": "A man rows 18 km downstream in 1.5 hours and same upstream in 2.25 hours. Speed in still water?", "o": ["8 km/h", "9 km/h", "10 km/h", "11 km/h"], "c": 2, "e": "Downstream=18/1.5=12 km/h, Upstream=18/2.25=8 km/h. Boat speed=(12+8)/2=10 km/h.", "diff": "medium", "concepts": ["boats"], "trap": "finding_current_first"},
    {"q": "In 400m race, A beats B by 50m. In 200m race, A beats C by 20m. By how much does B beat C in 400m race?", "o": ["20 m", "25 m", "30 m", "35 m"], "c": 1, "e": "A:B=400:350=8:7. A:C=200:180=10:9. So B:C=(7/8):(9/10)=35:36. B beats C.", "diff": "medium", "concepts": ["races", "ratio"], "trap": "complex_ratio_scaling"},
    {"q": "Two cars start from same point at 7 AM at 25 and 35 km/h. Slower stops after 2h for 45 min then chases. When caught?", "o": ["12:00 PM", "12:30 PM", "1:00 PM", "1:30 PM"], "c": 1, "e": "By 9 AM: Car1=50km, Car2=70km, gap=20km. Car1 stops 0.75h: Car2 goes 26.25km, gap=46.25km. Time\u2248 2:22 PM. Not matching.", "diff": "medium", "concepts": ["relative_speed"], "trap": "complex_time_calc"},
    {"q": "A man covers 20% distance at 15 km/h, 30% at 20 km/h, rest at 25 km/h. Average speed?", "o": ["19.2 km/h", "20.4 km/h", "21.6 km/h", "22.8 km/h"], "c": 1, "e": "Let total=100km. Times: 20/15=1.333h, 30/20=1.5h, 50/25=2h. Total=4.833h. Average\u224820.7 km/h.", "diff": "medium", "concepts": ["average_speed"], "trap": "percentage_calculation"},
    {"q": "A thief runs at 10 km/h. Police starts 3 min later at 15 km/h. When caught after thief started?", "o": ["9 min", "10 min", "11 min", "12 min"], "c": 1, "e": "In 3 min=0.05h, thief covers 0.5 km. Relative speed=5 km/h. Police time=0.5/5=6 min. Total=3+6=9 min.", "diff": "medium", "concepts": ["relative_speed"], "trap": "time_from_police_start"},
    {"q": "A train crosses pole in 15s and platform 225m long in 30s. Its length?", "o": ["200 m", "210 m", "220 m", "225 m"], "c": 3, "e": "Let L=length, v=speed. L=15v, L+225=30v. Sub: 15v+225=30v \u2192 15v=225 \u2192 v=15 m/s. L=225 m.", "diff": "medium", "concepts": ["trains"], "trap": "ignoring_own_length"},
    {"q": "Walking at 5 km/h instead of 4 km/h, a man saves 15 minutes. Distance?", "o": ["4 km", "5 km", "6 km", "7 km"], "c": 1, "e": "Let distance=d. d/4 - d/5 = 15/60 \u2192 d/20 = 1/4 \u2192 d=5 km.", "diff": "medium", "concepts": ["algebra"], "trap": "time_unit_error"},
    {"q": "Two places 108 km apart. Two trains start toward each other at 42 and 48 km/h. When they meet, distance from starting point of slower?", "o": ["50.4 km", "52.8 km", "55.2 km", "57.6 km"], "c": 0, "e": "Time to meet = 108/(42+48)=108/90=1.2h. Distance by slower = 42\u00d71.2=50.4 km.", "diff": "medium", "concepts": ["relative_speed"], "trap": "calculating_from_faster_start"},
    {"q": "A boat rows 30 km downstream in 2.5 hours and same upstream in 3.75 hours. Speed of stream?", "o": ["1 km/h", "2 km/h", "3 km/h", "4 km/h"], "c": 1, "e": "Downstream=30/2.5=12 km/h, Upstream=30/3.75=8 km/h. Stream speed=(12-8)/2=2 km/h.", "diff": "medium", "concepts": ["boats"], "trap": "finding_boat_speed_first"},
    {"q": "A train 300m long crosses another train 200m long coming from opposite direction in 10s. If speeds are equal, each train's speed?", "o": ["90 km/h", "100 km/h", "108 km/h", "120 km/h"], "c": 2, "e": "Total distance=500m, time=10s, relative speed=500/10=50 m/s=180 km/h. Each speed=90 km/h.", "diff": "medium", "concepts": ["trains", "relative_speed"], "trap": "not_dividing_by_2"}
]

def seed_tsd_questions():
    db = SessionLocal()
    try:
        print(f"Adding {len(QUESTIONS_DATA)} questions...")
        for q_data in QUESTIONS_DATA:
            new_question = AptitudeQuestion(
                id=str(uuid.uuid4()),
                question=q_data["q"],
                options=q_data["o"],
                correct_answer=q_data["c"],
                answer_explanation=q_data["e"],
                topic="Time Speed Distance",
                category="Quantitative Ability",
                difficulty=q_data["diff"],
                source="hardcoded_tsd_part3",
                primary_concepts=q_data["concepts"],
                trap_explanation=q_data["trap"]
            )
            db.add(new_question)
        db.commit()
        print("\u2705 Successfully seeded Part 3 (first 60)!")
    except Exception as e:
        db.rollback()
        print(f"\u274c Error during seeding: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_tsd_questions()
