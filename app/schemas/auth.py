from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    is_admin: bool = False

class LoginRequest(BaseModel):
    email: str
    password: str
    is_admin: bool = False