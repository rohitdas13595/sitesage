import os
from sqlalchemy import create_engine, text
from app.config import get_settings

def fix_db():
    settings = get_settings()
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.connect() as conn:
        print("Checking for 'accessibility' column in 'seo_reports' table...")
        try:
            # Check if column exists
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='seo_reports' AND column_name='accessibility';
            """))
            column_exists = result.fetchone() is not None
            
            if not column_exists:
                print("Column 'accessibility' missing. Adding it...")
                conn.execute(text("ALTER TABLE seo_reports ADD COLUMN accessibility JSON;"))
                conn.commit()
                print("Column 'accessibility' added successfully.")
            else:
                print("Column 'accessibility' already exists.")
                
        except Exception as e:
            print(f"Error: {e}")
            conn.rollback()

if __name__ == "__main__":
    fix_db()
