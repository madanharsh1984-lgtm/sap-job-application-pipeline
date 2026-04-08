import asyncio
import logging

from playwright.async_api import async_playwright, Browser, Page, Playwright

logger = logging.getLogger(__name__)


class BrowserPool:
    """Manages a pool of Playwright browser instances with concurrency control.

    Attributes:
        max_browsers: Maximum number of concurrent browser pages allowed.
        initialized: Whether the pool has been started.
    """

    def __init__(self, max_browsers: int = 3) -> None:
        self.max_browsers = max_browsers
        self.semaphore = asyncio.Semaphore(max_browsers)
        self.initialized = False
        self._playwright: Playwright | None = None
        self._browser: Browser | None = None
        self._available_pages: asyncio.Queue[Page] = asyncio.Queue()

    async def start(self) -> None:
        """Launch Playwright and pre-create browser pages."""
        if self.initialized:
            logger.warning("Browser pool is already initialized")
            return

        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"],
        )

        for i in range(self.max_browsers):
            context = await self._browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/121.0.0.0 Safari/537.36"
                )
            )
            page = await context.new_page()
            await self._available_pages.put(page)
            logger.info("Browser page %d created", i + 1)

        self.initialized = True
        logger.info(
            "Browser pool started with %d pages", self.max_browsers
        )

    async def acquire(self) -> Page:
        """Acquire an available browser page from the pool.

        Blocks until a page is available if all pages are in use.

        Returns:
            A Playwright Page instance ready for use.
        """
        await self.semaphore.acquire()
        page = await self._available_pages.get()
        logger.debug("Browser page acquired")
        return page

    async def release(self, page: Page) -> None:
        """Return a browser page to the pool.

        Args:
            page: The Playwright Page instance to return.
        """
        await self._available_pages.put(page)
        self.semaphore.release()
        logger.debug("Browser page released")

    async def shutdown(self) -> None:
        """Close all browser instances and stop Playwright."""
        if not self.initialized:
            return

        while not self._available_pages.empty():
            page = await self._available_pages.get()
            try:
                await page.context.close()
            except Exception:
                logger.warning("Error closing browser context", exc_info=True)

        if self._browser:
            await self._browser.close()
            self._browser = None

        if self._playwright:
            await self._playwright.stop()
            self._playwright = None

        self.initialized = False
        logger.info("Browser pool shut down")


browser_pool = BrowserPool(max_browsers=3)
