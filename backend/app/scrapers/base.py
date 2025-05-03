from bs4 import BeautifulSoup
import requests
from datetime import datetime
from typing import List, Dict, Optional
import logging

class BaseScraper:
    def __init__(self, venue_name: str, base_url: str):
        self.venue_name = venue_name
        self.base_url = base_url
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
        self.logger.setLevel(logging.DEBUG)  # Set to DEBUG level

    def fetch_page(self) -> Optional[BeautifulSoup]:
        """Fetch and parse the events page."""
        try:
            self.logger.debug(f"Fetching page: {self.base_url}")
            response = requests.get(self.base_url)
            response.raise_for_status()
            self.logger.debug(f"Response status: {response.status_code}")
            soup = BeautifulSoup(response.text, 'html.parser')
            self.logger.debug(f"Page title: {soup.title.string if soup.title else 'No title'}")
            return soup
        except Exception as e:
            self.logger.error(f"Error fetching page: {str(e)}")
            return None

    def get_events(self) -> list:
        """Get all events from the venue. To be implemented by subclasses."""
        raise NotImplementedError

    def parse_date(self, date_str: str) -> datetime:
        """Parse a date string into a datetime object."""
        raise NotImplementedError("Subclasses must implement parse_date")

    def extract_events(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract events from parsed HTML.
        To be implemented by venue-specific scrapers."""
        raise NotImplementedError 