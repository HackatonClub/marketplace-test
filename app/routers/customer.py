from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse

import app.queries.customer as customer_queries

from app.utils.extracter import get_previous_id
from app.utils.formatter import format_records

from app.model import User
from fastapi.param_functions import Depends
from app.auth.oauth2 import get_current_user

customer_router = APIRouter(tags=["Customer"])


@customer_router.get('/customer')
async def get_customers(previous_id: int = Query(0, title='Индекс последнего запроса', ge=0)) -> JSONResponse:
    customers = await customer_queries.get_all_customers(previous_id)
    previous_id = get_previous_id(customers)
    customers = format_records(customers)
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'customers': customers,
        'previous_id': previous_id,
    })


@customer_router.delete('/customer')
async def delete_customer(current_user: str = Depends(get_current_user)) -> JSONResponse:
    await customer_queries.delete_customer(current_user)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed',
    })
