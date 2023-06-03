from fastapi import APIRouter, Path, Query, status
from fastapi.param_functions import Depends
from fastapi.responses import JSONResponse

import app.queries.review as review_queries
from app.auth.oauth2 import get_current_user
from app.model import Product, Review
from app.utils.extracter import get_previous_id
from app.utils.formatter import format_records

review_router = APIRouter(tags=["Review"])


@review_router.post('/review')
async def add_review(review: Review, current_user: str = Depends(get_current_user)) -> JSONResponse:
    await review_queries.add_review_to_product(current_user, review.product_id, review.body, review.rating)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed',
    })


@review_router.put('/review')
async def update_rewie(review: Review, current_user: str = Depends(get_current_user)) -> JSONResponse:
    await review_queries.update_review_to_product(current_user, review.product_id, review.body, review.rating)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed',
    })


@review_router.delete('/review')
async def delete_review(product: Product, current_user: str = Depends(get_current_user)) -> JSONResponse:
    await review_queries.delete_review_from_product(current_user, product.product_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'details': 'Executed',
    })


@review_router.get('/product/{product_id}/reviews')
async def get_reviews(product_id: int = Path(..., title='ID продукта', gt=0),
                      previous_id: int = Query(0, title='Индекс последнего запроса', ge=0)) -> JSONResponse:
    reviews = await review_queries.get_reviews_to_product(product_id, previous_id)
    previous_id = get_previous_id(reviews)
    reviews = format_records(reviews)
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'reviews': reviews,
        'previous_id': previous_id,
    })
