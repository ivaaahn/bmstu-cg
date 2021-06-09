import math
from copy import copy
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

    def __str__(self) -> str:
        return f"start: {self._p1}, end: {self._p2}"

    def is_vertical(self) -> bool:
        return self.p1.x == self.p2.x

    @property
    def tangent(self) -> Optional[float]:
        if self.p2.x == self.p1.x:
            return None

        return (self.p2.y - self.p1.y) / (self.p2.x - self.p1.x)

    def reverse(self) -> None:
        self.p1, self.p2 = self.p2, self.p1

    def _contains_proj(self, p: Point) -> bool:
        # a - наиболее длинная сторона треугольника, не считая исходный отрезок
        b, a = sorted([p.dist_to(self.p1), p.dist_to(self.p2)])
        c = self.p1.dist_to(self.p2)

        a_sqr, bc_sqr = a * a, b * b + c * c

        return a_sqr < bc_sqr

    def proj(self, p: Point) -> Point:
        if not self._contains_proj(p):
            return copy(self.p1) if p.dist_to(self.p1) < p.dist_to(self.p2) else copy(self.p2)

        if self.tangent is None:
            return Point(self.p1.x, p.y)
        elif self.tangent == 0:
            return Point(p.x, self.p1.y)
        else:
            # Имеем две прямые:
            # 1. y = k * (x - x1) + y1
            # 2. y = -1/k * (x - xp) + yp (перпендикулярная первой и проходящая через P(xp, yp)

            x1, y1, k = self.p1.x, self.p1.y, self.tangent
            xp, yp, kp = p.x, p.y, -1 / k
            res = np.linalg.solve([[k, -1], [kp, -1]], [k * x1 - y1, kp * xp - yp])

            return Point(utils.custom_round(res[0]), utils.custom_round(res[1]))

    def to_vector(self, direction: bool = True) -> Vector:
        x = (self.p2.x - self.p1.x)
        y = (self.p2.y - self.p1.y)

        if not direction:
            x = -x
            y = -y

        return Vector(x, y)

    def contains_point(self, p: Point) -> bool:
        if Vector.cross_prod(self.to_vector(), Segment(self.p1, p).to_vector()) <= 1e-6:
            if self.p1 <= p <= self.p2 or self.p2 <= p <= self.p1:
                return True

        return False

    def to_ndarray(self) -> np.ndarray:
        return np.array([self.p1.y - self.p2.y, self.p1.x - self.p2.x, self.p1.x * self.p2.y - self.p2.x * self.p1.y])

    @property
    def p1(self) -> Point:
        return self._p1

    @property
    def p2(self) -> Point:
        return self._p2

    @property
    def vertices(self) -> List[Point]:
        return [self._p1, self.p2]

    @p1.setter
    def p1(self, value) -> None:
        self._p1 = value

    @p2.setter
    def p2(self, value) -> None:
        self._p2 = value

    def to_qline(self) -> QLine:
        return QLine(self._p1.to_qpoint(), self.p2.to_qpoint())
