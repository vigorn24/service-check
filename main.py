from fastapi import FastAPI
from routers import redis_router
from logging_config import setup_logging
from middlewares.logging import log_requests


import logging
from fastapi import Request

logger = logging.getLogger("errors")

setup_logging()

app = FastAPI(title="Multi-Service API", version="1.0.0")
app.middleware("http")(log_requests)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error: %s %s", request.method, request.url.path)
    raise exc

app.include_router(redis_router.router)
#app.include_router(rabbitmq_router.router)
#app.include_router(mongodb_router.router)
#app.include_router(kafka_router.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)