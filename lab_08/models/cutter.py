from typing import List, Optional

from exceptions import UnableToClose, NonConvex
from models.point import Point
from models.segment import Segment
from models.vector import Vector


class Cutter:
    def __init__(self):
        self._last_vertex: Optional[Point] = None
        self._edges: List[Segment] = []
        self._closed: bool = False
        self._sign = None

    def reset(self) -> None:
        self._last_vertex = None
        self._edges.clear()
        self._closed = False
        self._sign = None

    def get_closing_edge(self) -> Segment:
        return Segment(self.last_edge.p2, self.first_edge.p1)

    def add_edge(self, new_edge: Segment) -> None:
        if len(self.edges) >= 2 and not self.is_convex(self.last_edge, new_edge):
            raise NonConvex("Невыпуклый отсекатель")

        self.edges.append(new_edge)

        if len(self.edges) == 2:
            self.set_sign()

    def close(self) -> Segment:
        if not self.ready_to_close():
            raise UnableToClose('Недостаточно ребер, чтобы замкнуть')

        closing_edge = self.get_closing_edge()

        if not self.is_convex(closing_edge, self.first_edge):
            raise NonConvex("Невыпуклый отсекатель")

        self.add_edge(closing_edge)

        self._closed = True

        return closing_edge

    def is_closed(self) -> bool:
        return self._closed

    def ready_to_close(self) -> bool:
        return len(self._edges) >= 2

    def is_convex(self, e1: Segment, e2: Segment) -> bool:
        return self._sign * Vector.cross_prod(Vector(e1), Vector(e2)) >= 0

    def set_sign(self) -> None:
        self._sign = 1 if Vector.cross_prod(Vector(self.first_edge), Vector(self.second_edge)) > 0 else -1

    @staticmethod
    def get_normal(e: Segment, e_next: Segment):
        vector = Vector(e)
        n = Vector(x=1, y=0) if vector.x == 0 else Vector(x=(-vector.y / vector.x), y=1)

        # Если < 0, то угол между нормалью и следующим ребром тупой, => нашли наружную нормаль. Меняем знак.
        if Vector.dot_prod(Vector(e_next), n) < 0:
            n = -n

        return n

    def get_normals(self) -> List[Vector]:
        e = self._edges
        return [self.get_normal(e[i], e[i + 1]) for i in range(len(e) - 1)] + [self.get_normal(e[-1], e[0])]

    @property
    def edges(self) -> List[Segment]:
        return self._edges

    @property
    def last_edge(self) -> Segment:
        return self._edges[-1]

    @property
    def first_edge(self) -> Segment:
        return self._edges[0]

    @property
    def second_edge(self) -> Segment:
        return self._edges[1]
