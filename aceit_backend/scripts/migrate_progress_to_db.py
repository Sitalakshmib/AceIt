import os
import sys
import json
from datetime import datetime

# Add parent directory to path so we can import models and DB
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_postgres import SessionLocal, init_db
from models.activity_progress_sql import ActivityProgress

PROGRESS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "progress.json")

def migrate():
    print("Initializing Database...")
    init_db()
    
    if not os.path.exists(PROGRESS_FILE):
        print(f"File {PROGRESS_FILE} not found. Nothing to migrate.")
        return

    print("Reading progress.json...")
    with open(PROGRESS_FILE, 'r') as f:
        try:
            progress_data = json.load(f)
        except json.JSONDecodeError:
            print("Failed to decode progress.json")
            return

    if not progress_data:
        print("progress.json is empty. Nothing to migrate.")
        return

    db = SessionLocal()
    try:
        migrated_count = 0
        skipped_count = 0
        for record in progress_data:
            rec_id = record.get("id")
            if not rec_id:
                skipped_count += 1
                continue
                
            # Check if already exists
            existing = db.query(ActivityProgress).filter(ActivityProgress.id == rec_id).first()
            if existing:
                skipped_count += 1
                continue
                
            # Extract core fields
            user_id = record.get("user_id")
            if not user_id:
                skipped_count += 1
                continue
                
            module = record.get("module", "unknown")
            timestamp_str = record.get("timestamp")
            timestamp = datetime.utcnow()
            if timestamp_str:
                try:
                    timestamp = datetime.fromisoformat(timestamp_str)
                except:
                    pass
            
            # Put remaining fields into payload
            payload = {}
            for k, v in record.items():
                if k not in ["id", "user_id", "module", "timestamp"]:
                    payload[k] = v
            
            new_record = ActivityProgress(
                id=rec_id,
                user_id=user_id,
                module=module,
                timestamp=timestamp,
                payload=payload
            )
            db.add(new_record)
            migrated_count += 1
            
        db.commit()
        print(f"Migration successful! Migrated {migrated_count} records. Skipped {skipped_count} (existing or invalid).")
    except Exception as e:
        db.rollback()
        print(f"Error during migration: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    migrate()
