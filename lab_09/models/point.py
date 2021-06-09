from __future__ import division

import math
from typing import Tuple

import numpy as np
from PyQt5.QtCore import QPoint, QPointF


class Point:
    def __init__(self, x: [float, int], y: [float, int]):
        self._x = x
        self._y = y

    @property
    def value(self) -> [Tuple[int, int], Tuple[float, float]]:
        return self.x, self.y

    @property
    def x(self) -> [float, int]:
        return self._x

    @property
    def y(self) -> [float, int]:
        return self._y

    @x.setter
    def x(self, value: [float, int]) -> None:
        self._x = value

    @y.setter
    def y(self, value: [float, int]) -> None:
        self._y = value

    def dist_to(self, other) -> float:
        return math.hypot(self.x - other.x, self.y - other.y)

    def rounder(func):
        def wrapper(self):
            return round(func(self), 2)

        return wrapper

    def to_qpoint(self):
        return QPoint(*self.value)

    def to_qpointf(self):
        return QPointF(*self.value)

    def to_ndarray(self) -> np.ndarray:
        return np.array([self.x, self.y, 1])

    def __repr__(self):
        return f'Point <{self.value}>'

    def __str__(self):
        return f'{self.value}'

    def __add__(self, other):
        return Point(x=self.x + other.x, y=self.y + other.y)

    def __imul__(self, other):
        self._x *= other
        self._y *= other
        return self

    def __iadd__(self, other):
        self._x += other.x
        self._y += other.y
        return self

    def __truediv__(self, number: float):
        return Point(x=self.x / number, y=self.y / number)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other) -> bool:
        return not self == other

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __lt__(self, other) -> bool:
        return self.x < other.x and self.y < other.y

    def __le__(self, other) -> bool:
        return self.x <= other.x and self.y <= other.y

    def __gt__(self, other) -> bool:
        return self.x > other.x and self.y > other.y

    def __ge__(self, other) -> bool:
        return self.x >= other.x and self.y >= other.y
