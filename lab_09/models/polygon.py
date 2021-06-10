from typing import List, Optional

from PyQt5.QtWidgets import QMessageBox

from exceptions import UnableToClose, SelfIntersection
from models.point import Point
from models.edge import Edge


class Polygon:
    def __init__(self, from_user: bool = True):
        self._vertices: List[Point] = []
        self._closed = False
        self._from_user = from_user

    def reset(self) -> None:
        self._vertices.clear()
        self._closed = False

    def reverse(self) -> None:
        self._vertices.reverse()

    def self_intersections_exist(self, v: Point, closing: bool) -> bool:
        edges = iter(self.edges[:-1])
        if closing:
            next(edges)

        for edge in edges:
            if Edge.is_intersect(edge, Edge(self.vertices[-1], v)):
                return True

        return False

    def add_vertex(self, v: Point, straight: bool = False, closing: bool = False) -> Optional[Edge]:
        if len(self.vertices) >= 1 and straight:
            prev = self.vertices[-1]
            if abs(v.x - prev.x) < abs(v.y - prev.y):
                v.x = prev.x
            else:
                v.y = prev.y

        # Проверка на самопересечения только при вводе многоугольника пользователем
        if self._from_user:
            if len(self.vertices) >= 3 and self.self_intersections_exist(v, closing):
                raise SelfIntersection("Многоугольник не может содержать самопересечения")

        self.vertices.append(v)

        if len(self.vertices) < 2:
            return None

        return Edge(self.vertices[-2], self.vertices[-1])

    @property
    def vertices(self) -> List[Point]:
        return self._vertices

    def close(self) -> Edge:
        if not self._vertices_enough_to_close():
            raise UnableToClose('Недостаточно ребер, чтобы замкнуть')

        if self.vertices[-1] != self.vertices[0]:
            self.add_vertex(self.vertices[0], closing=True)

        self._closed = True
        return Edge(self.vertices[-2], self.vertices[-1])

    def is_closed(self) -> bool:
        return self._closed

    def _vertices_enough_to_close(self) -> bool:
        return len(self._vertices) >= 3

    @property
    def edges(self) -> List[Edge]:
        v = self._vertices
        return [Edge(v[i], v[i + 1]) for i in range(len(v) - 1)]
