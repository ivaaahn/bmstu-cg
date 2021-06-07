from typing import List

from PyQt5.QtCore import QLine

from models.point import Point


class Segment:
    def __init__(self, start: Point = None, end: Point = None):
        self._p1 = start
        self._p2 = end

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
    def tangent(self) -> float:
        return (self.p2.y - self.p1.y) / (self.p2.x - self.p1.x)

    @staticmethod
    def build(p1: Point, p2: Point, straight: bool = False, along: bool = False) -> 'Segment':
        if straight:
            if abs(p2.x - p1.x) < abs(p2.y - p1.y):
                p2.x = p1.x
            else:
                p2.y = p1.y

        if along:
            pass

        return Segment(p1, p2)

    @staticmethod
    def cross_product(v1: 'Segment', v2: 'Segment') -> float:
        vec1 = v1.p2 - v1.p1
        vec2 = v2.p2 - v2.p1

        return vec1.x * vec2.y - vec1.y * vec2.x
