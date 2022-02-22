from app.db.db import DB
from app.model import ProductAdd

async def add_product(product: ProductAdd):

    sql = f""" insert into product(name,description,price,avg_rating,num_reviews) 
                                values ($1,$2,$3,0,0) """
    await DB.execute(sql,product.name,product.discription,product.price)

