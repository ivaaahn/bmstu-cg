from typing import List, Union

from color import Color
from way import Way
from point import Point


class Ellipse:
    def __init__(self, center: Point, rx: int, ry: int, way: Way, color: Color):
        self._center: Point = center
        self._rx: int = rx
        self._ry: int = ry
        self._way: Way = way
        self._color: Color = color
        self._points: Union[List[Point], None] = self._calculate()

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

    #TODO
    def _calculate(self) -> Union[List[Point], None]:
        pass