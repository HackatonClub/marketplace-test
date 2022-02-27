from fastapi import APIRouter, status, HTTPException, Query
from fastapi.responses import JSONResponse

import app.queries.favourite as favourite
from app.model import Favourite
from app.utils.formatter import format_records

favourite_router = APIRouter(tags=["Favourite"])


@favourite_router.post('/customer/favourite')
async def add_favourite(temp: Favourite):
    if not await favourite.add_favourite(temp.customer_name, temp.product_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Нет такого покупателя и/или продукта, или продукт уже добавлен в избранное'
        )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed'
    })


@favourite_router.delete('/customer/favourite')
async def delete_favourite(temp: Favourite):
    if not await favourite.remove_favourite(temp.customer_name, temp.product_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Уже удален из избранного'
        )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed'
    })


@favourite_router.get('/customer/favourite')
async def get_customer_favourite(customer_name: str = Query(None, description='Имя покупателя'),
                                 previous_id: int = Query(0, title='Индекс последнего запроса', gt=0)):
    favourites = await favourite.get_favourites(customer_name, previous_id)
    favourites = format_records(favourites)
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'favourite': favourites
    })
