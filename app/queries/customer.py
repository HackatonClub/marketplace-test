from app.db.db import DB


async def add_customer(name: str, password: str):
    sql = "insert into customer(name,password) values ($1,$2)"
    await DB.execute(sql, name, password)


async def delete_customer(customer_name: str):
    sql = "select id from customer where name = $1;"
    customer_id = (await DB.fetchrow(sql, customer_name))['id']
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


async def get_all_customers():
    sql = 'select name from customer;'
    return await DB.fetch(sql)
