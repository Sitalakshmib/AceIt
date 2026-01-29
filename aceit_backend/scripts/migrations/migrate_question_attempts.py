"""
Add category and topic columns to question_attempts table
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_postgres import SessionLocal, engine
from sqlalchemy import text

def migrate():
    db = SessionLocal()
    try:
        print("Adding category and topic columns to question_attempts table...")
        
        # Check if columns already exist
        result = db.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'question_attempts' 
            AND column_name IN ('category', 'topic')
        """))
        
        existing_columns = [row[0] for row in result]
        
        if 'category' not in existing_columns:
            db.execute(text("ALTER TABLE question_attempts ADD COLUMN category VARCHAR"))
            print("✅ Added 'category' column")
        else:
            print("ℹ️  'category' column already exists")
        
        if 'topic' not in existing_columns:
            db.execute(text("ALTER TABLE question_attempts ADD COLUMN topic VARCHAR"))
            print("✅ Added 'topic' column")
        else:
            print("ℹ️  'topic' column already exists")
        
        db.commit()
        print("\n✅ Migration completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    migrate()
