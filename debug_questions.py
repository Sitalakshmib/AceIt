
import sys
import os
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
sys.path.append(os.path.join(os.path.dirname(__file__), "aceit_backend"))
from models.aptitude_sql import AptitudeQuestion, UserAptitudeProgress
from database_postgres import DATABASE_URL

# Setup DB
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
db = Session()

USER_ID = "guest_user" # Assuming guest since no auth shown in logs, but api.js handles it. 
# Better to list all progress to find the active one.

print("--- QUESTION DISTRIBUTION ---")
results = db.query(
    AptitudeQuestion.topic, 
    AptitudeQuestion.difficulty, 
    func.count(AptitudeQuestion.id)
).group_by(AptitudeQuestion.topic, AptitudeQuestion.difficulty).all()

for row in results:
    print(f"Topic: {row[0]} | Difficulty: {row[1]} | Count: {row[2]}")

print("\n--- USER PROGRESS ---")
progress = db.query(UserAptitudeProgress).all()
for p in progress:
    print(f"User: {p.user_id} | Topic: {p.topic} | Diff: {p.current_difficulty} | Last Used: {p.last_practiced}")
