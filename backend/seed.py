from database import SessionLocal
from models import Event
from datetime import datetime, timedelta

def seed_database():
    db = SessionLocal()
    
    # Clear existing events
    db.query(Event).delete()
    
    # Create test events
    events = [
        Event(
            title="Live Music Night",
            description="Join us for an evening of live music featuring local artists. Food and drinks available.",
            venue="The Local Venue",
            start_time=datetime.now() + timedelta(days=2, hours=19),
            end_time=datetime.now() + timedelta(days=2, hours=23),
            url="https://example.com/live-music",
            image_url=None
        ),
        Event(
            title="Comedy Show",
            description="A night of laughter with some of the best comedians in town. 18+ event.",
            venue="Laugh Factory",
            start_time=datetime.now() + timedelta(days=3, hours=20),
            end_time=datetime.now() + timedelta(days=3, hours=22),
            url="https://example.com/comedy-show",
            image_url=None
        ),
        Event(
            title="Art Exhibition",
            description="Contemporary art exhibition featuring works from local artists. Free entry.",
            venue="City Art Gallery",
            start_time=datetime.now() + timedelta(days=5, hours=10),
            end_time=datetime.now() + timedelta(days=5, hours=18),
            url="https://example.com/art-exhibition",
            image_url=None
        )
    ]
    
    for event in events:
        db.add(event)
    
    db.commit()
    print(f"Added {len(events)} test events to database")
    db.close()

if __name__ == "__main__":
    seed_database() 