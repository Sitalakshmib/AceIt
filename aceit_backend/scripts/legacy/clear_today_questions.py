"""
Script to clear aptitude questions generated today from Neon PostgreSQL database.
This will remove only questions created on the current date (UTC).
"""

import os
import sys
from datetime import datetime, timedelta

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

# Get today's date (UTC)
today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
today_end = today_start + timedelta(days=1)

print(f"📅 Looking for questions created between:")
print(f"   Start: {today_start}")
print(f"   End:   {today_end}")

with engine.connect() as conn:
    # First, count how many questions will be deleted
    count_query = text("""
        SELECT COUNT(*) as count, category, topic
        FROM aptitude_questions 
        WHERE created_at >= :start_date AND created_at < :end_date
        GROUP BY category, topic
        ORDER BY category, topic
    """)
    
    result = conn.execute(count_query, {"start_date": today_start, "end_date": today_end})
    rows = result.fetchall()
    
    if not rows:
        print("\n✅ No questions found created today. Database is clean!")
        sys.exit(0)
    
    print("\n📊 Questions to be deleted:")
    print("-" * 50)
    total = 0
    for row in rows:
        print(f"   {row[1]} > {row[2]}: {row[0]} questions")
        total += row[0]
    print("-" * 50)
    print(f"   TOTAL: {total} questions")
    
    # Ask for confirmation
    print("\n⚠️  WARNING: This action cannot be undone!")
    confirm = input("Type 'DELETE' to confirm deletion: ")
    
    if confirm != "DELETE":
        print("❌ Deletion cancelled.")
        sys.exit(0)
    
    # Delete the questions and dependent attempts
    
    # 1. Delete dependent attempts first
    delete_attempts_query = text("""
        DELETE FROM question_attempts 
        WHERE question_id IN (
            SELECT id FROM aptitude_questions 
            WHERE created_at >= :start_date AND created_at < :end_date
        )
    """)
    
    print("\n🗑️  Deleting related question attempts...")
    result_attempts = conn.execute(delete_attempts_query, {"start_date": today_start, "end_date": today_end})
    print(f"   Deleted {result_attempts.rowcount} related attempts.")
    
    # 2. Delete the questions
    delete_query = text("""
        DELETE FROM aptitude_questions 
        WHERE created_at >= :start_date AND created_at < :end_date
    """)
    
    print("🗑️  Deleting questions...")
    result = conn.execute(delete_query, {"start_date": today_start, "end_date": today_end})
    conn.commit()
    
    print(f"\n✅ Successfully deleted {result.rowcount} questions created today!")
    print("🔄 The system will now generate fresh questions when you practice.")
