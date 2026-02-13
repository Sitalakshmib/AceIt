
import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'aceit_backend'))
from database_postgres import SessionLocal
from sqlalchemy import text

try:
    db = SessionLocal()
    print("Attempting to connect to DB...")
    result = db.execute(text("SELECT 1"))
    print("Connection successful:", result.fetchone())
    db.close()
except Exception as e:
    print("Connection failed:", e)
