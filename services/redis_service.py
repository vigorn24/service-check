from redis.asyncio.cluster import RedisCluster
from config import settings
import logging
from utils.logging_decorators import log_call
from metrics import SERVICE_CALLS
from utils.metrics_decorator import service_metric
from redis.exceptions import (RedisError, ConnectionError as RedisConnectionError, TimeoutError as RedisTimeoutError)
from fastapi import HTTPException
import asyncio

logger = logging.getLogger(__name__)

redis_client = RedisCluster.from_url(
    settings.redis.url,
    username=settings.redis.user,
    password=settings.redis.password,
    decode_responses=True
)

@service_metric("redis")
@log_call("redis")
async def write_to_redis(key: str, value: str, expire_time: int = 3600): # Default expire_time to 1 hour

#    SERVICE_CALLS.labels(
#        service="redis",
#        function="write"
#    ).inc()
    for attempt in range(3):
        try:
            await redis_client.set(key, value, ex=expire_time)
            return {"status": "written"}
        except (RedisConnectionError, RedisTimeoutError):
            logger.warning("Redis connection issue, attempt %s", attempt + 1, exc_info=True)
            await asyncio.sleep(0.1)

        except RedisError:
            logger.exception("Redis error (non-retriable)")
            break

    raise HTTPException(status_code=503, detail="Redis service unavailable")

@service_metric("redis")
@log_call("redis")
async def read_from_redis(key: str):

#    SERVICE_CALLS.labels(
#        service="redis",
#        function="read"
#    ).inc()

    value = await redis_client.get(key)
    return {"value": value if value else None}