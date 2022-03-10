from fastapi import status, HTTPException

from app.db.db import DB
from app.settings import ITEMS_PER_PAGE
from app.utils.extracter import get_col_values


async def add_new_tag(name: str):
    sql = "insert into tags (name) values ($1) ;"
    return await DB.execute(sql, name)


async def add_tag_to_product_by_id(tag_name: str, product_id: int):
    sql = 'insert into tags (name) values ($1) on conflict do nothing;'
    await DB.execute(sql, tag_name)
    tag_id = await get_tag_id(tag_name)
    if not tag_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Нет такого тэга'
        )
    sql = 'insert into tags_product(product_id, tag_id) values ($1,$2);'
    return await DB.execute(sql, product_id, tag_id)


async def remove_tag_from_product_by_id(tag_name: str, product_id: int):
    sql = 'delete from tags_product where product_id = $1 and tag_id in (select id from tags where name = $2)'
    return await DB.execute(sql, product_id, tag_name)


async def remove_tag(tag_name: str):
    tag_id = await get_tag_id(tag_name)
    if not tag_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Нет такого тэга'
        )
    sql = 'delete from tags_product where tag_id = $1'
    await DB.execute(sql, tag_id)
    sql = 'delete from tags where id = $1'
    return await DB.execute(sql, tag_id)


async def get_all_tags(previous_id: int):
    sql = "select name,id as previous_id from tags where id > $1 limit $2"
    return await DB.fetch(sql, previous_id, ITEMS_PER_PAGE)


async def get_tags_of_product_by_id(id: int, previous_id: int):
    sql = """
        SELECT  tags.name,
                tags.id AS previous_id
        FROM tags_product
        JOIN tags ON tags.id = tags_product.tag_id
        WHERE tags_product.product_id = $1
          AND tags.id > $2
        LIMIT $3;"""
    return await DB.fetch(sql, id, previous_id, ITEMS_PER_PAGE)


async def get_products_by_tags(tags: list, previous_id: int):
    if not tags:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Нет такого тэга'
        )
    sql = "select id from tags where name = ANY($1::text[])"
    tag_ids = get_col_values(await DB.fetch(sql, tags), 'id')
    sql = """
            WITH ids AS
              (SELECT product_id,
                        count(tag_id)
                FROM tags_product AS t
                WHERE t.tag_id = ANY($1::int[])
                GROUP BY product_id)
            SELECT p.name,
                   p.id AS previous_id
            FROM product AS p
            JOIN ids ON p.id = ids.product_id
            WHERE ids.count = $2
              AND p.id > $3
            LIMIT $4;"""
    return await DB.fetch(sql, tag_ids, len(tags), previous_id, ITEMS_PER_PAGE)


async def get_tag_id(tag_name: str):
    sql = 'select id from tags where name = $1'
    return await DB.fetchval(sql, tag_name)
