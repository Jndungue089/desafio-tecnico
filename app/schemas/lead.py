from pydantic import BaseModel, EmailStr
from typing import Optional


class LeadCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str


class LeadResponse(BaseModel):
    id: str
    name: str
    email: str
    phone: str
    birth_date: Optional[str] = None
