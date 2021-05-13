from __future__ import division

from typing import Tuple

import numpy as np
from PyQt5.QtCore import QPoint, QPointF


class TitleGenerator:
    _index = 0

    @staticmethod
    def generate() -> str:
        TitleGenerator._index += 1
        return 'P' + str(TitleGenerator._index)

    @staticmethod
    def reset() -> None:
        TitleGenerator._index = 0


class Point:
    def __init__(self, x: float, y: float, title: str = None, need_title: bool = False):
        self._x = x
        self._y = y

        if title:
            self._title = title
        elif need_title:
            self._title = TitleGenerator.generate()
        else:
            self._title = None

    @property
    def title(self) -> str:
        return self._title

    def set_title(self, title=None) -> str:
        self._title = title if title else TitleGenerator.generate()
        return self.title

    @property
    def value(self) -> Tuple[float, float]:
        return self.x, self.y

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @x.setter
    def x(self, value) -> None:
        self._x = value

    @y.setter
    def y(self, value) -> None:
        self._y = value

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

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)
