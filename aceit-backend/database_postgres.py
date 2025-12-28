from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Default to local postgres if not set in environment
# Format: postgresql://user:password@host/dbname
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:nayagarapopo,14@localhost/aceit_db")

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
