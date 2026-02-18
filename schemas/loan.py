# schemas/loan.py
from pydantic import BaseModel, condecimal
from typing import Literal, Optional

status: [1, 2, 3, 4] = ["pending", "approved", "disbursed", "rejected"]
class LoanCreate(BaseModel):
    user_id: int
    amount: condecimal(max_digits=10, decimal_places=2)
    status: Optional[Literal["pending", "approved", "disbursed", "rejected"]] = "pending"

