from math import sqrt
import numpy as np
from triangle import Triangle
from point import Point


class Circle():
    def __init__(self, triangle: Triangle):
        self._triangle = triangle
        self._init_center()
        self._init_radius()

    def __repr__(self):
        return f'{repr(self.center)}, R = {self.radius}'

    def __str__(self):
        return f'{str(self.center)}, R: {round(self.radius, 2)}'

    def _init_radius(self):
        _a = self._triangle.a
        _b = self._triangle.b
        _c = self._triangle.c

        self.radius = (_a * _b * _c) / (np.double(4 * self._triangle.square))

    def _init_center(self):
        mid1 = self._triangle.centerPerp(self._triangle.pA, self._triangle.pB)
        mid2 = self._triangle.centerPerp(self._triangle.pA, self._triangle.pC)

        left = np.copy([mid1[:-1], mid2[:-1]])
        right = np.array([-mid1[-1], -mid2[-1]])

        center_point = np.linalg.solve(left, right)

        self.center = Point(point=(tuple(center_point)), label='O')

    def into(self, p: Point) -> bool:
        dist = self._triangle._lenByPoints(p, self.center)
        return self.radius - dist > 1e-5
