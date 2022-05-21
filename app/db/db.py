import json
import logging
import sys

import asyncpg
from asyncpg import Record

from app.exceptions import InternalServerError
from app.settings import DATABASE_URL

logger = logging.getLogger(__name__)



class DB:
    con: asyncpg.connection.Connection = None

    @classmethod
    async def connect_db(cls) -> None:
        try:
            cls.con = await asyncpg.connect(DATABASE_URL)
        except asyncpg.PostgresError as error:
            logger.error(error)
            raise InternalServerError() from error
    @classmethod
    async def disconnect_db(cls) -> None:
        await cls.con.close()