"""Resume management routes for upload, listing, and deletion."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.resume import Resume
from app.schemas.resume import ResumeResponse
from app.services.s3 import s3_service

router = APIRouter(prefix="/api/resumes", tags=["Resumes"])


@router.get("/", response_model=list[ResumeResponse])
def list_resumes(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[Resume]:
    """List all resumes for the current user.

    Args:
        current_user: Authenticated user claims.
        db: Database session.

    Returns:
        List of the user's resumes.
    """
    return db.query(Resume).filter(Resume.user_id == current_user["id"]).all()


@router.post("/upload", response_model=ResumeResponse, status_code=status.HTTP_201_CREATED)
async def upload_resume(
    file: UploadFile,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Resume:
    """Upload a resume file and store its metadata.

    Args:
        file: The uploaded file.
        current_user: Authenticated user claims.
        db: Database session.

    Returns:
        The created resume record.

    Raises:
        HTTPException: 400 if no filename is provided.
    """
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename is required",
        )

    file_content = await file.read()
    s3_key = f"resumes/{current_user['id']}/{uuid.uuid4()}/{file.filename}"
    s3_service.upload_file(file_content, s3_key)

    resume = Resume(
        user_id=current_user["id"],
        filename=file.filename,
        s3_key=s3_key,
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)
    return resume


@router.get("/{resume_id}", response_model=ResumeResponse)
def get_resume(
    resume_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Resume:
    """Get a specific resume's metadata.

    Args:
        resume_id: The resume's database ID.
        current_user: Authenticated user claims.
        db: Database session.

    Returns:
        The requested resume record.

    Raises:
        HTTPException: 404 if not found or doesn't belong to the user.
    """
    resume = (
        db.query(Resume)
        .filter(Resume.id == resume_id, Resume.user_id == current_user["id"])
        .first()
    )
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found"
        )
    return resume


@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resume(
    resume_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    """Delete a resume and its associated file.

    Args:
        resume_id: The resume's database ID.
        current_user: Authenticated user claims.
        db: Database session.

    Raises:
        HTTPException: 404 if not found or doesn't belong to the user.
    """
    resume = (
        db.query(Resume)
        .filter(Resume.id == resume_id, Resume.user_id == current_user["id"])
        .first()
    )
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found"
        )

    if resume.s3_key:
        s3_service.delete_file(resume.s3_key)

    db.delete(resume)
    db.commit()
