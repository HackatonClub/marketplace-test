from app.db.db import DB


async def add_favourite(name: str, product_id: int):
    customer_id = None
    sql = "select id from customer where name = $1"
    try:
        customer_id = (await DB.con.fetchrow(sql, name))['id']
    except Exception as e:
        print(e)
        return False
    sql = "insert into favourite(customer_id, product_id) VALUES ($1,$2)"
    try:
        await DB.con.execute(sql, customer_id, product_id)
    except Exception as e:
        print(e)
        return False
    return True


async def remove_favourite(customer_name: str, product_id: int):
    sql = 'delete from favourite where product_id = $1 and customer_id in (select id from customer where name = $2)'
    try:
        await DB.con.execute(sql, product_id, customer_name)
    except Exception as e:
        print(e)
        return False
    return True


async def get_favourites(customer_name: str):
    customer_id = None
    sql = 'select id from customer where name = $1;'
    try:
        customer_id = (await DB.con.fetchrow(sql, customer_name))['id']
    except Exception as er:
        print(er)
        return False
    sql = 'select product_id from favourite where customer_id = $1;'
    try:
        return await DB.con.fetch(sql, customer_id)
    except Exception as er:
        print(er)
        return False
