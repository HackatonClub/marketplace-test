from fastapi import APIRouter, Query, status
from fastapi.param_functions import Depends
from fastapi.responses import JSONResponse

import app.queries.favourite as favourite_queries
from app.auth.oauth2 import get_current_user
from app.model import Favourite
from app.utils.extracter import get_previous_id
from app.utils.formatter import format_records

favourite_router = APIRouter(tags=["Favourite"])


@favourite_router.post('/customer/favourite')
async def add_favourite(favourite: Favourite, current_user: str = Depends(get_current_user)) -> JSONResponse:
    await favourite_queries.add_favourite(current_user, favourite.product_id)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed',
    })


@favourite_router.delete('/customer/favourite')
async def delete_favourite(favourite: Favourite, current_user: str = Depends(get_current_user)) -> JSONResponse:
    await favourite_queries.remove_favourite(current_user, favourite.product_id)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed',
    })


@favourite_router.get('/customer/favourite')
async def get_customer_favourite(previous_id: int = Query(0, title='Индекс последнего запроса', ge=0),
                                 current_user: str = Depends(get_current_user)) -> JSONResponse:
    favourites = await favourite_queries.get_favourites(current_user, previous_id)
    previous_id = get_previous_id(favourites)
    favourites = format_records(favourites)
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'favourite': favourites,
        'previous_id': previous_id,
    })
