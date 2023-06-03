from fastapi import status
from typing import Any, Mapping, Optional
from fastapi import status

class CommonException(Exception):
    def __init__(self, code: int, error: str) -> None:
        super().__init__()
        self.error = error
        self.code = code


class NotFoundException(CommonException):
    def __init__(self, error: str) -> None:
        super().__init__(status.HTTP_404_NOT_FOUND, error)


class ProductFileNotFoundException(NotFoundException):
    def __init__(self) -> None:
        super().__init__('Файл не существуе')


class CustomerNotFoundException(NotFoundException):
    def __init__(self) -> None:
        super().__init__('Нет такого покупателя')


class InternalServerError(Exception):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    message  = 'Упс! Что-то пошло не так ;('

    def __init__(self, message: Optional[str] = None, debug: Any = None) -> None:
        self.message = message or self.message
        self.debug = debug

    @classmethod
    def code(cls):
        return cls.__name__

    def to_json(self) -> Mapping:
        return {
            'code': self.status_code,
            'message': self.message,
            'debug': self.debug,
        }


class BadRequest(CommonException):
    def __init__(self, error: str) -> None:
        super().__init__(status.HTTP_400_BAD_REQUEST, error)


class ForbiddenException(CommonException):
    def __init__(self) -> None:
        super().__init__(status.HTTP_403_FORBIDDEN, "Forbidden")
        

class ReviewException(CommonException):
    def __init__(self) -> None:
        super().__init__(status.HTTP_400_BAD_REQUEST, "U have review")
