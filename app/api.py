import sys

from fastapi import FastAPI
from app.routers.tag import tags_router
from app.routers.registr import registr_router
from app.routers.customer import customer_router
from app.routers.cart import cart_router
from app.routers.favourite import favourite_router
from app.routers.photo import photo_router
from app.db.db import DB

app = FastAPI(
    title='Marketplace'
)


@app.on_event('startup')
async def startup():
    if not await DB.connect_db():
        sys.exit(0)


@app.on_event('shutdown')
async def shutdown():
    await DB.disconnect_db()


app.include_router(tags_router)
app.include_router(customer_router)
app.include_router(cart_router)
app.include_router(registr_router)
app.include_router(favourite_router)
app.include_router(photo_router)
