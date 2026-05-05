
import sys
import os
sys.path.append(os.getcwd())

from database_postgres import init_db, engine, Base
import traceback

try:
    print("Starting manual database initialization...")
    init_db()
    print("Database initialization successful!")
except Exception as e:
    print("Database initialization FAILED:")
    traceback.print_exc()
finally:
    engine.dispose()
