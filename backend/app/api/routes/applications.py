"""Application tracking routes for CRUD operations."""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.application import Application
from app.schemas.application import (
    ApplicationCreate,
    ApplicationResponse,
    ApplicationUpdate,
)

router = APIRouter(prefix="/api/applications", tags=["Applications"])


@router.get("/", response_model=list[ApplicationResponse])
def list_applications(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[Application]:
    """List all applications for the current user.

    Args:
        current_user: Authenticated user claims.
        db: Database session.

    Returns:
        List of the user's job applications.
    """
    return (
        db.query(Application)
        .filter(Application.user_id == current_user["id"])
        .all()
    )


@router.post("/", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
def create_application(
    app_data: ApplicationCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Application:
    """Create a new job application.

    Args:
        app_data: Application creation payload.
        current_user: Authenticated user claims.
        db: Database session.

    Returns:
        The newly created application.
    """
    application = Application(
        user_id=current_user["id"],
        job_id=app_data.job_id,
        notes=app_data.notes,
        resume_used=app_data.resume_used,
        applied_at=datetime.now(timezone.utc),
    )
    db.add(application)
    db.commit()
    db.refresh(application)
    return application


@router.get("/{app_id}", response_model=ApplicationResponse)
def get_application(
    app_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Application:
    """Get a specific application by ID.

    Args:
        app_id: The application's database ID.
        current_user: Authenticated user claims.
        db: Database session.

    Returns:
        The requested application.

    Raises:
        HTTPException: 404 if not found or doesn't belong to the user.
    """
    application = (
        db.query(Application)
        .filter(
            Application.id == app_id,
            Application.user_id == current_user["id"],
        )
        .first()
    )
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )
    return application


@router.put("/{app_id}", response_model=ApplicationResponse)
def update_application(
    app_id: int,
    app_data: ApplicationUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Application:
    """Update an application's status or notes.

    Args:
        app_id: The application's database ID.
        app_data: Fields to update.
        current_user: Authenticated user claims.
        db: Database session.

    Returns:
        The updated application.

    Raises:
        HTTPException: 404 if not found or doesn't belong to the user.
    """
    application = (
        db.query(Application)
        .filter(
            Application.id == app_id,
            Application.user_id == current_user["id"],
        )
        .first()
    )
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )

    update_data = app_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(application, field, value)

    db.commit()
    db.refresh(application)
    return application
