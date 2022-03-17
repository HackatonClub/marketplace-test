
import pathlib


import app.queries.photo as photo

from fastapi import APIRouter, HTTPException, Query, status
from fastapi.responses import FileResponse, JSONResponse


photo_router = APIRouter(tags=["Photo"])


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


@photo_router.delete('/product/{product_id}/photo/{image_name}')
async def delete_product_photo(product_id: int = Query(None, description='Id продукта'),
                               key: str = Query(None, description='photoid')):

    image_name = await photo.delete_photo_by_name(product_id, key)

    folder_path = pathlib.Path(__file__).parent.resolve()
    file_path = folder_path.joinpath(pathlib.Path(f"assets/{image_name[1:len(image_name)-1]}"))
    if not pathlib.Path.is_file(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Файл не существует',
        )

    pathlib.Path.unlink(file_path)
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'details': 'Файл удален',
    })
