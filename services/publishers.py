from fastapi.encoders import jsonable_encoder
import json
from core.redis import redis_client

async def publish_redis(channel: str, payload: dict):
    encoded = jsonable_encoder(payload)
    message = json.dumps(encoded)
    await redis_client.publish(channel, message)
