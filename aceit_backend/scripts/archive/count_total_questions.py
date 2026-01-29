"""
Script to count total aptitude questions in the database.
"""

import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("❌ DATABASE_URL not found in .env")
    sys.exit(1)

print("🔗 Connecting to Neon PostgreSQL database...")
engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    count_query = text("SELECT COUNT(*) FROM aptitude_questions")
    result = conn.execute(count_query)
    total_count = result.scalar()
    
    print(f"\n📊 Total Aptitude Questions: {total_count}")
