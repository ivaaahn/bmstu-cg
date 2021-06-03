from typing import List

from PyQt5.QtCore import QLine

from models.point import Point


class Segment:
    def __init__(self, start: Point = None, end: Point = None):
        self._start = start
        self._end = end

    @property
    def start(self) -> Point:
        return self._start

    @property
    def end(self) -> Point:
        return self._end

    def to_qline(self) -> QLine:
        return QLine(self._start.to_qpoint(), self.end.to_qpoint())

    def __str__(self) -> str:
        return f"start: {self._start}, end: {self._end}"

    @property
    def points(self) -> List[Point]:
        return [self._start, self.end]

    @start.setter
    def start(self, value):
        self._start = value



