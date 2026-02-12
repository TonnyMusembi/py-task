from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError


from src.database import get_db
from core.logger import logger


router = APIRouter(prefix="/customers", tags=["Customers"])


@router.get("/")
async def get_customers(db: AsyncSession = Depends(get_db)):
	result = await db.execute(text(""" SELECT id, full_name, email, created_at FROM customers """))
	customers = result.fetchall()
	logger.info("Fetched customers successfully.")
	return {"customers": [dict(row._mapping) for row in customers]}


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_customer(
    full_name: str,
    email: str,
    phone_number: str,
    db: AsyncSession = Depends(get_db),
):
    try:
        await db.execute(
            text("""
                INSERT INTO customers (full_name, email, phone_number)
                VALUES (:full_name, :email, :phone_number)
            """),
            {
                "full_name": full_name,
                "email": email,
                "phone_number": phone_number,
            },
        )

        await db.commit()

        logger.info(f"Customer {email} created successfully.")

        return {"message": "Customer created successfully"}

    except IntegrityError as e:
        await db.rollback()

        logger.warning(f"Duplicate entry attempt for {email}: {str(e)}")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or phone number already exists",
        )

    except Exception as e:
        await db.rollback()

        logger.error(f"Failed to create customer {email}: {str(e)}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create customer",
        )
