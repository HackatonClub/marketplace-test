from typing import Optional
from fastapi import APIRouter, status, HTTPException, Header
from fastapi.responses import JSONResponse

from app.utils.formatter import format_records

import app.queries.customer as customer

customer_router = APIRouter(tags=["Customer"])


# TODO: заменить хедеры на паф т.к. не принимают юникод

@customer_router.post('/customer')
async def add_customer(name: Optional[str] = Header(None, description='Имя покупателя'),
                       password: Optional[str] = Header(None, description='Пароль покупателя')):
    if not await customer.add_customer(name, password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Покупатель с таким именем существует'
        )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed'
    })


@customer_router.get('/customer')
async def get_customers():
    customers = await customer.get_all_customers()
    customers = format_records(customers)
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'customers': customers
    })


@customer_router.delete('/customer')
async def delete_customer(name: Optional[str] = Header(None, description='Имя покупателя')):
    if not await customer.delete_customer(name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Покупатель уже удален'
        )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed'
    })
