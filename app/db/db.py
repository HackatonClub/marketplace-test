
import asyncpg

from app.settings import DATABASE_URL

# TODO: add_tag_to_product_by_id возможно можно быстрее сделать, а также сделать проверку на то, существует ли продукт
# TODO: add_favourite в один запрос сделать, а также добавить проверку на неверного покупателя
# TODO: колда будевт функция добавить отзыв, не забыть добавить динамику в вычислении среднего рейтинга
#           и колва отзывов в продукт

class DB:
    con: asyncpg.connection.Connection = None

    @classmethod
    async def connect_db(cls):
        try:
            cls.con = await asyncpg.connect(DATABASE_URL)
        except Exception as er:
            print(er)
            cls.con = None
            return False
        return True

    @classmethod
    async def disconnect_db(cls):
        await cls.con.close()

    @classmethod
    async def execute(cls, sql, *args):
        try:
            await DB.con.execute(sql, *args)
        except Exception as er:
            print(er)
            return False
        return True

    @classmethod
    async def fetch(cls, sql, *args):
        try:
            return await DB.con.fetch(sql, *args)
        except Exception as er:
            print(er)
            return False

    @classmethod
    async def fetchrow(cls, sql, *args):
        try:
            return await DB.con.fetchrow(sql, *args)
        except Exception as er:
            print(er)
            return False

    @classmethod
    async def fetchval(cls, sql, *args):
        try:
            return await DB.con.fetchval(sql, *args)
        except Exception as er:
            print(er)
            return False
