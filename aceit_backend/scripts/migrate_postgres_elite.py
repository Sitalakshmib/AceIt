"""
PostgreSQL Migration for Elite Aptitude System

Adds elite metadata columns to existing PostgreSQL database.
Run from aceit_backend directory:
    python3 scripts/migrate_postgres_elite.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("❌ DATABASE_URL not found in .env file")
    exit(1)

print(f"[Migration] Connecting to PostgreSQL database...")
print(f"[Migration] Host: {DATABASE_URL.split('@')[1].split('/')[0] if '@' in DATABASE_URL else 'unknown'}")

engine = create_engine(DATABASE_URL)

def run_migration():
    """Execute database migration"""
    
    with engine.connect() as conn:
        try:
            # ===== APTITUDE_QUESTIONS TABLE MIGRATIONS =====
            print("\n[Migration] Adding columns to aptitude_questions table...")
            
            migrations_aptitude = [
                # Elite metadata columns
                "ALTER TABLE aptitude_questions ADD COLUMN IF NOT EXISTS primary_concepts TEXT[]",
                "ALTER TABLE aptitude_questions ADD COLUMN IF NOT EXISTS trap_explanation TEXT",
                "ALTER TABLE aptitude_questions ADD COLUMN IF NOT EXISTS optimal_solution_strategy TEXT",
                "ALTER TABLE aptitude_questions ADD COLUMN IF NOT EXISTS common_mistake TEXT",
                "ALTER TABLE aptitude_questions ADD COLUMN IF NOT EXISTS time_to_solve_sec INTEGER DEFAULT 120",
                
                # Multi-dimensional difficulty columns
                "ALTER TABLE aptitude_questions ADD COLUMN IF NOT EXISTS concept_depth VARCHAR(20) DEFAULT 'single'",
                "ALTER TABLE aptitude_questions ADD COLUMN IF NOT EXISTS cognitive_load VARCHAR(20) DEFAULT 'low'",
                "ALTER TABLE aptitude_questions ADD COLUMN IF NOT EXISTS trap_density VARCHAR(20) DEFAULT 'low'",
                
                # Follow-up logic and quality metrics
                "ALTER TABLE aptitude_questions ADD COLUMN IF NOT EXISTS follow_up_logic TEXT",
                "ALTER TABLE aptitude_questions ADD COLUMN IF NOT EXISTS discriminatory_index FLOAT DEFAULT 0.0",
                "ALTER TABLE aptitude_questions ADD COLUMN IF NOT EXISTS elite_accuracy_rate FLOAT DEFAULT 0.0",
            ]
            
            for migration in migrations_aptitude:
                try:
                    conn.execute(text(migration))
                    print(f"  ✓ {migration[:60]}...")
                except Exception as e:
                    if "already exists" in str(e).lower():
                        print(f"  ⚠ Column already exists (skipping)")
                    else:
                        raise
            
            # ===== USER_APTITUDE_PROGRESS TABLE MIGRATIONS =====
            print("\n[Migration] Adding columns to user_aptitude_progress table...")
            
            migrations_progress = [
                # Error pattern tracking
                "ALTER TABLE user_aptitude_progress ADD COLUMN IF NOT EXISTS conceptual_errors INTEGER DEFAULT 0",
                "ALTER TABLE user_aptitude_progress ADD COLUMN IF NOT EXISTS careless_errors INTEGER DEFAULT 0",
                "ALTER TABLE user_aptitude_progress ADD COLUMN IF NOT EXISTS overthinking_errors INTEGER DEFAULT 0",
                "ALTER TABLE user_aptitude_progress ADD COLUMN IF NOT EXISTS time_pressure_errors INTEGER DEFAULT 0",
                
                # Multi-dimensional state
                "ALTER TABLE user_aptitude_progress ADD COLUMN IF NOT EXISTS current_concept_depth VARCHAR(20) DEFAULT 'single'",
                "ALTER TABLE user_aptitude_progress ADD COLUMN IF NOT EXISTS current_cognitive_load VARCHAR(20) DEFAULT 'low'",
                "ALTER TABLE user_aptitude_progress ADD COLUMN IF NOT EXISTS current_trap_density VARCHAR(20) DEFAULT 'low'",
                
                # Performance classification
                "ALTER TABLE user_aptitude_progress ADD COLUMN IF NOT EXISTS user_tier VARCHAR(20) DEFAULT 'developing'",
            ]
            
            for migration in migrations_progress:
                try:
                    conn.execute(text(migration))
                    print(f"  ✓ {migration[:60]}...")
                except Exception as e:
                    if "already exists" in str(e).lower():
                        print(f"  ⚠ Column already exists (skipping)")
                    else:
                        raise
            
            # Commit changes
            conn.commit()
            
            print("\n[Migration] ✅ Migration completed successfully!")
            print("[Migration] Elite aptitude system is ready to use.")
            
        except Exception as e:
            conn.rollback()
            print(f"\n[Migration] ❌ Migration failed: {e}")
            raise


if __name__ == "__main__":
    print("="*70)
    print("ELITE APTITUDE SYSTEM - POSTGRESQL MIGRATION")
    print("="*70)
    
    try:
        run_migration()
        
        print("\n" + "="*70)
        print("✅ MIGRATION SUCCESSFUL!")
        print("="*70)
        print("\nNext steps:")
        print("1. Seed questions: python3 scripts/seed_basic_questions.py")
        print("2. Test the system: http://localhost:5173/")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        print("\nTroubleshooting:")
        print("- Check database connection")
        print("- Verify DATABASE_URL in .env file")
        print("- Ensure you have permission to ALTER tables")
