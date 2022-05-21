import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.db.db import DB
from app.db.redis import Redis
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from app.exceptions import (CommonException, InternalServerError)
from app.routers.cart import cart_router
from app.routers.customer import customer_router
from app.routers.favourite import favourite_router
from app.routers.photo import photo_router
from app.routers.product import product_router
from app.routers.registr import registr_router
from app.routers.review import review_router
from app.routers.tag import tags_router
from starlette.middleware.cors import CORSMiddleware
import time
logger = logging.getLogger(__name__)

origins = ["*"]
app = FastAPI(title='Marketplace')


@app.on_event('startup')
async def startup() -> None:
    await DB.connect_db()
    await Redis.connect_redis()
    await Redis.load_tags()


@app.on_event('shutdown')
async def shutdown() -> None:
    await DB.disconnect_db()
    await Redis.disconnect_redis()

@app.middleware("http")
async def log_requst(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = (time.perf_counter() - start_time)
    formatted_process_time = '{0:.5f}'.format(process_time)
    logger.info(f"""***INFO*** Date time: {time.ctime()}  path={request.url.path} Method {request.method}
                Completed_in = {formatted_process_time}s""")
    return response


@app.exception_handler(StarletteHTTPException)
async def http_exception(request, exc):
    logger.error(f"***ERROR*** Status code {exc.status_code} Message: {exc.detail}")
    return JSONResponse(
        content={"detail": exc.detail},
        status_code=exc.status_code,
    )


@app.exception_handler(Exception)
async def common_exception_handler(request: Request, exception: Exception):
    error = InternalServerError(debug=str(exception))
    logger.error(f"***ERROR*** Status code {error.status_code} Message: {error.message}")
    return JSONResponse(
        status_code=error.status_code,
        content=error.to_json()
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    logger.error(f"***ERROR*** Status code 422 Message: {str(exc)}")
    return JSONResponse(
        status_code=422,
        content={'details': exc.errors()}
    )


@app.exception_handler(CommonException)
async def common_exception_handler(request: Request, exception: CommonException) -> JSONResponse:
    del request
    logger.error(exception.error)
    if isinstance(exception, InternalServerError):
        return JSONResponse(
            status_code=exception.code,
            content={'details': "Internal server error"},
        )
    return JSONResponse(
        status_code=exception.code,
        content={'details': exception.error},
    )


app.include_router(tags_router)
app.include_router(customer_router)
app.include_router(cart_router)
app.include_router(registr_router)
app.include_router(favourite_router)
app.include_router(photo_router)
app.include_router(product_router)
app.include_router(review_router)
app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
)
