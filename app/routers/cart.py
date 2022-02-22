from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse

import app.queries.cart as cart
from app.model import Cart, CartDelete, Customer
from app.utils.formatter import format_records

cart_router = APIRouter(tags=["Cart"])


# TODO: заменить хедеры на паф т.к. не принимают юникод
# TODO: добавить проверку gt в product_num

@cart_router.post('/customer/cart')
async def add_product_to_cart(temp: Cart):
    if not await cart.add_product_to_cart(temp.customer_name, temp.product_id, temp.product_num):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Нет такого покупателя или продукт уже добавлен в корзину'
        )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed'
    })


@cart_router.put('/customer/cart')
async def update_product_in_cart(temp: Cart):
    if not await cart.update_product_in_cart(temp.customer_name, temp.product_id, temp.product_num):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Такого продукта не существует'
        )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed'
    })


@cart_router.delete('/customer/cart')
async def delete_favourite(temp: CartDelete):
    if not await cart.delete_product_from_cart(temp.customer_name, temp.product_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Уже удален из корзины'
        )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed'
    })


@cart_router.get('/customer/cart')
async def get_customers(temp: Customer):
    products = await cart.get_cart_products(temp.name)
    products = format_records(products)
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'products': products
    })
