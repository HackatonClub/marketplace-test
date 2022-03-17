
from app.db.db import DB
from app.model import ProductUp


async def add_product(name: str, description: str, price: int, tag_id: dict, urls: dict):

    sql = """  INSERT INTO product(name, description, price, avg_rating, num_reviews, url ,tag_id)
                VALUES ($1,$2,$3,0,0, $4 ::json, $5 ::json)  """
    await DB.execute(sql, name, description, price, urls, tag_id)


async def delete_product(product_id: int):

    sql = f"""  DELETE
                FROM product
                WHERE id = {product_id} """

    await DB.execute(sql)


async def update_product(product: ProductUp):
    sql = """UPDATE product
             SET name = $1,
                 description = $2,
                 price = $3
             WHERE id = $4  """
    return await DB.execute(sql, product.name, product.discription, product.price, product.product_id)


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
