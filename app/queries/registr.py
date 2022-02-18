from app.db.db import DB
from app.model import User


async def check_login(login: str):
    userlogin = await DB.con.fetchrow(f"""
                SELECT id FROM customer WHERE name = '{login}';
    """)
    return userlogin


async def create_user(User: User):
    await DB.con.execute(f'''
          INSERT INTO customer (name,password) VALUES ('{User.login}','{User.password}');
    ''')
