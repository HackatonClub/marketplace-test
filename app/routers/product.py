
import json
from typing import List
from fastapi import APIRouter, File, Form, HTTPException, Query, UploadFile, status
from fastapi.responses import JSONResponse
from app.model import ProductUp

from app.queries import photo
from app.queries import product
from app.queries import tag as tag_queries
from app.exceptions import BadRequest, ForbiddenException
from app.routers.download import downloadfilesproduct
from app.routers.delete import deletfilesproduct
from app.queries.customer import get_user_role
from app.model import User
from fastapi.param_functions import Depends
from app.auth.oauth2 import get_current_user

product_router = APIRouter(tags=["Product"])


@product_router.post('/product')
async def add_product(name: str = Form(..., title='Название продукта', max_length=50),
                      discription: str = Form(..., title='Описание продукта', max_length=350),
                      price: int = Form(..., title='Цена продукта', gt=0),
                      tag_names: List[str] = Query(..., title='Тэги продукта'),
                      upload_files: List[UploadFile] = File(...),
                      current_user: str = Depends(get_current_user)) -> JSONResponse:
    role = await get_user_role(current_user)
    if not role:
        raise ForbiddenException
    urls = await downloadfilesproduct(upload_files)
    product_tags = {'tags': tag_names}
    product_id = await product.add_product(name, discription, price, product_tags, urls)
    if not product_id:
        raise BadRequest('Продукт уже существует')
    await tag_queries.add_tags_to_product_by_id(tag_names,product_id)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed',
    })


@product_router.delete('/product')
async def delete_product(product_id: int = Query(None, description='Id продукта'),  current_user: str = Depends(get_current_user)) -> JSONResponse:
    role = await get_user_role(current_user)
    if not role:
        raise ForbiddenException
    urls = await photo.get_name_photo_for_delete(product_id)
    urls = json.loads(urls.replace("'", '"'))
    for image_name in urls.values():
        if not image_name:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Файл не существует',
                )
        await deletfilesproduct(image_name)

    await product.delete_product(product_id)

    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={
        'details': 'Executed',
    })


@product_router.put('/product/{product_id}')
async def update_product(produ: ProductUp,  current_user: str = Depends(get_current_user)) -> JSONResponse:
    role = await get_user_role(current_user)
    if not role:
        raise ForbiddenException
    print(produ.tag_id)
    if produ.urls:
        urls = await photo.get_name_photo_for_delete(produ.product_id)
        urls = json.loads(urls.replace("'", '"'))
        for image_name in urls.values():
            await deletfilesproduct(image_name)

    await product.update_product(produ)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed',
    })


@product_router.get('/product/{product_id}')
async def get_product(product_id: int = Query(None, description='Id продукта')):

    product_info = await product.get_info_product(product_id)
    return product_info
