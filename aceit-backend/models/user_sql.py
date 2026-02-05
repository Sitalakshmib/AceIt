from sqlalchemy import Column, String, DateTime
from database_postgres import Base
import datetime
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True)
    username = Column(String)
    password = Column(String)  # Storing hashed password
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
