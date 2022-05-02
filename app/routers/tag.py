from typing import List

from fastapi import APIRouter, Path, Query, status
from fastapi.param_functions import Depends
from fastapi.responses import JSONResponse

import app.queries.tag as tag_queries
from app.auth.oauth2 import get_current_user
from app.exceptions import ForbiddenException
from app.model import Tag
from app.queries.customer import get_user_role
from app.utils.extracter import get_previous_id
from app.utils.formatter import format_records

tags_router = APIRouter(tags=["Tags"])


@tags_router.post('/tag')
async def add_tag(tag: Tag, current_user: str = Depends(get_current_user)) -> JSONResponse:
    role = await get_user_role(current_user)
    if not role:
        raise ForbiddenException
    await tag_queries.add_new_tag(tag.tag_name)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed',
    })


@tags_router.post('/product/{product_id}/tag')
async def product_add_tag(tag: Tag, product_id: int = Path(..., title='ID продукта', gt=0),
                          current_user: str = Depends(get_current_user)) -> JSONResponse:
    role = await get_user_role(current_user)
    if not role:
        raise ForbiddenException
    await tag_queries.add_tag_to_product_by_id(tag.tag_name, product_id)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed',
    })


@tags_router.delete('/tag')
async def delete_tag(tag: Tag, current_user: str = Depends(get_current_user)) -> JSONResponse:
    role = await get_user_role(current_user)
    if not role:
        raise ForbiddenException
    await tag_queries.remove_tag(tag.tag_name)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed',
    })


@tags_router.delete('/product/{product_id}/tag')
async def remove_tag_from_product(tag: Tag, product_id: int = Path(..., title='ID продукта', gt=0),
                                  current_user: str = Depends(get_current_user)) -> JSONResponse:
    role = await get_user_role(current_user)
    if not role:
        raise ForbiddenException
    await tag_queries.remove_tag_from_product_by_id(tag.tag_name, product_id)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed',
    })


@tags_router.get('/tag')
async def get_all_tags(previous_id: int = Query(0, title='Индекс последнего запроса', ge=0)) -> JSONResponse:
    tags = await tag_queries.get_all_tags(previous_id)
    previous_id = get_previous_id(tags)
    tags = format_records(tags)
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'tags': tags,
        'previous_id': previous_id,
    })


@tags_router.get('/product/{product_id}/tag')
async def get_tags_of_product(product_id: int = Path(..., title='ID продукта', gt=0),
                              previous_id: int = Query(0, title='Индекс последнего запроса', ge=0)) -> JSONResponse:
    tags = await tag_queries.get_tags_of_product_by_id(product_id, previous_id)
    previous_id = get_previous_id(tags)
    tags = format_records(tags)
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'tags': tags,
        'previous_id': previous_id,
    })


@tags_router.get('/search/tag')
async def get_products_by_tags(tags: List[str] = Query(None, title='Список тэгов'),
                               search_query: str = Query(None, title='Строка поиска'),
                               current_user: str = Depends(get_current_user),
                               previous_id: int = Query(0, title='Индекс последнего запроса', ge=0)) -> JSONResponse:
    if not search_query:
        search_query = ''
    products, previous_id = await tag_queries.search_products(tags, search_query, current_user,previous_id)
    products = format_records(products)
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'products': products,
        'previous_id': previous_id
    })
