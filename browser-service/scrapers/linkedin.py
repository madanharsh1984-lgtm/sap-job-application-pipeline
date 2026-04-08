import logging
from urllib.parse import quote_plus

from scrapers.base import BaseScraper

logger = logging.getLogger(__name__)


class LinkedInScraper(BaseScraper):
    """Scraper for LinkedIn job listings.

    Navigates LinkedIn's public job search pages and extracts job data.
    This is a skeleton implementation — selectors may need updating as
    LinkedIn's markup changes.
    """

    BASE_URL = "https://www.linkedin.com/jobs/search"

    async def scrape(self, params: dict) -> list[dict]:
        """Scrape LinkedIn job listings matching the given parameters.

        Args:
            params: Dictionary with 'keywords' and optional 'location'.

        Returns:
            List of job dictionaries with title, company, location, and url.
        """
        keywords = params.get("keywords", "")
        location = params.get("location", "")

        search_url = (
            f"{self.BASE_URL}"
            f"?keywords={quote_plus(keywords)}"
            f"&location={quote_plus(location)}"
        )

        logger.info("LinkedIn scrape: url=%s", search_url)

        jobs: list[dict] = []

        try:
            await self.safe_goto(search_url)

            await self.page.wait_for_selector(
                ".jobs-search__results-list", timeout=15000
            )

            job_cards = await self.page.query_selector_all(
                ".jobs-search__results-list li"
            )

            for card in job_cards:
                try:
                    title_el = await card.query_selector("h3")
                    company_el = await card.query_selector("h4")
                    location_el = await card.query_selector(
                        ".job-search-card__location"
                    )
                    link_el = await card.query_selector("a")

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
                    url = (
                        await link_el.get_attribute("href")
                        if link_el
                        else ""
                    )

                    if title:
                        jobs.append(
                            {
                                "title": title,
                                "company": company,
                                "location": loc,
                                "url": url or "",
                                "source": "linkedin",
                            }
                        )
                except Exception:
                    logger.warning(
                        "Failed to parse a LinkedIn job card", exc_info=True
                    )
                    continue

            logger.info("LinkedIn scrape complete: %d jobs extracted", len(jobs))

        except Exception:
            logger.exception("LinkedIn scrape failed for params=%s", params)

        return jobs
