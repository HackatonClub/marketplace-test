from app.db.db import DB


async def add_customer(name: str, password: str):
    sql = "insert into customer(name,password) values ($1,$2)"
    try:
        await DB.con.execute(sql, name, password)
    except Exception as e:
        print(e)
        return False
    return True


async def delete_customer(customer_name: str):
    customer_id = None
    sql = "select id from customer where name = $1;"
    try:
        customer_id = (await DB.con.fetchrow(sql, customer_name))['id']
    except Exception as e:
        print(e)
        return False
    if not customer_id:
        return False
    sql = "delete from review where customer_id = $1;"
    try:
        await DB.con.execute(sql, customer_id)
    except Exception as e:
        print(e)
        return False
    sql = "delete from cart_product where customer_id = $1;"
    try:
        await DB.con.execute(sql, customer_id)
    except Exception as e:
        print(e)
        return False
    sql = "delete from favourite where customer_id = $1;"
    try:
        await DB.con.execute(sql, customer_id)
    except Exception as e:
        print(e)
        return False
    sql = "delete from customer where id = $1;"
    try:
        await DB.con.execute(sql, customer_id)
    except Exception as e:
        print(e)
        return False
    return True


async def get_all_customers():
    sql = 'select name from customer;'
    try:
        return await DB.con.fetch(sql)
    except Exception as er:
        print(er)
        return False
