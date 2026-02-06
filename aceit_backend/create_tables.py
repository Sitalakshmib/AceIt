from database_postgres import engine, Base
from models.user_sql import User

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")
