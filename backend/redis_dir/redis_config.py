import os

from dotenv import load_dotenv
from redis.asyncio import Redis

load_dotenv()

redis_client: Redis | None = None

async def init_redis():
    global redis_client
    redis_client = Redis.from_url(url = os.getenv("REDIS_URL"),
        decode_responses=True)

async def close_redis():
    if redis_client:
        await redis_client.close()