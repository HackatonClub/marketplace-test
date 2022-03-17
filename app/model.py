from typing import Optional, List

from fastapi import File, Form, Query, UploadFile
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


class Customer(BaseModel):
    name: str = Field(None, title='Имя покупателя')


class CutomerNew(Customer):
    password: str = Field(None, title='Пароль покупателя')


class Tag(BaseModel):
    tag_name: str = Field(None, title='Имя тэга')


class Product(BaseModel):
    product_id: int = Field(None, title='ID продукта', gt=0)


class Cart(BaseModel):
    product_id: int = Field(None, title='ID продукта', gt=0)
    product_num: int = Field(1, title='Кол-во продуктов', gt=0)
    customer_name: str = Field(None, title='Имя покупателя')


class CartDelete(BaseModel):
    product_id: int = Field(None, title='ID продукта', gt=0)
    customer_name: str = Field(None, title='Имя покупателя')


class Favourite(BaseModel):
    product_id: int = Field(None, title='ID продукта', gt=0)
    customer_name: str = Field(None, title='Имя покупателя')


class FavouriteOfUser(BaseModel):
    customer_name: str = Field(None, title='Имя покупателя')


class ProductAdd(BaseModel):
    name: str = Form(None, title='Название продукта', max_length=50)
    discription: str = Form(None, title='Описание продукта', max_length=350)
    price: int = Form(None, title='Цена продукта', gt=0)
    tag_id: str = Form(None, title='Тэги продукта')
    files: List[UploadFile] = File(...)


class ProductUp(BaseModel):
    product_id: int = Query(None, title='Id продукта', gt=0)
    name: str = Field(None, title='Название продукта')
    discription: str = Field(None, title='Описание продукта')
    price: int = Field(None, title='Цена продукта', gt=0)


class Review(BaseModel):
    product_id: int = Field(None, description='ID продукта', gt=0)
    customer_name: str = Field(None, description='Имя покупателя')
    body: str = Field(None, description='Тело отзыва')
    rating: int = Field(None, description='Рейтинг', ge=1, le=5)
