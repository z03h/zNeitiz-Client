
from __future__ import annotations

from typing import (
    Optional,
    Any
)

__all__ = ('Route',)


class Route:
    BASE_URL: str = 'https://zneitiz.herokuapp.com/image/'

    def __init__(
        self,
        endpoint: str,
        *,
        headers: dict[str, str],
        json: Optional[dict[Any, Any]] = None,
    ):
        self.endpoint: str = endpoint
        self.headers: dict[str, str] = headers
        self.json: dict[str, Any] = json

    @property
    def url(self) -> str:
        return self.BASE_URL + self.endpoint

    def __repr__(self) -> str:
        return f'<Route endpoint={self.endpoint}>'

    def __str__(self) -> str:
        return self.url
