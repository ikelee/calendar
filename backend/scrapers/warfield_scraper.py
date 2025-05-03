from .base_scraper import BaseScraper
from bs4 import BeautifulSoup
from datetime import datetime
import re
from typing import List, Dict

class WarfieldScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            venue_name="The Warfield",
            base_url="https://www.thewarfieldtheatre.com/events"
        )

    def parse_date(self, date_str: str) -> datetime:
        """Parse Warfield's date format."""
        try:
            # Remove any extra whitespace and normalize the string
            date_str = ' '.join(date_str.split())
            # Try to extract the date part
            match = re.search(r'([A-Za-z]+, [A-Za-z]+ \d+, \d{4})', date_str)
            if match:
                date_str = match.group(1)
            
            # Map of abbreviated month names to full month names
            month_map = {
                'Jan': 'January',
                'Feb': 'February',
                'Mar': 'March',
                'Apr': 'April',
                'May': 'May',
                'Jun': 'June',
                'Jul': 'July',
                'Aug': 'August',
                'Sep': 'September',
                'Oct': 'October',
                'Nov': 'November',
                'Dec': 'December'
            }
            
            # Replace abbreviated month names with full names
            for abbr, full in month_map.items():
                date_str = date_str.replace(f', {abbr} ', f', {full} ')
            
            # Try parsing with the new format first (e.g., "Sat, May 3, 2025")
            try:
                return datetime.strptime(date_str, "%a, %B %d, %Y")
            except ValueError:
                # Fall back to the old format (e.g., "Saturday, May 3, 2025")
                return datetime.strptime(date_str, "%A, %B %d, %Y")
        except Exception as e:
            print(f"Error parsing date {date_str}: {str(e)}")
            return None

    async def get_events(self) -> List[Dict]:
        """Get all events from The Warfield."""
        try:
            events = []
            soup = await self.fetch_page()
            if soup:
                events = self.extract_events(soup)
                print(f"Found {len(events)} events")
            return events
        except Exception as e:
            print(f"Error getting events: {str(e)}")
            return []

    def extract_events(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract events from the BeautifulSoup object."""
        events = []
        
        # Try different possible selectors for event containers
        selectors = [
            'div.event-item',
            'div.event',
            'div.event-container',
            'div.entry',
            'div.carousel_item'
        ]
        
        for selector in selectors:
            event_elements = soup.select(selector)
            if event_elements:
                break
        
        for element in event_elements:
            try:
                # Try different possible selectors for title
                title_elem = (
                    element.find('h3') or
                    element.find('h2') or
                    element.find('div', class_='event-title') or
                    element.find('div', class_='carousel_item_title_small')
                )
                if not title_elem:
                    continue
                    
                title = title_elem.text.strip()
                
                # Try different possible selectors for date
                date_elem = (
                    element.find('div', class_='date') or
                    element.find('div', class_='event-date') or
                    element.find('span', class_='date') or
                    element.find('span', class_='carousel_item_date')
                )
                if not date_elem:
                    continue
                    
                date_str = date_elem.text.strip()
                start_time = self.parse_date(date_str)
                if not start_time:
                    continue
                
                # Set end time to same day at 11:59 PM
                end_time = start_time.replace(hour=23, minute=59)
                
                # Try different possible selectors for URL
                url_elem = element.find('a')
                if not url_elem or 'href' not in url_elem.attrs:
                    continue
                    
                url = url_elem['href']
                if not url.startswith('http'):
                    url = f"https://www.thewarfieldtheatre.com{url}"
                
                # Try different possible selectors for description
                desc_elem = (
                    element.find('div', class_='description') or
                    element.find('div', class_='event-description') or
                    element.find('p') or
                    element.find('div', class_='carousel_item_description')
                )
                description = desc_elem.text.strip() if desc_elem else ""
                
                # Try different possible selectors for image
                img = (
                    element.find('img') or
                    element.find('div', class_='event-image') or
                    element.find('div', class_='carousel_item_image')
                )
                image_url = None
                if img and 'src' in img.attrs:
                    image_url = img['src']
                    if not image_url.startswith('http'):
                        image_url = f"https://www.thewarfieldtheatre.com{image_url}"
                
                event = {
                    'title': title,
                    'description': description,
                    'venue': self.venue_name,
                    'start_time': start_time,
                    'end_time': end_time,
                    'url': url,
                    'image_url': image_url
                }
                events.append(event)
            except Exception:
                continue
                
        return events 