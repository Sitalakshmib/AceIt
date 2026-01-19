from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Fallback to SQLite for development if no PostgreSQL URL provided
if not DATABASE_URL:
    print("[WARNING] DATABASE_URL not found. Using SQLite fallback for development.")
    DATABASE_URL = "sqlite:///./aceit_dev.db"
    
    # Create the database file directory if it doesn't exist
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "aceit_dev.db")
    print(f"[INFO] Using SQLite database at: {db_path}")

# For SQLite, we need to add check_same_thread=False for FastAPI development
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=300,
        pool_size=10,
        max_overflow=20
    )

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
