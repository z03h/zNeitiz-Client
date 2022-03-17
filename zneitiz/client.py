
from __future__ import annotations

import math
import time
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

from .route import Route
from .image import NeitizImage

from ._exceptions import (
    NeitizException,
    NeitizHTTPException,
    NeitizServerException,
    NeitizRatelimitException,
)


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
        self._ratelimited_until: float = 0.0
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

    def __repr__(self) -> str:
        return f'<NeitizClient closed={self.session.closed} ratelimited={self.is_ratelimited()}>'

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    async def close(self):
        if self._owned_session and self.session:
            await self.session.close()

    def request(self, route: Route) -> aiohttp.client._RequestContextManager:
        if not self.session:
            raise ValueError('session is not valid')

        url = route.url
        headers = route.headers
        body = route.json

        return self.session.get(url, headers=headers, json=body)

    async def _request(self, route: Route) -> NeitizImage:
        if not self.session:
            raise ValueError('session is not valid')

        duration = self.is_ratelimited()
        if duration > 0:
            raise NeitizException(f'Ratelimited for another {duration:.2f} seconds')

        url = route.url
        headers = route.headers
        body = route.json

        async with self.session.get(url, headers=headers, json=body) as r:
            data: bytes = await r.read()

            # check ratelimit header
            remaining = int(r.headers.get('x-ratelimit-remaining', 1))
            if remaining <= 0:
                duration = float(r.headers.get('x-ratelimit-reset', time.time() + 20))
                self._ratelimited_until = duration

            status = int(r.status)
            if 200 <= status < 300:
                # OK
                content_type: str = r.content_type
                file = NeitizImage(data, content_type=content_type, route=route)
                return file
            elif 500 <= status < 600:
                # server error
                raise NeitizServerException(status, r.reason)
            elif status == 429:
                # ratelimited
                err = NeitizRatelimitException(status, r.reason, r.headers)
                self._ratelimited_until = err.ratelimit_reset
                raise err
            else:
                raise NeitizHTTPException(status, r.reason)

    def is_ratelimited(self) -> float:
        duration = self._ratelimited_until - time.time()
        return 0.0 if duration <= 0.000001 else duration

    def particles(
        self,
        image_url: str,
        *,
        particle_type: ParticleType = 0,
        speed: int = 2,
        amount: int = 8,
        raw: bool = False,
    ) -> Union[Route, Coroutine[Any, Any, NeitizImage]]:
        if speed <= 0:
            raise ValueError('speed cannot be <= 0')
        if amount <= 0:
            raise ValueError('amount cannot be <= 0')

        data = {
            'image_url': image_url,
            'particle_type': int(particle_type),
            'speed': speed,
            'amount': amount,
        }

        route = Route('particles', headers=self.headers, json=data)
        return self._make_request(route, raw)

    def explode(
        self,
        image_url: str,
        *,
        percent: int = 80,
        raw: bool = False,
    ) -> Union[Route, Coroutine[Any, Any, NeitizImage]]:
        if 0 >= percent > 100:
            raise ValueError('percentage cannot be <= 0 or > 100')

        data = {
            'image_url': image_url,
            'percent': percent,
        }

        route = Route('explode', headers=self.headers, json=data)
        return self._make_request(route, raw)

    def dust(
        self,
        image_url: str,
        *,
        raw: bool = False,
    ) -> Union[Route, Coroutine[Any, Any, NeitizImage]]:

        data = {
            'image_url': image_url,
        }

        route = Route('dust', headers=self.headers, json=data)
        return self._make_request(route, raw)

    def sand(
        self,
        image_url: str,
        *,
        raw: bool = False,
    ) -> Union[Route, Coroutine[Any, Any, NeitizImage]]:

        data = {
            'image_url': image_url,
        }

        route = Route('sand', headers=self.headers, json=data)
        return self._make_request(route, raw)

    def runescape(
        self,
        text: str,
        *,
        raw: bool = False,
    ) -> Union[Route, Coroutine[Any, Any, NeitizImage]]:

        data = {
            'text': text,
        }

        route = Route('runescape', headers=self.headers, json=data)
        return self._make_request(route, raw)

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

        data = {
            'image_url': image_url,
            'colors': colors,
            'animated': animated,
            'max_dist': max_dist,
        }

        route = Route('replace_colors', headers=self.headers, json=data)
        return self._make_request(route, raw)

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

        data = {
            'source': source,
            'destination': destination,
            'num_colors': num_colors,
            'animated': animated,
            'max_distance': max_dist,
        }

        route = Route('merge_colors', headers=self.headers, json=data)
        return self._make_request(route, raw)

    def _make_request(self, route: Route, raw: bool) -> Union[Route, Coroutine[Any, Any, NeitizImage]]:
        if raw or self.session is None:
            return route
        else:
            return self._request(route)
