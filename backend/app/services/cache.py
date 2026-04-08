"""
Redis caching layer for keyword deduplication.

Prevents duplicate Apify calls by caching:
  - keyword_hash → "processing" (lock during scrape)
  - keyword_hash → "done" (scrape complete, results in DB)
"""

import logging

import redis

from backend.app.core.config import settings

logger = logging.getLogger(__name__)

_redis_client: redis.Redis | None = None


def get_redis() -> redis.Redis:
    """Get or create a Redis client singleton."""
    global _redis_client
    if _redis_client is None:
        _redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
    return _redis_client


def _cache_key(keyword_hash: str) -> str:
    """Build the Redis key for a keyword hash."""
    return f"kw:scrape:{keyword_hash}"


def is_scrape_done(keyword_hash: str) -> bool:
    """Check if scraping for this keyword hash is already complete."""
    r = get_redis()
    val = r.get(_cache_key(keyword_hash))
    return val == "done"


def is_scrape_in_progress(keyword_hash: str) -> bool:
    """Check if scraping for this keyword hash is currently running."""
    r = get_redis()
    val = r.get(_cache_key(keyword_hash))
    return val == "processing"


def mark_scrape_processing(keyword_hash: str) -> bool:
    """
    Atomically mark a keyword hash as 'processing'.

    Uses SET NX (set-if-not-exists) to prevent race conditions.
    Returns True if lock was acquired, False if already set.
    """
    r = get_redis()
    # NX = only set if not exists; EX = expire after APIFY_MAX_POLL_WAIT + buffer
    lock_ttl = settings.APIFY_MAX_POLL_WAIT + 60
    acquired = r.set(_cache_key(keyword_hash), "processing", nx=True, ex=lock_ttl)
    return bool(acquired)


def mark_scrape_done(keyword_hash: str) -> None:
    """Mark scraping as complete. TTL = KEYWORD_CACHE_TTL (24h default)."""
    r = get_redis()
    r.set(_cache_key(keyword_hash), "done", ex=settings.KEYWORD_CACHE_TTL)


def clear_scrape_status(keyword_hash: str) -> None:
    """Clear scrape status (e.g., on failure, to allow retry)."""
    r = get_redis()
    r.delete(_cache_key(keyword_hash))
