import sys
import os

# Add parent directory to path to allow importing from backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_postgres import engine
from sqlalchemy import text

def migrate_users_table():
    print("Starting migration for users table...")
    with engine.connect() as connection:
        # Add google_id columnn if it doesn't exist
        try:
            connection.execute(text("ALTER TABLE users ADD COLUMN google_id VARCHAR UNIQUE"))
            print("Added google_id column")
        except Exception as e:
            print(f"google_id column might already exist: {e}")

        # Add auth_provider column if it doesn't exist
        try:
            connection.execute(text("ALTER TABLE users ADD COLUMN auth_provider VARCHAR DEFAULT 'local'"))
            print("Added auth_provider column")
        except Exception as e:
            print(f"auth_provider column might already exist: {e}")

        # Add profile_picture column if it doesn't exist
        try:
            connection.execute(text("ALTER TABLE users ADD COLUMN profile_picture VARCHAR"))
            print("Added profile_picture column")
        except Exception as e:
            print(f"profile_picture column might already exist: {e}")
            
        # Make password nullable
        try:
            connection.execute(text("ALTER TABLE users ALTER COLUMN password DROP NOT NULL"))
            print("Made password column nullable")
        except Exception as e:
            print(f"Could not alter password column: {e}")

        connection.commit()
    print("Migration completed.")

if __name__ == "__main__":
    migrate_users_table()
