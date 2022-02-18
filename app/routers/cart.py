from typing import Optional
from fastapi import APIRouter, status, HTTPException, Header
from fastapi.responses import JSONResponse

from app.utils.formatter import format_records

import app.queries.cart as cart

cart_router = APIRouter()


# TODO: заменить хедеры на паф т.к. не принимают юникод
# TODO: добавить проверку gt в product_num

@cart_router.post('/customer/cart')
async def add_product_to_cart(product_id: Optional[int] = Header(None, description='Id продукта'),
                              name: Optional[str] = Header(None, description='Имя покупателя'),
                              product_num: Optional[int] = Header(None, description='Кол-во продуктов')):
    if not await cart.add_product_to_cart(name, product_id, product_num):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Нет такого покупателя или продукт уже добавлен в корзину'
        )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed'
    })


@cart_router.put('/customer/cart')
async def update_product_in_cart(product_id: Optional[int] = Header(None, description='Id продукта'),
                                 name: Optional[str] = Header(None, description='Имя покупателя'),
                                 product_num: Optional[int] = Header(None, description='Кол-во продуктов')):
    if not await cart.update_product_in_cart(name, product_id, product_num):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Такого продукта не существует'
        )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed'
    })


@cart_router.delete('/customer/cart')
async def delete_favourite(product_id: Optional[int] = Header(None, description='Id продукта'),
                           name: Optional[str] = Header(None, description='Имя покупателя')):
    if not await cart.delete_product_from_cart(name, product_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Уже удален из корзины'
        )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed'
    })


@cart_router.get('/customer/cart')
async def get_customers(name: Optional[str] = Header(None, description='Имя покупателя')):
    products = await cart.get_cart_products(name)
    products = format_records(products)
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'customers': products
    })
