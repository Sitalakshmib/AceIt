import sys
import os
from passlib.context import CryptContext

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_postgres import SessionLocal
from models.user_sql import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def test_login(email, password):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if user:
            print(f"User found: {user.email}")
            print(f"Stored Hash: '{user.password}'")
            
            try:
                is_valid = pwd_context.verify(password, user.password)
                print(f"Password Valid: {is_valid}")
            except Exception as e:
                print(f"Verify Error: {e}")
                import traceback
                traceback.print_exc()
        else:
            print(f"User {email} not found.")
    except Exception as e:
        print(f"DB Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_login("randneleh@gmail.com", "password123")
