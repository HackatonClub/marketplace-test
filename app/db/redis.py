import logging

import aioredis

from app.db.db import DB
from app.settings import HASH_EXPIRE,REDIS_PORT,REDIS_PASSWORD,REDIS_HOSTNAME

logger = logging.getLogger(__name__)


class Redis:

    con: aioredis.Redis = None
    @classmethod
    async def connect_redis(cls):
        try:
            cls.con = aioredis.from_url(f'redis://:{REDIS_PASSWORD}@{REDIS_HOSTNAME}:{REDIS_PORT}', encoding="utf-8", decode_responses=True)
        except Exception as error:
            logger.error(error)
        finally:
            cls.con = None

    @classmethod
    async def disconnect_redis(cls):
        if cls.con:
            await cls.con.close()

    @classmethod
    async def load_tags(cls):
        if not cls.con:
            return
        sql = 'select product_id,tag_id from tags_product'
        tags_product = await DB.fetch(sql)
        await cls.con.flushall()
        for link in tags_product:
            await cls.con.sadd(link['tag_id'],link['product_id'])

    @classmethod
    def check_connection(cls):
        return cls.con is not None

    @classmethod
    async def get_product_ids_by_tags(cls,tags: list[int]):
        if not cls.con:
            return
        product_ids = await cls.con.sinter(tags)
        return [int(x) for x in product_ids]

    @classmethod
    async def add_tag_to_product(cls,tag_id,product_id):
        if not cls.con:
            return
        await cls.con.sadd(tag_id,product_id)

    @classmethod
    async def remove_tag_from_product(cls,tag_id,product_id):
        if not cls.con:
            return
        await cls.con.srem(tag_id,product_id)

    @classmethod
    async def del_tag(cls,tag_id):
        if not cls.con:
            return
        await cls.con.delete(tag_id)

    @classmethod
    async def set_hash(cls,hash_name: str, hash_value: str):
        if not cls.con:
            return
        await cls.con.set(hash_name,hash_value,HASH_EXPIRE)

    @classmethod
    async def get_hash(cls,hash_name:str):
        if not cls.con:
            return
        return await cls.con.get(hash_name)
