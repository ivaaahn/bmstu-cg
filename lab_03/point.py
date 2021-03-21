from __future__ import division

from PyQt5.QtCore import QPoint
from loguru import logger
from typing import overload

import numpy as np


class Point():
    def __init__(self, x: float, y:float):
        self._x = self._round(x)
        self._y = self._round(y)


    @staticmethod
    def _round(num: float) -> int:
        def _sign(num: float) -> int:
            return 1 if num > 0 else -1

        return int(num + 0.5 * _sign(num))

    @property
    def value(self):
        return (self.x, self.y)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value: str):
        self._label = value

    def rounder(func):
        def wrapper(self):
            return round(func(self), 2)
        return wrapper

    @rounder
    def pretty_x(self):
        return self._x

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
