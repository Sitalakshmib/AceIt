from database_postgres import engine, Base
from models.coding_problem_sql import CodingProblem
from models.user_coding_progress import UserCodingProgress

print("Creating tables for coding module...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully.")
