from fastapi import APIRouter, HTTPException, Query, status
from fastapi.param_functions import Depends
from fastapi.responses import JSONResponse

import app.queries.cart as cart_queries
from app.auth.oauth2 import get_current_user
from app.model import Cart, CartDelete
from app.utils.extracter import get_previous_id
from app.utils.formatter import format_records

cart_router = APIRouter(tags=["Cart"])


@cart_router.post('/customer/cart')
async def add_product_to_cart(cart: Cart, current_user: str = Depends(get_current_user)) -> JSONResponse:
    await cart_queries.add_product_to_cart(current_user, cart.product_id, cart.product_num)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed',
    })


@cart_router.put('/customer/cart')
async def update_product_in_cart(cart: Cart, current_user: str = Depends(get_current_user)) -> JSONResponse:
    await cart_queries.update_product_in_cart(current_user, cart.product_id, cart.product_num)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed',
    })


@cart_router.delete('/customer/cart')
async def delete_cart_pr(cart: CartDelete, current_user: str = Depends(get_current_user)) -> JSONResponse:
    await cart_queries.delete_product_from_cart(current_user, cart.product_id)   
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'details': 'Executed',
    })


@cart_router.get('/customer/cart')
async def get_cart_products(previous_id: int = Query(0, title='Индекс последнего запроса', ge=0),
                            current_user: str = Depends(get_current_user)) -> JSONResponse:
    products = await cart_queries.get_cart_products(current_user, previous_id)
    previous_id = get_previous_id(products)
    products = format_records(products)
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'products': products,
        'previous_id': previous_id,
    })
