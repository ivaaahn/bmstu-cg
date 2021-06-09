from models.point import Point


class Vector:
    def __init__(self, x: float, y: float) -> None:
        self._value = Point(x, y)

    def normal(self) -> 'Vector':
        return Vector(1, 0) if self.x == 0 else Vector((-self.y / self.x), 1)

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
        return Vector(-self.x, -self.y)
