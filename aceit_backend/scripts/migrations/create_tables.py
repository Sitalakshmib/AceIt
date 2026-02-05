from database_postgres import engine, Base
from models.interview_question import InterviewQuestion
from models.user_sql import User

# Create all tables
Base.metadata.create_all(bind=engine)
print("✅ All tables created successfully")
