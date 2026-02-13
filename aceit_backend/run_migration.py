"""
Database migration script to add learning features to Neon DB
"""
import os
import sys
from dotenv import load_dotenv
import psycopg2

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("❌ DATABASE_URL not found in environment variables")
    sys.exit(1)

print("🔄 Connecting to Neon database...")

try:
    # Connect to database
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    print("✅ Connected successfully")
    print("\n📦 Running migrations...\n")
    
    # Read and execute migration SQL
    with open('migrations/add_learning_features.sql', 'r') as f:
        migration_sql = f.read()
    
    # Execute migration
    cursor.execute(migration_sql)
    conn.commit()
    
    print("✅ Migration completed successfully!")
    print("\n📊 Verifying tables...")
    
    # Verify bookmarked_problems table
    cursor.execute("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'bookmarked_problems'
        ORDER BY ordinal_position;
    """)
    
    bookmark_columns = cursor.fetchall()
    if bookmark_columns:
        print("\n✅ bookmarked_problems table:")
        for col in bookmark_columns:
            print(f"  - {col[0]}: {col[1]}")
    
    # Verify new columns in coding_problems
    cursor.execute("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'coding_problems'
        AND column_name IN ('solution_code', 'solution_explanation', 'approach_summary', 
                            'time_complexity', 'space_complexity', 'test_case_descriptions')
        ORDER BY column_name;
    """)
    
    new_columns = cursor.fetchall()
    if new_columns:
        print("\n✅ New columns in coding_problems table:")
        for col in new_columns:
            print(f"  - {col[0]}: {col[1]}")
    
    # Close connection
    cursor.close()
    conn.close()
    
    print("\n✅ Database migration complete!")

except Exception as e:
    print(f"❌ Error: {e}")
    if 'conn' in locals():
        conn.rollback()
    sys.exit(1)
