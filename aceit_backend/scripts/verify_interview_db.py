"""Quick verification script — checks Neon DB contains migrated interview sessions with scores/qa_pairs."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dotenv import load_dotenv; load_dotenv()
from database_postgres import SessionLocal
from models.interview_models import InterviewSession

db = SessionLocal()
try:
    total = db.query(InterviewSession).count()
    print(f"Total sessions in Neon DB: {total}")

    # Check sessions WITH scores
    with_scores = db.query(InterviewSession).filter(InterviewSession.scores != None).all()
    print(f"Sessions with scores data: {len([s for s in with_scores if s.scores])}")

    # Show sample per type
    for itype in ["technical", "hr", "video-practice"]:
        rows = db.query(InterviewSession).filter(InterviewSession.interview_type == itype).all()
        if rows:
            s = rows[0]
            print(f"  [{itype}] {s.id[:12]}... | scores={s.scores[:3] if s.scores else []} | qa_pairs={len(s.qa_pairs) if s.qa_pairs else 0}")
        else:
            print(f"  [{itype}] No sessions")
    print("\n✅ Verification complete!")
finally:
    db.close()
