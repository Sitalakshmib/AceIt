from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Neon Database connection
# Format: postgresql://user:password@host/dbname?sslmode=require
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Fallback for development if .env is missing
    DATABASE_URL = "postgresql://postgres:postgres@localhost/aceit_db"
    print("⚠️ Warning: DATABASE_URL not found in environment, falling back to local PostgreSQL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables
def init_db():
    """Initialize database tables"""
    from models.user_sql import User
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")
