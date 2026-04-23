from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, Contact, InsuranceType
from app.schemas import (
    UserListResponse,
    UserResponse,
    ContactListResponse,
    ContactResponse,
    MessageResponse,
)
from app.auth import get_current_admin, TokenData

router = APIRouter(prefix="/admin", tags=["Admin"])


# ──────────────────────────────────────────────
# GET /admin/users  — paginated + searchable
# ──────────────────────────────────────────────
@router.get(
    "/users",
    response_model=UserListResponse,
    summary="Get all registered users (admin only)",
)
def get_all_users(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Filter by name or email"),
    admin: TokenData = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    query = db.query(User)

    if search:
        search_term = f"%{search.strip()}%"
        query = query.filter(
            (User.full_name.ilike(search_term)) | (User.email.ilike(search_term))
        )

    total = query.count()
    users = (
        query.order_by(User.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return UserListResponse(
        total=total,
        page=page,
        page_size=page_size,
        users=users,
    )


# ──────────────────────────────────────────────
# GET /admin/contacts  — paginated + filter by insurance_type
# ──────────────────────────────────────────────
@router.get(
    "/contacts",
    response_model=ContactListResponse,
    summary="Get all contact/inquiry submissions (admin only)",
)
def get_all_contacts(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    insurance_type: Optional[str] = Query(
        None, description="Filter by insurance type (health, life, motor, ...)"
    ),
    search: Optional[str] = Query(None, description="Filter by name or email"),
    admin: TokenData = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    query = db.query(Contact)

    # Filter by insurance_type
    if insurance_type:
        try:
            ins_enum = InsuranceType(insurance_type.lower().strip())
            query = query.filter(Contact.insurance_type == ins_enum)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Invalid insurance_type '{insurance_type}'. "
                       "Allowed: health, life, motor, travel, home, business, other",
            )

    # Search by name or email
    if search:
        search_term = f"%{search.strip()}%"
        query = query.filter(
            (Contact.full_name.ilike(search_term)) | (Contact.email.ilike(search_term))
        )

    total = query.count()
    contacts = (
        query.order_by(Contact.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return ContactListResponse(
        total=total,
        page=page,
        page_size=page_size,
        contacts=contacts,
    )


# ──────────────────────────────────────────────
# GET /admin/user/{id}  — single user
# ──────────────────────────────────────────────
@router.get(
    "/user/{user_id}",
    response_model=UserResponse,
    summary="Get a single user by ID (admin only)",
)
def get_user(
    user_id: int,
    admin: TokenData = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )
    return user


# ──────────────────────────────────────────────
# DELETE /admin/user/{id}
# ──────────────────────────────────────────────
@router.delete(
    "/user/{user_id}",
    response_model=MessageResponse,
    summary="Delete a user by ID (admin only)",
)
def delete_user(
    user_id: int,
    admin: TokenData = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )
    db.delete(user)
    db.commit()
    return MessageResponse(message=f"User {user_id} deleted successfully")


# ──────────────────────────────────────────────
# GET /admin/contact/{id}  — single contact
# ──────────────────────────────────────────────
@router.get(
    "/contact/{contact_id}",
    response_model=ContactResponse,
    summary="Get a single contact/inquiry by ID (admin only)",
)
def get_contact(
    contact_id: int,
    admin: TokenData = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contact with id {contact_id} not found",
        )
    return contact


# ──────────────────────────────────────────────
# DELETE /admin/contact/{id}
# ──────────────────────────────────────────────
@router.delete(
    "/contact/{contact_id}",
    response_model=MessageResponse,
    summary="Delete a contact/inquiry by ID (admin only)",
)
def delete_contact(
    contact_id: int,
    admin: TokenData = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contact with id {contact_id} not found",
        )
    db.delete(contact)
    db.commit()
    return MessageResponse(message=f"Contact {contact_id} deleted successfully")
