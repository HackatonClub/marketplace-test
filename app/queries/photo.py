from asyncpg import Record

from app.db.db import DB


async def add_photo(product_id: int, url: dict) -> None:

    sql = """  INSERT INTO product_photo (product_id, url)
                VALUES ($1, $2 ::json ); """
    return await DB.execute(sql, product_id, url)


async def get_all_name_photo(product_id: int) -> list[Record]:

    sql = """  SELECT url
                FROM product
                WHERE product.id = $1"""

    photo_name = await DB.fetch(sql, product_id)
    return photo_name


async def delete_photo_by_name(product_id: int, key: str) -> None:

    sql = """SELECT product.url ->$1 FROM product WHERE id=$2;"""
    image_name = await DB.fetchval(sql, key, product_id)
    sql = """  UPDATE product
                SET url = url - $1
                WHERE id=$2;"""

    await DB.execute(sql, key, product_id)
    return image_name


async def get_name_photo_for_delete(product_id: int) -> list[Record]:

    sql = """  SELECT url
                FROM product
                WHERE product.id = $1"""

    photo_name = await DB.fetchval(sql, product_id)
    return photo_name
