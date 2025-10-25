from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class LoanCreate(BaseModel):
    loan_type: str
    amount: float
    tenure_months: int
    interest_rate: float  # Annual interest rate in percentage, e.g., 12.5

class LoanResponse(BaseModel):
    id: int
    customer_id: int
    loan_type: str
    amount: float
    tenure_months: int
    interest_rate: float
    emi: Optional[float]
    status: str
    applied_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class LoanUpdate(BaseModel):
    status: str  # 'approved' or 'rejected'

class LoanList(BaseModel):
    loans: List[LoanResponse]