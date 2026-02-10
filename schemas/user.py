# schemas/user.py
from pydantic import BaseModel, EmailStr
from typing import Literal


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: Literal["admin", "agent", "customer"] = "customer"
