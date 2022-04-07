from asyncpg import Record
from app.db.db import DB
from app.db.redis import Redis
from app.queries.product import get_info_product
from app.utils.extracter import prepare_search_query, get_col_values
from app.exceptions import BadRequest, NotFoundException
from app.settings import ITEMS_PER_PAGE


async def add_new_tag(name: str) -> None:
    sql = """  INSERT INTO tags (name)
               VALUES ($1) ;"""
    if not await DB.execute(sql, name):
        raise BadRequest('Тэг уже существует')


async def add_tag_to_product_by_id(tag_name: str, product_id: int) -> None:
    sql = '''  INSERT INTO tags (name)
               VALUES ($1)
               ON CONFLICT DO NOTHING;'''
    await DB.execute(sql, tag_name)
    tag_id = await get_tag_id(tag_name)
    sql = '''  INSERT INTO tags_product(product_id, tag_id)
               VALUES ($1,$2);'''
    if not await DB.execute(sql, product_id, tag_id):
        raise BadRequest('Тэг уже присвоен или не существует такого продукта')
    await Redis.add_tag_to_product(tag_id, product_id)


async def add_tags_to_product_by_id(tag_names: list[str], product_id: int) -> None:
    sql = '''  INSERT INTO tags (name)
               VALUES ($1)
               ON CONFLICT DO NOTHING;'''
    add_tags = [(x,) for x in tag_names]
    await DB.executemany(sql, add_tags)
    tag_ids = await get_multiple_tag_ids(tag_names)
    tags_products = [(product_id, x) for x in tag_ids]
    sql = '''  INSERT INTO tags_product(product_id, tag_id)
               VALUES ($1,$2);'''
    if not await DB.executemany(sql, tags_products):
        raise BadRequest('Тэг уже присвоен или не существует такого продукта')
    await Redis.add_tags_to_product(tag_ids, product_id)


async def remove_tag_from_product_by_id(tag_name: str, product_id: int) -> None:
    tag_id = await get_tag_id(tag_name)
    sql = '''  DELETE FROM tags_product
               WHERE product_id = $1 AND tag_id = $2'''
    if not await DB.execute(sql, product_id, tag_id):
        raise BadRequest('Тэг уже удалён')
    await Redis.remove_tag_from_product(tag_id, product_id)


async def remove_tag(tag_name: str) -> None:
    tag_id = await get_tag_id(tag_name)
    sql = '''  DELETE FROM tags_product
               WHERE tag_id = $1'''
    await DB.execute(sql, tag_id)
    sql = '''  DELETE FROM tags
               WHERE id = $1'''
    await DB.execute(sql, tag_id)
    await Redis.del_tag(tag_name)


async def get_all_tags(previous_id: int) -> list[Record]:
    sql = """  SELECT name,id AS previous_id
               FROM tags
               WHERE id > $1
               LIMIT $2"""
    return await DB.fetch(sql, previous_id, ITEMS_PER_PAGE)


async def get_tags_of_product_by_id(product_id: int, previous_id: int) -> list[Record]:
    sql = """  SELECT  tags.name,tags.id AS previous_id
               FROM tags_product
               JOIN tags ON tags.id = tags_product.tag_id
               WHERE tags_product.product_id = $1 AND tags.id > $2
               LIMIT $3;"""
    return await DB.fetch(sql, product_id, previous_id, ITEMS_PER_PAGE)


async def search_products(tags: list, search_query: str, current_user: str) -> list[Record]:
    prepared_query = prepare_search_query(search_query)
    sql = """  SELECT id
               FROM product
               WHERE to_tsvector(description) @@ to_tsquery($1)
               OR to_tsvector(name) @@ to_tsquery($1);"""
    product_ids_search = set(get_col_values(await DB.fetch(sql, prepared_query), 'id'))
    product_ids_tags = product_ids_search
    if tags:
        tag_ids = await get_multiple_tag_ids(tags)
        if tag_ids:
            if not Redis.check_connection():
                sql = '''  WITH ids AS
                           (SELECT product_id,count(tag_id)
                             FROM tags_product AS t
                             WHERE t.tag_id = ANY($1::int[])
                             GROUP BY product_id)
                           SELECT p.id
                           FROM product AS p
                           JOIN ids ON p.id = ids.product_id
                           WHERE ids.count = $2'''
                product_ids_tags = set(get_col_values(await DB.fetch(sql, tag_ids, len(tags)), 'id'))
            else:
                product_ids_tags = set(await Redis.get_product_ids_by_tags(tag_ids))
    if not product_ids_tags:
        product_ids_tags = product_ids_search
    product_ids = product_ids_search.intersection(product_ids_tags)
    return await get_info_product(product_ids, current_user)


async def get_tag_id(tag_name: str) -> int:
    tag_id = await Redis.get_hash(tag_name)
    if not tag_id:
        sql = '''  SELECT id
                   FROM tags
                   WHERE name = $1'''
        tag_id = await DB.fetchval(sql, tag_name)
        if not tag_id:
            raise NotFoundException('Тэг отсутсвует')
    await Redis.set_hash(tag_name, tag_id)
    return int(tag_id)


async def get_multiple_tag_ids(tag_names: list[str]) -> list[int]:
    found = []
    not_found = []
    for i in tag_names:
        tag_id = await Redis.get_hash(i)
        if not tag_id:
            not_found.append(i)
        else:
            found.append(int(tag_id))
    if not_found:
        sql = '''  SELECT id,name
                   FROM tags
                   WHERE name = ANY($1::text[])'''
        tag_ids = await DB.fetch(sql, not_found)
        for i in tag_ids:
            found.append(int(i['id']))
            await Redis.set_hash(i['name'], i['id'])
    return found
