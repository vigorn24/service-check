from redis.asyncio.cluster import RedisCluster
from config import config
import logging
from utils.logging_decorators import log_call
from metrics import SERVICE_CALLS
from utils.metrics_decorator import service_metric


logger = logging.getLogger(__name__)

redis_client = RedisCluster.from_url(
    config.REDIS_URL,
    decode_responses=True
)

@service_metric("redis")
@log_call("redis")
async def write_to_redis(key: str, value: str):

    SERVICE_CALLS.labels(
        service="redis",
        function="write"
    ).inc()

    await redis_client.set(key, value)
    return {"status": "written"}

@service_metric("redis")
@log_call("redis")
async def read_from_redis(key: str):

    SERVICE_CALLS.labels(
        service="redis",
        function="read"
    ).inc()

    value = await redis_client.get(key)
    return {"value": value if value else None}