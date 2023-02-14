from __future__ import annotations

import time
from typing import TYPE_CHECKING

__all__ = (
    'Uptimer'
)

if TYPE_CHECKING:
    from ..MemberCounter import MemberCounter

class Uptimer:

    __slots__ = (
        'client',
        'starttime'
    )

    def __init__(self, client: MemberCounter) -> None:
        self.client: MemberCounter = client
        self.starttime: float = 0

    @property
    def uptime(self) -> int:
        if self.starttime == 0:
            return 0
        return int(time.time() - self.starttime)

    def start(self):
        self.starttime = time.time()
