from sqlalchemy import Column, String, DateTime
from database_postgres import Base
import datetime
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True)
    username = Column(String)
    password = Column(String, nullable=True)  # Storing hashed password (nullable for OAuth)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # OAuth specific fields
    google_id = Column(String, unique=True, nullable=True)
    auth_provider = Column(String, default="local") # local, google, etc.
    profile_picture = Column(String, nullable=True)
