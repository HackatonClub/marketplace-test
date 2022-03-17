from app.db.db import DB


async def check_product(product_id: int):

    sql = f""" SELECT id
               FROM product
               WHERE id = {product_id}"""

    try:

        prod_id = await DB.fetchrow(sql)

        if not prod_id:
            return True

        return False

    except Exception as error:
        print(error)
        return False


async def add_photo(product_id: int, url: dict):

    sql = """  INSERT INTO product_photo (product_id, url)
                VALUES ($1, $2 ::json ); """
    return await DB.execute(sql, product_id, url)


async def get_all_name_photo(product_id: int):

    sql = """  SELECT url
                FROM product
                WHERE product.id = $1"""

    photo_name = await DB.fetchrow(sql, product_id)
    return photo_name


async def delete_photo_by_name(product_id: int, key: str):

    sql = """select product.url ->$1 from product where id=$2;"""
    image_name = await DB.fetchval(sql, key, product_id)
    sql = """  UPDATE product
                SET url = url - $1
                WHERE id=$2;"""

    await DB.execute(sql, key, product_id)
    return image_name
