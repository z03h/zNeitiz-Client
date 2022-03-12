

class NeitizException(Exception):
    pass


class NeitizHTTPException(NeitizException):
    def __init__(self, status: int, message: str):
        self.stats = status
        self.message = message


class NeitizServerException(NeitizException):
    def __init__(self, status: int, message: str):
        self.stats = status
        self.message = message