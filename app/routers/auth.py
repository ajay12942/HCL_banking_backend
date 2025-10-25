from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Customer, BankAdmin
from ..schemas.customer import CustomerCreate, CustomerResponse
from ..schemas.auth import LoginRequest, Token
from ..auth import get_password_hash, verify_password, create_access_token
from ..config import settings

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=CustomerResponse)
def register_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    db_customer = db.query(Customer).filter(Customer.email == customer.email).first()
    if db_customer:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(customer.password)
    db_customer = Customer(
        name=customer.name,
        email=customer.email,
        password_hash=hashed_password,
        age=customer.age,
        phone=customer.phone,
        address=customer.address
    )
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@router.post("/token", response_model=Token)
def login_for_access_token(form_data: LoginRequest, db: Session = Depends(get_db)):
    if form_data.is_admin:
        user = db.query(BankAdmin).filter(BankAdmin.email == form_data.email).first()
    else:
        user = db.query(Customer).filter(Customer.email == form_data.email).first()
    
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email, "is_admin": form_data.is_admin}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}