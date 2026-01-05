from fastapi import APIRouter, Depends
from models import DataModel
from services.redis_service import write_to_redis, read_from_redis

router = APIRouter(prefix="/redis", tags=["Redis"])

@router.post("/write")
async def redis_write(data: DataModel):
    return await write_to_redis(data.key, data.value)

@router.get("/read/{key}")
async def redis_read(key: str):
    return await read_from_redis(key)