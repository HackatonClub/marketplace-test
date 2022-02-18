from typing import Optional
from fastapi import APIRouter, status, HTTPException, Header
from fastapi.responses import JSONResponse

from app.formatter import format_records

from app.db.db import DB

customer_router = APIRouter()


# TODO: заменить хедеры на паф т.к. не принимают юникод

@customer_router.post('/customer')
async def add_customer(name: Optional[str] = Header(None, description='Имя покупателя'),
                       password: Optional[str] = Header(None, description='Пароль покупателя')):
    if not await DB.add_customer(name, password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Покупатель с таким именем существует'
        )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed'
    })


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


@customer_router.get('/customer')
async def get_customers():
    customers = await DB.get_all_customers()
    customers = format_records(customers)
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'customers': customers
    })


@customer_router.get('/customer/favourite')
async def get_customer_favourite(name: Optional[str] = Header(None, description='Имя покупателя')):
    favourites = await DB.get_favourites(name)
    favourites = format_records(favourites)
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'favourite': favourites
    })


@customer_router.delete('/customer')
async def delete_customer(name: Optional[str] = Header(None, description='Имя покупателя')):
    if not await DB.delete_customer(name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Покупатель уже удален'
        )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed'
    })
