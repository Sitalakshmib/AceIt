"""
Add missing user to database
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_postgres import SessionLocal
from models.user_sql import User

def add_user():
    db = SessionLocal()
    try:
        # The user ID from the error
        user_id = '2da86b5a-35cf-422c-8fa0-d6e60cc42ee4'
        
        # Check if user exists
        existing = db.query(User).filter(User.id == user_id).first()
        
        if existing:
            print(f"✅ User {user_id} already exists")
        else:
            # Create the user
            user = User(
                id=user_id,
                email='user@aceit.com',
                username='Test User',
                password='hashed_password'
            )
            db.add(user)
            db.commit()
            print(f"✅ User {user_id} created successfully")
        
        # Show all users
        all_users = db.query(User).all()
        print(f"\n📊 Total users in database: {len(all_users)}")
        for u in all_users:
            print(f"  - {u.id}: {u.email} ({u.username})")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_user()
