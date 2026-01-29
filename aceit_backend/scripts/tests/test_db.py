from database_postgres import SessionLocal, engine
from sqlalchemy import text

try:
    # Try to connect
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("\n✅ SUCCESS: Connected to PostgreSQL!")
except Exception as e:
    print(f"\n❌ ERROR: Could not connect to PostgreSQL.\nDetails: {e}")
