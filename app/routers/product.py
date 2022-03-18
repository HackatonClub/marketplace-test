

from typing import List
from fastapi import APIRouter, File, Form, HTTPException, Query, UploadFile, status
from fastapi.responses import JSONResponse
from app.model import ProductUp
import json

import app.queries.photo as photo
import app.queries.product as product
from app.routers.download import downloadfilesproduct
from app.routers.delete import deletfilesproduct


product_router = APIRouter(tags=["Product"])


@product_router.post('/product')
async def add_product(name: str = Form(..., title='Название продукта', max_length=50),
                      discription: str = Form(..., title='Описание продукта', max_length=350),
                      price: int = Form(..., title='Цена продукта', gt=0),
                      tag_id: str = Form(..., title='Тэги продукта'),
                      upload_files: List[UploadFile] = File(...)):
    urls = await downloadfilesproduct(upload_files)
    # TODO: чтото сделать с тэгами
    # тэги словарь
    tag_id1 = {}
    tag_id1["asdf"] = tag_id
    print(await product.add_product(name, discription, price, tag_id1, urls))
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed',
    })


@product_router.delete('/product')
async def delete_product(product_id: int = Query(None, description='Id продукта')):
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
async def update_product(produ: ProductUp):
    if not await product.update_product(produ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Такого продукта не существует',
        )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed',
    })


@product_router.get('/product/{product_id}')
async def get_product(product_id: int = Query(None, description='Id продукта')):

    product_info = await product.get_info_product(product_id)
    return product_info
