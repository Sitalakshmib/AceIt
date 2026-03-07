"""
Interview Session Service

Handles persisting and loading interview sessions to/from Neon (PostgreSQL).
Used by SimVoiceInterviewer to replace JSON file storage as primary store.
"""

from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert as pg_insert
from typing import Dict, Optional
from datetime import datetime

from models.interview_models import InterviewSession


def _parse_dt(val):
    """Safely convert string or datetime to datetime object."""
    if not val:
        return None
    if isinstance(val, datetime):
        return val
    try:
        return datetime.fromisoformat(str(val))
    except Exception:
        return None


def session_dict_to_row(session_dict: dict) -> dict:
    """
    Convert an in-memory session dict (from SimVoiceInterviewer) into a
    flat dict suitable for upserting into the `interview_sessions` table.
    """
    start_time = _parse_dt(session_dict.get("start_time"))

    # Determine completed_at: if status is completed and there's a last qa_pair timestamp
    completed_at = None
    qa_pairs = session_dict.get("qa_pairs", [])

    # For video-presence sessions, completion time can come from a timestamp field
    if session_dict.get("status") in ("completed",):
        # Try to get last timestamp from qa_pairs
        if qa_pairs:
            last_ts = None
            for qa in reversed(qa_pairs):
                ts = qa.get("timestamp")
                if ts:
                    last_ts = _parse_dt(ts)
                    break
            completed_at = last_ts

    return {
        "id": session_dict["id"],
        "user_id": session_dict.get("user_id", "unknown"),
        "interview_type": session_dict.get("interview_type", "technical"),
        "topic": session_dict.get("topic", "realtime"),
        "started_at": start_time or datetime.utcnow(),
        "completed_at": completed_at,
        "question_count": len(session_dict.get("q_bank", [])),
        "status": session_dict.get("status", "active"),
        # Analytics data
        "scores": session_dict.get("scores", []),
        "qa_pairs": qa_pairs,
        "weak_areas": session_dict.get("weak_areas", []),
        "feedback": session_dict.get("feedback"),
        "indicators": session_dict.get("indicators"),
        "last_feedback": session_dict.get("last_feedback"),
        # Session state
        "round": session_dict.get("round", 1),
        "answer_count": session_dict.get("answer_count", 0),
    }


def row_to_session_dict(row: InterviewSession) -> dict:
    """
    Convert an InterviewSession ORM row back to an in-memory session dict
    compatible with SimVoiceInterviewer.sessions.
    """
    return {
        "id": row.id,
        "user_id": row.user_id,
        "interview_type": row.interview_type,
        "topic": row.topic or "realtime",
        "start_time": row.started_at.isoformat() if row.started_at else None,
        "status": row.status or "active",
        "scores": list(row.scores) if row.scores else [],
        "qa_pairs": list(row.qa_pairs) if row.qa_pairs else [],
        "weak_areas": list(row.weak_areas) if row.weak_areas else [],
        "feedback": row.feedback or {},
        "indicators": row.indicators or {},
        "last_feedback": row.last_feedback,
        "round": row.round or 1,
        "answer_count": row.answer_count or 0,
        # Provide empty defaults for fields not stored in DB (runtime-only)
        "history": [],
        "q_bank": [],
        "current_q_index": 0,
        "resume": "",
        "jd": "",
        "project_text": "",
    }


def upsert_session(db: Session, session_dict: dict) -> bool:
    """
    Upsert a session dict into the interview_sessions table.
    Returns True on success, False on error.
    """
    try:
        row_data = session_dict_to_row(session_dict)

        stmt = pg_insert(InterviewSession).values(**row_data)
        stmt = stmt.on_conflict_do_update(
            index_elements=["id"],
            set_={
                "status": stmt.excluded.status,
                "scores": stmt.excluded.scores,
                "qa_pairs": stmt.excluded.qa_pairs,
                "weak_areas": stmt.excluded.weak_areas,
                "feedback": stmt.excluded.feedback,
                "indicators": stmt.excluded.indicators,
                "last_feedback": stmt.excluded.last_feedback,
                "round": stmt.excluded.round,
                "answer_count": stmt.excluded.answer_count,
                "completed_at": stmt.excluded.completed_at,
                "question_count": stmt.excluded.question_count,
            }
        )
        db.execute(stmt)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"[InterviewSessionService] Error upserting session {session_dict.get('id')}: {e}")
        return False


def load_all_sessions(db: Session) -> Dict[str, dict]:
    """
    Load all interview sessions from Neon DB.
    Returns a dict: {session_id: session_dict} compatible with engine.sessions.
    """
    try:
        rows = db.query(InterviewSession).all()
        sessions = {}
        for row in rows:
            sessions[row.id] = row_to_session_dict(row)
        print(f"[InterviewSessionService] Loaded {len(sessions)} sessions from Neon DB")
        return sessions
    except Exception as e:
        print(f"[InterviewSessionService] Error loading sessions from DB: {e}")
        return {}


def get_user_sessions(db: Session, user_id: str) -> Dict[str, dict]:
    """
    Load all sessions for a specific user from Neon DB.
    """
    try:
        rows = db.query(InterviewSession).filter(
            InterviewSession.user_id == user_id
        ).all()
        sessions = {}
        for row in rows:
            sessions[row.id] = row_to_session_dict(row)
        return sessions
    except Exception as e:
        print(f"[InterviewSessionService] Error loading user sessions: {e}")
        return {}
