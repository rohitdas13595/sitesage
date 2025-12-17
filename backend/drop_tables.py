import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

from app.database import engine, Base
from app.models import User, SEOReport

def reset_database():
    print("Dropping all tables...")
    try:
        # Drop alembic_version table explicitly
        from sqlalchemy import text
        with engine.connect() as connection:
            connection.execute(text("DROP TABLE IF EXISTS alembic_version"))
            connection.commit()
            print("Dropped alembic_version table.")

        Base.metadata.drop_all(bind=engine)
        print("All tables dropped successfully.")
    except Exception as e:
        print(f"Error dropping tables: {e}")

if __name__ == "__main__":
    reset_database()
