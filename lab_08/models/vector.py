from models.point import Point
from models.segment import Segment


class Vector:
    def __init__(self, seg: Segment = None, direction: bool = True, x: float = None, y: float = None) -> None:
        if x is not None and y is not None:
            self._value = Point(x, y)
        else:
            if not direction:
                seg.p1, seg.p2 = seg.p2, seg.p1

            self._value = Point(seg.p2.x - seg.p1.x, seg.p2.y - seg.p1.y)

    @property
    def x(self) -> float:
        return self._value.x

    @property
    def y(self) -> float:
        return self._value.y

    @staticmethod
    def cross_prod(v1: 'Vector', v2: 'Vector') -> float:
        return v1.x * v2.y - v1.y * v2.x

    @staticmethod
    def dot_prod(v1: 'Vector', v2: 'Vector') -> float:
        return v1.x * v2.x + v1.y * v2.y

    def __neg__(self):
        return Vector(x=-self.x, y=-self.y)
