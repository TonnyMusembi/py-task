# schemas/loan.py
from pydantic import BaseModel, condecimal
from typing import Literal, Optional


class LoanCreate(BaseModel):
    user_id: int
    amount: condecimal(max_digits=10, decimal_places=2)
    status: Optional[Literal["pending", "approved", "disbursed", "rejected"]] = "pending"
