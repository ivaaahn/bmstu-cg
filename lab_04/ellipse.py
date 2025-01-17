from typing import List, Union
from algorithms import Algorithms

from figure import Figure
from color import Color
from way import Way
from point import Point


class Ellipse:
    def __init__(self, center: Point, rx: int, ry: int, way: Way, color: Color):
        self._center = center
        self._rx = rx
        self._ry = ry
        self._way = way
        self._color = color
        self._points: Union[List[Point], None] = None
        self._calculate_points()

    @property
    def color(self) -> Color:
        return self._color

    @property
    def rx(self) -> int:
        return self._rx

    @property
    def ry(self) -> int:
        return self._ry

    @property
    def way(self) -> int:
        return self._way

    @property
    def center(self) -> Point:
        return self._center

    @property
    def points(self) -> Union[List[Point], None]:
        return self._points

    def __repr__(self) -> str:
        return f'Ellipse <({str(self._center)}, {self._rx}, {self._ry}), way: {str(self.way)}, color: {str(self.color)}>'

    def _calculate_points(self):
        figure = Figure.CIRCLE if (self.rx == self.ry) else Figure.ELLIPSE
        method = Algorithms.get_method(figure, self.way)

        if figure is Figure.CIRCLE:
            self._points = method(self.center, self.rx)
        else:
            self._points = method(self.center, self.rx, self.ry)
