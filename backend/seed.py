from database import SessionLocal
from models import Event
from datetime import datetime, timedelta

def seed_database():
    db = SessionLocal()
    
    # Check if we already have events
    if db.query(Event).count() == 0:
        # Create a test event
        test_event = Event(
            title="Test Event",
            description="This is a test event to demonstrate the application.",
            venue="Test Venue",
            start_time=datetime.now() + timedelta(days=1),
            end_time=datetime.now() + timedelta(days=1, hours=2),
            url="https://example.com/test-event",
            image_url=None
        )
        
        db.add(test_event)
        db.commit()
        print("Added test event to database")
    else:
        print("Database already has events")
    
    db.close()

if __name__ == "__main__":
    seed_database() 