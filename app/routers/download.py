

import pathlib
from typing import List
from fastapi import UploadFile


class DownloadFiles():
    async def __call__(self, upload_files: List[UploadFile]):

        async def download_file(upload_files: List[UploadFile]):
            folder_path = pathlib.Path(__file__).parent.resolve()
            upload_path = folder_path.joinpath(pathlib.Path("assets"))
            i = 1
            urls = {}
            for upload_file in upload_files:
                photo_path = upload_path.joinpath(pathlib.Path(f"{upload_file.filename}"))
                with open(photo_path, "wb+") as file_object:
                    file_object.write(upload_file.file.read())
                urls[f"photo{i}"] = upload_file.filename
                i += 1
            return urls
        return await download_file(upload_files)


downloadfilesproduct = DownloadFiles()
