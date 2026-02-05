import os
import sys
import random
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from collections import Counter

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.aptitude_sql import AptitudeQuestion

load_dotenv()

def verify_shuffling():
    print("🕵️‍♀️ Verifying Database Shuffling...")
    
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        print("❌ DATABASE_URL not found!")
        return

    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Get total count
        count = session.query(AptitudeQuestion).count()
        print(f"📊 Total Questions in DB: {count}")
        
        # Sample random questions (Postgres RANDOM())
        print("\n🎲 Sampling 20 Random Questions across categories...")
        samples = session.query(AptitudeQuestion).order_by(func.random()).limit(20).all()
        
        correct_indices = []
        
        print(f"{'Cat/Topic':<40} | {'Correct Index':<15} | {'Correct Answer (Text Sample)':<30}")
        print("-" * 90)
        
        for q in samples:
            idx = q.correct_answer
            correct_indices.append(idx)
            
            # Safe access
            ans_text = "N/A"
            if q.options and 0 <= idx < len(q.options):
                ans_text = q.options[idx][:25] + "..."
            
            # Color code index
            idx_str = f"{idx}"
            if idx == 0: idx_str += " (A)"
            elif idx == 1: idx_str += " (B)"
            elif idx == 2: idx_str += " (C)"
            elif idx == 3: idx_str += " (D)"
            
            cat_topic = f"{q.category}/{q.topic}"[:38]
            
            print(f"{cat_topic:<40} | {idx_str:<15} | {ans_text:<30}")
            
        # Stats
        print("\n📈 Statistical Distribution of Correct Options:")
        ctr = Counter(correct_indices)
        total = len(correct_indices)
        
        for k in sorted(ctr.keys()):
            pct = (ctr[k] / total) * 100
            print(f"  Index {k}: {ctr[k]} ({pct:.1f}%)")
            
        if ctr[0] == total:
             print("\n⚠️ WARNING: All correct answers are Option A (Index 0). Shuffling has not applied yet.")
        else:
             print("\n✅ SUCCESS: Correct answers are distributed across indices.")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    verify_shuffling()
