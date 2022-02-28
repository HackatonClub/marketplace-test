from app.db.db import DB
from app.settings import ITEMS_PER_PAGE

# TODO: Добавить динамику в добавление и удаление, но тогда код станет менее стабильным

async def add_review_to_product(customer_name: str, product_id: int, body: str, rating: int):
    sql = "select id from customer where name = $1"
    customer_id = await DB.fetchrow(sql, customer_name)
    if not customer_id:
        return False
    customer_id = customer_id['id']
    sql = "insert into review(product_id, customer_id, body, rating) VALUES ($1,$2,$3,$4)"
    await DB.execute(sql, product_id, customer_id, body, rating)
    return update_product_dynamic_data(product_id)


async def delete_review_from_product(customer_name: str, product_id: int):
    sql = "select id from customer where name = $1"
    customer_id = await DB.fetchrow(sql, customer_name)
    if not customer_id:
        return False
    customer_id = customer_id['id']
    sql = "delete from review where customer_id = $1 and product_id = $2"
    await DB.execute(sql, customer_id, product_id)
    return update_product_dynamic_data(product_id)


async def update_review_to_product(customer_name: str, product_id: int, body: str, rating: int):
    sql = "select id from customer where name = $1"
    customer_id = await DB.fetchrow(sql, customer_name)
    if not customer_id:
        return False
    customer_id = customer_id['id']
    sql = "update review set body = $1, rating = $2 where customer_id = $3 and product_id = $4"
    await DB.execute(sql, body, rating, customer_id, product_id)
    return await update_product_dynamic_data(product_id)


async def update_product_dynamic_data(product_id: int):
    sql = "select sum(rating),count(customer_id) from review where product_id = $1"
    temp = await DB.fetchrow(sql, product_id)
    if temp['sum'] is None:
        temp = {'sum': 0, 'count': 1}
    sql = "update product set num_reviews = $2, avg_rating = $1 where id = $3"
    num_reviews = temp['count']
    avg_rating = temp['sum'] / temp['count']
    return await DB.execute(sql, avg_rating, num_reviews, product_id)


async def get_reviews_to_product(product_id: int, previous_id: int):
    sql = "select r.body, r.rating, c.name,r.id as previous_id from review as r join customer c on r.customer_id = c.id where product_id = $1 and r.id > $2 limit $3"
    return await DB.fetch(sql, product_id, previous_id, ITEMS_PER_PAGE)
