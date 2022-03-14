class NotFoundException(Exception):
    def __init__(self, error: str):
        self.error = error


class CustomerNotFoundException(NotFoundException):
    def __init(self, error: str = 'Нет такого покупателя'):
        self.error = error


class InternalServerError(Exception):
    def __init__(self, error: str):
        self.error = error


class BadRequest(Exception):
    def __init__(self, error: str):
        self.error = error