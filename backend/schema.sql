-- =============================================================================
-- Database Schema — JobAccelerator AI
-- =============================================================================
-- Keyword Deduplication + Shared Scraping Architecture
--
-- Core principle: Multiple users with similar resumes share the same
-- keyword_set and job results. Apify is triggered ONLY once per unique
-- keyword hash.
-- =============================================================================

-- 1. Users
CREATE TABLE IF NOT EXISTS users (
    id              SERIAL PRIMARY KEY,
    email           VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    created_at      TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users (email);

-- 2. Resumes (one per user upload)
CREATE TABLE IF NOT EXISTS resumes (
    id          SERIAL PRIMARY KEY,
    user_id     INTEGER      NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    raw_text    TEXT         NOT NULL,
    parsed_data TEXT,                  -- JSON: extracted keywords
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_resumes_user_id ON resumes (user_id);

-- 3. Keyword Sets (deduplicated by hash)
CREATE TABLE IF NOT EXISTS keyword_sets (
    id                   SERIAL PRIMARY KEY,
    keyword_hash         VARCHAR(64)  NOT NULL UNIQUE,  -- SHA-256
    normalized_keywords  TEXT         NOT NULL,          -- JSON array
    created_at           TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_keyword_sets_hash ON keyword_sets (keyword_hash);

-- 4. User ↔ Keyword Set mapping (many-to-many)
CREATE TABLE IF NOT EXISTS user_keyword_map (
    id              SERIAL PRIMARY KEY,
    user_id         INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    keyword_set_id  INTEGER NOT NULL REFERENCES keyword_sets(id) ON DELETE CASCADE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_user_keyword UNIQUE (user_id, keyword_set_id)
);

CREATE INDEX IF NOT EXISTS idx_ukm_user_id ON user_keyword_map (user_id);
CREATE INDEX IF NOT EXISTS idx_ukm_keyword_set_id ON user_keyword_map (keyword_set_id);

-- 5. Jobs (linked to keyword_set, shared across users)
CREATE TABLE IF NOT EXISTS jobs (
    id              SERIAL PRIMARY KEY,
    keyword_set_id  INTEGER       NOT NULL REFERENCES keyword_sets(id) ON DELETE CASCADE,
    external_id     VARCHAR(255),          -- Apify post URL for dedup
    title           VARCHAR(500)  NOT NULL,
    company         VARCHAR(255),
    location        VARCHAR(255),
    email           VARCHAR(255),
    post_url        VARCHAR(2048),
    job_data        TEXT          NOT NULL, -- Full JSON blob
    source          VARCHAR(100),
    created_at      TIMESTAMPTZ   NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_jobs_keyword_set_id ON jobs (keyword_set_id);
CREATE INDEX IF NOT EXISTS idx_jobs_external_id ON jobs (external_id);

-- 6. Applications (future — tracks user applications)
CREATE TABLE IF NOT EXISTS applications (
    id          SERIAL PRIMARY KEY,
    user_id     INTEGER      NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    job_id      INTEGER      NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    status      VARCHAR(50)  NOT NULL DEFAULT 'pending',  -- pending, applied, rejected, interview
    applied_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_user_job_application UNIQUE (user_id, job_id)
);

CREATE INDEX IF NOT EXISTS idx_applications_user_id ON applications (user_id);

-- =============================================================================
-- DEDUPLICATION FLOW (comment for documentation):
--
--   User uploads resume
--     → extract_keywords(resume_text) → ["aws", "fastapi", "python", "sap"]
--     → normalize + sort → SHA-256 hash
--     → SELECT * FROM keyword_sets WHERE keyword_hash = ?
--       → IF EXISTS: reuse keyword_set, map user → DO NOT call Apify
--       → IF NOT EXISTS: create keyword_set, call Apify, store jobs
--
-- For 50 users with similar SAP resumes:
--   - Maybe 10-15 unique keyword hashes
--   - Apify called ≤15 times (not 50!)
--   - All users get the same shared job results
-- =============================================================================
