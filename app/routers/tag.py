from typing import Optional
from fastapi import APIRouter, status, HTTPException, Header
from fastapi.responses import JSONResponse

from app.utils.formatter import format_records

import app.queries.tag as tag

tags_router = APIRouter(tags=["Tags"])


# TODO: заменить хедеры на паф т.к. не принимают юникод

@tags_router.post('/tag')
async def add_tag(tag_name: Optional[str] = Header(None, description='Имя тега')):
    if not await tag.add_new_tag(tag_name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Тэг уже существует'
        )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed'
    })


@tags_router.post('/product/tag')
async def product_add_tag(product_id: Optional[int] = Header(None, description='Id продукта'),
                          tag_name: Optional[str] = Header(None, description='Имя тэга')):
    if not await tag.add_tag_to_product_by_id(tag_name, product_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Нет заданного продукта или тэг уже присвоен'
        )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed'
    })


@tags_router.delete('/tag')
async def delete_tag(tag_name: Optional[str] = Header(None, description='Имя тэга')):
    if not await tag.remove_tag(tag_name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Тэг уже удален'
        )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed'
    })


@tags_router.delete('/product/tag')
async def remove_tag_from_product(product_id: Optional[int] = Header(None, description='Id продукта'),
                                  tag_name: Optional[str] = Header(None, description='Имя тэга')):
    if not await tag.remove_tag_from_product_by_id(tag_name, product_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Тэг уже удален'
        )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed'
    })


@tags_router.get('/tag')
async def get_all_tags():
    tags = await tag.get_all_tags()
    tags = format_records(tags)
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'tags': tags
    })


@tags_router.get('/product/tag')
async def get_tags_of_product(product_id: Optional[int] = Header(None, description='Id продукта')):
    tags = await tag.get_tags_of_product_by_id(product_id)
    tags = format_records(tags)
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'tags': tags
    })
