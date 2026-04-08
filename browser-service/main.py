import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from browser_pool import browser_pool

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage browser pool lifecycle."""
    await browser_pool.start()
    logger.info("Browser pool started")
    yield
    await browser_pool.shutdown()
    logger.info("Browser pool shut down")


app = FastAPI(
    title="JobAccelerator Browser Service",
    version="1.0.0",
    lifespan=lifespan,
)


class ScrapeRequest(BaseModel):
    """Parameters for a job scraping request."""

    keywords: str
    location: str = ""
    source: str = "linkedin"


class ApplyRequest(BaseModel):
    """Parameters for a job application request."""

    job_url: str
    resume_text: str
    cover_letter: str = ""
    user_id: int


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "healthy", "service": "browser-service"}


@app.post("/api/scrape")
async def scrape_jobs(request: ScrapeRequest) -> dict:
    """Trigger job scraping using a browser instance.

    Args:
        request: Scraping parameters including keywords, location, and source.

    Returns:
        Dictionary containing the list of scraped jobs.
    """
    logger.info(
        "Scrape request: keywords='%s', location='%s', source='%s'",
        request.keywords,
        request.location,
        request.source,
    )

    page = None
    try:
        page = await browser_pool.acquire()

        from scrapers.linkedin import LinkedInScraper
        from scrapers.indeed import IndeedScraper

        scraper_map = {
            "linkedin": LinkedInScraper,
            "indeed": IndeedScraper,
        }

        scraper_cls = scraper_map.get(request.source)
        if scraper_cls is None:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported source: {request.source}",
            )

        scraper = scraper_cls(page)
        jobs = await scraper.scrape(
            {
                "keywords": request.keywords,
                "location": request.location,
            }
        )

        logger.info("Scrape completed: %d jobs found", len(jobs))
        return {"jobs": jobs, "count": len(jobs)}

    except HTTPException:
        raise

    except Exception:
        logger.exception("Error during scraping")
        raise HTTPException(status_code=500, detail="Scraping failed")

    finally:
        if page is not None:
            await browser_pool.release(page)


@app.post("/api/apply")
async def apply_to_job(request: ApplyRequest) -> dict:
    """Trigger automated job application using a browser instance.

    Args:
        request: Application parameters including job URL and resume.

    Returns:
        Dictionary with application result status.
    """
    logger.info(
        "Apply request: job_url='%s', user_id=%d",
        request.job_url,
        request.user_id,
    )

    # Placeholder: real auto-apply logic will be implemented per job board.
    return {
        "status": "submitted",
        "job_url": request.job_url,
        "message": "Application submitted (mock)",
    }


@app.get("/api/pool/status")
async def pool_status() -> dict:
    """Return the current browser pool status.

    Returns:
        Dictionary with pool capacity and availability information.
    """
    return {
        "max_browsers": browser_pool.max_browsers,
        "available": browser_pool.semaphore._value,
        "initialized": browser_pool.initialized,
    }
