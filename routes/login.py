from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from fastapi import HTTPException
from core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
)
from core.logger import logger
from jose import JWTError
from core.security import hash_password

from src.database import get_db
router = APIRouter(prefix="/login", tags=["Users"])

@router.post("/login")
async def login_user(email: str, password: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        text("""
            SELECT id, full_name, email, password, role
            FROM users
            WHERE email = :email
        """),
        {"email": email},
    )
    user = result.fetchone()

    # ✅ same error for both cases — prevents email enumeration
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token_data = {"sub": str(user.id), "role": user.role}

    access_token  = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    logger.info("User logged in | user_id=%s | email=%s", user.id, user.email)

    return {
        "access_token":  access_token,
        "refresh_token": refresh_token,
        "token_type":    "bearer",
        "user_id":       user.id,
        "role":          user.role,
        "full_name":     user.full_name,
    }

@router.post("/refresh")
async def refresh_access_token(refresh_token: str):
    try:
        payload = decode_refresh_token(refresh_token)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    # Issue a new access token from the refresh token's claims
    token_data   = {"sub": payload["sub"], "role": payload["role"]}
    access_token = create_access_token(token_data)

    logger.info("Access token refreshed | user_id=%s", payload["sub"])

    return {
        "access_token": access_token,
        "token_type":   "bearer",
    }

@router.post("/reset-password")
async def reset_password(email: str, new_password: str, db: AsyncSession = Depends(get_db)):
    # Check if user exists
    result = await db.execute(
        text("SELECT id FROM users WHERE email = :email"),
        {"email": email},
    )
    user = result.fetchone()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        await db.execute(
            text("""
                UPDATE users
                SET password = :password
                WHERE email = :email
            """),
            {
                "password": hash_password(new_password),
                "email": email,
            },
        )
        await db.commit()

        logger.info("Password reset successful | user_id=%s | email=%s", user.id, email)

        return {"message": "Password reset successful"}

    except Exception:
        await db.rollback()
        logger.exception("Failed to reset password | email=%s", email)
        raise HTTPException(status_code=500, detail="Internal server error")
