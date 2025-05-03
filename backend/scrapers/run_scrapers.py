import sys
import os
import asyncio
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal
from models import Event
from scrapers.warfield_scraper import WarfieldScraper
from typing import List, Dict

async def run_scrapers() -> List[Dict]:
    """Run all scrapers and save events to database."""
    db = SessionLocal()
    try:
        # Initialize scrapers
        scrapers = [
            WarfieldScraper()
        ]
        
        all_events = []
        for scraper in scrapers:
            try:
                print(f"Running {scraper.venue_name} scraper")
                events = await scraper.get_events()
                print(f"Retrieved {len(events)} events from {scraper.venue_name}")
                
                for event_data in events:
                    # Check if event already exists
                    existing_event = db.query(Event).filter(
                        Event.title == event_data['title'],
                        Event.start_time == event_data['start_time'],
                        Event.venue == event_data['venue']
                    ).first()
                    
                    if not existing_event:
                        # Create new event
                        event = Event(**event_data)
                        db.add(event)
                        print(f"Added new event: {event.title} on {event.start_time}")
                    else:
                        print(f"Event already exists: {event_data['title']} on {event_data['start_time']}")
                
                db.commit()
                print(f"Successfully committed changes for {scraper.venue_name}")
                all_events.extend(events)
                
            except Exception as e:
                print(f"Error running {scraper.venue_name} scraper: {str(e)}")
                db.rollback()
                continue
                
        return all_events
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(run_scrapers()) 