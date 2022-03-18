from typing import NamedTuple, Literal

from .client import *
from .image import *
from ._enums import *
from ._exceptions import *

__version__: str = '0.1.0'


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int


version_info: VersionInfo = VersionInfo(major=0, minor=1, micro=0, releaselevel='final', serial=0)
