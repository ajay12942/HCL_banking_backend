from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime

class CustomerCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    age: int
    phone: Optional[str] = None
    address: Optional[str] = None

    @field_validator('age')
    @classmethod
    def age_must_be_valid(cls, v):
        if v < 18:
            raise ValueError('Age must be at least 18')
        return v

class CustomerLogin(BaseModel):
    email: EmailStr
    password: str

class CustomerResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int
    phone: Optional[str]
    address: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True