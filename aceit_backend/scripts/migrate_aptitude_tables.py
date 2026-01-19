"""
Database Migration Script - Add New Columns

This script adds the new columns to existing tables for the adaptive aptitude system.
Run from aceit_backend directory:
    python scripts/migrate_aptitude_tables.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_postgres import engine
from sqlalchemy import text

def migrate_tables():
    """Add new columns to existing tables"""
    print("=" * 60)
    print("DATABASE MIGRATION - Adding New Columns")
    print("=" * 60)
    
    conn = engine.connect()
    trans = conn.begin()
    
    try:
        print("\n[1/2] Migrating aptitude_questions table...")
        
        # Add new columns to aptitude_questions
        migrations = [
            "ALTER TABLE aptitude_questions ADD COLUMN IF NOT EXISTS tags TEXT[] DEFAULT ARRAY[]::TEXT[]",
            "ALTER TABLE aptitude_questions ADD COLUMN IF NOT EXISTS times_attempted INTEGER DEFAULT 0",
            "ALTER TABLE aptitude_questions ADD COLUMN IF NOT EXISTS times_correct INTEGER DEFAULT 0",
            "ALTER TABLE aptitude_questions ADD COLUMN IF NOT EXISTS average_time_seconds FLOAT DEFAULT 0.0",
            "ALTER TABLE aptitude_questions ADD COLUMN IF NOT EXISTS last_used TIMESTAMP"
        ]
        
        for migration in migrations:
            conn.execute(text(migration))
            print(f"  ✓ {migration.split('ADD COLUMN IF NOT EXISTS')[1].split()[0]}")
        
        print("\n[2/2] Migrating user_aptitude_progress table...")
        
        # Add new columns to user_aptitude_progress
        progress_migrations = [
            "ALTER TABLE user_aptitude_progress ADD COLUMN IF NOT EXISTS consecutive_correct INTEGER DEFAULT 0",
            "ALTER TABLE user_aptitude_progress ADD COLUMN IF NOT EXISTS consecutive_incorrect INTEGER DEFAULT 0",
            "ALTER TABLE user_aptitude_progress ADD COLUMN IF NOT EXISTS last_difficulty_change TIMESTAMP",
            "ALTER TABLE user_aptitude_progress ADD COLUMN IF NOT EXISTS total_time_spent_seconds INTEGER DEFAULT 0",
            "ALTER TABLE user_aptitude_progress ADD COLUMN IF NOT EXISTS average_time_per_question FLOAT DEFAULT 0.0",
            "ALTER TABLE user_aptitude_progress ADD COLUMN IF NOT EXISTS recent_accuracy FLOAT DEFAULT 0.0",
            "ALTER TABLE user_aptitude_progress ADD COLUMN IF NOT EXISTS overall_accuracy FLOAT DEFAULT 0.0"
        ]
        
        for migration in progress_migrations:
            conn.execute(text(migration))
            print(f"  ✓ {migration.split('ADD COLUMN IF NOT EXISTS')[1].split()[0]}")
        
        trans.commit()
        print("\n✅ Migration completed successfully!")
        print("\n" + "=" * 60)
        print("All new columns added. Backend is now ready to use.")
        print("=" * 60)
        
    except Exception as e:
        trans.rollback()
        print(f"\n❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        conn.close()
    
    return True

if __name__ == "__main__":
    success = migrate_tables()
    sys.exit(0 if success else 1)
