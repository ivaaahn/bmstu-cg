from typing import List, Optional, Tuple

from exceptions import UnableToClose, NonConvex, DegenerateCutter
from models.point import Point
from models.segment import Segment
from models.vector import Vector


class Cutter:
    def __init__(self):
        self._last_vertex: Optional[Point] = None
        self._vertices: List[Point] = []
        self._edges: List[Segment] = []
        self._normals: List[float] = []
        self._closed: bool = False
        self._sign = None

    def reset(self) -> None:
        self._last_vertex = None
        self._edges.clear()
        self._closed = False
        self._sign = None
        self._normals.clear()
        self.vertices.clear()

    @property
    def vertices(self) -> List[Point]:
        if not self._vertices:
            self._vertices = [e.p1 for e in self.edges]

        return self._vertices

    def get_closing_edge(self) -> Segment:
        return Segment(self.last_edge.p2, self.first_edge.p1)

    def add_edge(self, new_edge: Segment) -> None:
        if len(self.edges) >= 2 and not self._is_convex(self.last_edge, new_edge):
            raise NonConvex("Невыпуклый отсекатель")

        self.edges.append(new_edge)

        if len(self.edges) >= 2 and self._sign is None:
            self.set_sign()

    def close(self) -> Segment:
        if not self._edges_enough():
            raise UnableToClose('Недостаточно ребер, чтобы замкнуть отсекатель')

        closing_edge = self.get_closing_edge()

        if not self._is_convex(closing_edge, self.first_edge):
            raise NonConvex("Невыпуклый отсекатель")

        self.add_edge(closing_edge)

        if self._sign is None:
            raise DegenerateCutter("Вырожденный отсекатель")

        self._closed = True

        return closing_edge

    def is_closed(self) -> bool:
        return self._closed

    def _edges_enough(self) -> bool:
        return len(self._edges) >= 2

    def _is_convex(self, e1: Segment, e2: Segment) -> bool:
        if self._sign is None:
            return True
        return self._sign * Vector.cross_prod(e1.to_vector(), e2.to_vector()) >= 0

    def set_sign(self) -> None:
        cross_prod = Vector.cross_prod(self.edges[-2].to_vector(), self.edges[-1].to_vector())
        if cross_prod > 0:
            self._sign = 1
        elif cross_prod < 0:
            self._sign = -1

    def _get_normal(self, seg_index: int):
        curr_edge = self.edges[seg_index]
        vector = curr_edge.to_vector()

        n = vector.normal()

        verts = self.vertices
        dot_prod = 0
        p = seg_index + 2
        while not dot_prod and p < len(self.vertices) + seg_index:
            dot_prod = Vector.dot_prod(n, Segment(curr_edge.p1, verts[p % len(verts)]).to_vector())
            p += 1

        if dot_prod < 0:
            n = -n

        return n

    @property
    def normals(self) -> List[Vector]:
        if not self._normals:
            self._normals = [self._get_normal(i) for i in range(len(self.edges))]

        return self._normals

    def get_tangents(self) -> List[Optional[float]]:
        return [e.tangent for e in self.edges]

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

    def edges_with_distance(self, p: Point) -> List[Tuple[Segment, float]]:
        return list(zip(self.edges, [e.dist(p) for e in self.edges]))
