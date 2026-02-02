from sqlalchemy import text
from aceit_backend.database_postgres import engine

def migrate():
    with engine.connect() as conn:
        print("Adding column 'answer_text' to 'mock_test_responses'...")
        try:
            conn.execute(text("ALTER TABLE mock_test_responses ADD COLUMN answer_text VARCHAR;"))
            conn.commit()
            print("Successfully added column.")
        except Exception as e:
            if "already exists" in str(e):
                print("Column 'answer_text' already exists.")
            else:
                print(f"Error adding column: {e}")

if __name__ == "__main__":
    migrate()
