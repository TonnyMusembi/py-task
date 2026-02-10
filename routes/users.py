from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from schemas.user import UserCreate
from core.security import hash_password
# from database import get_db
from src.database import get_db
from core.logger import logger



router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    # check email existence
    result = await db.execute(
        text("SELECT id FROM users WHERE email = :email"),
        {"email": payload.email},
    )
    if result.fetchone():
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    await db.execute(
        text("""
            INSERT INTO users (full_name, email, password, role)
            VALUES (:full_name, :email, :password, :role)
        """),
        {
            "full_name": payload.full_name,
            "email": payload.email,
            "password": hash_password(payload.password),
            "role": payload.role,
        },
    )

    await db.commit()

    return {"message": "User created successfully"}
    logger.info(f"User {payload.email} created successfully.")


async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        text("""
            SELECT id, full_name, email, role, created_at
            FROM users
        """)
    )
    users = result.fetchall()
    logger.info("Fetched users successfully.")

    return {"users": [dict(row._mapping) for row in users]}
    logger.info("Returned users data successfully.")


async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        text("""
            SELECT id, full_name, email, role, created_at
            FROM users
            WHERE id = :user_id
        """),
        {"user_id": user_id},
    )

    user = result.fetchone()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {"user": dict(user._mapping)}

async def get_loans(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        text("""
            SELECT id, amount, status, created_at
            FROM loans
        """)
    )
    loans = result.fetchall()
    logger.info("Fetched loans successfully.")

    return {"loans": [dict(row._mapping) for row in loans]}
    logger.info("Returned loans data successfully.")


async def create_loan(payload: dict, db: AsyncSession = Depends(get_db)):
    await db.execute(
        text("""
            INSERT INTO loans (amount, status)
            VALUES (:amount, :status)
        """),
        {
            "amount": payload["amount"],
            "status": payload["status"],
        },
    )
    await db.commit()
    logger.info("Loan created successfully.")
    return {"message": "Loan created successfully"}
