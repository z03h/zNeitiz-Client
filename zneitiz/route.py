
from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Optional,
    Any
)

from .image import NeitizImage
from ._exceptions import (
    NeitizException,
    NeitizHTTPException,
    NeitizServerException,
    NeitizRatelimitException,
)


if TYPE_CHECKING:
    import aiohttp

__all__ = ('Route',)


class Route:
    BASE_URL: str = 'https://zneitiz.herokuapp.com/image/'

    def __init__(
        self,
        endpoint: str,
        *,
        headers: dict[str, str],
        json: Optional[dict[Any, Any]] = None,
        session: Optional[aiohttp.ClientSession]
    ):
        self.endpoint: str = endpoint
        self.headers: dict[str, str] = headers
        self.json: dict[str, Any] = json
        self.__session = session

    @property
    def url(self) -> str:
        return self.BASE_URL + self.endpoint

    def __repr__(self) -> str:
        return f'<Route endpoint={self.endpoint}>'

    def __str__(self) -> str:
        return self.url

    def __aenter__(self):
        if not self.__session or self.__session.closed:
            raise NeitizException('session is not valid')

        url = self.url
        headers = self.headers
        body = self.json

        return self.__session.get(url, headers=headers, json=body)

    def __await__(self):
        return self.__request().__await__()

    async def __request(self) -> NeitizImage:
        if not self.__session or self.__session.closed:
            raise NeitizException('session is not valid')

        url = self.url
        headers = self.headers
        body = self.json

        async with self.__session.get(url, headers=headers, json=body) as r:
            data: bytes = await r.read()

            status = int(r.status)
            if 200 <= status < 300:
                # OK
                content_type: str = r.content_type
                file = NeitizImage(data, content_type=content_type, route=self)
                return file
            elif 500 <= status < 600:
                # server error
                raise NeitizServerException(status, r.reason)
            elif status == 429:
                # ratelimited
                raise NeitizRatelimitException(status, r.reason, r.headers)
            else:
                raise NeitizHTTPException(status, r.reason)
