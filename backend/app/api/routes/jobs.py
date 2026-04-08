"""Job listing routes for CRUD operations."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.job import Job
from app.schemas.job import JobCreate, JobListResponse, JobResponse, JobUpdate

router = APIRouter(prefix="/api/jobs", tags=["Jobs"])


@router.get("/", response_model=JobListResponse)
def list_jobs(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    """List all jobs for the current user with pagination.

    Args:
        page: Page number (1-based).
        per_page: Number of results per page.
        current_user: Authenticated user claims.
        db: Database session.

    Returns:
        Paginated list of jobs.
    """
    query = db.query(Job).filter(Job.user_id == current_user["id"])
    total = query.count()
    jobs = query.offset((page - 1) * per_page).limit(per_page).all()
    return {"jobs": jobs, "total": total, "page": page, "per_page": per_page}


@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
def create_job(
    job_data: JobCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Job:
    """Create a new job listing for the current user.

    Args:
        job_data: Job creation payload.
        current_user: Authenticated user claims.
        db: Database session.

    Returns:
        The newly created job.
    """
    job = Job(user_id=current_user["id"], **job_data.model_dump())
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


@router.get("/{job_id}", response_model=JobResponse)
def get_job(
    job_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Job:
    """Get a specific job by ID.

    Args:
        job_id: The job's database ID.
        current_user: Authenticated user claims.
        db: Database session.

    Returns:
        The requested job.

    Raises:
        HTTPException: 404 if the job is not found or doesn't belong to the user.
    """
    job = (
        db.query(Job)
        .filter(Job.id == job_id, Job.user_id == current_user["id"])
        .first()
    )
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job not found"
        )
    return job


@router.put("/{job_id}", response_model=JobResponse)
def update_job(
    job_id: int,
    job_data: JobUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Job:
    """Update an existing job listing.

    Args:
        job_id: The job's database ID.
        job_data: Fields to update.
        current_user: Authenticated user claims.
        db: Database session.

    Returns:
        The updated job.

    Raises:
        HTTPException: 404 if the job is not found or doesn't belong to the user.
    """
    job = (
        db.query(Job)
        .filter(Job.id == job_id, Job.user_id == current_user["id"])
        .first()
    )
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job not found"
        )

    update_data = job_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(job, field, value)

    db.commit()
    db.refresh(job)
    return job


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(
    job_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    """Delete a job listing.

    Args:
        job_id: The job's database ID.
        current_user: Authenticated user claims.
        db: Database session.

    Raises:
        HTTPException: 404 if the job is not found or doesn't belong to the user.
    """
    job = (
        db.query(Job)
        .filter(Job.id == job_id, Job.user_id == current_user["id"])
        .first()
    )
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job not found"
        )
    db.delete(job)
    db.commit()
