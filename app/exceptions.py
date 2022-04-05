class NotFoundException(Exception):
    def __init__(self, error: str) -> None:
        super().__init__()
        self.error = error


class CustomerNotFoundException(NotFoundException):
    def __init__(self) -> None:
        super().__init__('Нет такого покупателя')


class InternalServerError(Exception):
    def __init__(self, error: str) -> None:
        super().__init__()
        self.error = error


class BadRequest(Exception):
    def __init__(self, error: str) -> None:
        super().__init__()
        self.error = error

class ForbiddenException(Exception):
    def __init__(self, error: str = 'Forbidden') -> None:
        super().__init__()
        self.error = error
