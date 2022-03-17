
from __future__ import annotations

from io import BytesIO
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .route import Route

__all__ = (
    'NeitizImage',
)


class NeitizImage(BytesIO):
    __slots__ = ('content_type', 'route')

    def __init__(self, *args, content_type: str, route: Route, **kwargs):
        super().__init__(*args, **kwargs)
        self.content_type: str = content_type
        self.route: Route = route

    @property
    def extension(self) -> str:
        return self.content_type.partition('/')[-1]

    @property
    def endpoint(self) -> str:
        return self.route.endpoint

    def __repr__(self) -> str:
        return f'<NeitizImage endpoint={self.route.endpoint} content_type={self.content_type}>'

    def __str__(self) -> str:
        return f'{self.endpoint}.{self.extension}'
