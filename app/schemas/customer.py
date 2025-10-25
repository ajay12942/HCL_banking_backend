from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime
import re

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

    @field_validator('phone')
    @classmethod
    def phone_must_be_valid(cls, v):
        if v is not None and not re.match(r'^\+?1?[-.\s]?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})$', v):
            raise ValueError('Phone number must be in valid format (e.g., +1-123-456-7890 or 1234567890)')
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