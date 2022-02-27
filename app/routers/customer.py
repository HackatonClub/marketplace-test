from fastapi import APIRouter, status, HTTPException, Query
from fastapi.responses import JSONResponse

import app.queries.customer as customer
from app.model import Customer, CutomerNew
from app.utils.formatter import format_records

customer_router = APIRouter(tags=["Customer"])


# TODO: заменить хедеры на паф т.к. не принимают юникод

@customer_router.post('/customer')
async def add_customer(temp: CutomerNew):
    if not await customer.add_customer(temp.name, temp.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Покупатель с таким именем существует'
        )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed'
    })


@customer_router.get('/customer')
async def get_customers(previous_id: int = Query(0, title='Индекс последнего запроса', gt=0)):
    customers = await customer.get_all_customers(previous_id)
    customers = format_records(customers)
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'customers': customers
    })


@customer_router.delete('/customer')
async def delete_customer(temp: Customer):
    if not await customer.delete_customer(temp.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Покупатель уже удален'
        )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed'
    })
