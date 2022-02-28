from app.db.db import DB
from app.queries.customer import get_customer_id
from app.settings import ITEMS_PER_PAGE


async def add_favourite(name: str, product_id: int):
    customer_id = await get_customer_id(name)
    if not customer_id:
        return False
    sql = "insert into favourite(customer_id, product_id) VALUES ($1,$2)"
    return await DB.execute(sql, customer_id, product_id)


async def remove_favourite(customer_name: str, product_id: int):
    sql = 'delete from favourite where product_id = $1 and customer_id in (select id from customer where name = $2)'
    return await DB.execute(sql, product_id, customer_name)


async def get_favourites(customer_name: str, previous_id: int):
    customer_id = await get_customer_id(customer_name)
    if not customer_id:
        return False
    sql = 'select product_id,id as previous_id from favourite where customer_id = $1 and id > $2 limit $3;'
    return await DB.fetch(sql, customer_id, previous_id, ITEMS_PER_PAGE)
