from __future__ import division

from PyQt5.QtCore import QPoint, QPointF
from typing import NoReturn, Tuple

import numpy as np


class Point():
    def __init__(self, x: float, y: float):
        self._x = x
        self._y = y

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

    def to_qpointf(self):
        return QPointF(*self.value)

    def pretty_value(self) -> tuple:
        return self.pretty_x(), self.pretty_y()

    def to_ndarray(self) -> np.ndarray:
        return np.array([self.x, self.y, 1])

    def bisect_mirror(self, center):
        return Point(center.x+self._y-center._y, center.y+self._x-center.x)

    def y_mirror(self, center):
        return Point(2*center.x-self.x, self.y)

    def x_mirror(self, center):
        return Point(self.x, 2*center.y-self.y)

    def __repr__(self):
        return f'Point <{self.value}>'

    def __str__(self):
        return f'{self.pretty_value()}'

    def __add__(self, other):
        return Point(x=self.x+other.x, y=self.y+other.y)

    def __imul__(self, other):
        self._x *= other
        self._y *= other
        return self

    def __iadd__(self, other):
        self._x += other.x
        self._y += other.y
        return self

    def __truediv__(self, number: float):
        return Point(x=self.x/number, y=self.y/number)

    def __eq__(self, other):

        return self.x == other.x and self.y == other.y

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)
