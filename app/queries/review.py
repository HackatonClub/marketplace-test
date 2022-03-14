from app.db.db import DB
from app.exceptions import (BadRequest, CustomerNotFoundException,
                            NotFoundException)
from app.queries.customer import get_customer_id
from app.settings import ITEMS_PER_PAGE

# TODO: Добавить динамику в добавление и удаление, но тогда код станет менее стабильным


async def add_review_to_product(customer_name: str, product_id: int, body: str, rating: int):
    customer_id = await get_customer_id(customer_name)
    if not customer_id:
        raise CustomerNotFoundException
    sql = "insert into review(product_id, customer_id, body, rating) VALUES ($1,$2,$3,$4)"
    await DB.execute(sql, product_id, customer_id, body, rating)
    await update_product_dynamic_data(product_id)


async def delete_review_from_product(customer_name: str, product_id: int):
    customer_id = await get_customer_id(customer_name)
    if not customer_id:
        raise CustomerNotFoundException
    sql = "delete from review where customer_id = $1 and product_id = $2"
    await DB.execute(sql, customer_id, product_id)
    if not update_product_dynamic_data(product_id):
        raise NotFoundException('Отзыв уже удалён')


async def update_review_to_product(customer_name: str, product_id: int, body: str, rating: int):
    customer_id = await get_customer_id(customer_name)
    if not customer_id:
        raise CustomerNotFoundException
    sql = "update review set body = $1, rating = $2 where customer_id = $3 and product_id = $4"
    if not await DB.execute(sql, body, rating, customer_id, product_id):
        raise BadRequest('Нет такого продукта')
    await update_product_dynamic_data(product_id)


async def update_product_dynamic_data(product_id: int):
    sql = "select sum(rating),count(customer_id) from review where product_id = $1"
    temp = await DB.fetchrow(sql, product_id)
    if temp['sum'] is None:
        temp = {'sum': 0, 'count': 1}
    sql = "update product set num_reviews = $2, avg_rating = $1 where id = $3"
    num_reviews = temp['count']
    avg_rating = temp['sum'] / temp['count']
    if not await DB.execute(sql, avg_rating, num_reviews, product_id):
        raise BadRequest('Нет такого продукта')


async def get_reviews_to_product(product_id: int, previous_id: int):
    sql = """   SELECT r.body,
                       r.rating,
                       c.name,
                       r.id AS previous_id
                FROM review AS r
                JOIN customer c ON r.customer_id = c.id
                WHERE product_id = $1
                AND r.id > $2
                LIMIT $3"""
    return await DB.fetch(sql, product_id, previous_id, ITEMS_PER_PAGE)
