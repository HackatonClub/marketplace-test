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
    