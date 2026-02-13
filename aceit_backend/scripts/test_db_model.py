
import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'aceit_backend'))
from database_postgres import SessionLocal
from models.coding_problem_sql import CodingProblem

try:
    db = SessionLocal()
    print("Attempting to query CodingProblem...")
    problems = db.query(CodingProblem).limit(5).all()
    print(f"Query successful. Found {len(problems)} problems.")
    for p in problems:
        print(f" - {p.title} ({p.difficulty})")
    db.close()
except Exception as e:
    print("Query failed:", e)
    import traceback
    traceback.print_exc()
