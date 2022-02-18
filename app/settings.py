import os
from dotenv import load_dotenv


load_dotenv("local.env")

DB_DATABASE:  str = os.getenv('DB_DATABASE')
DB_HOST:      str = os.getenv('DB_HOST')
DB_PORT:      str = os.getenv('DB_PORT')
DB_USER:      str = os.getenv('DB_USER')
DB_PASSWORD:  str = os.getenv('DB_PASSWORD')

DATABASE_URL: str = os.getenv("DATABASE_URL")

SECRET_KEY: str = os.getenv("SECRET_KEY")
ALGORITHM: str = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))