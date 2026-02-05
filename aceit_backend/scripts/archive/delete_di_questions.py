"""
Script to DELETE all Data Interpretation questions from the database.
"""
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.aptitude_sql import AptitudeQuestion
from database_postgres import Base

load_dotenv()

def delete_di_questions():
    print("🗑️  Starting Deletion of Data Interpretation Questions...")
    
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        print("❌ DATABASE_URL not found!")
        return

    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Check count before
        count_before = session.query(AptitudeQuestion).filter(
            AptitudeQuestion.category == "Data Interpretation"
        ).count()
        print(f"📊 Count BEFORE deletion: {count_before}")
        
        if count_before == 0:
            print("✅ Count is already 0. Nothing to delete.")
            return

        # Delete
        deleted = session.query(AptitudeQuestion).filter(
            AptitudeQuestion.category == "Data Interpretation"
        ).delete(synchronize_session=False)
        
        session.commit()
        print(f"✓ Deleted {deleted} questions.")
        
        # Verify count after
        count_after = session.query(AptitudeQuestion).filter(
            AptitudeQuestion.category == "Data Interpretation"
        ).count()
        print(f"📊 Count AFTER deletion: {count_after}")
        
        if count_after == 0:
            print("✅ SUCCESS: Data Interpretation questions count is 0.")
        else:
            print(f"❌ WARNING: Some questions remain ({count_after}).")
            
    except Exception as e:
        session.rollback()
        print(f"❌ Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    delete_di_questions()
