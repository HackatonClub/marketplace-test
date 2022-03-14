import app.queries.favourite as favourite_queries
from app.model import Favourite
from app.utils.extracter import get_previous_id
from app.utils.formatter import format_records

from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse


favourite_router = APIRouter(tags=["Favourite"])


@favourite_router.post('/customer/favourite')
async def add_favourite(favourite: Favourite):
    await favourite_queries.add_favourite(favourite.customer_name, favourite.product_id)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed',
    })


@favourite_router.delete('/customer/favourite')
async def delete_favourite(favourite: Favourite):
    await favourite_queries.remove_favourite(favourite.customer_name, favourite.product_id)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed',
    })


@favourite_router.get('/customer/favourite')
async def get_customer_favourite(customer_name: str = Query(None, description='Имя покупателя'),
                                 previous_id: int = Query(0, title='Индекс последнего запроса', ge=0)):
    favourites = await favourite_queries.get_favourites(customer_name, previous_id)
    previous_id = get_previous_id(favourites)
    favourites = format_records(favourites)
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'favourite': favourites,
        'previous_id': previous_id,
    })
