from sqlalchemy import Column, String, Text, DateTime, JSON
from database_postgres import Base
import datetime
import uuid


class CodingProblem(Base):
    """SQLAlchemy model for coding problems stored in Neon PostgreSQL."""
    __tablename__ = "coding_problems"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    title_slug = Column(String(255), unique=True, index=True)
    description = Column(Text)  # HTML description with examples
    difficulty = Column(String(20))  # Easy, Medium, Hard
    tags = Column(JSON, default=list)  # List of tag strings
    function_name = Column(String(100))  # Function name to call for testing
    starter_code = Column(JSON, default=dict)  # Dict with language keys
    test_cases = Column(JSON, default=list)  # List of {input, output} dicts
    solution = Column(Text)  # Reference solution
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def to_dict(self):
        """Convert model to dictionary for API responses."""
        return {
            "id": self.id,
            "title": self.title,
            "titleSlug": self.title_slug,
            "description": self.description,
            "difficulty": self.difficulty,
            "tags": self.tags or [],
            "function_name": self.function_name,
            "starter_code": self.starter_code or {},
            "test_cases": self.test_cases or [],
            "solution": self.solution
        }
