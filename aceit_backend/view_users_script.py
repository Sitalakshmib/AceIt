from sqlalchemy import create_engine, text
import os

# CONFIGURATION
# If you have a different password, verify it here or set DB_PASSWORD env var
DB_PASSWORD = os.getenv("DB_PASSWORD", "nayagarapopo,14") 
DB_USER = "postgres"
DB_NAME = "aceit_db"
DB_HOST = "localhost"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

def view_data():
    print(f"Attempting to connect to database: {DB_NAME} on {DB_HOST}...")
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            print("\n[SUCCESS] Connected successfully!\n")
            
            print("--- REGISTERED USERS ---")
            # Select relevant columns (excluding password hash for clarity)
            result = conn.execute(text("SELECT username, email, created_at FROM users"))
            rows = result.fetchall()
            
            if not rows:
                print("No active users found in the database.")
            else:
                print(f"{'USERNAME':<20} | {'EMAIL':<30} | {'CREATED AT'}")
                print("-" * 80)
                for row in rows:
                    print(f"{row.username:<20} | {row.email:<30} | {row.created_at}")
            print("\n------------------------")
            
    except Exception as e:
        print("\n[ERROR] Connection Failed!")
        print(f"Error Details: {e}")
        print("\n[TROUBLESHOOTING]:")
        print(f"1. Make sure PostgreSQL is running.")
        print(f"2. Check if password '{DB_PASSWORD}' is correct for user '{DB_USER}'.")
        print(f"3. Open this file ('view_users_script.py') and update DB_PASSWORD variable.")

if __name__ == "__main__":
    view_data()
