from database_postgres import SessionLocal
from models.aptitude_sql import AptitudeQuestion
from sqlalchemy import func

def audit_difficulties():
    db = SessionLocal()
    try:
        # Get count of Easy, Medium, Hard for every (Category, Topic)
        results = db.query(
            AptitudeQuestion.category,
            AptitudeQuestion.topic,
            AptitudeQuestion.difficulty,
            func.count(AptitudeQuestion.id)
        ).group_by(
            AptitudeQuestion.category,
            AptitudeQuestion.topic,
            AptitudeQuestion.difficulty
        ).all()

        # Organize data
        stats = {}
        for cat, topic, diff, count in results:
            if not topic: continue
            key = (cat, topic)
            if key not in stats:
                stats[key] = {"Easy": 0, "Medium": 0, "Hard": 0, "Total": 0}
            
            d_norm = diff.title() if diff else "Medium" # Default to Medium if null
            if d_norm not in ["Easy", "Medium", "Hard"]: d_norm = "Medium"
            
            stats[key][d_norm] += count
            stats[key]["Total"] += count

        # Check for violations
        print(f"{'CATEGORY':<25} | {'TOPIC':<30} | {'EASY':<5} | {'MED':<5} | {'HARD':<5} | {'STATUS'}")
        print("-" * 110)
        
        missing_easy = []
        
        for (cat, topic), counts in sorted(stats.items()):
            status = "OK"
            if counts["Easy"] == 0:
                status = "MISSING EASY"
                missing_easy.append((cat, topic, counts["Total"]))
            elif counts["Medium"] == 0: 
                status = "MISSING MED"
            elif counts["Hard"] == 0:
                status = "MISSING HARD"
                
            print(f"{cat:<25} | {topic:<30} | {counts['Easy']:<5} | {counts['Medium']:<5} | {counts['Hard']:<5} | {status}")

        print("\n" + "="*50)
        if missing_easy:
            print(f"CRITICAL: Found {len(missing_easy)} topics with NO EASY questions.")
            print("These topics will FAIL to start Practice Mode correctly.")
        else:
            print("SUCCESS: All topics have at least one Easy question.")
            
    finally:
        db.close()

if __name__ == "__main__":
    audit_difficulties()
