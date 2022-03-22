import logging

import aioredis

from app.db.db import DB

logger = logging.getLogger(__name__)


class Redis:

    con: aioredis.Redis = None
    @classmethod
    async def connect_redis(cls):
        try:
            cls.con = aioredis.from_url('redis://localhost', encoding="utf-8", decode_responses=True)
        except Exception as error:
            logger.error(error)

    @classmethod
    async def disconnect_redis(cls):
        await cls.con.close()

    @classmethod
    async def load_tags(cls):
        sql = 'select product_id,tag_id from tags_product'
        tags_product = await DB.fetch(sql)
        for link in tags_product:
            await cls.con.sadd(link['tag_id'],link['product_id'])


    @classmethod
    async def get_product_ids_by_tags(cls,tags: list[str]):
        product_ids = await cls.con.sinter(tags)
        return product_ids

    @classmethod
    async def add_tag_to_product(cls,tag_id,product_id):
        await cls.con.sadd(tag_id,product_id)

    @classmethod
    async def remove_tag_from_product(cls,tag_id,product_id):
        await cls.con.srem(tag_id,product_id)

