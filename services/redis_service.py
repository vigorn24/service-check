from redis.asyncio.cluster import RedisCluster
from config import config

redis_client = RedisCluster.from_url(
    config.REDIS_URL,
    decode_responses=True
)

async def write_to_redis(key: str, value: str):
    await redis_client.set(key, value)
    return {"status": "written"}

async def read_from_redis(key: str):
    value = await redis_client.get(key)
    return {"value": value.decode() if value else None}