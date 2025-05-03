from bs4 import BeautifulSoup
import requests
from datetime import datetime
from typing import List, Dict, Optional
import logging
from playwright.async_api import async_playwright
import time

class BaseScraper:
    def __init__(self, venue_name: str, base_url: str):
        self.venue_name = venue_name
        self.base_url = base_url
        self.logger = logging.getLogger(__name__)
        self.playwright = None
        self.browser = None
        self.context = None

    async def fetch_page(self, url: str = None) -> Optional[BeautifulSoup]:
        """Fetch and parse a webpage using Playwright."""
        if url is None:
            url = self.base_url
            
        try:
            # Initialize Playwright
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(headless=True)
            self.context = await self.browser.new_context()
            
            page = await self.context.new_page()
            await page.goto(url, wait_until="networkidle")
            await page.wait_for_timeout(2000)
            content = await page.content()
            await page.close()
            
            return BeautifulSoup(content, 'html.parser')
        except Exception as e:
            print(f"Error fetching {url}: {str(e)}")
            return None
        finally:
            await self.cleanup()

    async def cleanup(self):
        """Clean up browser resources."""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

    async def get_events(self) -> List[Dict]:
        """Get all events from the venue."""
        raise NotImplementedError("Subclasses must implement get_events")

    def parse_date(self, date_str: str) -> datetime:
        """Parse a date string into a datetime object."""
        raise NotImplementedError("Subclasses must implement parse_date")

    def extract_events(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract events from parsed HTML.
        To be implemented by venue-specific scrapers."""
        raise NotImplementedError

    def setup_browser(self):
        """Set up the Playwright browser."""
        # This method is no longer used with the new async fetch_page method
        pass 