from typing import List, Union
from numpy import linspace

from point import Point
from way import Way
from color import Color
from figure import Figure
from ellipse import Ellipse


class Spectrum:
    def __init__(self, figure: Figure, way: Way, color: Color, center: int,
                 rx_start: int, ry_start: int, step: int, count: int) -> None:
        self._figure_type: Figure = figure
        self._step: int = step
        self._center: Point = center
        self._color: Color = color
        self._way: Way = way
        self._count: int = count
        self._rx_start: int = rx_start
        self._ry_start: int = ry_start
        self._ellipses: List[Ellipse] = self._calculate()

    @property
    def figure_type(self) -> Figure:
        return self._figure_type

    @property
    def step(self) -> int:
        return self._step

    @property
    def count(self) -> int:
        return self._count

    @property
    def rx_start(self) -> int:
        return self._rx_start

    @property
    def ry_start(self) -> int:
        return self._ry_start

    @property
    def ellipses(self) -> List[Ellipse]:
        return self._ellipses

    @property
    def center(self) -> Point:
        return self._center

    @property
    def color(self) -> Color:
        return self._color

    @property
    def way(self) -> Way:
        return self._way

    # TODO
    def _calculate(self) -> List[Ellipse]:
        r_end = self.rx_start + self.count * self.step
        new_spectrum: List[Ellipse] = []

        for r in range(self.rx_start, r_end+1, self.step):
            new_spectrum.append(Ellipse(self.center, r, r, self.way, self.color))

        return new_spectrum