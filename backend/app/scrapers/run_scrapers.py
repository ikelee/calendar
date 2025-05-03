from typing import List
from .warfield import WarfieldScraper
from ..database import SessionLocal
from ..models.event import Event

def run_scrapers() -> List[dict]:
    """Run all scrapers and save events to database."""
    events = []
    db = SessionLocal()
    
    try:
        # Initialize scrapers
        warfield_scraper = WarfieldScraper()
        
        # Get events from each scraper
        warfield_events = warfield_scraper.get_events()
        events.extend(warfield_events)
        
        # Save events to database
        for event_data in events:
            # Check if event already exists
            existing_event = db.query(Event).filter_by(
                event_id=event_data['event_id'],
                venue=event_data['venue']
            ).first()
            
            if not existing_event:
                # Create new event
                new_event = Event(
                    event_id=event_data['event_id'],
                    title=event_data['title'],
                    date=event_data['date'],
                    ticket_url=event_data['ticket_url'],
                    venue=event_data['venue']
                )
                db.add(new_event)
        
        db.commit()
        
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
        
    return events 