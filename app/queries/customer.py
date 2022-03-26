from app.db.db import DB
from app.db.redis import Redis
from app.exceptions import BadRequest, CustomerNotFoundException
from app.settings import ITEMS_PER_PAGE


async def add_customer(name: str, password: str):
    sql = "insert into customer(name,password) values ($1,$2)"
    if not await DB.execute(sql, name, password):
        raise BadRequest('Покупатель с таким именем существует')


async def delete_customer(customer_name: str):
    customer_id = await get_customer_id(customer_name)
    if not customer_id:
        raise CustomerNotFoundException()
    sql = "delete from review where customer_id = $1;"
    await DB.execute(sql, customer_id)
    sql = "delete from cart_product where customer_id = $1;"
    await DB.execute(sql, customer_id)
    sql = "delete from favourite where customer_id = $1;"
    await DB.execute(sql, customer_id)
    sql = "delete from customer where id = $1;"
    if not await DB.execute(sql, customer_id):
        raise BadRequest('Покупатель уже удален')
    await Redis.del_tag(customer_name)


async def get_customer_id(customer_name: str):
    customer_id = await Redis.get_hash(customer_name)
    if not customer_id:
        sql = "select id from customer where name = $1"
        customer_id = await DB.fetchval(sql, customer_name)
        if not customer_id:
            raise CustomerNotFoundException()
    await Redis.set_hash(customer_name, customer_id)
    return int(customer_id)


async def get_all_customers(previous_id: int):
    sql = 'select name,id as previous_id from customer where id > $1 limit $2'
    return await DB.fetch(sql, previous_id, ITEMS_PER_PAGE)
