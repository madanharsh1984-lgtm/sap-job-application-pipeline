import logging
from urllib.parse import quote_plus

from scrapers.base import BaseScraper

logger = logging.getLogger(__name__)


class IndeedScraper(BaseScraper):
    """Scraper for Indeed job listings.

    Navigates Indeed's job search pages and extracts job data.
    This is a skeleton implementation — selectors may need updating as
    Indeed's markup changes.
    """

    BASE_URL = "https://www.indeed.com/jobs"

    async def scrape(self, params: dict) -> list[dict]:
        """Scrape Indeed job listings matching the given parameters.

        Args:
            params: Dictionary with 'keywords' and optional 'location'.

        Returns:
            List of job dictionaries with title, company, location, and url.
        """
        keywords = params.get("keywords", "")
        location = params.get("location", "")

        search_url = (
            f"{self.BASE_URL}"
            f"?q={quote_plus(keywords)}"
            f"&l={quote_plus(location)}"
        )

        logger.info("Indeed scrape: url=%s", search_url)

        jobs: list[dict] = []

        try:
            await self.safe_goto(search_url)

            await self.page.wait_for_selector(
                ".jobsearch-ResultsList", timeout=15000
            )

            job_cards = await self.page.query_selector_all(
                ".jobsearch-ResultsList .result"
            )

            for card in job_cards:
                try:
                    title_el = await card.query_selector("h2 a")
                    company_el = await card.query_selector(
                        "[data-testid='company-name']"
                    )
                    location_el = await card.query_selector(
                        "[data-testid='text-location']"
                    )

                    title = (
                        (await title_el.inner_text()).strip()
                        if title_el
                        else ""
                    )
                    company = (
                        (await company_el.inner_text()).strip()
                        if company_el
                        else ""
                    )
                    loc = (
                        (await location_el.inner_text()).strip()
                        if location_el
                        else ""
                    )
                    url = ""
                    if title_el:
                        href = await title_el.get_attribute("href")
                        if href:
                            url = (
                                f"https://www.indeed.com{href}"
                                if href.startswith("/")
                                else href
                            )

                    if title:
                        jobs.append(
                            {
                                "title": title,
                                "company": company,
                                "location": loc,
                                "url": url,
                                "source": "indeed",
                            }
                        )
                except Exception:
                    logger.warning(
                        "Failed to parse an Indeed job card", exc_info=True
                    )
                    continue

            logger.info("Indeed scrape complete: %d jobs extracted", len(jobs))

        except Exception:
            logger.exception("Indeed scrape failed for params=%s", params)

        return jobs
