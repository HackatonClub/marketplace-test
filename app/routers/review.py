from fastapi import APIRouter, status, HTTPException, Path, Query
from fastapi.responses import JSONResponse

import app.queries.review as review
from app.model import Product, Review, Customer
from app.utils.extracter import get_previous_id
from app.utils.formatter import format_records

review_router = APIRouter(tags=["Review"])


# TODO: поменять status_code'ы

@review_router.post('/review')
async def add_product_to_cart(temp: Review):
    if not await review.add_review_to_product(temp.customer_name, temp.product_id, temp.body, temp.rating):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Нет такого покупателя и/или продукта'
        )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed'
    })


@review_router.put('/review')
async def update_product_in_cart(temp: Review):
    if not await review.update_review_to_product(temp.customer_name, temp.product_id, temp.body, temp.rating):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Нет такого покупателя и/или продукта'
        )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed'
    })


@review_router.delete('/review')
async def delete_favourite(temp_product: Product, temp_customer: Customer):
    if not await review.delete_review_from_product(temp_customer.name, temp_product.product_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Отзыв уже удалён'
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'details': 'Executed'
    })


@review_router.get('/product/{product_id}/reviews')
async def get_reviews(product_id: int = Path(..., title='ID продукта', gt=0),
                      previous_id: int = Query(0, title='Индекс последнего запроса', ge=0)):
    reviews = await review.get_reviews_to_product(product_id, previous_id)
    previous_id = get_previous_id(reviews)
    reviews = format_records(reviews)
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'reviews': reviews,
        'previous_id': previous_id
    })
