from sqlalchemy import Column, String, DateTime, JSON, ForeignKey
from database_postgres import Base
import datetime
import uuid

class ActivityProgress(Base):
    """Universal progress tracking model to replace progress.json"""
    __tablename__ = "activity_progress"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), index=True, nullable=False)
    module = Column(String, index=True, nullable=False)  # 'coding', 'aptitude', 'resume', 'communication'
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    
    # Store dynamic module-specific payload
    # e.g., {'percentage': 100, 'action': 'run'} for coding
    payload = Column(JSON, default={})
    
    def to_dict(self):
        """Convert to dict matching old progress.json schema"""
        data = {
            "id": self.id,
            "user_id": self.user_id,
            "module": self.module,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
        }
        # Merge payload properties into top level for backwards compatibility
        if self.payload:
            for k, v in self.payload.items():
                if k not in data:  # Don't overwrite base fields
                    data[k] = v
        return data
