from app.db.db import DB
from app.model import ProductAdd, ProductUp


async def add_product(product: ProductAdd):

    sql = """  INSERT INTO product(name, description, price, avg_rating, num_reviews)
                VALUES ($1,$2,$3,0,0)  """
    await DB.execute(sql, product.name, product.discription, product.price)


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
    sql = """ SELECT array
                (SELECT url
                FROM product_photo
                WHERE product_photo.product_id=$1) AS image,
                    array
                (SELECT tag_id
                FROM tags_product
                WHERE tags_product.product_id=$1) AS tags_id,
                    product.name,
                    product.description,
                    product.price,
                    product.avg_rating,
                    product.num_reviews
                FROM product
                WHERE product.id=3"""
    return await DB.fetch(sql, product_id)
