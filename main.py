from fastapi import FastAPI
from routers import redis_router
from logging_config import setup_logging
from middlewares.logging import log_requests
import logging
from fastapi import Request
from middlewares.metrics import metrics_middleware

from fastapi import Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from config import APP_NAME

logger = logging.getLogger("errors")

setup_logging()

app = FastAPI(title="Multi-Service API", version="1.0.0", docs_url=None, redoc_url=None, openapi_url="/openapi.json")
app.mount(f"/{APP_NAME}/static", StaticFiles(directory="static"), name="static")

app.middleware("http")(log_requests)
app.middleware("http")(metrics_middleware)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error: %s %s", request.method, request.url.path)
    raise exc

@app.get(f"/{APP_NAME}/metrics")
def metrics():
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )

@app.get(f"/{APP_NAME}/docs", include_in_schema=False)
def custom_swagger_ui():
    return HTMLResponse("""
<!DOCTYPE html>
<html>
<head>
  <title>Swagger UI</title>
  <link rel="stylesheet" type="text/css" href="/service-check/static/swagger/swagger-ui.css" />
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="/service-check/static/swagger/swagger-ui-bundle.js"></script>
  <script src="/service-check/static/swagger/swagger-ui-standalone-preset.js"></script>
  <script>
    window.onload = () => {
      SwaggerUIBundle({
        url: "/openapi.json",
        dom_id: "#swagger-ui",
        presets: [
          SwaggerUIBundle.presets.apis,
          SwaggerUIStandalonePreset
        ],
        layout: "StandaloneLayout"
      });
    };
  </script>
</body>
</html>
""")


app.include_router(redis_router.router)
#app.include_router(rabbitmq_router.router)
#app.include_router(mongodb_router.router)
#app.include_router(kafka_router.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)