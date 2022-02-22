
import pathlib
import app.queries.product as product
import app.queries.tag as tag
from fastapi import APIRouter,  status, HTTPException,Query
from fastapi.responses import JSONResponse
from app.model import ProductAdd
from app.db.db import DB as db
from app.routers.photo import delete_product_photo, get_product_photo_all_filename


product_router = APIRouter(tags=["Product"])


@product_router.post('/product')
async def add_product(prod: ProductAdd):
    await product.add_product(prod)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed'
    })


@product_router.delete('/product')
async def delete_product(product_id: int = Query(None, description='Id продукта')):
    # удаление product_photo
    
    

    
    return " ;lytv"





