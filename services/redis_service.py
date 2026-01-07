from redis.asyncio.cluster import RedisCluster
from config import config
import logging
from utils.logging_decorators import log_call

logger = logging.getLogger(__name__)

redis_client = RedisCluster.from_url(
    config.REDIS_URL,
    decode_responses=True
)

@log_call("redis")
async def write_to_redis(key: str, value: str):
    await redis_client.set(key, value)
    return {"status": "written"}

@log_call("redis")
async def read_from_redis(key: str):
    value = await redis_client.get(key)
    return {"value": value if value else None}