from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_admin
from app.models.job import Job
from app.models.resume import Resume
from app.models.user import User
from app.schemas.admin import MetricsOut
from app.services.local_storage_service import get_admin_stats

router = APIRouter(prefix='/admin', tags=['admin'])


@router.get('/users')
def admin_users(db: Session = Depends(get_db), _admin: User = Depends(require_admin)):
    users = db.query(User).order_by(User.created_at.desc()).all()
    return [
        {
            'id': u.id,
            'email': u.email,
            'role': u.role,
            'created_at': u.created_at.isoformat(),
        }
        for u in users
    ]


@router.get('/metrics', response_model=MetricsOut)
def admin_metrics(db: Session = Depends(get_db), _admin: User = Depends(require_admin)):
    users_count = db.query(func.count(User.id)).scalar() or 0
    jobs_count = db.query(func.count(Job.id)).scalar() or 0
    resumes_count = db.query(func.count(Resume.id)).scalar() or 0
    return MetricsOut(users_count=users_count, jobs_count=jobs_count, resumes_count=resumes_count)


@router.get('/stats')
def admin_stats():
    return get_admin_stats()
