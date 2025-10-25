from app.database import SessionLocal
from app.models import BankAdmin
from app.auth import get_password_hash

db = SessionLocal()

# Check if admin already exists
existing_admin = db.query(BankAdmin).filter(BankAdmin.email == "admin@example.com").first()
if existing_admin:
    print("Admin already exists")
else:
    admin = BankAdmin(
        username="admin",
        email="admin@example.com",
        password_hash=get_password_hash("admin123")
    )
    db.add(admin)
    db.commit()
    print("Admin created: username=admin, email=admin@example.com, password=admin123")

db.close()