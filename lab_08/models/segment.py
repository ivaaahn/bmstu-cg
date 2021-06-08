import math
from typing import List, Optional

import numpy as np
from PyQt5.QtCore import QLine

import utils
from models.point import Point
from models.vector import Vector


class Segment:
    def __init__(self, p1: Point = None, p2: Point = None):
        self._p1 = p1
        self._p2 = p2

    @property
    def p1(self) -> Point:
        return self._p1

    @property
    def p2(self) -> Point:
        return self._p2

    def to_qline(self) -> QLine:
        return QLine(self._p1.to_qpoint(), self.p2.to_qpoint())

    def __str__(self) -> str:
        return f"start: {self._p1}, end: {self._p2}"

    @property
    def points(self) -> List[Point]:
        return [self._p1, self.p2]

    @p1.setter
    def p1(self, value):
        self._p1 = value

    def is_vertical(self) -> bool:
        return self.p1.x == self.p2.x

    @property
    def tangent(self) -> Optional[float]:
        if self.p2.x == self.p1.x:
            return None

        return (self.p2.y - self.p1.y) / (self.p2.x - self.p1.x)

    @staticmethod
    def _get_intersect(s1: 'Segment', s2: 'Segment'):
        l1 = np.cross(s1.p1.to_ndarray(), s1.p2.to_ndarray())
        l2 = np.cross(s2.p1.to_ndarray(), s2.p2.to_ndarray())
        x, y, z = np.cross(l1, l2)

        return Point(utils.custom_round(x / z), utils.custom_round(y / z))

    def put_on_segment(self, p: Point) -> Point:
        x = self.p1.x

        if self.tangent is None:
            s = Segment(p, Point(self.p1.x, p.y))
        elif self.tangent == 0:
            s = Segment(p, Point(p.x, p.y - 10))
        else:
            m = -1 / self.tangent
            s = Segment(p, Point(self.p1.x, m * (x - p.x) + p.y))

        return self._get_intersect(self, s)

    @staticmethod
    def build(p1: Point, p2: Point, straight: bool = False) -> 'Segment':
        if straight:
            if abs(p2.x - p1.x) < abs(p2.y - p1.y):
                p2.x = p1.x
            else:
                p2.y = p1.y
        return Segment(p1, p2)

    def dist(self, p: Point) -> float:
        a = self.p1.y - self.p2.y
        b = self.p2.x - self.p1.x
        c = self.p1.x * self.p2.y - self.p2.x * self.p1.y

        return abs(a * p.x + b * p.y + c) / math.sqrt(a ** 2 + b ** 2)

    def to_vector(self, direction: bool = True) -> Vector:
        x = (self.p2.x - self.p1.x)
        y = (self.p2.y - self.p1.y)

        if not direction:
            x = -x
            y = -y

        return Vector(x, y)

    @p2.setter
    def p2(self, value):
        self._p2 = value

    def contains_point(self, p: Point) -> bool:
        if Vector.cross_prod(self.to_vector(), Segment(self.p1, p).to_vector()) <= 1e-6:
            if self.p1 <= p <= self.p2 or self.p2 <= p <= self.p1:
                return True

        return False

    def to_ndarray(self) -> np.ndarray:
        return np.array([self.p1.y - self.p2.y, self.p1.x - self.p2.x, self.p1.x * self.p2.y - self.p2.x * self.p1.y])
