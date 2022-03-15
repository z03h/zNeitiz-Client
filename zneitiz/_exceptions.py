

class NeitizException(Exception):
    def __init__(self, message: str):
        self.message: str = message


class NeitizHTTPException(NeitizException):
    def __init__(self, status: int, message: str):
        self.status: int = status
        self.message: str = message


class NeitizRatelimitException(NeitizHTTPException):
    def __init__(self, status: int, message: str, *, headers: dict[str, str]):
        super().__init__(status, message)
        self.ratelimit_reset: float = float(headers.get('x-ratelimit-resest', -1.0))
        self.limit: int = int(headers.get('x-ratelimit-limit', -1))
        self.remaining: int = int(headers.get('x-ratelimit-remaining', -1))


class NeitizServerException(NeitizHTTPException):
    def __init__(self, status: int, message: str):
        self.status: int = status
        self.message: str = message
