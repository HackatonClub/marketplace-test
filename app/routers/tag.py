from typing import List

from fastapi import APIRouter, status, HTTPException, Path, Query
from fastapi.responses import JSONResponse

import app.queries.tag as tag
from app.model import Tag
from app.utils.extracter import get_previous_id
from app.utils.formatter import format_records

tags_router = APIRouter(tags=["Tags"])


# TODO: можно создавать пустой тэг, не знаю это баг или фича

@tags_router.post('/tag')
async def add_tag(temp: Tag):
    if not await tag.add_new_tag(temp.tag_name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Тэг уже существует'
        )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed'
    })


@tags_router.post('/product/{product_id}/tag')
async def product_add_tag(temp_tag: Tag, product_id: int = Path(..., title='ID продукта', gt=0)):
    if not await tag.add_tag_to_product_by_id(temp_tag.tag_name, product_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Нет заданного продукта или тэг уже присвоен'
        )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed'
    })


@tags_router.delete('/tag')
async def delete_tag(temp: Tag):
    if not await tag.remove_tag(temp.tag_name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Тэг уже удален'
        )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed'
    })


@tags_router.delete('/product/{product_id}/tag')
async def remove_tag_from_product(temp_tag: Tag, product_id: int = Path(..., title='ID продукта', gt=0)):
    if not await tag.remove_tag_from_product_by_id(temp_tag.tag_name, product_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Тэг уже удален'
        )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed'
    })


@tags_router.get('/tag')
async def get_all_tags(previous_id: int = Query(0, title='Индекс последнего запроса', ge=0)):
    tags = await tag.get_all_tags(previous_id)
    previous_id = get_previous_id(tags)
    tags = format_records(tags)
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'tags': tags,
        'previous_id': previous_id
    })


@tags_router.get('/product/{product_id}/tag')
async def get_tags_of_product(product_id: int = Path(..., title='ID продукта', gt=0),
                              previous_id: int = Query(0, title='Индекс последнего запроса', ge=0)):
    tags = await tag.get_tags_of_product_by_id(product_id, previous_id)
    previous_id = get_previous_id(tags)
    tags = format_records(tags)
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'tags': tags,
        'previous_id': previous_id
    })


@tags_router.get('/search/tag')
async def get_products_by_tags(tags: List[str] = Query(None),
                               previous_id: int = Query(0, title='Индекс последнего запроса', ge=0)):
    products = await tag.get_products_by_tags(tags, previous_id)
    previous_id = get_previous_id(products)
    products = format_records(products)
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'products': products,
        'previous_id': previous_id
    })
