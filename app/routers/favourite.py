from typing import Optional
from fastapi import APIRouter, status, HTTPException, Header
from fastapi.responses import JSONResponse

from app.utils.formatter import format_records

import app.queries.favourite as favourite

favourite_router = APIRouter(tags=["Favourite"])


@favourite_router.post('/customer/favourite')
async def add_favourite(product_id: Optional[int] = Header(None, description='Id продукта'),
                        name: Optional[str] = Header(None, description='Имя покупателя')):
    if not await favourite.add_favourite(name, product_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Нет такого покупателя или продукт уже добавлен в избранное'
        )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed'
    })


@favourite_router.delete('/customer/favourite')
async def delete_favourite(product_id: Optional[int] = Header(None, description='Id продукта'),
                           name: Optional[str] = Header(None, description='Имя покупателя')):
    if not await favourite.remove_favourite(name, product_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Уже удален из избранного'
        )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed'
    })


@favourite_router.get('/customer/favourite')
async def get_customer_favourite(name: Optional[str] = Header(None, description='Имя покупателя')):
    favourites = await favourite.get_favourites(name)
    favourites = format_records(favourites)
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'favourite': favourites
    })
