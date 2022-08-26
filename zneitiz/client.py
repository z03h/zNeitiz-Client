from __future__ import annotations
from typing import TYPE_CHECKING

import sys
import math

import aiohttp

from .route import Route
from ._enums import ParticleType

if TYPE_CHECKING:
    import io

    from typing import (
        Optional,
        Union,
        Any,
    )


if TYPE_CHECKING:
    from ._enums import ParticleType

__all__ = ('NeitizClient',)


class NeitizClient:

    URL = 'https://zneitiz.onrender.com/'

    def __init__(
        self,
        token: Optional[str],
        *,
        session: Optional[aiohttp.ClientSession] = ...,
    ):
        self._token: Optional[str] = token
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

    async def __aexit__(self, *args):
        await self.close()

    async def close(self):
        if self._owned_session and self.session:
            await self.session.close()

    def particles(
        self,
        image: Union[io.BufferedIOBase, str],
        *,
        particle_type: ParticleType = ParticleType.salt,
        speed: int = 2,
        amount: int = 8,
    ) -> Route:
        if speed <= 0:
            raise ValueError('speed cannot be <= 0')
        if amount <= 0:
            raise ValueError('amount cannot be <= 0')

        data: dict[str, Any] = {
            'particle_type': int(particle_type),
            'speed': speed,
            'amount': amount,
        }
        if isinstance(image, str):
            data['image_url'] = image
            files = None
        else:
            files = {'image': image}

        return Route('particles', headers=self.headers, json=data, session=self.session, files=files)

    def explode(self, image: Union[io.BufferedIOBase, str], *, percent: int = 80) -> Route:
        if percent <= 0 or percent > 100:
            raise ValueError('percentage must be greater than 0 and less than 101')

        data: dict[str, Any] = {
            'percent': percent,
        }
        if isinstance(image, str):
            data['image_url'] = image
            files = None
        else:
            files = {'image': image}

        return Route('explode', headers=self.headers, json=data, session=self.session, files=files)

    def dust(self, image: Union[io.BufferedIOBase, str]) -> Route:

        if isinstance(image, str):
            data = {'image_url': image}
            files = None
        else:
            data = None
            files = {'image': image}

        return Route('dust', headers=self.headers, json=data, session=self.session, files=files)

    def sand(self, image: Union[io.BufferedIOBase, str]) -> Route:

        if isinstance(image, str):
            data = {'image_url': image}
            files = None
        else:
            data = None
            files = {'image': image}

        return Route('sand', headers=self.headers, json=data, session=self.session, files=files)

    def runescape(self, text: str) -> Route:
        data = {'text': text}
        return Route('runescape', headers=self.headers, json=data, session=self.session)

    def replace_colors(
        self,
        image: Union[io.BufferedIOBase, str],
        colors: list[list[int]],
        *,
        animated: Optional[bool] = None,
        max_dist: float = 16.0,
    ) -> Route:
        if math.isnan(max_dist) or math.isinf(max_dist):
            raise ValueError('max_dist cannot be nan or inf')

        data = {
            'colors': colors,
            'animated': animated,
            'max_dist': max_dist,
        }
        if isinstance(image, str):
            data['image_url'] = image
            files = None
        else:
            files = {'image': image}

        return Route('replace_colors', headers=self.headers, json=data, session=self.session, files=files)

    def merge_colors(
        self,
        destination: Union[io.BufferedIOBase, str],
        source: Union[io.BufferedIOBase, str],
        *,
        num_colors: int = 16,
        animated: Optional[bool] = None,
        max_dist: float = 16.0,
    ) -> Route:
        if math.isnan(max_dist) or math.isinf(max_dist):
            raise ValueError('max_dist cannot be nan or inf')

        data = {
            'num_colors': num_colors,
            'animated': animated,
            'max_distance': max_dist,
        }
        files = {}
        if isinstance(source, str):
            data['source_url'] = source
        else:
            files['source_image'] = source

        if isinstance(destination, str):
            data['destination_url'] = destination
        else:
            files['destination_image'] = destination

        if not files:
            files = None

        return Route('merge_colors', headers=self.headers, json=data, session=self.session, files=files)
