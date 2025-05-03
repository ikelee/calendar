from database import engine, Base
from models import Event
import os
from dotenv import load_dotenv

def init_db():
    # Check if we're in production (Render sets RENDER=true)
    is_production = os.getenv('RENDER', 'false').lower() == 'true'
    
    if is_production:
        print("Running in production environment")
        # In production, we want to create tables if they don't exist
        Base.metadata.create_all(bind=engine)
        print("Database tables created/verified successfully.")
    else:
        print("Running in local environment")
        # In local, we can be more aggressive about table creation
        Base.metadata.drop_all(bind=engine)  # Drop existing tables
        Base.metadata.create_all(bind=engine)  # Create fresh tables
        print("Local database tables recreated successfully.")

if __name__ == "__main__":
    init_db() 