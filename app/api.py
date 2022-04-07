import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.db.db import DB
from app.db.redis import Redis
from app.exceptions import (CommonException,InternalServerError)
from app.routers.cart import cart_router
from app.routers.customer import customer_router
from app.routers.favourite import favourite_router
from app.routers.photo import photo_router
from app.routers.product import product_router
from app.routers.registr import registr_router
from app.routers.review import review_router
from app.routers.tag import tags_router


logger = logging.getLogger(__name__)


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
