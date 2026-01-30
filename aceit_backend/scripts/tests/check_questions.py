"""
Check database questions for mock test generation
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_postgres import SessionLocal
from models.aptitude_sql import AptitudeQuestion
from sqlalchemy import func

def check_questions():
    db = SessionLocal()
    try:
        # Total questions
        total = db.query(AptitudeQuestion).count()
        print(f"Total questions in database: {total}")
        print()
        
        # Breakdown by category and difficulty
        print("Breakdown by Category and Difficulty:")
        print("-" * 60)
        
        breakdown = db.query(
            AptitudeQuestion.category,
            AptitudeQuestion.difficulty,
            func.count(AptitudeQuestion.id).label('count')
        ).group_by(
            AptitudeQuestion.category,
            AptitudeQuestion.difficulty
        ).order_by(
            AptitudeQuestion.category,
            AptitudeQuestion.difficulty
        ).all()
        
        current_cat = None
        for cat, diff, count in breakdown:
            if cat != current_cat:
                if current_cat is not None:
                    print()
                print(f"\n{cat}:")
                current_cat = cat
            print(f"  {diff:8} : {count:3} questions")
        
        print()
        print("-" * 60)
        
        # Check if we have enough for different test types
        print("\nTest Generation Feasibility:")
        print(f"  Topic Test (20 questions): {'Possible' if total >= 20 else 'Not enough questions'}")
        print(f"  Section Test (30 questions): {'Possible' if total >= 30 else 'Not enough questions'}")
        print(f"  Full-Length Test (100 questions): {'Possible' if total >= 100 else 'Not enough questions'}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    check_questions()
