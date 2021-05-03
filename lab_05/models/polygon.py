from .point import Point


class Polygon:
    def __init__(self):
        self._vertices: list[Point] = []
        self._extrema: list[int] = []

    @property
    def all_vertices(self):
        return self._vertices

    @property
    def all_extrema(self):
        return self._extrema

    def add_vertex(self, vertex: Point) -> None:
        self._vertices.append(vertex)

        if self.size() > 2:
            self.update_extrema()

    def update_extrema(self) -> None:
        vert, curr_index = self._vertices, len(self._vertices) - 2
        if vert[curr_index].y == min([p.y for p in vert[-3:]]) or vert[curr_index].y == max([p.y for p in vert[-3:]]):
            self._extrema.append(curr_index)

        print(self._extrema)

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
