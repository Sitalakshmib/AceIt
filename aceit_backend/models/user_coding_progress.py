from sqlalchemy import Column, String, Boolean, Integer, Text, DateTime
from database_postgres import Base
import datetime
import uuid


class UserCodingProgress(Base):
    """SQLAlchemy model for tracking user progress on coding problems."""
    __tablename__ = "user_coding_progress"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False)
    problem_id = Column(String, nullable=False)
    is_solved = Column(Boolean, default=False)
    attempts = Column(Integer, default=0)
    last_submission_code = Column(Text)
    last_submission_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def to_dict(self):
        """Convert model to dictionary for API responses."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "problem_id": self.problem_id,
            "is_solved": self.is_solved,
            "attempts": self.attempts,
            "last_submission_date": self.last_submission_date.isoformat() if self.last_submission_date else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
