from aceit_backend.database_postgres import engine
from aceit_backend.models.interview_question import InterviewQuestion

InterviewQuestion.metadata.create_all(bind=engine)
print("✅ Tables created")
