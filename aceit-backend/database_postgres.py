from sqlalchemy import create_engine, text
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

# Add connection timeout and pooling settings to prevent hanging
try:
    engine = create_engine(
        DATABASE_URL,
        connect_args={
            "connect_timeout": 5  # 5 second timeout
        },
        pool_pre_ping=True,  # Verify connections before using
        pool_recycle=3600  # Recycle connections every hour
    )
    # Test the connection
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("✅ Database connection established successfully!")
except Exception as e:
    print(f"⚠️ Warning: Could not connect to database: {e}")
    print("📦 App will use local data fallback")
    # Create a dummy engine that will fail gracefully
    engine = None

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) if engine else None

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
    from models.coding_problem_sql import CodingProblem
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")
