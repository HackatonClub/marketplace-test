from app.db.db import DB


async def add_product_to_cart(customer_name: str, product_id: int, product_num: int):
    customer_id = None
    sql = "select id from customer where name = $1;"
    try:
        customer_id = (await DB.con.fetchrow(sql, customer_name))['id']
    except Exception as e:
        print(e)
        return False
    if not customer_id:
        return False
    sql = 'insert into cart_product(customer_id, product_id, product_num) VALUES ($1,$2,$3);'
    try:
        await DB.con.execute(sql, customer_id, product_id, product_num)
    except Exception as er:
        print(er)
        return False
    return True


async def update_product_in_cart(customer_name: str, product_id: int, product_num: int):
    customer_id = None
    sql = "select id from customer where name = $1;"
    try:
        customer_id = (await DB.con.fetchrow(sql, customer_name))['id']
    except Exception as e:
        print(e)
        return False
    if not customer_id:
        return False
    sql = 'update cart_product set product_num = $1 where customer_id = $2 and product_id = $3'
    try:
        await DB.con.execute(sql, customer_id, product_id, product_num)
    except Exception as er:
        print(er)
        return False
    return True


async def delete_product_from_cart(customer_name: str, product_id: int):
    customer_id = None
    sql = "select id from customer where name = $1;"
    try:
        customer_id = (await DB.con.fetchrow(sql, customer_name))['id']
    except Exception as e:
        print(e)
        return False
    if not customer_id:
        return False
    sql = 'delete from cart_product where product_id = $1 and customer_id = $2'
    try:
        await DB.con.execute(sql, product_id, customer_id)
    except Exception as er:
        print(er)
        return False
    return True


async def get_cart_products(customer_name: str):
    customer_id = None
    sql = "select id from customer where name = $1;"
    try:
        customer_id = (await DB.con.fetchrow(sql, customer_name))['id']
    except Exception as e:
        print(e)
        return False
    if not customer_id:
        return False
    sql = 'select p.id as product_id,p.name,cart_product.product_num from cart_product join product p on p.id = cart_product.product_id where customer_id = $1'
    try:
        return await DB.con.fetch(sql, customer_id)
    except Exception as er:
        print(er)
        return False
