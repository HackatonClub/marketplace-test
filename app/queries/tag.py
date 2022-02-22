from app.db.db import DB


async def add_new_tag(name: str):
    sql = "insert into tags (name) values ($1) ;"
    return await DB.execute(sql, name)


async def add_tag_to_product_by_id(tag_name: str, product_id: int):
    sql = 'insert into tags (name) values ($1) on conflict do nothing;'
    await DB.execute(sql, tag_name)
    sql = 'select id from tags where name = $1;'
    customer_id = (await DB.fetchrow(sql, tag_name))['id']
    if not customer_id:
        return False
    sql = 'insert into tags_product(product_id, tag_id) values ($1,$2);'
    return await DB.execute(sql, product_id, customer_id)


async def remove_tag_from_product_by_id(tag_name: str, product_id: int):
    sql = 'delete from tags_product where product_id = $1 and tag_id in (select id from tags where name = $2)'
    return await DB.execute(sql, product_id, tag_name)


async def remove_tag(tag_name: str):
    customer_id = None
    sql = 'select id from tags where name = $1'
    customer_id = (await DB.fetchrow(sql, tag_name))['id']
    sql = 'delete from tags_product where tag_id = $1'
    await DB.execute(sql, customer_id)
    sql = 'delete from tags where id = $1'
    return await DB.execute(sql, customer_id)


async def get_all_tags():
    sql = "select name from tags"
    return await DB.fetch(sql)


async def get_tags_of_product_by_id(id: int):
    sql = "select tags.name from tags_product join tags on tags.id = tags_product.tag_id where tags_product.product_id = $1;"
    return await DB.fetch(sql, id)
