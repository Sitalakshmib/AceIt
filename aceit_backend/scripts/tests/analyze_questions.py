"""
Script to provide detailed breakdown of aptitude questions by category, topic, and difficulty.
"""

import os
import sys
import pandas as pd
from tabulate import tabulate

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("❌ DATABASE_URL not found in .env")
    sys.exit(1)

print("🔗 Connecting to Neon PostgreSQL database...")
engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    print("\n📊 Question Distribution Analysis")
    print("=" * 60)
    
    # 1. By Category
    print("\n🔹 BY CATEGORY:")
    print("-" * 30)
    cat_query = text("""
        SELECT category, COUNT(*) as count 
        FROM aptitude_questions 
        GROUP BY category 
        ORDER BY count DESC
    """)
    result = conn.execute(cat_query)
    rows = result.fetchall()
    print(tabulate(rows, headers=["Category", "Count"], tablefmt="grid"))
    
    # 2. By Difficulty
    print("\n🔹 BY DIFFICULTY:")
    print("-" * 30)
    diff_query = text("""
        SELECT difficulty, COUNT(*) as count 
        FROM aptitude_questions 
        GROUP BY difficulty 
        ORDER BY count DESC
    """)
    result = conn.execute(diff_query)
    rows = result.fetchall()
    print(tabulate(rows, headers=["Difficulty", "Count"], tablefmt="grid"))
    
    # 3. By Category, Topic and Difficulty
    print("\n🔹 DETAILED BREAKDOWN (Category > Topic > Difficulty):")
    print("-" * 80)
    
    detailed_query = text("""
        SELECT 
            category, 
            topic, 
            difficulty,
            COUNT(*) as count
        FROM aptitude_questions 
        GROUP BY category, topic, difficulty
        ORDER BY category, topic, difficulty
    """)
    
    result = conn.execute(detailed_query)
    rows = result.fetchall()
    
    # Process for display
    # Group by Category > Topic
    data = {}
    for r in rows:
        cat = r[0]
        topic = r[1]
        diff = r[2]
        count = r[3]
        
        key = (cat, topic)
        if key not in data:
            data[key] = {"easy": 0, "medium": 0, "hard": 0, "total": 0}
            
        if diff in data[key]:
            data[key][diff] = count
        data[key]["total"] += count
        
    display_rows = []
    for (cat, topic), stats in sorted(data.items()):
        display_rows.append([
            cat, 
            topic, 
            stats["easy"], 
            stats["medium"], 
            stats["hard"], 
            stats["total"]
        ])
        
    print(tabulate(display_rows, headers=["Category", "Topic", "Easy", "Medium", "Hard", "Total"], tablefmt="grid"))
    
    # Summary
    print(f"\n✅ Total Topics: {len(data)}")
