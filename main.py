from fastapi import FastAPI, Request
from core.logger import logger
import time
import json
from api.routers import storage, test, buildsite, users, ocr

app = FastAPI()

#app.include_router(test.router)
app.include_router(users.router)
app.include_router(buildsite.router)
app.include_router(storage.router)
app.include_router(ocr.router)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    body = await request.body()
    try:
        body_data = json.loads(body.decode("utf-8")) if body else None
    except Exception:
        body_data = None

    logger.info(f"📥 {request.method} {request.url.path} | body={body_data}")
    logger.debug(f"📥 {request.headers} | body={body_data}")

    try:
        response = await call_next(request)
    except Exception as ex:
        logger.error(ex)
        raise ex
    finally:
        process_time = (time.time() - start_time) * 1000

    logger.info(f"📤 status={response.status_code} | time={process_time:.2f}ms")

    return response