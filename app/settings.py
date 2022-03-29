import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv("local.env")

DATABASE_URL: str = os.getenv("DATABASE_URL")
REDIS_HOSTNAME: str = os.getenv('REDIS_HOSTNAME')
REDIS_PORT: str = os.getenv('REDIS_PORT')
REDIS_PASSWORD: str = os.getenv('REDIS_PASSWORD')

SECRET_KEY: str = os.getenv("SECRET_KEY")
ALGORITHM: str = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
ITEMS_PER_PAGE: int = int(os.getenv('ITEMS_PER_PAGE'))
HASH_EXPIRE: timedelta = timedelta(minutes=5)
