import aio_pika
from app.config import settings

async def get_connection():
    return await aio_pika.connect_robust(settings.RABBIT_URL)
