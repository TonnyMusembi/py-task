from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
# from models  import Contact
from model.contacts import Contact

router = APIRouter()

class ContactRequest(BaseModel):
    name:    str
    email:   EmailStr   # validates email format automatically
    message: str

@router.post("/api/contact", status_code=201)
async def send_contact(data: ContactRequest, db: AsyncSession = Depends(get_db)):
    try:
        contact = Contact(
            name=data.name,
            email=data.email,
            message=data.message
        )
        db.add(contact)
        await db.commit()
        await db.refresh(contact)

        return {"message": "Message received", "id": contact.id}

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to save contact")
