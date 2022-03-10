from app.db.db import DB
from app.model import User


async def check_login(login: str):
    sql = f"""   SELECT id
                FROM customer
                WHERE name = '{login}';"""
    userlogin = await DB.fetchrow(sql)
    return userlogin


async def create_user(user: User):

    sql = f"""  INSERT INTO customer (name, password)
                VALUES ('{user.login}','{user.password}');  """

    await DB.execute(sql)
