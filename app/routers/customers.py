from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..auth import get_current_customer
from ..models import Loan
from ..schemas import LoanCreate, LoanResponse, CustomerResponse

router = APIRouter(prefix="/customers", tags=["customers"])

@router.get("/me", response_model=CustomerResponse)
def get_customer_profile(current_customer=Depends(get_current_customer)):
    return current_customer

@router.post("/loans", response_model=LoanResponse)
def apply_for_loan(loan: LoanCreate, db: Session = Depends(get_db), current_customer=Depends(get_current_customer)):
    db_loan = Loan(
        customer_id=current_customer.id,
        loan_type=loan.loan_type,
        amount=loan.amount,
        tenure_months=loan.tenure_months,
        interest_rate=loan.interest_rate,
        status="pending"
    )
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan

@router.get("/loans", response_model=list[LoanResponse])
def get_customer_loans(db: Session = Depends(get_db), current_customer=Depends(get_current_customer)):
    loans = db.query(Loan).filter(Loan.customer_id == current_customer.id).all()
    return loans