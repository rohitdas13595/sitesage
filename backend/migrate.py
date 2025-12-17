from sqlalchemy import create_all, text
from app.database import engine

def migrate():
    with engine.connect() as conn:
        print("Adding accessibility column to seo_reports table...")
        try:
            conn.execute(text("ALTER TABLE seo_reports ADD COLUMN accessibility JSON;"))
            conn.commit()
            print("Successfully added accessibility column.")
        except Exception as e:
            print(f"Error adding column: {e}")
            conn.rollback()

if __name__ == "__main__":
    migrate()
