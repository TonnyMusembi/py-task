# workers/redis_subscriber.py
import redis.asyncio as redis

async def listen():
    client = redis.Redis(decode_responses=True)
    pubsub = client.pubsub()
    await pubsub.subscribe("loan.created")

    async for message in pubsub.listen():
        if message["type"] == "message":
            print("Received:", message["data"])
