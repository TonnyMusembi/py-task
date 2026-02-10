from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from schemas.user import UserCreate
from core.security import hash_password
# from database import get_db
from src.database import get_db

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


async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        text("""
            SELECT id, full_name, email, role, created_at
            FROM users
        """)
    )

    users = result.fetchall()

    return {"users": [dict(row._mapping) for row in users]}
