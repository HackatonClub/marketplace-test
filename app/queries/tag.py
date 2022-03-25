from app.db.db import DB
from app.db.redis import Redis
from app.exceptions import BadRequest, NotFoundException
from app.settings import ITEMS_PER_PAGE
from app.utils.extracter import get_col_values


async def add_new_tag(name: str):
    sql = "insert into tags (name) values ($1) ;"
    if not await DB.execute(sql, name):
        raise BadRequest('Тэг уже существует')


async def add_tag_to_product_by_id(tag_name: str, product_id: int):
    sql = 'insert into tags (name) values ($1) on conflict do nothing;'
    await DB.execute(sql, tag_name)
    tag_id = await get_tag_id(tag_name)
    sql = 'insert into tags_product(product_id, tag_id) values ($1,$2);'
    if not await DB.execute(sql, product_id, tag_id):
        raise BadRequest('Тэг уже присвоен или не существует такого продукта')
    await Redis.add_tag_to_product(tag_id,product_id)


async def remove_tag_from_product_by_id(tag_name: str, product_id: int):
    tag_id = await get_tag_id(tag_name)
    sql = 'delete from tags_product where product_id = $1 and tag_id = $2'
    if not await DB.execute(sql, product_id, tag_id):
        raise BadRequest('Тэг уже удалён')
    await Redis.remove_tag_from_product(tag_id,product_id)


async def remove_tag(tag_name: str):
    tag_id = await get_tag_id(tag_name)
    sql = 'delete from tags_product where tag_id = $1'
    await DB.execute(sql, tag_id)
    await Redis.del_tag(tag_id)
    sql = 'delete from tags where id = $1'
    await DB.execute(sql, tag_id)


async def get_all_tags(previous_id: int):
    sql = "select name,id as previous_id from tags where id > $1 limit $2"
    return await DB.fetch(sql, previous_id, ITEMS_PER_PAGE)


async def get_tags_of_product_by_id(product_id: int, previous_id: int):
    sql = """
        SELECT  tags.name,
                tags.id AS previous_id
        FROM tags_product
        JOIN tags ON tags.id = tags_product.tag_id
        WHERE tags_product.product_id = $1
          AND tags.id > $2
        LIMIT $3;"""
    return await DB.fetch(sql, product_id, previous_id, ITEMS_PER_PAGE)


async def get_products_by_tags(tags: list):
    if not tags:
        raise BadRequest('Множество тегов пусто')
    tag_ids = await get_multiple_tag_ids(tags)
    if not tag_ids:
        raise BadRequest('Тэги не найдены')
    product_ids = await Redis.get_product_ids_by_tags(tag_ids)
    sql = 'select * from product where id = ANY($1::int[])'
    return await DB.fetch(sql, product_ids)


async def get_tag_id(tag_name: str):
    tag_id = await Redis.get_hash(tag_name)
    if not tag_id:
        sql = 'select id from tags where name = $1'
        tag_id = await DB.fetchval(sql, tag_name)
    if not tag_id:
        raise NotFoundException('Тэг отсутсвует')
    await Redis.set_hash(tag_name, tag_id)
    return int(tag_id)

async def get_multiple_tag_ids(tag_names: list[str]):
    found = list()
    not_found = list()
    for i in tag_names:
        tag_id = await Redis.get_hash(i)
        if not tag_id:
            not_found.append(i)
        else:
            found.append(int(tag_id))
    if not_found:
        sql = 'select id,name from tags where name = ANY($1::text[])'
        tag_ids = await DB.fetch(sql, not_found)
        for i in tag_ids:
            found.append(int(i['id']))
            await Redis.set_hash(i['name'], i['id'])
    return found