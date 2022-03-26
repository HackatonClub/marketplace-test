
import pathlib

from fastapi import HTTPException, status


class DeleteeFile():
    async def __call__(self, image_name: str):

        async def delete_file(image_name: str):
            folder_path = pathlib.Path(__file__).parent.resolve()
            file_path = folder_path.joinpath(pathlib.Path(f"assets/{image_name}"))
            if not pathlib.Path.is_file(file_path):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Файл не существует',
                )

            pathlib.Path.unlink(file_path)
        return await delete_file(image_name)


deletfilesproduct = DeleteeFile()