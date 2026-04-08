from fastapi import APIRouter, File, Form, HTTPException, Query, UploadFile
from app.services.local_storage_service import (
    get_dashboard,
    get_user_jobs,
    onboard_user,
)

router = APIRouter(tags=['user'])


@router.post('/api/user/onboard')
def onboard_resume(
    email: str = Form(...),
    content: str | None = Form(default=None),
    file: UploadFile | None = File(default=None),
):
    resume_content = content or ''
    if file is not None:
        bytes_content = file.file.read()
        resume_content = bytes_content.decode('utf-8', errors='ignore')

    if not resume_content.strip():
        raise HTTPException(status_code=400, detail='Resume content is required')

    try:
        payload = onboard_user(email, resume_content)
        payload['email'] = email
        return payload
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get('/api/jobs')
def get_jobs(
    email: str = Query(...),
):
    try:
        return get_user_jobs(email)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get('/api/dashboard')
def user_dashboard(
    email: str = Query(...),
):
    try:
        return get_dashboard(email)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
