import os
import sys
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.aptitude_sql import AptitudeQuestion
from database_postgres import get_db

load_dotenv()

def shuffle_all_questions():
    print("🚀 Starting Database Option Shuffle...")
    
    # Connect manually for script
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        print("❌ DATABASE_URL not found!")
        return

    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Fetch all questions
        questions = session.query(AptitudeQuestion).all()
        print(f"📊 Found {len(questions)} questions to process.")
        
        updated_count = 0
        
        for q in questions:
            if not q.options or len(q.options) < 2:
                continue
            
            # Get current correct answer text
            try:
                correct_text = q.options[q.correct_answer]
            except IndexError:
                # Handle cases where index might be out of bounds (corrupt data)
                print(f"⚠️ Corrupt data for ID {q.id}: Index {q.correct_answer} out of bounds for options len {len(q.options)}")
                continue
                
            # Zip options with indices to track them if needed, but easier to just shuffle list
            # and find new index of correct_text
            
            # Create a copy and shuffle
            shuffled_options = q.options.copy()
            random.shuffle(shuffled_options)
            
            # Find new index
            try:
                new_correct_index = shuffled_options.index(correct_text)
            except ValueError:
                 print(f"⚠️ Error finding '{correct_text}' in shuffled options for ID {q.id}")
                 continue

            # Update fields
            # Note: SQLAlchemy detects mutation of mutable attributes like lists differently depending on configuration.
            # Best practice is to re-assign the list.
            q.options = shuffled_options
            q.correct_answer = new_correct_index
            
            updated_count += 1
            
        session.commit()
        print(f"✅ Successfully shuffled {updated_count} questions.")
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    shuffle_all_questions()
