import os

import asyncpg
from app.settings import DATABASE_URL,DB_DATABASE,DB_HOST,DB_USER,DB_PASSWORD,DB_PORT

# TODO: add_tag_to_product_by_id возможно можно быстрее сделать

class DB:
    con : asyncpg.connection.Connection = None

    @classmethod
    async def connect_db(cls):
        try:
            if DATABASE_URL:
                cls.con = await asyncpg.connect(DATABASE_URL)
            else:
                cls.con = await  asyncpg.connect(database=DB_DATABASE,user=DB_USER,password=DB_PASSWORD,host=DB_HOST,port=DB_PORT)
        except Exception as er:
            print(er)
            cls.con = None
            return False

    @classmethod
    async def add_new_tag(cls,name: str):
        sql = "insert into tags (name) values ($1) ;"
        try:
            return await cls.con.execute(sql, name )
        except Exception as e:
            print(e)
            return False

    @classmethod
    async def add_tag_to_product_by_id(cls,tag_name:str,product_id:int):
        id = None
        sql = 'insert into tags (name) values ($1) on conflict do nothing;'
        try:
            await cls.con.execute(sql)
        except Exception as er:
            print(er)
            return False
        sql = 'select id from tags where name = $1;'
        try:
            id = await cls.con.fetchrow(sql)['id']
        except Exception as er:
            print(er)
            return False
        if not id:
            return False
        sql = 'insert into tags_product(product_id, tag_id) values ($1,$2);'
        try:
            await cls.con.execute(sql,product_id,id)
        except Exception as er:
            print(er)
            return False
        return True

    @classmethod
    async def get_all_tags(cls):
        sql = "select name from tags"
        try:
            return await cls.con.fetch(sql)
        except Exception as er:
            print(er)
            return False

    @classmethod
    async def get_tags_of_product_by_id(cls,id:int):
        sql = "select tags.name from tags_product join tags on tags.id = tags_product.tag_id where tags_product.product_id = $1;"
        try:
            return await cls.con.fetch(sql, id)
        except Exception as e:
            print(e)
            return False

