from asyncpg import Record

from app.db.db import DB
from app.exceptions import BadRequest, CustomerNotFoundException
from app.queries.customer import get_customer_id
from app.settings import ITEMS_PER_PAGE


async def add_favourite(name: str, product_id: int) -> None:
    customer_id = await get_customer_id(name)
    if not customer_id:
        raise CustomerNotFoundException
    sql = "insert into favourite(customer_id, product_id) VALUES ($1,$2)"
    if not await DB.execute(sql, customer_id, product_id):
        raise BadRequest('Продукт уже добавлен в избранное')


async def remove_favourite(customer_name: str, product_id: int) -> None:
    sql = 'delete from favourite where product_id = $1 and customer_id in (select id from customer where name = $2)'
    if not await DB.execute(sql, product_id, customer_name):
        raise BadRequest('Уже удален из избранного')


async def get_favourites(customer_name: str, previous_id: int) -> list[Record]:
    customer_id = await get_customer_id(customer_name)
    if not customer_id:
        raise CustomerNotFoundException
    sql = 'select product_id,id as previous_id from favourite where customer_id = $1 and id > $2 limit $3;'
    return await DB.fetch(sql, customer_id, previous_id, ITEMS_PER_PAGE)
