from datetime import datetime
from typing import List, Dict
from .base_scraper import BaseScraper

class WarfieldScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            venue_name="The Warfield",
            base_url="https://www.thewarfieldtheatre.com/events"
        )

    def get_events(self) -> List[Dict]:
        """Get all events from The Warfield."""
        soup = self.fetch_page()
        if not soup:
            return []
            
        return self.extract_events(soup)

    def parse_date(self, date_str: str) -> datetime:
        """Parse Warfield date string into datetime object.
        Format example: 'Sat, May 3, 2025'"""
        try:
            # Clean up the date string by removing extra whitespace
            date_str = ' '.join(date_str.split())
            return datetime.strptime(date_str, '%a, %b %d, %Y')
        except ValueError:
            self.logger.error(f"Error parsing date: {date_str}")
            return None

    def extract_events(self, soup) -> List[Dict]:
        """Extract events from The Warfield's events page."""
        events = []
        
        # Find all event elements
        event_elements = soup.select('div.entry.warfield')
        
        if not event_elements:
            self.logger.error("No event elements found")
            return events
        
        for element in event_elements:
            try:
                # Extract event ID from the detail link
                detail_link = element.select_one('a[href*="/events/detail/"]')
                if not detail_link:
                    continue
                    
                event_id = detail_link['href'].split('/')[-1]
                
                # Extract title
                title = element.select_one('h3.carousel_item_title_small a')
                if not title:
                    continue
                title = title.text.strip()
                
                # Extract date and time
                date_time = element.select_one('h5')
                if not date_time:
                    continue
                    
                date_str = date_time.text.strip()
                event_date = self.parse_date(date_str)
                if not event_date:
                    continue
                
                # Extract ticket link
                ticket_link = element.select_one('a[href*="axs.com"]')
                ticket_url = ticket_link['href'] if ticket_link else None
                
                events.append({
                    'event_id': event_id,
                    'title': title,
                    'date': event_date,
                    'ticket_url': ticket_url,
                    'venue': self.venue_name
                })
                
            except Exception as e:
                self.logger.error(f"Error extracting event: {str(e)}")
                continue
                
        return events