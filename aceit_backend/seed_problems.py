"""
Seed script to populate the coding_problems table in Neon PostgreSQL.
Run this once to migrate problems from local_problems.py to the database.

Usage:
    cd aceit-backend
    python seed_problems.py
"""

from database_postgres import SessionLocal, init_db
from models.coding_problem_sql import CodingProblem
from services.local_problems import get_local_problems


def seed_coding_problems():
    """Seed the database with coding problems from local_problems.py"""
    
    # Initialize database tables if they don't exist
    init_db()
    
    # Get database session
    db = SessionLocal()
    
    try:
        # Get local problems
        local_problems = get_local_problems()
        print(f"📚 Found {len(local_problems)} problems to seed...")
        
        added_count = 0
        skipped_count = 0
        
        for problem in local_problems:
            # Check if problem already exists
            existing = db.query(CodingProblem).filter(
                CodingProblem.id == problem["id"]
            ).first()
            
            if existing:
                print(f"  🔄 Updating '{problem['title']}'")
                existing.title = problem["title"]
                existing.title_slug = problem.get("titleSlug", problem["id"])
                existing.description = problem.get("description", "")
                existing.difficulty = problem.get("difficulty", "Medium")
                existing.tags = problem.get("tags", [])
                existing.function_name = problem.get("function_name", "")
                existing.starter_code = problem.get("starter_code", {})
                existing.test_cases = problem.get("test_cases", [])
                existing.solution = problem.get("solution", "")
                added_count += 1
                continue
            
            # Create new problem record
            new_problem = CodingProblem(
                id=problem["id"],
                title=problem["title"],
                title_slug=problem.get("titleSlug", problem["id"]),
                description=problem.get("description", ""),
                difficulty=problem.get("difficulty", "Medium"),
                tags=problem.get("tags", []),
                function_name=problem.get("function_name", ""),
                starter_code=problem.get("starter_code", {}),
                test_cases=problem.get("test_cases", []),
                solution=problem.get("solution", "")
            )
            
            db.add(new_problem)
            print(f"  ✅ Added '{problem['title']}' ({problem['difficulty']})")
            added_count += 1
        
        # Commit all changes
        db.commit()
        
        print(f"\n🎉 Seeding complete!")
        print(f"   Added: {added_count} problems")
        print(f"   Skipped: {skipped_count} problems (already existed)")
        print(f"   Total in DB: {db.query(CodingProblem).count()} problems")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def clear_all_problems():
    """Clear all problems from the database (for testing/reset)"""
    db = SessionLocal()
    try:
        count = db.query(CodingProblem).delete()
        db.commit()
        print(f"🗑️  Deleted {count} problems from database")
    except Exception as e:
        print(f"❌ Error clearing database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--clear":
        print("⚠️  Clearing all problems from database...")
        clear_all_problems()
    else:
        print("🌱 Seeding coding problems to Neon PostgreSQL...")
        seed_coding_problems()
