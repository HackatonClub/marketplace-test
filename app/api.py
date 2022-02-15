import sys

from fastapi import FastAPI
from app.tags.api import tags_router
from app.customer.api import customer_router
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
