from sqlalchemy import create_engine, text
import os

# Connect to 'postgres' database first to create the new db
DB_PASSWORD = os.getenv("DB_PASSWORD", "nayagarapopo,14")
DB_USER = "postgres"
DB_HOST = "localhost"
DEFAULT_DB = "postgres"
TARGET_DB = "aceit_db"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DEFAULT_DB}"

def create_database():
    engine = create_engine(DATABASE_URL, isolation_level="AUTOCOMMIT")
    with engine.connect() as conn:
        print(f"Connected to '{DEFAULT_DB}' database.")
        
        # Check if database exists
        result = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname = '{TARGET_DB}'"))
        exists = result.scalar()
        
        if exists:
            print(f"Database '{TARGET_DB}' already exists.")
        else:
            print(f"Creating database '{TARGET_DB}'...")
            conn.execute(text(f"CREATE DATABASE {TARGET_DB}"))
            print(f"Successfully created database '{TARGET_DB}'!")

if __name__ == "__main__":
    create_database()
