from database_postgres import engine, Base
from models.interview_models import InterviewSession, InterviewHistory
from models.interview_question import InterviewQuestion

print("Creating tables for interview module...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully.")
