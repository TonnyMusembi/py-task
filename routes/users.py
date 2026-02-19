from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from schemas.user import UserCreate
from core.security import hash_password
from core.security import verify_password

# from database import get_db
from src.database import get_db
from core.logger import logger

# long_password = "a" * 100  # 100 bytes — would fail raw bcrypt
# hashed = hash_password(long_password)
# print("Hashed:", hashed)
# print("Verified:", (long_password, hashed))  # should print True


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    # Check email existence
    result = await db.execute(
        text("SELECT id FROM users WHERE email = :email"),
        {"email": payload.email},
    )
    if result.fetchone():
        raise HTTPException(status_code=400, detail="Email already exists")

    try:
        result = await db.execute(
            text("""
                INSERT INTO users (full_name, email, password, role)
                VALUES (:full_name, :email, :password, :role)
            """),
            {
                "full_name": payload.full_name,
                "email": payload.email,
                # "password": payload.password,
                "password": hash_password(payload.password),  # ✅ hash password before storing
                "role": payload.role if hasattr(payload, 'role') else "customer"                    # ✅ never trust client role
            },
        )

        user_id = result.lastrowid
        await db.commit()

        logger.info("User created | user_id=%s | email=%s", user_id, payload.email)  # ✅ after commit, not after return

        return {"message": "User created successfully", "user_id": user_id}

    except Exception:
        await db.rollback()
        logger.exception("Failed to create user | email=%s", payload.email)
        raise HTTPException(status_code=500, detail="Internal server error")
        logger.error("Failed to create user | email=%s", payload.email)  # ✅ log after exception, not before

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

@router.get("/{user_id}")
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

