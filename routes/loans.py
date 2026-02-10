# routes/loans.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
# from schemas.loan import LoanCreate
from schemas.loan import LoanCreate
from src.database import get_db
from core.logger import logger

router = APIRouter(prefix="/loans", tags=["Loans"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_loan(
    payload: LoanCreate,
    db: AsyncSession = Depends(get_db),
):
    if not db:
        logger.error("Database connection failed in create_loan")
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        # Optional: validate user exists
        result = await db.execute(
            text("SELECT id FROM users WHERE id = :user_id"),
            {"user_id": payload.user_id},
        )
        if not result.fetchone():
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        await db.execute(
    text("""
        INSERT INTO loans (user_id, amount, status)
        VALUES (:user_id, :amount, :status)
    """),
    {
        "user_id": payload.user_id,
        "amount": payload.amount,
        "status": payload.status,
    },
)

        await db.commit()
        logger.info(
            "Loan created successfully | user_id=%s | amount=%s",
            payload.user_id,
            payload.amount,
        )
        logger.info("Create loan payload: %s", payload.dict())


        return {"message": "Loan created successfully"}

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.exception("Failed to create loan")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
     )
