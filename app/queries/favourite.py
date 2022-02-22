from app.db.db import DB


async def add_favourite(name: str, product_id: int):
    sql = "select id from customer where name = $1"
    customer_id = (await DB.fetchrow(sql, name))
    if not customer_id:
        return False
    customer_id = customer_id['id']
    sql = "insert into favourite(customer_id, product_id) VALUES ($1,$2)"
    return await DB.execute(sql, customer_id, product_id)


async def remove_favourite(customer_name: str, product_id: int):
    sql = 'delete from favourite where product_id = $1 and customer_id in (select id from customer where name = $2)'
    return await DB.execute(sql, product_id, customer_name)


async def get_favourites(customer_name: str):
    sql = 'select id from customer where name = $1;'
    customer_id = (await DB.fetchrow(sql, customer_name))
    if not customer_id:
        return False
    customer_id = customer_id['id']
    sql = 'select product_id from favourite where customer_id = $1;'
    return await DB.fetch(sql, customer_id)
