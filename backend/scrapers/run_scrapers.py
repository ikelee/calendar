import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal
from models import Event
from scrapers.warfield_scraper import WarfieldScraper
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def save_events(events, db):
    """Save events to the database, avoiding duplicates."""
    for event_data in events:
        # Check if event already exists (based on title and start time)
        existing = db.query(Event).filter(
            Event.title == event_data['title'],
            Event.start_time == event_data['start_time']
        ).first()
        
        if not existing:
            event = Event(**event_data)
            db.add(event)
            logger.info(f"Added new event: {event.title} on {event.start_time}")
    
    db.commit()

def run_scrapers():
    """Run all venue scrapers and save results to database."""
    db = SessionLocal()
    try:
        # Initialize and run the Warfield scraper
        warfield = WarfieldScraper()
        logger.info("Starting Warfield scraper...")
        events = warfield.get_events()
        logger.info(f"Found {len(events)} events at The Warfield")
        
        # Save events to database
        save_events(events, db)
        
    except Exception as e:
        logger.error(f"Error running scrapers: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    run_scrapers() 