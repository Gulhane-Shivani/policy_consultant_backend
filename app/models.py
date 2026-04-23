from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
from sqlalchemy.sql import func
import enum
from app.database import Base


# ──────────────────────────────────────────────
# Enums
# ──────────────────────────────────────────────
class UserRole(str, enum.Enum):
    user = "user"
    admin = "admin"


class InsuranceType(str, enum.Enum):
    health = "health"
    life = "life"
    motor = "motor"
    travel = "travel"
    home = "home"
    business = "business"
    other = "other"


# ──────────────────────────────────────────────
# Models
# ──────────────────────────────────────────────
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(150), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    mobile = Column(String(20), nullable=True)
    role = Column(
        Enum(UserRole, name="userrole"),
        default=UserRole.user,
        nullable=False,
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(150), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    insurance_type = Column(
        Enum(InsuranceType, name="insurancetype"),
        nullable=False,
    )
    message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
