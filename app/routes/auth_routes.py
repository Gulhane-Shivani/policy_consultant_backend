from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models import User, UserRole
from app.schemas import UserRegister, UserLogin, AdminLogin, Token, UserResponse
from app.auth import hash_password, verify_password, create_access_token
from app.config import settings

router = APIRouter(tags=["Authentication"])


# ──────────────────────────────────────────────
# POST /register
# ──────────────────────────────────────────────
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    # Check duplicate email
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email already exists",
        )

    new_user = User(
        full_name=payload.full_name.strip(),
        email=payload.email.lower().strip(),
        password=hash_password(payload.password),
        mobile=payload.mobile,
        role=UserRole.user,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# ──────────────────────────────────────────────
# POST /login
# ──────────────────────────────────────────────
@router.post(
    "/login",
    response_model=Token,
    summary="Login as a registered user",
)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    email = payload.email.lower().strip()

    # ── 1. Try hardcoded admin ──────────────────
    if (
        email == settings.ADMIN_EMAIL.lower()
        and payload.password == settings.ADMIN_PASSWORD
    ):
        access_token = create_access_token(
            data={"sub": "0", "role": "admin"}
        )
        admin_user = {
            "id": 0,
            "full_name": "System Administrator",
            "email": settings.ADMIN_EMAIL,
            "role": "admin",
            "created_at": datetime.now()
        }
        return Token(access_token=access_token, user=admin_user)

    # ── 2. Try regular user ─────────────────────
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(payload.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role.value}
    )
    return Token(access_token=access_token, user=user)


# ──────────────────────────────────────────────
# POST /admin/login
# ──────────────────────────────────────────────
@router.post(
    "/admin/login",
    response_model=Token,
    summary="Login as admin (hardcoded or DB admin)",
)
def admin_login(payload: AdminLogin, db: Session = Depends(get_db)):
    email = payload.email.lower().strip()

    # ── 1. Try hardcoded admin first ────────────
    if (
        email == settings.ADMIN_EMAIL.lower()
        and payload.password == settings.ADMIN_PASSWORD
    ):
        access_token = create_access_token(
            data={"sub": "0", "role": "admin"}
        )
        # Create a mock user object for hardcoded admin
        admin_user = {
            "id": 0,
            "full_name": "System Administrator",
            "email": settings.ADMIN_EMAIL,
            "role": "admin",
            "created_at": datetime.now()
        }
        return Token(access_token=access_token, user=admin_user)

    # ── 2. Try DB admin ─────────────────────────
    user = db.query(User).filter(User.email == email).first()
    if not user or user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin credentials",
        )
    if not verify_password(payload.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin credentials",
        )

    access_token = create_access_token(
        data={"sub": str(user.id), "role": "admin"}
    )
    return Token(access_token=access_token, user=user)
