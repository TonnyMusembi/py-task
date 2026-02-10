import os
from urllib.parse import quote_plus
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import logging
logging.basicConfig(level=logging.INFO)

load_dotenv()
logging.info("Environment variables loaded successfully.")

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

logging.info(f"DB_USER: {DB_USER}, DB_HOST: {DB_HOST}, DB_PORT: {DB_PORT}, DB_NAME: {DB_NAME}")

if None in [DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]:
    raise ValueError("One or more DB environment variables are not set")

DB_PASSWORD = quote_plus(DB_PASSWORD)
logging.info("Database password URL-encoded successfully.")


DATABASE_URL = f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(DATABASE_URL, echo=True, pool_size=10, max_overflow=20)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
