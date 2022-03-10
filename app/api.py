import sys

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.db.db import DB
from app.exceptions import NotFoundException, ServerException
from app.routers.cart import cart_router
from app.routers.customer import customer_router
from app.routers.favourite import favourite_router
from app.routers.photo import photo_router
from app.routers.product import product_router
from app.routers.registr import registr_router
from app.routers.review import review_router
from app.routers.tag import tags_router

app = FastAPI(title='Marketplace')


@app.on_event('startup')
async def startup():
    if not await DB.connect_db():
        sys.exit(0)


@app.on_event('shutdown')
async def shutdown():
    await DB.disconnect_db()


@app.exception_handler(NotFoundException)
async def not_found_error_handler(request: Request, exception: NotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={'details': exception.error},
    )


@app.exception_handler(ServerException)
async def server_error_handler(request: Request, exception: ServerException):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
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
