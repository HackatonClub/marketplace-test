from app.db.db import DB
from app.queries.customer import get_customer_id
from app.settings import ITEMS_PER_PAGE


async def add_product_to_cart(customer_name: str, product_id: int, product_num: int):
    customer_id = await get_customer_id(customer_name)
    if not customer_id:
        return False
    sql = 'insert into cart_product(customer_id, product_id, product_num) VALUES ($1,$2,$3);'
    return await DB.execute(sql, customer_id, product_id, product_num)


async def update_product_in_cart(customer_name: str, product_id: int, product_num: int):
    customer_id = await get_customer_id(customer_name)
    if not customer_id:
        return False
    sql = 'update cart_product set product_num = $1 where customer_id = $2 and product_id = $3'
    await DB.execute(sql, customer_id, product_id, product_num)


async def delete_product_from_cart(customer_name: str, product_id: int):
    customer_id = await get_customer_id(customer_name)
    if not customer_id:
        return False
    sql = 'delete from cart_product where product_id = $1 and customer_id = $2;'
    return await DB.execute(sql, product_id, customer_id)


async def get_cart_products(customer_name: str, previous_id: int):
    customer_id = await get_customer_id(customer_name)
    if not customer_id:
        return False
    sql = 'select p.id as product_id,p.name,cart_product.product_num,cart_product.id as previous_id from cart_product join product p on p.id = cart_product.product_id where customer_id = $1 and cart_product.id > $2 limit $3'
    return await DB.fetch(sql, customer_id, previous_id, ITEMS_PER_PAGE)
