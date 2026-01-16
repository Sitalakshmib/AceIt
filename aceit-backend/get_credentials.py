from sqlalchemy import create_engine, text
import os

# Configuration
DB_PASSWORD = os.getenv("DB_PASSWORD", "nayagarapopo,14") 
DB_USER = "postgres"
DB_NAME = "aceit_db"
DB_HOST = "localhost"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

def get_creds():
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT email, password FROM users"))
            rows = result.fetchall()
            
            if not rows:
                print("NO_USERS_FOUND")
            else:
                for row in rows:
                    # Strip 'hashed_' from password to show the plain credential for the user
                    plain_pass = row.password.replace("hashed_", "") if row.password.startswith("hashed_") else row.password
                    print(f"User: {row.email} | Password: {plain_pass}")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    get_creds()
