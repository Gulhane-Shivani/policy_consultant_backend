from app.database import SessionLocal
from app.models import User, UserRole
from app.auth import hash_password

def create_superadmin():
    db = SessionLocal()
    try:
        # Check if superadmin already exists
        email = "superadmin@safeguard.com"
        existing = db.query(User).filter(User.email == email).first()
        
        if existing:
            print(f"Superadmin already exists: {email}")
            # Update role just in case
            existing.role = UserRole.super_admin
            db.commit()
            print("Role verified as super_admin.")
            return

        new_user = User(
            full_name="Super Administrator",
            email=email,
            password=hash_password("admin123"),
            role=UserRole.super_admin
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print(f"Superadmin created successfully!")
        print(f"Email: {email}")
        print(f"Password: admin123")
        
    except Exception as e:
        print(f"Error creating superadmin: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_superadmin()
