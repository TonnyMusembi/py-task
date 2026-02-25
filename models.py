from sqlalchemy import Column, Integer, String, SmallInteger, Boolean, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import relationship
from src.database import get_db
class Branch():
    __tablename__ = "branches"

    id               = Column(Integer, primary_key=True, autoincrement=True)
    name             = Column(String(40), unique=True, nullable=False)
    lower_name       = Column(String(40), unique=True, nullable=True)
    physical_address = Column(String(255), nullable=False)
    loan_period      = Column(String(40), nullable=False)
    approves_loan    = Column(Boolean, nullable=False)
    status           = Column(SmallInteger, nullable=False, default=1)
    version          = Column(String(10), nullable=False, default="0")
    company_id       = Column(Integer, ForeignKey("companies.id"), nullable=False)
    branch_code      = Column(String(20), unique=True, nullable=True)
    manager_name     = Column(String(100), nullable=True)
    email            = Column(String(100), nullable=True)
    phone            = Column(String(20), nullable=True)
    created_at       = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at       = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by       = Column(Integer, nullable=True)
    updated_by       = Column(Integer, nullable=True)

    # Relationships
    company = relationship("Company", back_populates="branches")
