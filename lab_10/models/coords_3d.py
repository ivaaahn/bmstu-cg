from typing import Tuple


class Coords3D:
    def __init__(self, x: [float, int] = 0, y: [float, int] = 0, z: [float, int] = 0):
        self._x = x
        self._y = y
        self._z = z

    @property
    def value(self) -> [Tuple[int, int, int], Tuple[float, float, float]]:
        return self._x, self._y, self._z

    @property
    def x(self) -> [float, int]:
        return self._x

    @property
    def y(self) -> [float, int]:
        return self._y

    @property
    def z(self) -> [float, int]:
        return self._z

    @x.setter
    def x(self, value: [float, int]) -> None:
        self._x = value

    @y.setter
    def y(self, value: [float, int]) -> None:
        self._y = value

    @z.setter
    def z(self, value: [float, int]) -> None:
        self._z = value
