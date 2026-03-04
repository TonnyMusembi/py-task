from datetime import datetime
from sqlalchemy import Integer, String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from src.database import get_db

class Contact():
    __tablename__ = "contacts"

    id:         Mapped[int]      = mapped_column(Integer, primary_key=True, autoincrement=True)
    name:       Mapped[str]      = mapped_column(String(100), nullable=False)
    email:      Mapped[str]      = mapped_column(String(255), nullable=False)
    message:    Mapped[str]      = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
