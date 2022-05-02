from typing import Optional

from fastapi import Query
from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    login: Optional[str] = None


class User(BaseModel):
    login: str
    password: str


class UserDelete(BaseModel):
    login: str


class Tag(BaseModel):
    tag_name: str = Field(None, title='Имя тэга')


class Product(BaseModel):
    product_id: int = Field(None, title='ID продукта', gt=0)


class Cart(BaseModel):
    product_id: int = Field(None, title='ID продукта', gt=0)
    product_num: int = Field(1, title='Кол-во продуктов', gt=0)


class CartDelete(BaseModel):
    product_id: int = Field(None, title='ID продукта', gt=0)


class Favourite(BaseModel):
    product_id: int = Field(None, title='ID продукта', gt=0)


class ProductUp(BaseModel):
    product_id: int = Query(None, title='Id продукта', gt=0)
    name: str = Field(None, title='Название продукта')
    discription: str = Field(None, title='Описание продукта')
    price: int = Field(None, title='Цена продукта', gt=0)
    urls: dict = Field(None, title='photoid : image_name')


class Review(BaseModel):
    product_id: int = Field(None, description='ID продукта', gt=0)
    body: str = Field(None, description='Тело отзыва')
    rating: int = Field(None, description='Рейтинг', ge=1, le=5)
