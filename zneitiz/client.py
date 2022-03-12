
from __future__ import annotations

import io
import math
from typing import (
    TYPE_CHECKING,
    Optional,
    Union,
    Coroutine,
    Any
)
try:
    import orjson as json
except ModuleNotFoundError:
    import json

import aiohttp

from ._exceptions import NeitizHTTPException, NeitizServerException

from .route import Route

if TYPE_CHECKING:
    from ._enums import ParticleType

__all__ = ('NeitizClient',)


class NeitizClient:

    URL = 'https://zneitiz.herokuapp.com/'

    def __init__(
        self,
        token: str,
        *,
        session: Optional[aiohttp.ClientSession] = ...,
    ):
        self._token: str = token
        self.headers: dict[str, str] = {
            'Authorization': f'Bearer {token}',
        }

        self.session: Optional[aiohttp.ClientSession] = None
        self._owned_session: bool = False

        if isinstance(session, aiohttp.ClientSession):
            self.session = session
            self._owned_session = False
        elif session is ...:
            self.session = aiohttp.ClientSession()
            self._owned_session = True

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    async def close(self):
        if self._owned_session and self.session:
            await self.session.close()

    async def request(self, route: Route) -> tuple[io.BytesIO, str]:
        if not self.session:
            raise ValueError('session is not valid')

        url = route.url
        headers = route.headers
        body = route.json

        async with self.session.get(url, headers=headers, json=body) as r:
            data: bytes = await r.read()
            status = int(r.status)
            if 200 <= status < 300:
                # OK
                image_format: str = r.content_type.partition('/')[-1]
                file: io.BytesIO = io.BytesIO(data)
                return file, image_format
            elif 500 <= status < 600:
                # server error
                raise NeitizServerException(status, r.reason)
            elif status == 404:
                message = json.loads(data.decode('utf-8'))['detail']
                raise NeitizHTTPException(status, message)
            else:
                # handle http error
                message = json.loads(data.decode('utf-8'))['message']
                raise NeitizHTTPException(status, message)

    def particles(
        self,
        image_url: str,
        *,
        particle_type: ParticleType = 0,
        speed: int = 2,
        amount: int = 8,
        raw: bool = False,
    ) -> Union[Route, Coroutine[Any, Any, tuple[io.BytesIO, str]]]:
        if speed <= 0:
            raise ValueError('speed cannot be <= 0')
        if amount <= 0:
            raise ValueError('amount cannot be <= 0')

        json = {
            'image_url': image_url,
            'particle_type': int(particle_type),
            'speed': speed,
            'amount': amount,
        }

        route = Route('particles', headers=self.headers, json=json)
        return route if raw or not self.session else self.request(route)

    def explode(
        self,
        image_url: str,
        *,
        percent: int = 80,
        raw: bool = False,
    ) -> Union[Route, Coroutine[Any, Any, tuple[io.BytesIO, str]]]:
        if 0 >= percent > 100:
            raise ValueError('percentage cannot be <= 0 or > 100')

        json = {
            'image_url': image_url,
            'percent': percent,
        }

        route = Route('explode', headers=self.headers, json=json)
        return route if raw or not self.session else self.request(route)

    def dust(
        self,
        image_url: str,
        *,
        raw: bool = False,
    ) -> Union[Route, Coroutine[Any, Any, tuple[io.BytesIO, str]]]:

        json = {
            'image_url': image_url,
        }

        route = Route('dust', headers=self.headers, json=json)
        return route if raw or not self.session else self.request(route)

    def sand(
        self,
        image_url: str,
        *,
        raw: bool = False,
    ) -> Union[Route, Coroutine[Any, Any, tuple[io.BytesIO, str]]]:

        json = {
            'image_url': image_url,
        }

        route = Route('sand', headers=self.headers, json=json)
        return route if raw or not self.session else self.request(route)

    def runescape(
        self,
        text: str,
        *,
        raw: bool = False,
    ) -> Union[Route, Coroutine[Any, Any, tuple[io.BytesIO, str]]]:

        json = {
            'text': text,
        }

        route = Route('runescape', headers=self.headers, json=json)
        return route if raw or not self.session else self.request(route)

    def replace_colors(
        self,
        image_url: str,
        colors: list[list[int, int, int]],
        *,
        animated: Optional[bool] = None,
        max_dist: float = 16.0,
        raw: bool = False,
    ):
        if math.isnan(max_dist) or math.isinf(max_dist):
            raise ValueError('max_dist cannot be nan or inf')

        json = {
            'image_url': image_url,
            'colors': colors,
            'animated': animated,
            'max_dist': max_dist,
        }

        route = Route('replace_colors', headers=self.headers, json=json)
        return route if raw or not self.session else self.request(route)

    def merge_colors(
        self,
        destination: str,
        source: str,
        *,
        num_colors: int = 16,
        animated: Optional[bool] = None,
        max_dist: float = 16.0,
        raw: bool = False,
    ):
        if math.isnan(max_dist) or math.isinf(max_dist):
            raise ValueError('max_dist cannot be nan or inf')

        json = {
            'source': source,
            'destination': destination,
            'num_colors': num_colors,
            'animated': animated,
            'max_distance': max_dist,
        }

        route = Route('merge_colors', headers=self.headers, json=json)
        return route if raw or not self.session else self.request(route)
