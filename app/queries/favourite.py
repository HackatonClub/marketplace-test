from asyncpg import Record

from app.db.db import DB
from app.exceptions import BadRequest, CustomerNotFoundException
from app.queries.customer import get_customer_id
from app.settings import ITEMS_PER_PAGE


async def add_favourite(name: str, product_id: int) -> None:
    customer_id = await get_customer_id(name)
    if not customer_id:
        raise CustomerNotFoundException
    sql = """  INSERT INTO favourite(customer_id, product_id)
               VALUES ($1,$2)"""
    if not await DB.con.execute(sql, customer_id, product_id):
        raise BadRequest('Продукт уже добавлен в избранное')


async def remove_favourite(customer_name: str, product_id: int) -> None:
    sql = '''  DELETE FROM favourite
               WHERE product_id = $1 AND customer_id IN
               (SELECT id
                 FROM users
                 WHERE name = $2)'''
    if not await DB.con.execute(sql, product_id, customer_name):
        raise BadRequest('Уже удален из избранного')


async def get_favourites(customer_name: str, previous_id: int) -> list[Record]:
    customer_id = await get_customer_id(customer_name)
    if not customer_id:
        raise CustomerNotFoundException
    sql = '''  SELECT product_id,id AS previous_id
               FROM favourite
               WHERE customer_id = $1 AND id > $2
               LIMIT $3;'''
    return await DB.con.fetch(sql, customer_id, previous_id, ITEMS_PER_PAGE)
