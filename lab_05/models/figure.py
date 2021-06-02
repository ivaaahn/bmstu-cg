import utils
from properties.color import Color
from .point import Point
from .polygon import Polygon


class Figure:
    def __init__(self, color: Color = Color.MAGENTA) -> None:
        self._color = color
        self._data: list[Polygon] = [Polygon()]
        self.p_min = Point(utils.W + 10, utils.H + 10)
        self.p_max = Point(-10, -10)

    def __bool__(self) -> bool:
        return not self.is_empty()

    def is_empty(self) -> bool:
        return len(self._data) == 1 and self.last_polygon.size() == 0

    def clear(self) -> None:
        self.p_min = Point(100000, 100000)
        self.p_max = Point(-100000, -100000)
        self._data = [Polygon()]

    def add_polygon(self) -> None:
        self._data.append(Polygon())

    @property
    def all_polygons(self):
        return self._data

    @property
    def color(self) -> Color:
        return self._color

    @color.setter
    def color(self, color: Color) -> None:
        self._color = color

    @property
    def last_polygon(self) -> Polygon:
        return self._data[-1]

    def add_vertex(self, vertex: Point):
        self.p_max.x = max(vertex.x, self.p_max.x)
        self.p_max.y = max(vertex.y, self.p_max.y)

        self.p_min.x = min(vertex.x, self.p_min.x)
        self.p_min.y = min(vertex.y, self.p_min.y)

        self.last_polygon.add_vertex(vertex)

    def close_this_polygon(self) -> None:
        self.last_polygon.close()
        self.add_polygon()
