from typing import List

from PyQt5.QtCore import QRect, QPoint

from models.point import Point
from models.segment import Segment


class Cutter:
    def __init__(self, left_top: Point, right_bottom: Point):
        self._ltop = left_top
        self._rbottom = right_bottom

    @property
    def left(self) -> int:
        return self._ltop.x

    @property
    def right(self) -> int:
        return self._rbottom.x

    @property
    def top(self) -> int:
        return self._ltop.y

    @property
    def bottom(self) -> int:
        return self._rbottom.y

    @property
    def rbottom(self) -> Point:
        return self._rbottom

    @property
    def ltop(self) -> Point:
        return self._ltop

    @property
    def lbottom(self) -> Point:
        return Point(self.left, self.bottom)

    @property
    def rtop(self) -> Point:
        return Point(self.right, self.top)

    def get_lines(self) -> List[Segment]:
        return [Segment(self.ltop, self.lbottom), Segment(self.lbottom, self.rbottom), Segment(self.rbottom, self.rtop),
                Segment(self.ltop, self.rtop)]

    def to_qrect(self) -> QRect:
        return QRect(self.ltop.to_qpoint(), self.rbottom.to_qpoint())
