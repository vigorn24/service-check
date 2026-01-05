from fastapi import FastAPI
from routers import redis_router

app = FastAPI(title="Multi-Service API", version="1.0.0")

app.include_router(redis_router.router)
#app.include_router(rabbitmq_router.router)
#app.include_router(mongodb_router.router)
#app.include_router(kafka_router.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)