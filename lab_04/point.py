from __future__ import division

from PyQt5.QtCore import QPoint
from typing import NoReturn, Tuple

import numpy as np


class Point():
    def __init__(self, x: int, y: int, intens: int = 100):
        self._x: int = x
        self._y: int = y
        self._color_intens = self._round(255 * intens / 100)

    @staticmethod
    def _round(num: float) -> int:
        return int(num + (0.5 if num > 0 else -0.5))

    @property
    def intensity(self) -> int:
        return self._color_intens

    @property
    def value(self) -> Tuple[float]:
        return (self.x, self.y)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value) -> NoReturn:
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    def rounder(func):
        def wrapper(self):
            return round(func(self), 2)
        return wrapper

    @rounder
    def pretty_x(self):
        return self._x

    def copy(self):
        return Point(self._x, self._y, self._color_intens)

    @rounder
    def pretty_y(self):
        return self._y

    def to_qpoint(self):
        return QPoint(*self.value)

    def pretty_value(self) -> tuple:
        return self.pretty_x(), self.pretty_y()

    def to_ndarray(self) -> np.ndarray:
        return np.array([self.x, self.y, 1])

    def __repr__(self):
        return f'Point <{self.value}>'

    def __str__(self):
        return f'{self.pretty_value()}'

    def __add__(self, other):
        return Point(x=self.x+other.x, y=self.y+other.y)

    def __truediv__(self, number: float):
        return Point(x=self.x/number, y=self.y/number)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
