from enum import Enum
from typing import List

from numpy import arange

import utils
from models.point import Point


class Visible(Enum):
    NOT = 0
    TOP = 1
    BOTTOM = -1


class Horizon:
    def __init__(self) -> None:
        self._top: List[float] = []
        self._bottom: List[float] = []

        self.reset_all()

    @property
    def top(self) -> List[float]:
        return self._top

    @property
    def bottom(self) -> List[float]:
        return self._bottom

    def reset_all(self) -> None:
        self.reset_top()
        self.reset_bottom()

    def reset_top(self) -> None:
        self._top = [0.0 for _ in range(utils.W)]

    def reset_bottom(self) -> None:
        self._bottom = [float(utils.H) for _ in range(utils.W)]

    def visibility_type(self, p: Point) -> Visible:
        if p.y >= self.top[p.x]:
            return Visible.TOP

        if p.y <= self.bottom[p.x]:
            return Visible.BOTTOM

        return Visible.NOT

    def fill(self, p1: Point, p2: Point) -> None:
        if p1.x > p2.x:
            p1, p2 = p2, p1

        if p2.x == p1.x:
            self.top[p2.x] = max(self.top[p2.x], p2.y)
            self.bottom[p2.x] = min(self.bottom[p2.x], p2.y)
        else:
            m = (p2.y - p1.y) / (p2.x - p1.x)
            for x in arange(p1.x, p2.x + 1):
                y = m * (x - p1.x) + p1.y
                self.top[x] = max(self.top[x], y)
                self.bottom[x] = min(self.bottom[x], y)
