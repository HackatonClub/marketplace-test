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

    sql = f"""  SELECT url
                FROM product_photo
                WHERE product_id = {product_id}"""

    photo_name = await DB.fetchrow(sql)
    return photo_name


async def delete_photo_by_name(product_id: int, url: str):

    sql = f"""  DELETE
                FROM product_photo
                WHERE product_id = {product_id}
                  AND url = '{url}'"""

    await DB.execute(sql)
