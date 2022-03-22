import logging

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.db.db import DB
from app.db.redis import Redis
from app.exceptions import BadRequest, CustomerNotFoundException, InternalServerError, NotFoundException
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
async def startup():
    await DB.connect_db()
    await Redis.connect_redis()
    await Redis.load_tags()


@app.on_event('shutdown')
async def shutdown():
    await DB.disconnect_db()
    await Redis.disconnect_redis()

@app.exception_handler(NotFoundException)
async def not_found_error_handler(request: Request, exception: NotFoundException):
    del request
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={'details': exception.error},
    )


@app.exception_handler(CustomerNotFoundException)
async def customer_not_found_error_handler(request: Request, exception: CustomerNotFoundException):
    del request
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={'details': exception.error},
    )


@app.exception_handler(InternalServerError)
async def internal_server_error_handler(request: Request, exception: InternalServerError):
    del request
    logger.error(exception)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={'details': 'Internal server error'},
    )


@app.exception_handler(BadRequest)
async def bad_request_handler(request: Request, exception: BadRequest):
    del request
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
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
