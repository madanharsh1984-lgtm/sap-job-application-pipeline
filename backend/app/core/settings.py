from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    DATABASE_URL: str = 'postgresql://postgres:postgres@postgres:5432/sap_pipeline'
    DB_STARTUP_MAX_ATTEMPTS: int = 30
    DB_STARTUP_RETRY_SECONDS: float = 2.0
    SECRET_KEY: str = 'change-me-in-production'
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    CORS_ORIGINS: str = 'http://localhost:3000'
    APIFY_TOKEN: str = ''
    APIFY_ACTOR_ID: str = 'harvestapi~linkedin-post-search'
    APIFY_MAX_POSTS: int = 50
    APIFY_MAX_CONCURRENT_RUNS: int = 2
    APIFY_CONCURRENCY_WAIT_SECONDS: int = 180
    APIFY_CONCURRENCY_POLL_SECONDS: float = 3.0
    APIFY_RUN_STATUS_MAX_POLLS: int = 30
    APIFY_RUN_STATUS_POLL_SECONDS: float = 2.0


settings = Settings()
