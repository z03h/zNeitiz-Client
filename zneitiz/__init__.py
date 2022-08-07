from typing import NamedTuple, Literal

from .client import *
from .image import *
from ._enums import *
from ._exceptions import *

__version__: str = '0.2.0'


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int

_major, _minor, _micro = (int(i) for i in __version__.split('.'))

version_info: VersionInfo = VersionInfo(major=_major, minor=_minor, micro=_micro, releaselevel='final', serial=0)
