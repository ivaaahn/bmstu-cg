from __future__ import division

import math

import numpy as np
from PyQt5.QtCore import QPoint, QPointF

import utils
from models.coords_3d import Coords3D


class Point(Coords3D):
    def __init__(self, x: [float, int], y: [float, int], z: [float, int] = 0):
        super().__init__(x, y, z)

    def translate(self, dx: [float, int] = 0, dy: [float, int] = 0, dz: [float, int] = 0) -> None:
        self.x += dx
        self.y += dy
        self.z += dz

    def is_visible(self) -> bool:
        return (0 <= self.x < utils.W) and (0 <= self.y < utils.H)

    def dist_to(self, other) -> float:
        return math.hypot(self.x - other.x, self.y - other.y)

    def to_qpoint(self) -> QPoint:
        return QPoint(self.x, self.y)

    def to_qpointf(self) -> QPointF:
        return QPointF(self.x, self.y)

    def to_ndarray(self) -> np.ndarray:
        return np.array([self.x, self.y, self.z, 1])

    def __repr__(self):
        return f'Point <{self.value}>'

    def __str__(self):
        return f'{self.value}'

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __imul__(self, other):
        self._x *= other
        self._y *= other
        return self

    def __iadd__(self, other):
        self._x += other.x
        self._y += other.y
        return self

    def __truediv__(self, number: [float, int]):
        return Point(self.x / number, self.y / number, self._z / number)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __ne__(self, other) -> bool:
        return not self == other

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def __lt__(self, other) -> bool:
        return self.x < other.x and self.y < other.y and self.z < other.z

    def __le__(self, other) -> bool:
        return self.x <= other.x and self.y <= other.y and self.z <= other.z

    def __gt__(self, other) -> bool:
        return self.x > other.x and self.y > other.y and self.z > other.z

    def __ge__(self, other) -> bool:
        return self.x >= other.x and self.y >= other.y and self.z >= other.z
