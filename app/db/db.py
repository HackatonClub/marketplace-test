import os

import asyncpg
from app.settings import DATABASE_URL, DB_DATABASE, DB_HOST, DB_USER, DB_PASSWORD, DB_PORT


# TODO: add_tag_to_product_by_id возможно можно быстрее сделать, а также сделать проверку на то, существует ли продукт
# TODO: add_favourite в один запрос сделать, а также добавить проверку на неверного покупателя
# TODO: колда будевт функция добавить отзыв, не забыть добавить динамику в вычислении среднего рейтинга и колва отзывов в продукт

class DB:
    con: asyncpg.connection.Connection = None

    @classmethod
    async def connect_db(cls):
        try:
            if DATABASE_URL:
                cls.con = await asyncpg.connect(DATABASE_URL)
            else:
                cls.con = await asyncpg.connect(database=DB_DATABASE, user=DB_USER, password=DB_PASSWORD, host=DB_HOST,
                                                port=DB_PORT)
        except Exception as er:
            print(er)
            cls.con = None
            return False
        return True

    @classmethod
    async def disconnect_db(cls):
        await cls.con.close()

    @classmethod
    async def add_new_tag(cls, name: str):
        sql = "insert into tags (name) values ($1) ;"
        try:
            await cls.con.execute(sql, name)
        except Exception as e:
            print(e)
            return False
        return True

    @classmethod
    async def add_tag_to_product_by_id(cls,tag_name:str,product_id:int):
        customer_id = None
        sql = 'insert into tags (name) values ($1) on conflict do nothing;'
        try:
            await cls.con.execute(sql, tag_name)
        except Exception as er:
            print(er)
            return False
        sql = 'select id from tags where name = $1;'
        try:
            customer_id = (await cls.con.fetchrow(sql, tag_name))['id']
        except Exception as er:
            print(er)
            return False
        if not customer_id:
            return False
        sql = 'insert into tags_product(product_id, tag_id) values ($1,$2);'
        try:
            await cls.con.execute(sql, product_id, customer_id)
        except Exception as er:
            print(er)
            return False
        return True

    @classmethod
    async def remove_tag_from_product_by_id(cls,tag_name:str,product_id:int):
        sql = 'delete from tags_product where product_id = $1 and tag_id in (select id from tags where name = $2)'
        try:
            await cls.con.execute(sql, product_id,tag_name)
        except Exception as er:
            print(er)
            return False
        return True

    @classmethod
    async def remove_tag(cls,tag_name:str):
        customer_id = None
        sql = 'select id from tags where name = $1'
        try:
            customer_id = (await cls.con.fetchrow(sql, tag_name))['id']
        except Exception as er:
            print(er)
            return False
        sql = 'delete from tags_product where tag_id = $1'
        try:
            await cls.con.execute(sql, customer_id)
        except Exception as er:
            print(er)
            return False
        sql = 'delete from tags where id = $1'
        try:
            await cls.con.execute(sql, customer_id)
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

    @classmethod
    async def add_customer(cls,name:str):
        sql = "insert into customer(name) values ($1)"
        try:
            await cls.con.execute(sql, name)
        except Exception as e:
            print(e)
            return False
        return True

    @classmethod
    async def add_favourite(cls,name:str,product_id:int):
        customer_id = None
        sql = "select id from customer where name = $1"
        try:
            customer_id = (await cls.con.fetchrow(sql, name))['id']
        except Exception as e:
            print(e)
            return False
        sql = "insert into favourite(customer_id, product_id) VALUES ($1,$2)"
        try:
            await cls.con.execute(sql, customer_id, product_id)
        except Exception as e:
            print(e)
            return False
        return True

    @classmethod
    async def remove_favourite(cls, customer_name: str, product_id: int):
        sql = 'delete from favourite where product_id = $1 and customer_id in (select id from customer where name = $2)'
        try:
            await cls.con.execute(sql, product_id, customer_name)
        except Exception as e:
            print(e)
            return False
        return True

    @classmethod
    async def get_favourites(cls, customer_name: str):
        customer_id = None
        sql = 'select id from customer where name = $1;'
        try:
            customer_id = await cls.con.fetchrow(sql, customer_name)['id']
        except Exception as er:
            print(er)
            return False
        sql = 'select product_id from favourite where customer_id = $1;'
        try:
            await cls.con.execute(sql, customer_id)
        except Exception as er:
            print(er)
            return False
        return True

    @classmethod
    async def delete_customer(cls, customer_name: str):
        customer_id = None
        sql = "select id from customer where name = $1;"
        try:
            customer_id = await cls.con.fetchrow(sql, customer_name)['id']
        except Exception as e:
            print(e)
            return False
        if not customer_id:
            return False
        sql = "delete from review where customer_id = $1;"
        try:
            await cls.con.execute(sql, customer_id)
        except Exception as e:
            print(e)
            return False
        sql = "delete from cart_product where customer_id = $1;"
        try:
            await cls.con.execute(sql, customer_id)
        except Exception as e:
            print(e)
            return False
        sql = "delete from favourite where customer_id = $1;"
        try:
            await cls.con.execute(sql, customer_id)
        except Exception as e:
            print(e)
            return False
        return True

    @classmethod
    async def get_all_customers(cls):
        sql = 'select name from customer;'
        try:
            return await cls.con.fetch(sql)
        except Exception as er:
            print(er)
            return False

    @classmethod
    async def add_product_to_cart(cls, customer_name: str, product_id: int, product_num: int):
        customer_id = None
        sql = "select id from customer where name = $1;"
        try:
            customer_id = await cls.con.fetchrow(sql, customer_name)['id']
        except Exception as e:
            print(e)
            return False
        if not customer_id:
            return False
        sql = 'insert into cart_product(customer_id, product_id, product_num) VALUES ($1,$2,$3);'
        try:
            await cls.con.execute(sql, customer_id, product_id, product_num)
        except Exception as er:
            print(er)
            return False
        return True

    @classmethod
    async def update_product_in_cart(cls, customer_name: str, product_id: int, product_num: int):
        customer_id = None
        sql = "select id from customer where name = $1;"
        try:
            customer_id = await cls.con.fetchrow(sql, customer_name)['id']
        except Exception as e:
            print(e)
            return False
        if not customer_id:
            return False
        sql = 'update cart_product set product_num = $1 where customer_id = $2 and product_id = $3'
        try:
            await cls.con.execute(sql, customer_id, product_id, product_num)
        except Exception as er:
            print(er)
            return False
        return True

    @classmethod
    async def delete_product_from_cart(cls, customer_name: str, product_id: int):
        customer_id = None
        sql = "select id from customer where name = $1;"
        try:
            customer_id = await cls.con.fetchrow(sql, customer_name)['id']
        except Exception as e:
            print(e)
            return False
        if not customer_id:
            return False
        sql = 'delete from cart_product where product_id = $1 and customer_id = $2'
        try:
            await cls.con.execute(sql, product_id, customer_id)
        except Exception as er:
            print(er)
            return False
        return True

    @classmethod
    async def get_cart_products(cls, customer_name: str):
        customer_id = None
        sql = "select id from customer where name = $1;"
        try:
            customer_id = await cls.con.fetchrow(sql, customer_name)['id']
        except Exception as e:
            print(e)
            return False
        if not customer_id:
            return False
        sql = 'select p.id,p.name,cart_product.product_num from cart_product join product p on p.id = cart_product.product_id where customer_id = $1'
        try:
            return await cls.con.fetch(sql, customer_id)
        except Exception as er:
            print(er)
            return False
