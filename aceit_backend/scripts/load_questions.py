import json

from database_postgres import SessionLocal
from models.interview_question import InterviewQuestion

FILES = [
    "data/java_questions.json",
    "data/python_questions.json",
    "data/dsa_questions.json",
    "data/dbms_questions.json",
]

def main():
    db = SessionLocal()

    for file_path in FILES:
        print(f"📥 Loading {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            questions = json.load(f)

        print(f"   ➜ {len(questions)} questions found")

        for q in questions:
            db.add(
                InterviewQuestion(
                    question_text=q["question_text"],
                    domain=q["domain"],
                    language=q.get("language"),
                    topic=q["topic"],
                    subtopic=q.get("subtopic"),
                    difficulty=q["difficulty"],
                )
            )

    db.commit()
    db.close()
    print("✅ Interview questions loaded successfully")

if __name__ == "__main__":
    main()
