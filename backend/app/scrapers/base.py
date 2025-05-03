from bs4 import BeautifulSoup
import requests
from datetime import datetime
from typing import List, Dict, Optional
import logging

class BaseScraper:
    def __init__(self, venue_name: str, base_url: str):
        self.venue_name = venue_name
        self.base_url = base_url
        self.logger = logging.getLogger(__name__)

    def fetch_page(self, url: str = None) -> Optional[BeautifulSoup]:
        """Fetch and parse a webpage using requests."""
        if url is None:
            url = self.base_url
            
        try:
            response = requests.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            self.logger.error(f"Error fetching {url}: {str(e)}")
            return None

    def get_events(self) -> List[Dict]:
        """Get all events from the venue."""
        raise NotImplementedError("Subclasses must implement get_events")

    def parse_date(self, date_str: str) -> datetime:
        """Parse a date string into a datetime object."""
        raise NotImplementedError("Subclasses must implement parse_date")

    def extract_events(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract events from parsed HTML.
        To be implemented by venue-specific scrapers."""
        raise NotImplementedError 