from math import sqrt
import numpy as np
from numpy import cross, array
from point import Point


class Triangle():
    def __init__(self, points: list):
        self.pA, self.pB, self.pC = points

        self._a = None
        self._b = None
        self._c = None

        self._square = None

    def __str__(self):
        return f'{str(self.pA)}, {str(self.pB)}, {str(self.pC)}'

    def getPoints(self) -> list:
        return [self.pA, self.pB, self.pC]

    @property
    def a(self):
        if self._a is None:
            self._a = self._lenByPoints(self.pB, self.pC)

        return self._a

    @property
    def b(self):
        if self._b is None:
            self._b = self._lenByPoints(self.pA, self.pC)

        return self._b

    @property
    def c(self):
        if self._c is None:
            self._c = self._lenByPoints(self.pA, self.pB)

        return self._c

    @property
    def square(self):
        if self._square is None:
            p = (self._a + self._b + self._c) / 2
            self._square = sqrt(p * (p - self._a) *
                                (p - self._b) * (p - self._c))
        return self._square

    @staticmethod
    def _lenByPoints(A: Point, B: Point) -> float:
        vx = B.x - A.x
        vy = B.y - A.y

        return np.linalg.norm(array([vx, vy]))

    @staticmethod
    def midline(A: Point, B: Point) -> Point:
        return Point(point=(np.double((A.x + B.x) / 2), np.double((A.y + B.y) / 2)))

    def centerPerp(self, A: Point, B: Point) -> tuple:
        def _dirVec(P1: Point, P2: Point) -> Point:
            A = P2.y - P1.y
            B = P1.x - P2.x
            return Point(point=(-B, A))

        C = self.midline(A, B)
        d = _dirVec(A, B)

        return (d.x, d.y, -(C.x * d.x + C.y * d.y))

    def into(self, p: Point) -> bool:
        def _vector(A: Point, B: Point) -> np.ndarray:
            return array([B.x - A.x, B.y - A.y])

        def _intoTr(cr1, cr2, cr3) -> bool:
            return (cr1 > 0 and cr2 > 0 and cr3 > 0) or (cr1 < 0 and cr2 < 0 and cr3 < 0)

        ab_ap = cross(_vector(self.pA, self.pB), _vector(self.pA, p))
        bc_bp = cross(_vector(self.pB, self.pC), _vector(self.pB, p))
        ca_cp = cross(_vector(self.pC, self.pA), _vector(self.pC, p))

        return _intoTr(ab_ap, bc_bp, ca_cp)
