from app.db.db import DB
from app.settings import ITEMS_PER_PAGE

async def add_customer(name: str, password: str):
    sql = "insert into customer(name,password) values ($1,$2)"
    await DB.execute(sql, name, password)


async def delete_customer(customer_name: str):
    customer_id = await get_customer_id(customer_name)
    if not customer_id:
        return False
    sql = "delete from review where customer_id = $1;"
    await DB.execute(sql, customer_id)
    sql = "delete from cart_product where customer_id = $1;"
    await DB.execute(sql, customer_id)
    sql = "delete from favourite where customer_id = $1;"
    await DB.execute(sql, customer_id)
    sql = "delete from customer where id = $1;"
    return await DB.execute(sql, customer_id)


async def get_customer_id(customer_name: str):
    sql = "select id from customer where name = $1"
    return await DB.fetchval(sql, customer_name)


async def get_all_customers(previous_id: int):
    sql = 'select name,id as previous_id from customer where id > $1 limit $2'
    return await DB.fetch(sql, previous_id, ITEMS_PER_PAGE)
