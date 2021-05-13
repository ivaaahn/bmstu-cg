from typing import List, Optional

from properties.color import Color
from .point import Point
from .polygon import Polygon


class Figure:
    def __init__(self, color: Color = Color.BLACK) -> None:
        self._color = color
        self._data: List[Polygon] = [Polygon()]
        self._seed_pixel: Optional[Point] = None

    def __bool__(self) -> bool:
        return not self.is_empty()

    @property
    def seed_pixel(self) -> Optional[Point]:
        return self._seed_pixel

    @seed_pixel.setter
    def seed_pixel(self, pixel: Point) -> None:
        self._seed_pixel = pixel

    def is_empty(self) -> bool:
        return len(self._data) == 1 and self.last_polygon.size() == 0

    def clear(self) -> None:
        self._data = [Polygon()]
        self._seed_pixel = None

    def add_polygon(self) -> None:
        self._data.append(Polygon())

    @property
    def all_polygons(self) -> List[Polygon]:
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

    def add_vertex(self, vertex: Point) -> None:
        self.last_polygon.add_vertex(vertex)

    def close_this_polygon(self) -> None:
        self.last_polygon.close()
        self.add_polygon()
