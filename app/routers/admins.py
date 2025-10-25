from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..auth import get_current_admin
from ..models import Loan
from ..schemas import LoanResponse, LoanUpdate
from ..utils import calculate_emi

router = APIRouter(prefix="/admins", tags=["admins"])

@router.get("/loans", response_model=list[LoanResponse])
def get_pending_loans(db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    loans = db.query(Loan).filter(Loan.status == "pending").all()
    # Calculate EMI for each pending loan so admin can see it before approval
    for loan in loans:
        loan.emi = calculate_emi(loan.amount, loan.interest_rate, loan.tenure_months)
    return loans

@router.put("/loans/{loan_id}", response_model=LoanResponse)
def update_loan_status(loan_id: int, update: LoanUpdate, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    if loan.status != "pending":
        raise HTTPException(status_code=400, detail="Loan is not pending")
    loan.status = update.status
    if update.status == "approved":
        emi = calculate_emi(loan.amount, loan.interest_rate, loan.tenure_months)
        loan.emi = emi
    db.commit()
    db.refresh(loan)
    return loan