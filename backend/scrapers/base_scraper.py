from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Optional
import logging
from playwright.sync_api import sync_playwright
import time

class BaseScraper:
    def __init__(self, venue_name: str, base_url: str):
        self.venue_name = venue_name
        self.base_url = base_url
        self.logger = logging.getLogger(__name__)
        self.playwright = None
        self.browser = None
        self.context = None

    def setup_browser(self):
        """Set up the Playwright browser."""
        if not self.playwright:
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(headless=True)
            self.context = self.browser.new_context()

    def cleanup(self):
        """Clean up browser resources."""
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def fetch_page(self, url: str = None) -> Optional[BeautifulSoup]:
        """Fetch and parse a webpage using Playwright."""
        if url is None:
            url = self.base_url

        try:
            self.setup_browser()
            self.logger.info(f"Fetching {url}")
            
            page = self.context.new_page()
            page.goto(url, wait_until="networkidle")
            
            # Wait for the content to load
            time.sleep(2)
            
            # Get the page content
            content = page.content()
            page.close()
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(content, 'html.parser')
            return soup

        except Exception as e:
            self.logger.error(f"Error fetching {url}: {str(e)}")
            return None

    def parse_date(self, date_str: str) -> datetime:
        """Parse a date string into a datetime object.
        To be implemented by venue-specific scrapers."""
        raise NotImplementedError

    def extract_events(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract events from parsed HTML.
        To be implemented by venue-specific scrapers."""
        raise NotImplementedError

    def get_events(self) -> List[Dict]:
        """Get all events from the venue."""
        try:
            events = []
            soup = self.fetch_page()
            if soup:
                events = self.extract_events(soup)
                self.logger.info(f"Found {len(events)} events")
            return events
        finally:
            self.cleanup() 