from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class BranchCreate(BaseModel):
    name:             str  = Field(..., max_length=40)
    physical_address: str  = Field(..., max_length=255)
    loan_period:      str  = Field(..., max_length=40)
    approves_loan:    bool
    company_id:       int
    branch_code:      Optional[str]  = Field(None, max_length=20)
    manager_name:     Optional[str]  = Field(None, max_length=100)
    email:            Optional[EmailStr] = None
    phone:            Optional[str]  = Field(None, max_length=20)
    status:           int  = 1

    model_config = {
        "json_schema_extra": {
            "example": {
                "name":             "Acme Nairobi Branch",
                "physical_address": "123 Kimathi Street, Nairobi",
                "loan_period":      "30 days",
                "approves_loan":    True,
                "company_id":       1,
                "branch_code":      "NBI-001",
                "manager_name":     "John Kamau",
                "email":            "nairobi@acme.co.ke",
                "phone":            "+254700000001"
            }
        }
    }


class BranchUpdate(BaseModel):
    name:             Optional[str]      = Field(None, max_length=40)
    physical_address: Optional[str]      = Field(None, max_length=255)
    loan_period:      Optional[str]      = Field(None, max_length=40)
    approves_loan:    Optional[bool]     = None
    branch_code:      Optional[str]      = Field(None, max_length=20)
    manager_name:     Optional[str]      = Field(None, max_length=100)
    email:            Optional[EmailStr] = None
    phone:            Optional[str]      = Field(None, max_length=20)
    status:           Optional[int]      = None


class BranchOut(BaseModel):
    id:               int
    name:             str
    lower_name:       Optional[str]
    physical_address: str
    loan_period:      str
    approves_loan:    bool
    status:           int
    version:          str
    company_id:       int
    branch_code:      Optional[str]
    manager_name:     Optional[str]
    email:            Optional[str]
    phone:            Optional[str]
    created_at:       datetime
    updated_at:       datetime
    created_by:       Optional[int]
    updated_by:       Optional[int]

    model_config = {"from_attributes": True}
