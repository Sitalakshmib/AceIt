import sys
import os
import json

# Add parent directory to path to import database_postgres
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_postgres import engine
from sqlalchemy import text

def fetch_and_save():
    print("Connecting to DB...")
    # engine is already initialized in database_postgres
    if not engine:
        print("Failed to connect to DB.")
        return

    print("Fetching problems...")
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM coding_problems"))
        problems = result.fetchall()

    print(f"Found {len(problems)} problems.")
    
    formatted_problems = []
    for p in problems:
        # Convert row to dict (assuming columns)
        # We need to know column names. Result keys usually available.
        # SQLAlchemy 2.0 returns Row objects.
        
        # Mapping based on typical schema
        prob_dict = {
            "id": p.id, # or p[0]
            "title": p.title,
            "titleSlug": p.title_slug if hasattr(p, 'title_slug') else p.title.lower().replace(" ", "-"),
            "description": p.description,
            "difficulty": p.difficulty,
            "tags": p.tags if p.tags else [],
            "function_name": "solution", # Default or from DB if exists
            "starter_code": p.starter_code if p.starter_code else {},
            "test_cases": p.test_cases if p.test_cases else []
        }
        
        if hasattr(p, 'function_name') and p.function_name:
             prob_dict["function_name"] = p.function_name
        
        formatted_problems.append(prob_dict)

    print(f"Formatted {len(formatted_problems)} problems.")

    import pprint
    
    # Write to file
    output_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "services", "full_problem_data.py")
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# Full dataset fetched from Neon DB\n\n")
        f.write("FULL_PROBLEM_DATA = ")
        f.write(pprint.pformat(formatted_problems, indent=4))
    
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    fetch_and_save()
