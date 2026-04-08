import logging
from abc import ABC, abstractmethod

from playwright.async_api import Page

logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """Abstract base class for all job board scrapers.

    Provides common browser interaction helpers and enforces the scraping
    interface via the abstract ``scrape`` method.

    Args:
        page: A Playwright Page instance to use for browser automation.
    """

    def __init__(self, page: Page) -> None:
        self.page = page

    @abstractmethod
    async def scrape(self, params: dict) -> list[dict]:
        """Scrape job listings based on the provided search parameters.

        Args:
            params: Dictionary of search parameters (e.g. keywords, location).

        Returns:
            A list of dictionaries, each representing a job listing.
        """

    async def safe_goto(self, url: str, timeout: float = 30000) -> None:
        """Navigate to a URL with error handling.

        Args:
            url: The URL to navigate to.
            timeout: Maximum navigation time in milliseconds.
        """
        try:
            logger.info("Navigating to %s", url)
            await self.page.goto(url, wait_until="domcontentloaded", timeout=timeout)
        except Exception:
            logger.exception("Failed to navigate to %s", url)
            raise

    async def wait_and_click(self, selector: str, timeout: float = 10000) -> None:
        """Wait for an element to appear and click it.

        Args:
            selector: CSS selector for the target element.
            timeout: Maximum time to wait in milliseconds.
        """
        try:
            await self.page.wait_for_selector(selector, timeout=timeout)
            await self.page.click(selector)
            logger.debug("Clicked element: %s", selector)
        except Exception:
            logger.warning("Failed to wait and click '%s'", selector)
            raise
