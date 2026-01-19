from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def view_neon_data():
    if not DATABASE_URL:
        print("DATABASE_URL not found in .env")
        return

    print(f"Attempting to connect to Neon database...")
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            print("\n[SUCCESS] Connected to Neon successfully!\n")
            
            print("--- REGISTERED USERS IN NEON ---")
            result = conn.execute(text("SELECT username, email, created_at FROM users"))
            rows = result.fetchall()
            
            if not rows:
                print("No active users found in the Neon database.")
            else:
                print(f"{'USERNAME':<20} | {'EMAIL':<30} | {'CREATED AT'}")
                print("-" * 80)
                for row in rows:
                    print(f"{row.username:<20} | {row.email:<30} | {row.created_at}")
            print("\n------------------------------")
            
    except Exception as e:
        print("\n[ERROR] Connection to Neon Failed!")
        print(f"Error Details: {e}")

if __name__ == "__main__":
    view_neon_data()
