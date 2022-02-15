from typing import Optional
from fastapi import APIRouter, status, HTTPException, Header
from fastapi.responses import JSONResponse

from app.db.db import DB

tags_router = APIRouter()

@tags_router.post('/tag')
async def add_tag(tag_name : Optional[str] = Header(None,description='Имя тега')):
    if not await DB.add_new_tag(tag_name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Тэг уже существует'
        )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed'
    })

@tags_router.post('/product/tag')
async def product_add_tag(product_id: Optional[int] = Header(None,description='Id продукта'),
                          tag_name: Optional[str] = Header(None,description='Имя тэга')):
    if not await DB.add_tag_to_product_by_id( tag_name,product_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Тэг уже присвоен'
        )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed'
    })

@tags_router.post('/customer')
async def add_customer(name : Optional[str] = Header(None,description='Имя покупателя')):
    if not await DB.add_customer(name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Покупатель с таким именем существует'
        )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed'
    })

@tags_router.delete('/product/tag')
async def remove_tag_from_product(product_id: Optional[int] = Header(None,description='Id продукта'),
                          tag_name: Optional[str] = Header(None,description='Имя тэга')):
    if not await DB.remove_tag_from_product_by_id( tag_name,product_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Тэг уже удален'
        )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed'
    })

@tags_router.delete('/favourite')
async def delete_favourite(product_id: Optional[int] = Header(None,description='Id продукта'),
                          tag_name: Optional[str] = Header(None,description='Имя покупателя')):
    if not await DB.remove_favourite( tag_name,product_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Уже удален из избранного'
        )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed'
    })

@tags_router.delete('/customer')
async def delete_customer(name: Optional[str] = Header(None,description='Имя покупателя')):
    pass

@tags_router.get('/tag')
async def get_all_tags():
    tags = await DB.get_all_tags()
    if not tags:
        tags = []
    return JSONResponse(status_code=status.HTTP_200_OK,content={
        'tags':tags
    })

@tags_router.get('/product/tag')
async def get_tags_of_product(product_id: Optional[int] = Header(None,description='Id продукта')):
    tags = await DB.get_tags_of_product_by_id(product_id)
    if not tags:
        tags = []
    return JSONResponse(status_code=status.HTTP_200_OK,content={
        'tags':tags
    })
@tags_router.get('/customer')
async def get_customers():
    pass