from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Contact, InsuranceType
from app.schemas import ContactCreate, ContactResponse, MessageResponse
from app.auth import get_current_user

router = APIRouter(tags=["Contact"])


# ──────────────────────────────────────────────
# POST /contact
# ──────────────────────────────────────────────
@router.post(
    "/contact",
    response_model=ContactResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit an insurance inquiry / contact form",
)
def submit_contact(
    payload: ContactCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Requires authentication.
    Only logged-in users can submit an inquiry form.
    """
    try:
        insurance_enum = InsuranceType(payload.insurance_type.lower())
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid insurance_type '{payload.insurance_type}'",
        )

    contact = Contact(
        full_name=payload.full_name.strip(),
        email=payload.email.lower().strip(),
        phone=payload.phone.strip(),
        insurance_type=insurance_enum,
        message=payload.message.strip() if payload.message else None,
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact
