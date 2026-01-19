"""
Initialize Adaptive Aptitude System

This script creates all database tables for the adaptive learning aptitude module.
Run this from the aceit_backend directory:
    python scripts/initialize_aptitude_system.py

Tables created:
- aptitude_questions (enhanced with metadata)
- user_aptitude_progress (enhanced with adaptive tracking)
- mock_tests
- mock_test_attempts
- mock_test_responses
- question_attempts
- user_analytics
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_postgres import engine, Base, SessionLocal
from models.aptitude_sql import AptitudeQuestion, UserAptitudeProgress
from models.mock_test_sql import MockTest, MockTestAttempt, MockTestResponse
from models.analytics_sql import QuestionAttempt, UserAnalytics
from models.user_sql import User

def create_tables():
    """Create all tables in the database"""
    print("=" * 60)
    print("ADAPTIVE APTITUDE SYSTEM - DATABASE INITIALIZATION")
    print("=" * 60)
    
    print("\n[1/3] Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ All tables created successfully!")
        
        # List created tables
        print("\n📊 Tables created:")
        tables = [
            "users",
            "aptitude_questions",
            "user_aptitude_progress",
            "mock_tests",
            "mock_test_attempts",
            "mock_test_responses",
            "question_attempts",
            "user_analytics"
        ]
        for table in tables:
            print(f"   ✓ {table}")
            
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False
    
    print("\n[2/3] Verifying table structure...")
    db = SessionLocal()
    try:
        # Test queries to verify tables exist
        db.query(AptitudeQuestion).count()
        db.query(UserAptitudeProgress).count()
        db.query(MockTest).count()
        db.query(MockTestAttempt).count()
        db.query(MockTestResponse).count()
        db.query(QuestionAttempt).count()
        db.query(UserAnalytics).count()
        print("✅ All tables verified and accessible!")
    except Exception as e:
        print(f"❌ Error verifying tables: {e}")
        return False
    finally:
        db.close()
    
    print("\n[3/3] Database initialization complete!")
    print("\n" + "=" * 60)
    print("NEXT STEPS:")
    print("=" * 60)
    print("1. Run question seeding script:")
    print("   python scripts/seed_comprehensive_questions.py")
    print("\n2. Start the backend server:")
    print("   npm run dev:full")
    print("\n3. Test the API endpoints:")
    print("   - GET  /aptitude/categories")
    print("   - POST /aptitude/practice/next-question")
    print("   - POST /mock-tests/generate")
    print("   - GET  /analytics/dashboard/{user_id}")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = create_tables()
    sys.exit(0 if success else 1)
