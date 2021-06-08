import math
from typing import List, Optional

from PyQt5.QtCore import QLine

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
    def build(p1: Point, p2: Point, straight: bool = False) -> 'Segment':
        if straight:
            if abs(p2.x - p1.x) < abs(p2.y - p1.y):
                p2.x = p1.x
            else:
                p2.y = p1.y
        return Segment(p1, p2)

    def dist(self, p: Point) -> float:
        a = self.p1.y - self.p2.y
        b = self.p1.x - self.p2.x
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
