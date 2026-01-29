#!/usr/bin/env python3
"""
AceIt System Health Check Script
Verifies all required components are ready before starting servers
"""

import os
import sys
from dotenv import load_dotenv
import psycopg2
from psycopg2 import OperationalError

# Load environment variables
load_dotenv()

def check_env_variables():
    """Check if required environment variables are set"""
    print("🔍 Checking environment variables...")
    required_vars = ['DATABASE_URL', 'JWT_SECRET', 'GEMINI_API_KEY']
    missing = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing.append(var)
            print(f"  ❌ {var}: NOT SET")
        else:
            # Show partial value for security
            display_value = value[:20] + "..." if len(value) > 20 else value
            print(f"  ✅ {var}: {display_value}")
    
    return len(missing) == 0, missing

def check_database_connection():
    """Test database connectivity with timeout"""
    print("\n🔍 Testing database connection...")
    db_url = os.getenv('DATABASE_URL')
    
    if not db_url:
        print("  ❌ DATABASE_URL not found in environment")
        return False
    
    try:
        # Set a connection timeout of 5 seconds
        conn = psycopg2.connect(db_url, connect_timeout=5)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"  ✅ Database connected successfully")
        print(f"  📊 PostgreSQL version: {version[0][:50]}...")
        cursor.close()
        conn.close()
        return True
    except OperationalError as e:
        print(f"  ❌ Database connection failed: {str(e)[:100]}")
        print("  💡 Possible issues:")
        print("     - Network connectivity problems")
        print("     - Database server is down")
        print("     - Invalid credentials")
        print("     - Firewall blocking connection")
        return False
    except Exception as e:
        print(f"  ❌ Unexpected error: {str(e)[:100]}")
        return False

def check_python_packages():
    """Check if required Python packages are installed"""
    print("\n🔍 Checking Python packages...")
    required_packages = [
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'psycopg2',
        'python-jose',
        'google.generativeai'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package}")
            missing.append(package)
    
    return len(missing) == 0, missing

def check_directories():
    """Check if required directories exist"""
    print("\n🔍 Checking required directories...")
    required_dirs = ['static', 'routes', 'models', 'services']
    missing = []
    
    for dir_name in required_dirs:
        if os.path.isdir(dir_name):
            print(f"  ✅ {dir_name}/")
        else:
            print(f"  ❌ {dir_name}/ (missing)")
            missing.append(dir_name)
    
    return len(missing) == 0, missing

def main():
    print("=" * 60)
    print("  AceIt System Health Check")
    print("=" * 60)
    
    all_checks_passed = True
    
    # Run all checks
    env_ok, missing_env = check_env_variables()
    all_checks_passed = all_checks_passed and env_ok
    
    packages_ok, missing_packages = check_python_packages()
    all_checks_passed = all_checks_passed and packages_ok
    
    dirs_ok, missing_dirs = check_directories()
    all_checks_passed = all_checks_passed and dirs_ok
    
    db_ok = check_database_connection()
    all_checks_passed = all_checks_passed and db_ok
    
    # Summary
    print("\n" + "=" * 60)
    if all_checks_passed:
        print("  ✅ ALL CHECKS PASSED - System is ready!")
        print("=" * 60)
        return 0
    else:
        print("  ❌ SOME CHECKS FAILED - Please fix the issues above")
        print("=" * 60)
        
        if missing_env:
            print(f"\n💡 Missing environment variables: {', '.join(missing_env)}")
            print("   Add them to .env file")
        
        if missing_packages:
            print(f"\n💡 Missing Python packages: {', '.join(missing_packages)}")
            print("   Run: pip install -r requirements.txt")
        
        if missing_dirs:
            print(f"\n💡 Missing directories: {', '.join(missing_dirs)}")
        
        return 1

if __name__ == "__main__":
    sys.exit(main())
