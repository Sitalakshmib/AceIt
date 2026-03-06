"""
One-Time Migration Script: Interview Sessions JSON → Neon DB

Reads all existing sessions from data/interview_sessions.json
and upserts them into the interview_sessions table in Neon.

Safe to run multiple times (upserts are idempotent).

Usage:
    cd d:\AceIt\aceit_backend
    python scripts/migrate_interview_json_to_db.py
"""

import sys
import os
import json

# Ensure project root is on the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv
load_dotenv()

from database_postgres import SessionLocal, engine, Base
from models.interview_models import InterviewSession, InterviewHistory
from services.interview_session_service import upsert_session

SESSIONS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "interview_sessions.json")


def run_migration():
    print("=" * 60)
    print("Interview Sessions Migration: JSON → Neon DB")
    print("=" * 60)

    # 1. Ensure tables exist
    print("\n[1] Ensuring interview_sessions table exists in Neon...")
    try:
        Base.metadata.create_all(bind=engine, tables=[
            InterviewSession.__table__,
            InterviewHistory.__table__
        ])
        print("    ✅ Tables ready")
    except Exception as e:
        print(f"    ❌ Table creation failed: {e}")
        sys.exit(1)

    # 2. Load JSON
    sessions_path = os.path.abspath(SESSIONS_FILE)
    if not os.path.exists(sessions_path):
        print(f"\n❌ Sessions file not found at: {sessions_path}")
        print("   Nothing to migrate.")
        return

    print(f"\n[2] Loading sessions from: {sessions_path}")
    with open(sessions_path, "r") as f:
        all_sessions = json.load(f)
    print(f"    Found {len(all_sessions)} sessions")

    # 3. Upsert each session
    print(f"\n[3] Migrating sessions to Neon DB...")
    db = SessionLocal()
    success = 0
    failed = 0

    try:
        for session_id, session_dict in all_sessions.items():
            # Ensure session has an id field
            if "id" not in session_dict:
                session_dict["id"] = session_id

            ok = upsert_session(db, session_dict)
            if ok:
                success += 1
                print(f"    ✅ {session_id[:8]}... | {session_dict.get('interview_type', '?')} | "
                      f"user={session_dict.get('user_id', '?')[:12]}... | "
                      f"scores={len(session_dict.get('scores', []))} scores")
            else:
                failed += 1
                print(f"    ❌ Failed: {session_id}")
    finally:
        db.close()

    # 4. Summary
    print("\n" + "=" * 60)
    print(f"Migration Complete!")
    print(f"  ✅ Migrated: {success} sessions")
    if failed:
        print(f"  ❌ Failed:   {failed} sessions")
    print("=" * 60)

    # 5. Verify
    print("\n[4] Verifying data in Neon DB...")
    db = SessionLocal()
    try:
        count = db.query(InterviewSession).count()
        print(f"    Total sessions in DB: {count}")
        sample = db.query(InterviewSession).first()
        if sample:
            scores_count = len(sample.scores) if sample.scores else 0
            qa_count = len(sample.qa_pairs) if sample.qa_pairs else 0
            print(f"    Sample session: {sample.id[:8]}... | scores={scores_count} | qa_pairs={qa_count}")
    finally:
        db.close()

    print("\n✅ Migration complete! Interview sessions are now persisted in Neon DB.")


if __name__ == "__main__":
    run_migration()
