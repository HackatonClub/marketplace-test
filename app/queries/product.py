from app.db.db import DB
from app.model import ProductAdd, ProductUp

async def add_product(product: ProductAdd):

    sql = f""" insert into product(name,description,price,avg_rating,num_reviews) 
                                values ($1,$2,$3,0,0) """
    await DB.execute(sql,product.name,product.discription,product.price)


async def delete_product(product_id: int):
    sql = f""" delete from product where id = {product_id}  """
    await DB.execute(sql)


async def update_product (product: ProductUp):
    sql = 'update product set name = $1 , description = $2 , price = $3 where id = $4  '
    return await DB.execute(sql,product.name,product.discription, product.price,product.id)

