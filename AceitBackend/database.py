# Massive Question Database
import json
import os

# File to store user data
USERS_FILE = "users.json"

# Load existing users from file, or start with empty list
def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

# Save users to file
def save_users():
    with open(USERS_FILE, 'w') as f:
        # Convert all datetime objects to strings before saving
        serializable_data = []
        for user in users_data:
            user_copy = user.copy()
            # Convert datetime objects to ISO format strings
            for key, value in user_copy.items():
                if hasattr(value, 'isoformat'):  # Check if it's a datetime
                    user_copy[key] = value.isoformat()
            serializable_data.append(user_copy)
        json.dump(serializable_data, f, indent=2)

# Initialize users_data from file
users_data = load_users()
questions_data = []
progress_data = []
# User proficiency data - tracks performance per topic and difficulty
user_proficiency_data = {}

from massive_database import massive_db

def load_massive_database():
    """Load questions from massive database"""
    global questions_data
    
    print("🚀 LOADING MASSIVE QUESTION DATABASE...")
    
    # Get all questions from massive database
    coding_problems = massive_db.datasets["coding"]
    aptitude_questions = massive_db.datasets["aptitude"] 
    interview_questions = massive_db.datasets["interview"]
    
    # Format coding problems for frontend
    formatted_coding = []
    for problem in coding_problems:
        formatted_problem = {
            "id": problem.get("id"),
            "title": problem.get("title"),
            "description": problem.get("description", ""),
            "difficulty": problem.get("difficulty", "Medium").capitalize(),
            "topics": problem.get("topics", []),
            "test_cases": problem.get("test_cases", []),
            "starter_code": {
                "javascript": problem.get("starter_code", "// Write your solution here")
            },
            "source": problem.get("source", "")
        }
        formatted_coding.append(formatted_problem)
    
    # Format aptitude questions for frontend
    formatted_aptitude = []
    for question in aptitude_questions:
        formatted_question = {
            "id": question.get("id"),
            "question": question.get("question"),
            "options": question.get("options", []),
            "correct_answer": question.get("correct_answer"),
            "type": question.get("topic", "general"),
            "explanation": question.get("explanation", ""),
            "topic": question.get("topic", "general"),
            "difficulty": question.get("difficulty", "easy"),
            "source": question.get("source", "")
        }
        formatted_aptitude.append(formatted_question)
    
    # Combine all questions
    questions_data.clear()
    questions_data.extend(formatted_coding)
    questions_data.extend(formatted_aptitude)
    questions_data.extend(interview_questions)
    
    print("🎉 MASSIVE DATABASE LOADED SUCCESSFULLY!")
    print(f"📊 BREAKDOWN:")
    print(f"   - Coding Problems: {len(formatted_coding)}")
    print(f"   - Aptitude Questions: {len(formatted_aptitude)}")
    print(f"   - Interview Questions: {len(interview_questions)}")
    print(f"   - TOTAL: {len(questions_data)} questions")

# Database functions
def get_aptitude_questions():
    return [q for q in questions_data if 'options' in q and 'question' in q]

def get_coding_problems():
    return [q for q in questions_data if 'title' in q]

def find_user_by_email(email):
    return next((u for u in users_data if u.get('email') == email), None)

def add_user(user_data):
    users_data.append(user_data)
    save_users()
    return True

def add_progress(progress_data_item):
    progress_data.append(progress_data_item)
    return True

# User proficiency functions
def get_user_proficiency(user_id):
    """Get user's proficiency data"""
    return user_proficiency_data.get(user_id, {})

def update_user_proficiency(user_id, topic, difficulty, is_correct):
    """Update user's proficiency based on answer correctness"""
    if user_id not in user_proficiency_data:
        user_proficiency_data[user_id] = {}
    
    if topic not in user_proficiency_data[user_id]:
        user_proficiency_data[user_id][topic] = {
            "easy": {"correct": 0, "total": 0},
            "medium": {"correct": 0, "total": 0},
            "hard": {"correct": 0, "total": 0}
        }
    
    # Update counters
    user_proficiency_data[user_id][topic][difficulty]["total"] += 1
    if is_correct:
        user_proficiency_data[user_id][topic][difficulty]["correct"] += 1

def get_user_topic_proficiency(user_id, topic):
    """Get user's proficiency for a specific topic"""
    proficiency = get_user_proficiency(user_id)
    return proficiency.get(topic, {
        "easy": {"correct": 0, "total": 0},
        "medium": {"correct": 0, "total": 0},
        "hard": {"correct": 0, "total": 0}
    })

def get_next_difficulty(user_id, topic):
    """Determine next question difficulty based on user performance"""
    proficiency = get_user_topic_proficiency(user_id, topic)
    
    # Calculate success rates for each difficulty
    easy_rate = proficiency["easy"]["correct"] / proficiency["easy"]["total"] if proficiency["easy"]["total"] > 0 else 0
    medium_rate = proficiency["medium"]["correct"] / proficiency["medium"]["total"] if proficiency["medium"]["total"] > 0 else 0
    hard_rate = proficiency["hard"]["correct"] / proficiency["hard"]["total"] if proficiency["hard"]["total"] > 0 else 0
    
    # Adaptive algorithm:
    # If user is doing well on current level, move to next level
    # If user is struggling, move to easier level
    # If no data, start with easy
    
    if proficiency["easy"]["total"] == 0:
        return "easy"  # Start with easy questions
    
    # If user has attempted at least 3 questions of current difficulty
    if proficiency["easy"]["total"] >= 3:
        if easy_rate >= 0.8:  # 80% success rate
            if proficiency["medium"]["total"] == 0:
                return "medium"  # Move to medium
            elif proficiency["medium"]["total"] >= 3 and medium_rate >= 0.7:  # 70% success rate
                return "hard"  # Move to hard
            elif proficiency["medium"]["total"] >= 3 and medium_rate < 0.5:  # Less than 50% success rate
                return "easy"  # Go back to easy
            else:
                return "medium"  # Stay at medium
        else:
            return "easy"  # Stay at easy
    
    return "easy"  # Default to easy

# Load massive database
load_massive_database()

# Export collections
users_collection = users_data
questions_collection = questions_data  
progress_collection = progress_data