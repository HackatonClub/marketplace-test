from asyncpg import Record

from app.db.db import DB
from app.model import User


async def check_login(login: str) -> Record:
    sql = f"""   SELECT id
                FROM customer
                WHERE name = '{login}';"""
    userlogin = await DB.fetchrow(sql)
    return userlogin


async def create_user(user: User) -> None:

    sql = f"""  INSERT INTO customer (name, password)
                VALUES ('{user.login}','{user.password}');  """

    await DB.execute(sql)
