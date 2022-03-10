class NotFoundException(Exception):
    def __init__(self, error: str):
        self.error = error


class ServerException(Exception):
    def __init__(self, error: str):
        self.error = error
