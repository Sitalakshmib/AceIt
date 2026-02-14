
import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Add parent directory to path to use auth utils
sys.path.append(os.path.join(os.getcwd(), 'aceit_backend'))
from routes.auth import hash_password, verify_password

def reset_to_karthika():
    load_dotenv('aceit_backend/.env')
    DATABASE_URL = os.getenv('DATABASE_URL')
    if not DATABASE_URL:
        print("DATABASE_URL not found")
        return

    email = "k@gmail.com"
    new_pwd = "karthika"
    
    # Use our patched hash_password (includes 72-byte safety)
    hashed_password = hash_password(new_pwd)

    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        result = conn.execute(
            text("UPDATE users SET password = :password WHERE email = :email"),
            {"password": hashed_password, "email": email}
        )
        conn.commit()
        print(f"✅ Successfully set password for {email} to '{new_pwd}'")
        
        # Immediate verification
        verify_result = conn.execute(text("SELECT password FROM users WHERE email = :email"), {"email": email})
        stored_hash = verify_result.fetchone()[0]
        if verify_password(new_pwd, stored_hash):
            print("✅ Verification successful: New hash matches 'karthika'.")
        else:
            print("❌ Verification failed: Hash mismatch!")

if __name__ == "__main__":
    reset_to_karthika()
