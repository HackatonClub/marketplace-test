from app.db.db import DB




async def check_product(product_id: int):
    sql = f"SELECT id FROM product WHERE id = {product_id}"
    try:

        id = await DB.con.fetchrow(sql)

        if not id :
           return True

        return False

    except Exception as er:
        print(er)
        return False


async def add_photo(product_id : int , url : str):
    sql = f"""Insert into product_photo (product_id, url) values ('{product_id}' , '{url}'); """
    await DB.con.execute(sql)


async def get_all_name_photo(product_id : int):
    sql = f""" SELECT url from product_photo where product_id = {product_id}"""
    photo_name = await DB.con.fetch(sql)
    return photo_name

async def delete_photo_by_name(product_id : int , url : str):
    sql = f""" DELETE from product_photo where product_id = {product_id} and url = '{url}' """
    await DB.con.execute(sql)
    
    