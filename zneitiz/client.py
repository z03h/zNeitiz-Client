
from __future__ import annotations

import sys
import math
from typing import TYPE_CHECKING

import aiohttp

from . import __version__
from .route import Route
from ._enums import ParticleType

if TYPE_CHECKING:
    from typing import (
        Optional,
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
        self._token: str = token
        self.headers: dict[str, str] = {
            'Authorization': f'Bearer {token}',
            'User-Agent': f'Python/{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} aiohttp/{aiohttp.__version__}',
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
        return f'<NeitizClient closed={self.session.closed if self.session else self.session}>'

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    async def close(self):
        if self._owned_session and self.session:
            await self.session.close()

    def particles(
        self,
        image_url: str,
        *,
        particle_type: ParticleType = ParticleType.salt,
        speed: int = 2,
        amount: int = 8,
    ) -> Route:
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

        return Route('particles', headers=self.headers, json=data, session=self.session)

    def explode(
        self,
        image_url: str,
        *,
        percent: int = 80,
    ) -> Route:
        if 0 >= percent > 100:
            raise ValueError('percentage cannot be <= 0 or > 100')

        data = {
            'image_url': image_url,
            'percent': percent,
        }

        return Route('explode', headers=self.headers, json=data, session=self.session)

    def dust(
        self,
        image_url: str,
    ) -> Route:

        data = {
            'image_url': image_url,
        }

        return Route('dust', headers=self.headers, json=data, session=self.session)

    def sand(
        self,
        image_url: str,
    ) -> Route:

        data = {
            'image_url': image_url,
        }

        return Route('sand', headers=self.headers, json=data, session=self.session)

    def runescape(
        self,
        text: str,
    ) -> Route:

        data = {
            'text': text,
        }
        return Route('runescape', headers=self.headers, json=data, session=self.session)

    def replace_colors(
        self,
        image_url: str,
        colors: list[list[int]],
        *,
        animated: Optional[bool] = None,
        max_dist: float = 16.0,
    ) -> Route:
        if math.isnan(max_dist) or math.isinf(max_dist):
            raise ValueError('max_dist cannot be nan or inf')

        data = {
            'image_url': image_url,
            'colors': colors,
            'animated': animated,
            'max_dist': max_dist,
        }

        return Route('replace_colors', headers=self.headers, json=data, session=self.session)

    def merge_colors(
        self,
        destination: str,
        source: str,
        *,
        num_colors: int = 16,
        animated: Optional[bool] = None,
        max_dist: float = 16.0,
    ) -> Route:
        if math.isnan(max_dist) or math.isinf(max_dist):
            raise ValueError('max_dist cannot be nan or inf')

        data = {
            'source': source,
            'destination': destination,
            'num_colors': num_colors,
            'animated': animated,
            'max_distance': max_dist,
        }

        return Route('merge_colors', headers=self.headers, json=data, session=self.session)
