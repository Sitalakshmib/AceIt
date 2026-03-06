"""Create gd_sessions and resume_analyses tables in Neon DB."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dotenv import load_dotenv; load_dotenv()
from database_postgres import engine, Base, SessionLocal
from models.gd_resume_sql import GDSession, ResumeAnalysis
from sqlalchemy import text

# Create tables
Base.metadata.create_all(bind=engine, tables=[GDSession.__table__, ResumeAnalysis.__table__])
print("Tables created: gd_sessions, resume_analyses")

# Verify columns
db = SessionLocal()
try:
    result = db.execute(text(
        "SELECT table_name, column_name FROM information_schema.columns "
        "WHERE table_name IN ('gd_sessions','resume_analyses') "
        "ORDER BY table_name, ordinal_position"
    ))
    rows = result.fetchall()
    current_table = None
    for table_name, col in rows:
        if table_name != current_table:
            current_table = table_name
            print(f"\n  [{table_name}]")
        print(f"    - {col}")
    print("\n✅ GD and Resume tables ready in Neon!")
finally:
    db.close()
