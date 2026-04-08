import json

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.job import Job
from app.models.resume import Resume
from app.models.user import User
from app.schemas.job import JobOut
from app.services.job_service import ingest_jobs_from_file, list_jobs, trigger_scrape

router = APIRouter(tags=['user'])
MIN_KEYWORD_LENGTH = 4
MAX_KEYWORDS = 30


@router.post('/api/user/onboard')
def onboard_resume(
    content: str | None = Form(default=None),
    file: UploadFile | None = File(default=None),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    resume_content = content or ''
    if file is not None:
        bytes_content = file.file.read()
        resume_content = bytes_content.decode('utf-8', errors='ignore')

    if not resume_content.strip():
        raise HTTPException(status_code=400, detail='Resume content is required')

    keywords = [w.lower() for w in resume_content.split() if len(w) > MIN_KEYWORD_LENGTH][:MAX_KEYWORDS]
    resume = Resume(user_id=user.id, content=resume_content, keywords=','.join(keywords))
    db.add(resume)
    db.commit()
    db.refresh(resume)
    return {'id': resume.id, 'keywords': keywords}


@router.get('/api/jobs', response_model=list[JobOut])
def get_jobs(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    jobs = list_jobs(db)
    if jobs:
        return jobs

    trigger_scrape()
    ingest_jobs_from_file(db)
    jobs = list_jobs(db)
    if not jobs:
        # fallback placeholder for MVP visibility
        sample = Job(
            keyword_group='SAP',
            job_data=json.dumps({'title': 'SAP Program Manager', 'source': 'MVP sample'}),
        )
        db.add(sample)
        db.commit()
        db.refresh(sample)
        return [sample]

    return jobs
