from app.db.db import DB


async def add_new_tag(name: str):
    sql = "insert into tags (name) values ($1) ;"
    try:
        await DB.con.execute(sql, name)
    except Exception as e:
        print(e)
        return False
    return True


async def add_tag_to_product_by_id(tag_name: str, product_id: int):
    customer_id = None
    sql = 'insert into tags (name) values ($1) on conflict do nothing;'
    try:
        await DB.con.execute(sql, tag_name)
    except Exception as er:
        print(er)
        return False
    sql = 'select id from tags where name = $1;'
    try:
        customer_id = (await DB.con.fetchrow(sql, tag_name))['id']
    except Exception as er:
        print(er)
        return False
    if not customer_id:
        return False
    sql = 'insert into tags_product(product_id, tag_id) values ($1,$2);'
    try:
        await DB.con.execute(sql, product_id, customer_id)
    except Exception as er:
        print(er)
        return False
    return True


async def remove_tag_from_product_by_id(tag_name: str, product_id: int):
    sql = 'delete from tags_product where product_id = $1 and tag_id in (select id from tags where name = $2)'
    try:
        await DB.con.execute(sql, product_id, tag_name)
    except Exception as er:
        print(er)
        return False
    return True


async def remove_tag(tag_name: str):
    customer_id = None
    sql = 'select id from tags where name = $1'
    try:
        customer_id = (await DB.con.fetchrow(sql, tag_name))['id']
    except Exception as er:
        print(er)
        return False
    sql = 'delete from tags_product where tag_id = $1'
    try:
        await DB.con.execute(sql, customer_id)
    except Exception as er:
        print(er)
        return False
    sql = 'delete from tags where id = $1'
    try:
        await DB.con.execute(sql, customer_id)
    except Exception as er:
        print(er)
        return False
    return True


async def get_all_tags():
    sql = "select name from tags"
    try:
        return await DB.con.fetch(sql)
    except Exception as er:
        print(er)
        return False


async def get_tags_of_product_by_id(id: int):
    sql = "select tags.name from tags_product join tags on tags.id = tags_product.tag_id where tags_product.product_id = $1;"
    try:
        return await DB.con.fetch(sql, id)
    except Exception as e:
        print(e)
        return False
