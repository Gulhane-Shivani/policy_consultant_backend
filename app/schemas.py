from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator
import re


# ──────────────────────────────────────────────
# Auth Schemas
# ──────────────────────────────────────────────
class UserRegister(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    mobile: Optional[str] = None

    @field_validator("full_name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("full_name cannot be empty")
        return v

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v

    @field_validator("mobile")
    @classmethod
    def validate_mobile(cls, v: Optional[str]) -> Optional[str]:
        if v:
            # Allow common characters but strip them for validation
            v = v.strip()
            # Remove spaces, hyphens, parentheses, and dots
            clean_v = re.sub(r"[\s\-\(\)\.]", "", v)
            if not re.match(r"^[0-9]{10}$", clean_v):
                raise ValueError("Mobile number must be exactly 10 digits")
            return clean_v
        return v


# ──────────────────────────────────────────────
# User Response Schemas
# ──────────────────────────────────────────────
class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    mobile: Optional[str] = None
    role: str
    created_at: datetime

    model_config = {"from_attributes": True}


class UserListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    users: list[UserResponse]


# ──────────────────────────────────────────────
# Auth Schemas
# ──────────────────────────────────────────────
class UserLogin(BaseModel):
    email: EmailStr
    password: str


class AdminLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: Optional[UserResponse] = None


class TokenData(BaseModel):
    user_id: Optional[int] = None
    role: Optional[str] = None


# ──────────────────────────────────────────────
# Contact Schemas
# ──────────────────────────────────────────────
class ContactCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    insurance_type: str
    message: Optional[str] = None

    @field_validator("full_name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("full_name cannot be empty")
        return v

    @field_validator("insurance_type")
    @classmethod
    def valid_insurance_type(cls, v: str) -> str:
        allowed = {"health", "life", "motor", "travel", "home", "business", "other"}
        v = v.lower().strip()
        if v not in allowed:
            raise ValueError(f"insurance_type must be one of: {', '.join(allowed)}")
        return v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        v = v.strip()
        # Remove spaces, hyphens, parentheses, and dots
        clean_v = re.sub(r"[\s\-\(\)\.]", "", v)
        if not re.match(r"^[0-9]{10}$", clean_v):
            raise ValueError("Phone number must be exactly 10 digits")
        return clean_v


class ContactResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone: str
    insurance_type: str
    message: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class ContactListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    contacts: list[ContactResponse]


# ──────────────────────────────────────────────
# Generic
# ──────────────────────────────────────────────
class MessageResponse(BaseModel):
    message: str
