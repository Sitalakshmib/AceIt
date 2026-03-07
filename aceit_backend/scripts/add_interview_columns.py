"""
Adds new analytics columns to the existing interview_sessions table in Neon DB.
Run this once before running the migration script.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv
load_dotenv()

from database_postgres import SessionLocal
from sqlalchemy import text


ALTER_STATEMENTS = [
    "ALTER TABLE interview_sessions ADD COLUMN IF NOT EXISTS scores FLOAT[] DEFAULT ARRAY[]::FLOAT[]",
    "ALTER TABLE interview_sessions ADD COLUMN IF NOT EXISTS qa_pairs JSONB DEFAULT '[]'::jsonb",
    "ALTER TABLE interview_sessions ADD COLUMN IF NOT EXISTS weak_areas TEXT[] DEFAULT ARRAY[]::TEXT[]",
    "ALTER TABLE interview_sessions ADD COLUMN IF NOT EXISTS feedback JSONB",
    "ALTER TABLE interview_sessions ADD COLUMN IF NOT EXISTS indicators JSONB",
    "ALTER TABLE interview_sessions ADD COLUMN IF NOT EXISTS last_feedback JSONB",
    "ALTER TABLE interview_sessions ADD COLUMN IF NOT EXISTS round INTEGER DEFAULT 1",
    "ALTER TABLE interview_sessions ADD COLUMN IF NOT EXISTS answer_count INTEGER DEFAULT 0",
]


def run():
    print("Adding analytics columns to interview_sessions table...")
    db = SessionLocal()
    try:
        for stmt in ALTER_STATEMENTS:
            col = stmt.split("ADD COLUMN IF NOT EXISTS ")[1].split(" ")[0]
            try:
                db.execute(text(stmt))
                db.commit()
                print(f"  ✅ Added: {col}")
            except Exception as e:
                db.rollback()
                print(f"  ⚠️  Skipped {col}: {e}")

        # Verify
        result = db.execute(text(
            "SELECT column_name FROM information_schema.columns "
            "WHERE table_name='interview_sessions' ORDER BY ordinal_position"
        ))
        cols = [r[0] for r in result]
        print(f"\nFinal columns in interview_sessions: {cols}")
        print("\n✅ Schema update complete!")
    finally:
        db.close()


if __name__ == "__main__":
    run()
