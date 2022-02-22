from typing import Optional, List
import os
import pathlib
import app.queries.photo as photo
from fastapi import APIRouter, File, Path, UploadFile, Form, Query
from fastapi.responses import FileResponse

from app.db.db import DB as db


photo_router = APIRouter(tags=["Photo"])


@photo_router.post("/product/{product_id}/photos")
async def create_files(product_id: int = Path(..., title='ID продукта', gt=0),
                       files: List[UploadFile] = File(...)):

    # Проверку на существование продукта
    if await photo.check_product(product_id):
        return "Данного продукта не существует"

    # Получение пути каталога , куда сохранять
    folder_path = pathlib.Path(__file__).parent.resolve()
    # + assets/{product_id}
    upload_path = folder_path.joinpath(pathlib.Path(f"assets/{product_id}"))
    if not pathlib.Path.is_dir(upload_path):
        pathlib.Path.mkdir(upload_path)

    # Загрузка
    for file in files:
        photo_path = upload_path.joinpath(pathlib.Path(f"{file.filename}"))
        with open(photo_path, "wb+") as file_object:
            file_object.write(file.file.read())
        await photo.add_photo(product_id, f"assets/{product_id}/{file.filename}")
    # Внесение каталога в бд
    

    return "Files succeful added"

#
# !!!!!! Добавить проверку на то что существует ли файл
@photo_router.get('/product/{product_id}/photo/{image_name}')
async def get_product_photo( product_id: str = Query(None, description='Id продукта'), 
                                image_name: str = Query(None, description='Имя файла')):
    folder_path = pathlib.Path(__file__).parent.resolve()
    file_path = folder_path.joinpath(
        pathlib.Path(f"assets/{product_id}/{image_name}"))
    #path_files = pathlib.Path(upload_path).glob('*.*')

    return FileResponse(file_path)
