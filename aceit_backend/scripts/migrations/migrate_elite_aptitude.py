"""
Database Migration Script for Elite Aptitude System

Adds new columns to existing aptitude_questions and user_aptitude_progress tables
to support elite-level adaptive learning features.

IMPORTANT: This is a backward-compatible migration. Existing data will not be affected.
"""

from sqlalchemy import create_engine, text
from database_postgres import DATABASE_URL
import os

def run_migration():
    """Execute database migration"""
    
    print("[Migration] Starting Elite Aptitude System database migration...")
    print(f"[Migration] Database URL: {DATABASE_URL[:30]}...")
    
    engine = create_engine(DATABASE_URL)
    
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
                    print(f"  ⚠ {migration[:60]}... (may already exist)")
            
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
                    print(f"  ⚠ {migration[:60]}... (may already exist)")
            
            # Commit changes
            conn.commit()
            
            print("\n[Migration] ✅ Migration completed successfully!")
            print("[Migration] Elite aptitude system is ready to use.")
            
        except Exception as e:
            conn.rollback()
            print(f"\n[Migration] ❌ Migration failed: {e}")
            raise


def verify_migration():
    """Verify that migration was successful"""
    
    print("\n[Verification] Checking migration status...")
    
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        # Check aptitude_questions columns
        result = conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'aptitude_questions'
        """))
        
        columns = [row[0] for row in result]
        
        required_columns = [
            'primary_concepts', 'trap_explanation', 'optimal_solution_strategy',
            'common_mistake', 'time_to_solve_sec', 'concept_depth',
            'cognitive_load', 'trap_density', 'follow_up_logic',
            'discriminatory_index', 'elite_accuracy_rate'
        ]
        
        missing = [col for col in required_columns if col not in columns]
        
        if missing:
            print(f"  ⚠ Missing columns in aptitude_questions: {missing}")
        else:
            print("  ✓ All aptitude_questions columns present")
        
        # Check user_aptitude_progress columns
        result = conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'user_aptitude_progress'
        """))
        
        columns = [row[0] for row in result]
        
        required_columns = [
            'conceptual_errors', 'careless_errors', 'overthinking_errors',
            'time_pressure_errors', 'current_concept_depth',
            'current_cognitive_load', 'current_trap_density', 'user_tier'
        ]
        
        missing = [col for col in required_columns if col not in columns]
        
        if missing:
            print(f"  ⚠ Missing columns in user_aptitude_progress: {missing}")
        else:
            print("  ✓ All user_aptitude_progress columns present")
        
        print("\n[Verification] Complete!")


if __name__ == "__main__":
    print("="*70)
    print("ELITE APTITUDE SYSTEM - DATABASE MIGRATION")
    print("="*70)
    
    # Check if using SQLite or PostgreSQL
    if DATABASE_URL.startswith("sqlite"):
        print("\n⚠️  WARNING: SQLite detected!")
        print("SQLite has limited ALTER TABLE support.")
        print("For SQLite, you may need to recreate tables or use SQLAlchemy's create_all().")
        print("\nRecommendation: Delete aceit_dev.db and let SQLAlchemy recreate it.")
        
        response = input("\nProceed with migration anyway? (y/n): ")
        if response.lower() != 'y':
            print("Migration cancelled.")
            exit(0)
    
    try:
        run_migration()
        verify_migration()
        
        print("\n" + "="*70)
        print("✅ MIGRATION SUCCESSFUL!")
        print("="*70)
        print("\nNext steps:")
        print("1. Test the new elite endpoints")
        print("2. Generate sample questions")
        print("3. Verify adaptive intelligence")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        print("\nTroubleshooting:")
        print("- Check database connection")
        print("- Verify table names match your schema")
        print("- For SQLite: Consider recreating the database")
