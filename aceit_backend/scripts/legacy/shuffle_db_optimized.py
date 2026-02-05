"""
Optimized Database Shuffle Script
Shuffles answer options for ALL questions in the database with batch commits.
"""
import os
import sys
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.aptitude_sql import AptitudeQuestion

load_dotenv()

def shuffle_all_questions_optimized():
    print("🚀 Starting OPTIMIZED Database Option Shuffle...")
    
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
        total = len(questions)
        print(f"📊 Found {total} questions to process.")
        
        updated_count = 0
        batch_size = 500
        
        for i, q in enumerate(questions):
            if not q.options or len(q.options) < 2:
                continue
            
            # Get current correct answer text
            try:
                correct_text = q.options[q.correct_answer]
            except IndexError:
                print(f"⚠️ Corrupt data for ID {q.id}")
                continue
            
            # Shuffle options
            shuffled_options = q.options.copy()
            random.shuffle(shuffled_options)
            
            # Find new index
            try:
                new_correct_index = shuffled_options.index(correct_text)
            except ValueError:
                print(f"⚠️ Error finding correct answer for ID {q.id}")
                continue

            # Update fields
            q.options = shuffled_options
            q.correct_answer = new_correct_index
            updated_count += 1
            
            # Batch commit every batch_size questions
            if (i + 1) % batch_size == 0:
                session.commit()
                progress = ((i + 1) / total) * 100
                print(f"   ✓ Processed {i + 1}/{total} ({progress:.1f}%)")
        
        # Final commit
        session.commit()
        print(f"\n✅ Successfully shuffled {updated_count} questions!")
        
        # Verify distribution
        print("\n📈 Verifying correct answer distribution...")
        from sqlalchemy import func
        dist = session.query(AptitudeQuestion.correct_answer, func.count(AptitudeQuestion.id)).group_by(AptitudeQuestion.correct_answer).all()
        for idx, count in sorted(dist):
            pct = (count/total)*100
            print(f"   Index {idx}: {count} ({pct:.1f}%)")
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()

if __name__ == "__main__":
    shuffle_all_questions_optimized()
