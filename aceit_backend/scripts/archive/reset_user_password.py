import sys
import os
from passlib.context import CryptContext

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_postgres import SessionLocal
from models.user_sql import User

# Setup password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def reset_password(email, new_password):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if user:
            print(f"User found: {user.email}")
            print(f"Old Hash: '{user.password}'")
            
            hashed_password = pwd_context.hash(new_password)
            user.password = hashed_password
            
            db.commit()
            print(f"Password reset successfully. New stored hash: {hashed_password}")
        else:
            print(f"User {email} not found.")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    reset_password("randneleh@gmail.com", "password123")
