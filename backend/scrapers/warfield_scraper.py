from .base_scraper import BaseScraper
from bs4 import BeautifulSoup
from datetime import datetime
import re
import time

class WarfieldScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            venue_name="Warfield",
            base_url="https://www.thewarfieldtheatre.com/events"
        )

    def parse_date(self, date_str: str) -> datetime:
        """Parse Warfield's date format."""
        try:
            # Remove any extra whitespace and normalize the string
            date_str = ' '.join(date_str.split())
            # Extract the date part
            match = re.search(r'([A-Za-z]+, [A-Za-z]+ \d+, \d{4})', date_str)
            if match:
                date_str = match.group(1)
                # The website uses abbreviated month names
                return datetime.strptime(date_str, '%a, %b %d, %Y')
        except Exception as e:
            self.logger.error(f"Error parsing date {date_str}: {str(e)}")
        return None

    def extract_events(self, soup: BeautifulSoup) -> list:
        """Extract events from the Warfield's webpage."""
        events = []
        try:
            # Find all event containers
            event_containers = soup.find_all('div', class_='entry')
            self.logger.info(f"Found {len(event_containers)} event containers")

            for container in event_containers:
                try:
                    # Extract title
                    title_elem = container.find('h3', class_='carousel_item_title_small')
                    if not title_elem or not title_elem.find('a'):
                        continue
                    title = title_elem.find('a').text.strip()

                    # Extract date and time
                    date_elem = container.find('span', class_='date')
                    time_elem = container.find('span', class_='time')
                    if not date_elem or not time_elem:
                        continue

                    date_text = date_elem.text.strip()
                    time_text = time_elem.text.strip()
                    
                    # Parse date
                    event_date = self.parse_date(date_text)
                    if not event_date:
                        continue

                    # Extract time
                    time_match = re.search(r'(\d{1,2}:\d{2} [AP]M)', time_text)
                    if time_match:
                        time_str = time_match.group(1)
                        time_obj = datetime.strptime(time_str, '%I:%M %p')
                        event_date = event_date.replace(
                            hour=time_obj.hour,
                            minute=time_obj.minute
                        )

                    # Extract URL
                    url = None
                    ticket_link = container.find('a', class_='btn-tickets')
                    if ticket_link:
                        url = ticket_link.get('href')

                    # Extract description (tour name, supporting acts)
                    description_parts = []
                    tour_name = container.find('h5', class_=None)
                    if tour_name and tour_name.text.strip():
                        description_parts.append(tour_name.text.strip())
                    
                    supporting_acts = container.find('h4', class_='animated')
                    if supporting_acts and supporting_acts.text.strip():
                        description_parts.append(f"Supporting: {supporting_acts.text.strip()}")

                    description = " | ".join(description_parts)

                    # Create event dictionary
                    event = {
                        'title': title,
                        'description': description,
                        'venue': self.venue_name,
                        'start_time': event_date,
                        'end_time': event_date.replace(hour=23, minute=59),  # Set end time to end of day
                        'url': url
                    }
                    events.append(event)

                except Exception as e:
                    self.logger.error(f"Error parsing event container: {str(e)}")
                    continue

        except Exception as e:
            self.logger.error(f"Error extracting events: {str(e)}")

        return events

    def get_events(self) -> list:
        """Get all events from the venue, handling pagination."""
        all_events = []
        page = 1
        max_pages = 5  # Limit to prevent infinite loops
        
        while page <= max_pages:
            url = f"{self.base_url}?page={page}" if page > 1 else self.base_url
            self.logger.info(f"Fetching page {page}")
            
            soup = self.fetch_page(url)
            if not soup:
                break
                
            events = self.extract_events(soup)
            if not events:
                break
                
            all_events.extend(events)
            self.logger.info(f"Found {len(events)} events on page {page}")
            
            # Check if there's a next page
            next_page = soup.find('a', class_='next_page')
            if not next_page or 'disabled' in next_page.get('class', []):
                break
                
            page += 1
            time.sleep(1)  # Be nice to the server
            
        self.logger.info(f"Total events found: {len(all_events)}")
        return all_events 