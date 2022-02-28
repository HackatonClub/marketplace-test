from fastapi import APIRouter, status, HTTPException, Query
from fastapi.responses import JSONResponse

import app.queries.customer as customer_queries
from app.model import Customer, CutomerNew
from app.utils.extracter import get_previous_id
from app.utils.formatter import format_records

customer_router = APIRouter(tags=["Customer"])


@customer_router.post('/customer')
async def add_customer(customer: CutomerNew):
    if not await customer_queries.add_customer(customer.name, customer.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Покупатель с таким именем существует'
        )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed'
    })


@customer_router.get('/customer')
async def get_customers(previous_id: int = Query(0, title='Индекс последнего запроса', ge=0)):
    customers = await customer_queries.get_all_customers(previous_id)
    previous_id = get_previous_id(customers)
    customers = format_records(customers)
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'customers': customers,
        'previous_id': previous_id
    })


@customer_router.delete('/customer')
async def delete_customer(customer: Customer):
    if not await customer_queries.delete_customer(customer.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Покупатель уже удален'
        )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed'
    })
