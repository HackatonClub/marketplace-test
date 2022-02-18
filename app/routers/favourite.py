from typing import Optional
from fastapi import APIRouter, status, HTTPException, Header
from fastapi.responses import JSONResponse

from app.utils.formatter import format_records

from app.db.db import DB

favourite_router = APIRouter(tags=["Favourite"])


@customer_router.post('/customer/favourite')
async def add_favourite(product_id: Optional[int] = Header(None, description='Id продукта'),
                        name: Optional[str] = Header(None, description='Имя покупателя')):
    if not await DB.add_favourite(name, product_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Нет такого покупателя или продукт уже добавлен в избранное'
        )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed'
    })


@customer_router.delete('/customer/favourite')
async def delete_favourite(product_id: Optional[int] = Header(None, description='Id продукта'),
                           name: Optional[str] = Header(None, description='Имя покупателя')):
    if not await DB.remove_favourite(name, product_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Уже удален из избранного'
        )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed'
    })


@customer_router.get('/customer/favourite')
async def get_customer_favourite(name: Optional[str] = Header(None, description='Имя покупателя')):
    favourites = await DB.get_favourites(name)
    favourites = format_records(favourites)
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'favourite': favourites
    })
