"""
Create or verify guest user exists in database
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_postgres import SessionLocal
from models.user_sql import User
import uuid

def ensure_guest_user():
    db = SessionLocal()
    try:
        # Check if guest_user exists
        guest = db.query(User).filter(User.id == 'guest_user').first()
        
        if not guest:
            # Create guest user
            guest = User(
                id='guest_user',
                email='guest@aceit.com',
                username='Guest User',
                password='not_used'  # Guest doesn't need password
            )
            db.add(guest)
            db.commit()
            print("✅ Guest user created successfully")
        else:
            print("✅ Guest user already exists")
        
        # Also check if there are any regular users
        user_count = db.query(User).count()
        print(f"📊 Total users in database: {user_count}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    ensure_guest_user()
