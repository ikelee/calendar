from database import SessionLocal
from models import Event
from datetime import datetime
from collections import defaultdict

def show_events():
    db = SessionLocal()
    try:
        events = db.query(Event).order_by(Event.start_time).all()
        print("\nEvents in database:")
        print("-" * 80)
        
        # Group events by venue
        venue_events = defaultdict(list)
        for event in events:
            venue_events[event.venue].append(event)
        
        # Print events grouped by venue
        for venue, venue_events_list in venue_events.items():
            print(f"\n{venue} Events ({len(venue_events_list)}):")
            print("-" * 80)
            for event in venue_events_list:
                print(f"Title: {event.title}")
                print(f"Date: {event.start_time.strftime('%Y-%m-%d %H:%M')}")
                print(f"Venue: {event.venue}")
                print(f"Description: {event.description}")
                print(f"URL: {event.url}")
                print("-" * 80)
        
        print(f"\nTotal events: {len(events)}")
        print("\nBreakdown by venue:")
        for venue, events_list in venue_events.items():
            print(f"{venue}: {len(events_list)} events")
            
    finally:
        db.close()

if __name__ == "__main__":
    show_events() 