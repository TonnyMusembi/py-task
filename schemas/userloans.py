# schemas/userloans.py
from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from typing import Optional

# Input schema - for receiving data
class LoanCreate(BaseModel):
    loan_product_id: int
    company_percentage_id: int
    employee_id: int
    waiver: Decimal
    interest: Decimal
    principal: Decimal
    total_amount: Decimal
    paid_amount: Decimal
    penalty: Decimal
    status: Optional[int] = 1
    version: Optional[str] = "0"

    model_config = ConfigDict(from_attributes=True)


# Response schema - for returning data (keep it simple)
class LoanResponse(BaseModel):
    message: str
    employee_id: int
    principal: Decimal
    total_amount: Decimal
    status: Optional[int] = 1
