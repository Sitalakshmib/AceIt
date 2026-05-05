import os
import sys

# Add parent directory to path to import db
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_postgres import SessionLocal
from models.activity_progress_sql import ActivityProgress

def show_progress():
    print("--- Database Activity Progress Table ---")
    db = SessionLocal()
    try:
        records = db.query(ActivityProgress).all()
        print(f"Total Records Found: {len(records)}\n")
        
        for i, record in enumerate(records, 1):
            print(f"Record #{i}")
            print(f"  Module: {record.module}")
            print(f"  Action/Score (from Payload): {record.payload.get('action') or record.payload.get('score', 'N/A')}")
            print(f"  Timestamp: {record.timestamp}")
            print(f"  Full Payload: {record.payload}")
            print("-" * 40)
            
    except Exception as e:
        print(f"Error reading database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    show_progress()
