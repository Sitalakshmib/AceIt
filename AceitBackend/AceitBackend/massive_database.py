# massive_database.py
import requests
import json
import random

class MassiveQuestionDatabase:
    def __init__(self):
        self.datasets = {
            "coding": self.load_coding_datasets(),
            "aptitude": self.load_aptitude_datasets(), 
            "interview": self.load_interview_datasets()
        }
    
    def load_coding_datasets(self):
        """Load coding problems"""
        print("💻 Loading coding problems...")
        
        # Source 1: LeetCode problems
        leetcode_problems = self.get_leetcode_problems()
        
        # Source 2: Custom coding problems
        custom_problems = self.get_custom_coding_problems()
        
        return leetcode_problems + custom_problems
    
    def load_aptitude_datasets(self):
        """Load aptitude questions"""
        print("🧮 Loading aptitude questions...")
        
        # Generate questions for different topics with difficulty levels
        percentage_questions = self.generate_percentage_questions(500)
        number_series_questions = self.generate_number_series_questions(500)
        ratio_proportion_questions = self.generate_ratio_proportion_questions(500)
        time_work_questions = self.generate_time_work_questions(500)
        profit_loss_questions = self.generate_profit_loss_questions(500)
        
        return (percentage_questions + number_series_questions + 
                ratio_proportion_questions + time_work_questions + 
                profit_loss_questions)
    
    def load_interview_datasets(self):
        """Load interview questions"""
        print("🏢 Loading interview questions...")
        
        hr_questions = self.get_hr_questions(1000)
        tech_questions = self.get_technical_questions(1000)
        
        return hr_questions + tech_questions
    
    def get_leetcode_problems(self):
        """Get LeetCode problems - using comprehensive fallback"""
        try:
            return self.get_comprehensive_coding_fallback(2000)
        except:
            return self.get_comprehensive_coding_fallback(2000)
    
    def get_comprehensive_coding_fallback(self, count=2000):
        """Comprehensive fallback with categorized coding problems"""
        # Easy Problems (20)
        easy_problems = [
            {
                "id": f"easy_{i}",
                "title": f"Two Sum - Variation {i}",
                "description": f"Find two numbers that add up to target - problem {i}",
                "difficulty": "easy",
                "topics": ["array", "hash table"],
                "test_cases": [
                    {"input": [[2,7,11,15], 9], "output": [0,1]},
                    {"input": [[3,2,4], 6], "output": [1,2]}
                ],
                "starter_code": "def two_sum(nums, target):\n    # Your code here\n    pass",
                "source": "leetcode_fallback"
            } for i in range(1, 251)
        ]
        
        # Medium Problems (20)
        medium_problems = [
            {
                "id": f"medium_{i}",
                "title": f"Add Two Numbers - Variation {i}",
                "description": f"Add two linked lists representing numbers - problem {i}",
                "difficulty": "medium", 
                "topics": ["linked list", "math"],
                "test_cases": [
                    {"input": [[2,4,3], [5,6,4]], "output": [7,0,8]},
                    {"input": [[9,9,9], [1]], "output": [0,0,0,1]}
                ],
                "starter_code": "def add_two_numbers(l1, l2):\n    # Your code here\n    pass",
                "source": "leetcode_fallback"
            } for i in range(1, 751)
        ]
        
        # Hard Problems (10)
        hard_problems = [
            {
                "id": f"hard_{i}",
                "title": f"Median of Arrays - Variation {i}",
                "description": f"Find median of two sorted arrays - problem {i}",
                "difficulty": "hard",
                "topics": ["array", "binary search"],
                "test_cases": [
                    {"input": [[1,3], [2]], "output": 2.0},
                    {"input": [[1,2], [3,4]], "output": 2.5}
                ],
                "starter_code": "def find_median_sorted_arrays(nums1, nums2):\n    # Your code here\n    pass", 
                "source": "leetcode_fallback"
            } for i in range(1, 1001)
        ]
        
        return easy_problems + medium_problems + hard_problems
    
    def get_custom_coding_problems(self):
        """Additional custom coding problems"""
        return [
            {
                "id": "custom_1",
                "title": "Fibonacci Sequence",
                "description": "Write a function to return the nth Fibonacci number",
                "difficulty": "easy",
                "topics": ["recursion", "dynamic programming"],
                "test_cases": [
                    {"input": [5], "output": 5},
                    {"input": [6], "output": 8},
                    {"input": [7], "output": 13}
                ],
                "starter_code": "def fibonacci(n):\n    # Your code here\n    pass",
                "source": "custom"
            },
            {
                "id": "custom_2",
                "title": "Palindrome Check",
                "description": "Check if a string is a palindrome",
                "difficulty": "easy",
                "topics": ["string", "two pointers"],
                "test_cases": [
                    {"input": ["racecar"], "output": True},
                    {"input": ["hello"], "output": False},
                    {"input": ["a"], "output": True}
                ],
                "starter_code": "def is_palindrome(s):\n    # Your code here\n    pass",
                "source": "custom"
            },
            {
                "id": "custom_3",
                "title": "Reverse String",
                "description": "Reverse a string in-place",
                "difficulty": "easy",
                "topics": ["string", "two pointers"],
                "test_cases": [
                    {"input": ["hello"], "output": "olleh"},
                    {"input": ["python"], "output": "nohtyp"}
                ],
                "starter_code": "def reverse_string(s):\n    # Your code here\n    pass",
                "source": "custom"
            }
        ]
    
    def generate_percentage_questions(self, count):
        """Generate percentage aptitude questions with difficulty levels"""
        questions = []
        for i in range(1, count + 1):
            # Determine difficulty based on complexity
            if i <= count // 3:
                difficulty = "easy"
                # Simple percentage calculation
                base = random.randint(10, 100)
                percent = random.choice([10, 20, 25, 50])
                answer = (base * percent) // 100
                question = f"What is {percent}% of {base}?"
                options = [
                    str(answer),
                    str(answer + random.randint(1, 10)),
                    str(answer - random.randint(1, 10)),
                    str(answer + random.randint(11, 20))
                ]
                correct_answer = 0
                explanation = f"{percent}% of {base} = ({percent}/100) * {base} = {answer}"
            elif i <= 2 * (count // 3):
                difficulty = "medium"
                # Percentage increase/decrease
                original = random.randint(50, 200)
                change = random.randint(10, 50)
                if random.choice([True, False]):
                    # Increase
                    new_value = original + (original * change) // 100
                    question = f"The price of an item increased by {change}%. If the original price was ₹{original}, what is the new price?"
                    answer = new_value
                else:
                    # Decrease
                    new_value = original - (original * change) // 100
                    question = f"The price of an item decreased by {change}%. If the original price was ₹{original}, what is the new price?"
                    answer = new_value
                options = [
                    str(answer),
                    str(answer + random.randint(5, 20)),
                    str(answer - random.randint(5, 20)),
                    str(original)
                ]
                correct_answer = 0
                explanation = f"New value = Original ± (Original × Change%) = {original} {'+' if 'increased' in question else '-'} ({original} × {change}%) = {answer}"
            else:
                difficulty = "hard"
                # Complex percentage problem
                principal = random.randint(1000, 10000)
                rate = random.randint(5, 15)
                time = random.randint(1, 5)
                # Simple interest calculation
                interest = (principal * rate * time) // 100
                amount = principal + interest
                question = f"A sum of ₹{principal} is invested at {rate}% per annum simple interest for {time} years. What is the total amount at the end of {time} years?"
                answer = amount
                options = [
                    str(answer),
                    str(answer + random.randint(100, 500)),
                    str(answer - random.randint(100, 500)),
                    str(principal + (principal * rate * (time+1)) // 100)
                ]
                correct_answer = 0
                explanation = f"Simple Interest = (P × R × T)/100 = ({principal} × {rate} × {time})/100 = {interest}. Total Amount = P + SI = {principal} + {interest} = {answer}"
            
            # Shuffle options
            correct_option = options[correct_answer]
            random.shuffle(options)
            correct_answer = options.index(correct_option)
            
            questions.append({
                "id": f"percentage_{i}",
                "question": question,
                "options": options,
                "correct_answer": correct_answer,
                "explanation": explanation,
                "topic": "percentage",
                "difficulty": difficulty,
                "source": "generated"
            })
        return questions
    
    def generate_number_series_questions(self, count):
        """Generate number series aptitude questions with difficulty levels"""
        questions = []
        for i in range(1, count + 1):
            # Determine difficulty based on pattern complexity
            if i <= count // 3:
                difficulty = "easy"
                # Simple arithmetic progression
                start = random.randint(1, 10)
                diff = random.randint(2, 5)
                series = [start + j * diff for j in range(5)]
                question = f"Complete the series: {', '.join(map(str, series[:-1]))}, ?"
                answer = series[-1]
                options = [
                    str(answer),
                    str(answer + diff),
                    str(answer - diff),
                    str(answer + diff * 2)
                ]
                correct_answer = 0
                explanation = f"The series increases by {diff} each time: {', '.join(map(str, series))}"
            elif i <= 2 * (count // 3):
                difficulty = "medium"
                # Geometric progression
                start = random.randint(2, 5)
                ratio = random.randint(2, 4)
                series = [start * (ratio ** j) for j in range(5)]
                question = f"Complete the series: {', '.join(map(str, series[:-1]))}, ?"
                answer = series[-1]
                options = [
                    str(answer),
                    str(answer // ratio),
                    str(answer * ratio),
                    str(answer + ratio)
                ]
                correct_answer = 0
                explanation = f"Each term is multiplied by {ratio}: {', '.join(map(str, series))}"
            else:
                difficulty = "hard"
                # Complex pattern (alternating or multiple operations)
                pattern_type = random.choice(["alternating", "fibonacci_like"])
                if pattern_type == "alternating":
                    # Alternating pattern
                    a, b = random.randint(1, 5), random.randint(1, 5)
                    series = []
                    for j in range(6):
                        if j % 2 == 0:
                            series.append(a + (j // 2) * 2)
                        else:
                            series.append(b + (j // 2) * 3)
                    question = f"Complete the series: {', '.join(map(str, series[:-1]))}, ?"
                    answer = series[-1]
                    options = [
                        str(answer),
                        str(answer + 1),
                        str(series[-2] + 2),
                        str(answer - 1)
                    ]
                    correct_answer = 0
                    explanation = f"Two alternating sequences: {a}, {b}, {a+2}, {b+3}, {a+4}, {b+6}"
                else:
                    # Fibonacci-like pattern
                    a, b = random.randint(1, 10), random.randint(1, 10)
                    series = [a, b]
                    for j in range(4):
                        series.append(series[-1] + series[-2])
                    question = f"Complete the series: {', '.join(map(str, series[:-1]))}, ?"
                    answer = series[-1]
                    options = [
                        str(answer),
                        str(answer - series[-2]),
                        str(answer + series[-2]),
                        str(series[-2])
                    ]
                    correct_answer = 0
                    explanation = f"Each term is the sum of the two preceding terms: {', '.join(map(str, series))}"
            
            # Shuffle options
            correct_option = options[correct_answer]
            random.shuffle(options)
            correct_answer = options.index(correct_option)
            
            questions.append({
                "id": f"number_series_{i}",
                "question": question,
                "options": options,
                "correct_answer": correct_answer,
                "explanation": explanation,
                "topic": "number_series",
                "difficulty": difficulty,
                "source": "generated"
            })
        return questions
    
    def generate_ratio_proportion_questions(self, count):
        """Generate ratio and proportion aptitude questions with difficulty levels"""
        questions = []
        for i in range(1, count + 1):
            # Determine difficulty based on complexity
            if i <= count // 3:
                difficulty = "easy"
                # Simple ratio problem
                a, b = random.randint(2, 10), random.randint(2, 10)
                multiplier = random.randint(2, 8)
                total = (a + b) * multiplier
                question = f"Two numbers are in the ratio {a}:{b}. If their sum is {total}, what is the larger number?"
                answer = max(a * multiplier, b * multiplier)
                wrong_options = [min(a * multiplier, b * multiplier), total, total // 2]
                options = [str(answer)] + [str(opt) for opt in wrong_options]
                correct_answer = 0
                explanation = f"If the ratio is {a}:{b}, the numbers are {a}x and {b}x. Sum = {a}x + {b}x = {a+b}x = {total}. So x = {multiplier}. Numbers are {a*multiplier} and {b*multiplier}. Larger number = {answer}"
            elif i <= 2 * (count // 3):
                difficulty = "medium"
                # Proportion problem
                a, b, c = random.randint(2, 15), random.randint(2, 15), random.randint(20, 100)
                # a : b :: c : d => d = (b * c) / a
                d = (b * c) // a
                question = f"If {a} : {b} :: {c} : x, find the value of x."
                answer = d
                options = [
                    str(answer),
                    str((a * c) // b),
                    str((a * b) // c),
                    str(answer + random.randint(1, 10))
                ]
                correct_answer = 0
                explanation = f"In proportion a:b :: c:d, we have a×d = b×c. So {a}×x = {b}×{c} => x = ({b}×{c})/{a} = {answer}"
            else:
                difficulty = "hard"
                # Complex ratio problem
                ratio1, ratio2 = random.randint(2, 5), random.randint(2, 5)
                total_amount = random.randint(1000, 5000)
                # Make sure total_amount is divisible by (ratio1 + ratio2)
                total_amount = ((total_amount // (ratio1 + ratio2)) + 1) * (ratio1 + ratio2)
                diff = abs(ratio1 - ratio2) * (total_amount // (ratio1 + ratio2))
                question = f"Two numbers are in the ratio {ratio1}:{ratio2}. If their sum is ₹{total_amount}, what is the difference between the numbers?"
                answer = diff
                options = [
                    str(answer),
                    str(total_amount // (ratio1 + ratio2)),
                    str(total_amount),
                    str(answer + random.randint(10, 50))
                ]
                correct_answer = 0
                explanation = f"If ratio is {ratio1}:{ratio2} and sum is {total_amount}, the numbers are ({ratio1}/{ratio1+ratio2})×{total_amount} = {ratio1 * (total_amount // (ratio1 + ratio2))} and ({ratio2}/{ratio1+ratio2})×{total_amount} = {ratio2 * (total_amount // (ratio1 + ratio2))}. Difference = |{ratio1 * (total_amount // (ratio1 + ratio2))} - {ratio2 * (total_amount // (ratio1 + ratio2))}| = {answer}"
            
            # Shuffle options
            correct_option = options[correct_answer]
            random.shuffle(options)
            correct_answer = options.index(correct_option)
            
            questions.append({
                "id": f"ratio_proportion_{i}",
                "question": question,
                "options": options,
                "correct_answer": correct_answer,
                "explanation": explanation,
                "topic": "ratio_proportion",
                "difficulty": difficulty,
                "source": "generated"
            })
        return questions
    
    def generate_time_work_questions(self, count):
        """Generate time and work aptitude questions with difficulty levels"""
        questions = []
        for i in range(1, count + 1):
            # Determine difficulty based on complexity
            if i <= count // 3:
                difficulty = "easy"
                # Simple work problem
                days = random.randint(10, 30)
                workers = random.randint(2, 8)
                question = f"If {workers} workers can complete a work in {days} days, how many days will it take for 1 worker to complete the same work?"
                answer = workers * days
                options = [
                    str(answer),
                    str(days),
                    str(workers),
                    str(answer // 2)
                ]
                correct_answer = 0
                explanation = f"Total work = {workers} workers × {days} days = {answer} worker-days. For 1 worker, time = {answer} worker-days ÷ 1 worker = {answer} days"
            elif i <= 2 * (count // 3):
                difficulty = "medium"
                # Two workers problem
                days1, days2 = random.randint(10, 20), random.randint(15, 30)
                # Calculate time taken when working together
                # 1/day1 + 1/day2 = 1/together_days
                # together_days = (day1 * day2) / (day1 + day2)
                numerator = days1 * days2
                denominator = days1 + days2
                together_days = numerator // denominator  # Integer division for simplicity
                if numerator % denominator != 0:
                    # Adjust to make it clean
                    multiplier = denominator // gcd(numerator, denominator)
                    days1 *= multiplier
                    days2 *= multiplier
                    together_days = (days1 * days2) // (days1 + days2)
                question = f"A can complete a work in {days1} days and B can complete the same work in {days2} days. How many days will they take to complete the work together?"
                answer = together_days
                options = [
                    str(answer),
                    str(days1 + days2),
                    str(min(days1, days2)),
                    str(max(days1, days2))
                ]
                correct_answer = 0
                explanation = f"A's 1 day work = 1/{days1}, B's 1 day work = 1/{days2}. Together, 1 day work = 1/{days1} + 1/{days2} = ({days2}+{days1})/({days1}×{days2}) = {days1+days2}/{days1*days2}. Time taken = {days1*days2}/{days1+days2} = {answer} days"
            else:
                difficulty = "hard"
                # Complex work problem with efficiency
                efficiency_a = random.randint(80, 120)  # Percentage efficiency
                efficiency_b = random.randint(80, 120)
                days_a_alone = random.randint(15, 25)
                # Calculate days for B alone based on efficiency
                # Work = Efficiency × Time
                # Work is same, so Efficiency_A × Days_A = Efficiency_B × Days_B
                # Days_B = (Efficiency_A × Days_A) / Efficiency_B
                work = efficiency_a * days_a_alone
                days_b_alone = work // efficiency_b
                # Days working together
                together_days = work // (efficiency_a + efficiency_b)
                question = f"A is {efficiency_a}% as efficient as B. A alone can complete a work in {days_a_alone} days. How many days will they take to complete the work together?"
                answer = together_days
                options = [
                    str(answer),
                    str(days_b_alone),
                    str(days_a_alone),
                    str((days_a_alone + days_b_alone) // 2)
                ]
                correct_answer = 0
                explanation = f"If A is {efficiency_a}% as efficient as B, and A takes {days_a_alone} days, then B takes ({efficiency_a}×{days_a_alone})/{efficiency_b} ≈ {days_b_alone} days. Together, their combined efficiency = {efficiency_a}+{efficiency_b} = {efficiency_a+efficiency_b}. Time = {work}/({efficiency_a+efficiency_b}) = {answer} days"
            
            # Shuffle options
            correct_option = options[correct_answer]
            random.shuffle(options)
            correct_answer = options.index(correct_option)
            
            questions.append({
                "id": f"time_work_{i}",
                "question": question,
                "options": options,
                "correct_answer": correct_answer,
                "explanation": explanation,
                "topic": "time_work",
                "difficulty": difficulty,
                "source": "generated"
            })
        return questions
    
    def generate_profit_loss_questions(self, count):
        """Generate profit and loss aptitude questions with difficulty levels"""
        questions = []
        for i in range(1, count + 1):
            # Determine difficulty based on complexity
            if i <= count // 3:
                difficulty = "easy"
                # Simple profit/loss calculation
                cost_price = random.randint(100, 500)
                profit_percent = random.choice([5, 10, 15, 20])
                selling_price = cost_price + (cost_price * profit_percent) // 100
                question = f"A shopkeeper buys an article for ₹{cost_price} and sells it at a profit of {profit_percent}%. What is the selling price?"
                answer = selling_price
                options = [
                    str(answer),
                    str(cost_price),
                    str(cost_price + profit_percent),
                    str(answer + 50)
                ]
                correct_answer = 0
                explanation = f"Selling Price = Cost Price + Profit = ₹{cost_price} + ({profit_percent}% of ₹{cost_price}) = ₹{cost_price} + ₹{cost_price * profit_percent // 100} = ₹{selling_price}"
            elif i <= 2 * (count // 3):
                difficulty = "medium"
                # Loss percentage calculation
                cost_price = random.randint(200, 1000)
                selling_price = random.randint(int(cost_price * 0.7), int(cost_price * 0.95))
                loss = cost_price - selling_price
                loss_percent = (loss * 100) // cost_price
                question = f"A man sells an article for ₹{selling_price} and incurs a loss of ₹{loss}. What is his loss percentage?"
                answer = loss_percent
                options = [
                    f"{answer}%",
                    f"{answer + 5}%",
                    f"{answer - 5}%",
                    f"{answer + 10}%"
                ]
                correct_answer = 0
                explanation = f"Loss Percentage = (Loss/Cost Price) × 100 = (₹{loss}/₹{cost_price}) × 100 = {loss_percent}%"
            else:
                difficulty = "hard"
                # Successive profit/loss problem
                cost_price = random.randint(500, 2000)
                first_profit = random.randint(10, 25)
                second_loss = random.randint(5, 15)
                # After first profit
                price_after_profit = cost_price + (cost_price * first_profit) // 100
                # After second loss
                final_price = price_after_profit - (price_after_profit * second_loss) // 100
                overall_loss_or_profit = final_price - cost_price
                if overall_loss_or_profit > 0:
                    result_type = "profit"
                    result_percent = (overall_loss_or_profit * 100) // cost_price
                else:
                    result_type = "loss"
                    result_percent = (abs(overall_loss_or_profit) * 100) // cost_price
                question = f"A shopkeeper sells an article at a profit of {first_profit}%. Had he sold it for ₹{price_after_profit - final_price} less, he would have incurred a loss of {second_loss}%. What is his overall profit or loss percentage?"
                answer = result_percent
                options = [
                    f"{result_percent}% {result_type}",
                    f"{result_percent + 5}% {result_type}",
                    f"{result_percent}% profit" if result_type == "loss" else f"{result_percent}% loss",
                    f"{result_percent + 10}% {result_type}"
                ]
                correct_answer = 0
                explanation = f"Let CP = ₹{cost_price}. After {first_profit}% profit, price = ₹{cost_price} + {first_profit}% of ₹{cost_price} = ₹{price_after_profit}. If sold for ₹{price_after_profit - final_price} less, SP = ₹{final_price}. This represents a {second_loss}% loss. Overall, final SP = ₹{final_price}. Since this is {'greater' if overall_loss_or_profit > 0 else 'less'} than CP, there is a {result_type} of ₹{abs(overall_loss_or_profit)}. {result_type.capitalize()} % = (₹{abs(overall_loss_or_profit)}/₹{cost_price}) × 100 = {result_percent}%"
            
            # Shuffle options
            correct_option = options[correct_answer]
            random.shuffle(options)
            correct_answer = options.index(correct_option)
            
            questions.append({
                "id": f"profit_loss_{i}",
                "question": question,
                "options": options,
                "correct_answer": correct_answer,
                "explanation": explanation,
                "topic": "profit_loss",
                "difficulty": difficulty,
                "source": "generated"
            })
        return questions
    
    def get_hr_questions(self, count):
        """Generate HR interview questions"""
        base_questions = [
            "Tell me about yourself",
            "Why should we hire you?",
            "What are your strengths and weaknesses?",
            "Where do you see yourself in 5 years?",
            "Why do you want to work here?",
            "Describe a challenging situation and how you handled it",
            "What are your salary expectations?",
            "How do you handle pressure?",
            "What motivates you?",
            "Why are you leaving your current job?"
        ]
        
        questions = []
        for i in range(count):
            question_text = base_questions[i % len(base_questions)] + f" (Variant {i//len(base_questions) + 1})"
            questions.append({
                "id": f"hr_{i}",
                "question": question_text,
                "topic": "hr_general",
                "type": "interview",
                "source": "hr_database"
            })
        
        return questions
    
    def get_technical_questions(self, count):
        """Generate technical interview questions"""
        programming_questions = [
            "What is the difference between list and tuple?",
            "Explain object-oriented programming principles",
            "What are Python decorators?",
            "How does garbage collection work?",
            "What is the difference between == and is in Python?",
            "Explain memory management in Python",
            "What are generators and when to use them?",
            "What is the Global Interpreter Lock?",
            "How do you handle exceptions?",
            "What are lambda functions?"
        ]
        
        questions = []
        for i in range(count):
            question_text = programming_questions[i % len(programming_questions)] + f" (Variant {i//len(programming_questions) + 1})"
            questions.append({
                "id": f"tech_{i}",
                "question": question_text,
                "topic": "programming",
                "type": "interview", 
                "source": "tech_database"
            })
        
        return questions

def gcd(a, b):
    """Calculate Greatest Common Divisor"""
    while b:
        a, b = b, a % b
    return a

# Create global instance
massive_db = MassiveQuestionDatabase()