import os
import sys

# Add current dir to path
sys.path.append(os.getcwd())

from database_postgres import SessionLocal
from models.user_sql import User
from sqlalchemy import text

def check_postgres():
    print("Checking PostgreSQL connection...")
    try:
        db = SessionLocal()
        # Try a simple query
        db.execute(text("SELECT 1"))
        print("✅ Connection successful!")
        
        # Check users
        users = db.query(User).all()
        with open("scripts/users_list.txt", "w") as f:
            f.write(f"Found {len(users)} users in PostgreSQL:\n")
            for u in users:
                f.write(f"- {u.username} ({u.email})\n")
        
        db.close()
    except Exception as e:
        with open("scripts/users_list.txt", "w") as f:
            f.write(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    check_postgres()
