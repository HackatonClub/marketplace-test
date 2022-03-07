
import pathlib
import app.queries.product as product
import app.queries.tag as tag
from fastapi import APIRouter,  status, HTTPException, Query
from fastapi.responses import JSONResponse
from app.model import ProductAdd, ProductUp
from app.db.db import DB as db


product_router = APIRouter(tags=["Product"])


@product_router.post('/product')
async def add_product(prod: ProductAdd):
    await product.add_product(prod)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed'
    })


@product_router.delete('/product')
async def delete_product(product_id: int = Query(None, description='Id продукта')):

    await product.delete_product(product_id)

    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={
        'details': 'Executed'
    })


@product_router.put('/product/{product_id}')
async def update_product(produ: ProductUp):
    if not await product.update_product(produ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Такого продукта не существует'
        )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed'
    })
