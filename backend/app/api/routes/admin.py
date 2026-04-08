"""Admin routes for user management, stats, and system logs."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.application import Application
from app.models.job import Job
from app.models.log import Log
from app.models.user import User
from app.schemas.user import UserResponse

router = APIRouter(prefix="/api/admin", tags=["Admin"])


async def require_admin(current_user: dict = Depends(get_current_user)) -> dict:
    """Dependency that enforces admin role access.

    Args:
        current_user: Authenticated user claims.

    Returns:
        The current user claims if they have admin role.

    Raises:
        HTTPException: 403 if the user is not an admin.
    """
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user


@router.get("/users", response_model=list[UserResponse])
def list_users(
    _admin: dict = Depends(require_admin),
    db: Session = Depends(get_db),
) -> list[User]:
    """List all users in the system (admin only).

    Args:
        _admin: Verified admin user claims.
        db: Database session.

    Returns:
        List of all users.
    """
    return db.query(User).all()


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    _admin: dict = Depends(require_admin),
    db: Session = Depends(get_db),
) -> User:
    """Get a specific user by ID (admin only).

    Args:
        user_id: The user's database ID.
        _admin: Verified admin user claims.
        db: Database session.

    Returns:
        The requested user.

    Raises:
        HTTPException: 404 if the user is not found.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.put("/users/{user_id}/role", response_model=UserResponse)
def update_user_role(
    user_id: int,
    role: str = Query(..., pattern="^(admin|user)$"),
    _admin: dict = Depends(require_admin),
    db: Session = Depends(get_db),
) -> User:
    """Update a user's role (admin only).

    Args:
        user_id: The user's database ID.
        role: New role — must be 'admin' or 'user'.
        _admin: Verified admin user claims.
        db: Database session.

    Returns:
        The updated user.

    Raises:
        HTTPException: 404 if the user is not found.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    user.role = role
    db.commit()
    db.refresh(user)
    return user


@router.get("/stats")
def get_stats(
    _admin: dict = Depends(require_admin),
    db: Session = Depends(get_db),
) -> dict:
    """Get system-wide statistics (admin only).

    Args:
        _admin: Verified admin user claims.
        db: Database session.

    Returns:
        Dictionary with total users, jobs, and applications counts.
    """
    return {
        "total_users": db.query(User).count(),
        "total_jobs": db.query(Job).count(),
        "total_applications": db.query(Application).count(),
    }


@router.get("/logs")
def get_logs(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    _admin: dict = Depends(require_admin),
    db: Session = Depends(get_db),
) -> dict:
    """Get paginated system audit logs (admin only).

    Args:
        page: Page number (1-based).
        per_page: Number of results per page.
        _admin: Verified admin user claims.
        db: Database session.

    Returns:
        Paginated log entries with total count.
    """
    query = db.query(Log).order_by(Log.created_at.desc())
    total = query.count()
    logs = query.offset((page - 1) * per_page).limit(per_page).all()
    return {"logs": logs, "total": total, "page": page, "per_page": per_page}
