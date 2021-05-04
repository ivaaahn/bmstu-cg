from .point import Point


class Polygon:
    def __init__(self):
        self._vertices: list[Point] = []

    @property
    def all_vertices(self):
        return self._vertices

    def add_vertex(self, vertex: Point) -> None:
        self._vertices.append(vertex)

    def is_closed(self) -> bool:
        return len(self._vertices) > 1 and (self._vertices[0] == self._vertices[-1])

    def close(self) -> None:
        self.add_vertex(self._vertices[0])

    def size(self) -> int:
        return len(self._vertices)

    @property
    def first_vrtx(self) -> Point:
        return self._vertices[0]

    @property
    def last_vrtx(self) -> Point:
        return self._vertices[-1]

    @property
    def pre_last_vrtx(self) -> Point:
        return self._vertices[-2]
