from asyncpg import Record

from app.db.db import DB
from app.model import User


async def check_auth(login: str) -> Record:
    sql = """   SELECT id,name,password
                FROM users
                WHERE name = $1;"""
    return await DB.fetchrow(sql, login)


async def create_user(user: User) -> None:

    sql = f"""  INSERT INTO users (name, password,role)
                VALUES ('{user.login}','{user.password}',0);  """

    await DB.execute(sql)
