from typing import List

from way import Way
from point import Point
from color import Color
from figure import Figure
from ellipse import Ellipse


class Spectrum:
    def __init__(self, figure: Figure, way: Way, color: Color, center: Point,
                 rx_start: int, ry_start: int, step: int, count: int) -> None:
        self._figure_type: Figure = figure
        self._step: int = step
        self._center: Point = center
        self._color: Color = color
        self._way: Way = way
        self._count: int = count
        self._rx_start: int = rx_start
        self._ry_start: int = ry_start
        self._ellipses: List[Ellipse] = []

        self._generate_ellipses()

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

    def _generate_ellipses(self) -> None:
        def _round(num: float) -> int:
            return int(num + (0.5 if num >= 0 else -0.5))

        rx_end: int = self.rx_start + self.count * self.step
        ratio: float = self.ry_start / self.rx_start

        for rx in range(self.rx_start, rx_end+1, self.step):
            self.ellipses.append(
                Ellipse(self.center, rx, _round(rx*ratio), self.way, self.color))
