
import pathlib
from typing import List

from fastapi import (APIRouter, File, HTTPException, Path, Query, UploadFile,
                     status)
from fastapi.responses import FileResponse, JSONResponse

import app.queries.photo as photo

photo_router = APIRouter(tags=["Photo"])


@photo_router.post("/product/{product_id}/photos")
async def create_files(product_id: int = Path(..., title='ID продукта', gt=0),
                       files: List[UploadFile] = File(...)):

    # Проверку на существование продукта

    # Получение пути каталога , куда сохранять
    folder_path = pathlib.Path(__file__).parent.resolve()
    # + assets/{product_id}
    upload_path = folder_path.joinpath(pathlib.Path("assets"))

    # Загрузка
    i = 1
    urls = {}
    for file in files:
        photo_path = upload_path.joinpath(pathlib.Path(f"{file.filename}"))
        with open(photo_path, "wb+") as file_object:
            file_object.write(file.file.read())
        urls[f"photo{i}"] = file.filename
        i += 1
    print(urls)
    if not await photo.add_photo(product_id, urls):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Такого продукта с таким id не существует',
         )
    # Внесение каталога в бд

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed',
    })


@photo_router.get('/product/{product_id}/photo/{image_name}')
async def get_product_photo_by_name(product_id: int = Query(None, description='Id продукта'),
                                    image_name: str = Query(None, description='Имя файла')):

    folder_path = pathlib.Path(__file__).parent.resolve()
    # проверка на существование файла
    file_path = folder_path.joinpath(pathlib.Path(f"assets/{image_name}"))

    if not pathlib.Path.is_file(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Файл не найден',
        )

    return FileResponse(file_path)


@photo_router.get('/product/{product_id}/photos')
async def get_product_photo_all_filename(product_id: int = Query(None, description='Id продукта')):

    return await photo.get_all_name_photo(product_id)


@photo_router.delete('/product/{product_id}/photo')
async def delete_product_photo(product_id: int = Query(None, description='Id продукта'),
                               image_name: str = Query(None, description='Имя файла')):

    await photo.delete_photo_by_name(product_id, image_name)

    folder_path = pathlib.Path(__file__).parent.resolve()
    file_path = folder_path.joinpath(pathlib.Path(f"assets/{image_name}"))

    if not pathlib.Path.is_file(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Файл не существует',
        )

    pathlib.Path.unlink(file_path)
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'details': 'Файл удален',
    })
