import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.aptitude_sql import AptitudeQuestion

load_dotenv()

def delete_tsd_questions():
    DATABASE_URL = os.getenv("DATABASE_URL")
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Get IDs of questions to delete
        questions = session.query(AptitudeQuestion.id).filter(
            AptitudeQuestion.topic == "Time Speed Distance"
        ).all()
        
        question_ids = [str(q.id) for q in questions]
        count = len(question_ids)
        print(f"📊 Found {count} 'Time Speed Distance' questions.")

        if count > 0:
            # Delete dependent attempts first using raw SQL for speed/simplicity if model not imported
            # Assuming table name is 'question_attempts' and column 'question_id' based on error message
            if question_ids:
                # Convert list to tuple for SQL IN clause safe formatting
                ids_tuple = tuple(question_ids)
                if len(ids_tuple) == 1:
                   # Tuple with one item has trailing comma in python, format strictly
                   ids_tuple = f"('{ids_tuple[0]}')"
                else:
                   ids_tuple = str(ids_tuple)

                delete_attempts_sql = text(f"DELETE FROM question_attempts WHERE question_id IN {ids_tuple}")
                result = session.execute(delete_attempts_sql)
                print(f"🗑️ Deleted {result.rowcount} referencing question attempts.")

            # Now delete the questions
            deleted = session.query(AptitudeQuestion).filter(
                AptitudeQuestion.topic == "Time Speed Distance"
            ).delete(synchronize_session=False)
            
            session.commit()
            print(f"✅ Successfully deleted {deleted} questions.")
            
            # Verify count
            count_after = session.query(AptitudeQuestion).filter(
                AptitudeQuestion.topic == "Time Speed Distance"
            ).count()
            print(f"📉 Remaining count: {count_after}")
        else:
            print("⚠️ No questions found to delete.")

    except Exception as e:
        print(f"❌ Error during deletion: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    delete_tsd_questions()
