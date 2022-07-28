from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Mapping

__all__ = (
    'NeitizException',
    'NeitizHTTPException',
    'NeitizRatelimitException',
    'NeitizServerException',
)


class NeitizException(Exception):
    def __init__(self, message: str):
        self.message: str = message

    def __str__(self):
        return self.message


class NeitizHTTPException(NeitizException):
    def __init__(self, message: str, status: int):
        self.status: int = status
        self.message: str = message

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} status={self.status}>'


class NeitizRatelimitException(NeitizHTTPException):
    def __init__(self, message: str, status: int, *, headers: Mapping[str, str]):
        super().__init__(message, status)
        self.ratelimit_reset: float = float(headers.get('x-ratelimit-reset', -1.0))
        self.limit: int = int(headers.get('x-ratelimit-limit', -1))
        self.remaining: int = int(headers.get('x-ratelimit-remaining', -1))

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} status={self.status} ratelimit-reset={self.ratelimit_reset}>'


class NeitizServerException(NeitizHTTPException):
    pass
