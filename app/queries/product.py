import json
from asyncpg import Record

from app.db.db import DB
from app.model import ProductUp
from app.exceptions import BadRequest
from app.queries.customer import get_customer_id


async def add_product(name: str, description: str, price: int, tag_id: dict, urls: dict) -> int:

    sql = """  INSERT INTO product(name, description, price, avg_rating, num_reviews, url ,tag_id)
                VALUES ($1,$2,$3,0,0, $4 ::jsonb, $5 ::jsonb)  returning id"""
    return await DB.fetchval(sql, name, description, price, json.dumps(urls), json.dumps(tag_id))


async def delete_product(product_id: int) -> None:

    sql = f"""  DELETE
                FROM product
                WHERE id = {product_id} """

    await DB.execute(sql)


async def update_product(prod: ProductUp) -> None:
    sql = '''  UPDATE product
                SET name = coalesce($1, name),
                    description = coalesce($2, description),
                    price = coalesce($3, price),
                    url = coalesce( NULLIF($4, 'null' ::jsonb), url )
                WHERE product.id = $5; '''
    if not await DB.execute(sql, prod.name, prod.discription, prod.price, json.dumps(prod.urls), prod.product_id):
        raise BadRequest('Такого продукта не существует')


async def get_info_product(product_id: list, login: str) -> list[Record]:
    customer_id = await get_customer_id(login)
    sql = """SELECT
                product.id,
                product.name,
                product.description,
                product.price,
                product.avg_rating,
                product.num_reviews,
                product.url,
                product.tag_id,
                CASE
                    WHEN favourite.product_id = product.id THEN 'Yes'
                    ELSE 'No'
                END AS Love
            FROM product
            LEFT JOIN favourite ON favourite.customer_id = $2
            AND favourite.product_id = product.id
            WHERE product.id= ANY($1::int[])"""
    return await DB.fetch(sql, product_id, customer_id)
