from __future__ import annotations

import json
from pathlib import Path

from sqlalchemy.orm import Session

from app.models.job import Job
from app.services.script_runner import REPO_ROOT, run_script

MAX_JOBS_TO_INGEST = 200


def _jobs_file_path() -> Path:
    return REPO_ROOT / 'linkedin_posts_today.json'


def trigger_scrape() -> dict:
    return run_script('apify_scrape.py')


def ingest_jobs_from_file(db: Session, keyword_group: str = 'SAP') -> int:
    jobs_file = _jobs_file_path()
    if not jobs_file.exists():
        return 0

    try:
        records = json.loads(jobs_file.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return 0

    inserted = 0
    for record in records[:MAX_JOBS_TO_INGEST]:
        job = Job(keyword_group=keyword_group, job_data=json.dumps(record))
        db.add(job)
        inserted += 1
    db.commit()
    return inserted


def list_jobs(db: Session) -> list[Job]:
    return db.query(Job).order_by(Job.id.desc()).limit(200).all()
