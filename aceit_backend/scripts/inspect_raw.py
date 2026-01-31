from database_postgres import SessionLocal
from models.aptitude_sql import AptitudeQuestion
from sqlalchemy import func

def inspect_raw():
    db = SessionLocal()
    try:
        topic = "Time Speed Distance"
        res = db.query(AptitudeQuestion.difficulty, func.count(AptitudeQuestion.id))\
                .filter(AptitudeQuestion.topic == topic)\
                .group_by(AptitudeQuestion.difficulty).all()
        
        print(f"Raw results for topic '{topic}':")
        for diff, count in res:
            print(f"  '|{diff}|' : {count}")
    finally:
        db.close()

if __name__ == "__main__":
    inspect_raw()
