class NotFoundException(Exception):
    def __init__(self, error: str):
        super().__init__()
        self.error = error


class CustomerNotFoundException(NotFoundException):
    def __init__(self):
        super().__init__('Нет такого покупателя')


class InternalServerError(Exception):
    def __init__(self, error: str):
        super().__init__()
        self.error = error


class BadRequest(Exception):
    def __init__(self, error: str):
        super().__init__()
        self.error = error
