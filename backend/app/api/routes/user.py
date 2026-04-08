from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.resume import Resume
from app.models.user import User
from app.schemas.job import JobOut
from app.services.job_service import (
    extract_keywords,
    list_jobs_for_user,
    upsert_user_keyword_set,
)
from app.tasks.automation import trigger_apify

router = APIRouter(tags=['user'])


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

    keywords = extract_keywords(resume_content)
    if not keywords:
        raise HTTPException(status_code=400, detail='Could not extract meaningful keywords')

    keyword_set, created = upsert_user_keyword_set(db, user.id, keywords)
    resume = Resume(user_id=user.id, content=resume_content, keywords=','.join(keywords))
    db.add(resume)
    db.commit()
    db.refresh(resume)

    if created:
        trigger_apify.delay(keyword_set.id)

    return {'id': resume.id, 'keywords': keywords, 'keyword_set_id': keyword_set.id, 'scrape_queued': created}


@router.get('/api/jobs', response_model=list[JobOut])
def get_jobs(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return list_jobs_for_user(db, user.id)
