
from app.db.db import DB
from app.model import ProductUp
import json


async def add_product(name: str, description: str, price: int, tag_id: dict, urls: dict):

    sql = """  INSERT INTO product(name, description, price, avg_rating, num_reviews, url ,tag_id)
                VALUES ($1,$2,$3,0,0, $4 ::jsonb, $5 ::jsonb)  returning id"""
    return await DB.fetchval(sql, name, description, price, json.dumps(urls), json.dumps(tag_id))


async def delete_product(product_id: int):

    sql = f"""  DELETE
                FROM product
                WHERE id = {product_id} """

    await DB.execute(sql)


async def update_product(prod: ProductUp):
    sql = '''  UPDATE product
                SET name = coalesce($1, name),
                    description = coalesce($2, description),
                    price = coalesce($3, price),
                    url = coalesce( NULLIF($4, 'null' ::jsonb), url ),
                    tag_id  = coalesce( NULLIF($5, 'null' :: jsonb), tag_id)
                WHERE product.id =$6; '''
    return await DB.execute(sql, prod.name, prod.discription, prod.price,
                            json.dumps(prod.urls), json.dumps(prod.tag_id), prod.product_id)


async def get_info_product(product_id: int):
    sql = """   SELECT
                    product.name,
                    product.description,
                    product.price,
                    product.avg_rating,
                    product.num_reviews,
                    product.url,
                    product.tag_id
                FROM product
                WHERE product.id=$1;"""
    return await DB.fetchrow(sql, product_id)
