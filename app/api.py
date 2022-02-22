import sys

from fastapi import FastAPI

from app.db.db import DB
from app.routers.cart import cart_router
from app.routers.customer import customer_router
from app.routers.favourite import favourite_router
from app.routers.photo import photo_router
<<<<<<< HEAD
from app.routers.product import product_router
from app.db.db import DB
=======
from app.routers.registr import registr_router
from app.routers.review import review_router
from app.routers.tag import tags_router
>>>>>>> e503a361e171617a87de016e1e19d7c0f070356d

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
<<<<<<< HEAD
app.include_router(product_router)
=======
app.include_router(review_router)
>>>>>>> e503a361e171617a87de016e1e19d7c0f070356d
