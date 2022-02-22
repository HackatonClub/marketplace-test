from app.db.db import DB


async def add_product_to_cart(customer_name: str, product_id: int, product_num: int):
    sql = "select id from customer where name = $1;"
    customer_id = (await DB.fetchrow(sql, customer_name))['id']
    if not customer_id:
        return False
    sql = 'insert into cart_product(customer_id, product_id, product_num) VALUES ($1,$2,$3);'
    return await DB.execute(sql, customer_id, product_id, product_num)


async def update_product_in_cart(customer_name: str, product_id: int, product_num: int):
    sql = "select id from customer where name = $1;"
    customer_id = (await DB.fetchrow(sql, customer_name))['id']
    if not customer_id:
        return False
    sql = 'update cart_product set product_num = $1 where customer_id = $2 and product_id = $3'
    await DB.execute(sql, customer_id, product_id, product_num)


async def delete_product_from_cart(customer_name: str, product_id: int):
    sql = "select id from customer where name = $1;"
    customer_id = (await DB.fetchrow(sql, customer_name))['id']
    if not customer_id:
        return False
    sql = 'delete from cart_product where product_id = $1 and customer_id = $2;'
    return await DB.execute(sql, product_id, customer_id)


async def get_cart_products(customer_name: str):
    sql = "select id from customer where name = $1;"
    customer_id = (await DB.fetchrow(sql, customer_name))['id']
    if not customer_id:
        return False
    sql = 'select p.id as product_id,p.name,cart_product.product_num from cart_product join product p on p.id = cart_product.product_id where customer_id = $1'
    return await DB.fetch(sql, customer_id)
