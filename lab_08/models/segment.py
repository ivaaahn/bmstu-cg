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

    @p2.setter
    def p2(self, value) -> None:
        self._p2 = value

    def is_vertical(self) -> bool:
        return self.p1.x == self.p2.x

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

    @property
    def tangent(self) -> Optional[float]:
        if self.p2.x == self.p1.x:
            return None

        return (self.p2.y - self.p1.y) / (self.p2.x - self.p1.x)

    @staticmethod
    def build(p1: Point, p2: Point, straight: bool = False) -> 'Segment':
        if straight:
            if abs(p2.x - p1.x) < abs(p2.y - p1.y):
                p2.x = p1.x
            else:
                p2.y = p1.y
        return Segment(p1, p2)

    def to_vector(self, direction: bool = True) -> Vector:
        x = (self.p2.x - self.p1.x)
        y = (self.p2.y - self.p1.y)

        if not direction:
            x = -x
            y = -y

        return Vector(x, y)

    @staticmethod
    def is_intersect(s1: 'Segment', s2: 'Segment') -> bool:
        d1, d2 = s1.to_vector(), s2.to_vector()
        w1, w2 = Segment(s2.p1, s1.p1).to_vector(), Segment(s1.p1, s2.p1).to_vector()
        n1, n2 = s2.to_vector().normal(), s1.to_vector().normal()

        d_dp1 = Vector.dot_prod(d1, n1)
        if not d_dp1:
            return False

        d_dp2 = Vector.dot_prod(d2, n2)
        w_dp1, w_dp2 = Vector.dot_prod(w1, n1), Vector.dot_prod(w2, n2)

        t1, t2 = -w_dp1 / d_dp1, -w_dp2 / d_dp2
        return (0 <= t1 <= 1) and (0 <= t2 <= 1)
