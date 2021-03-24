from typing import List, NoReturn, Tuple, Dict
from enum import Enum
from bisect import insort
from loguru import logger

from math import cos, pi, sin, radians
import numpy as np

from numpy import arange

from line import Line
from algorithms import AlgType
from algorithms import Algorithms as algs
from color import Color
from point import Point


class Data:
    def __init__(self) -> None:
        self._lines: dict = {}
        self.line_ids: List[int] = [_ for _ in range(100)]
        self.spectrums: List[List] = []

    def _get_id(self) -> int:
        return self.line_ids.pop(0)

    @property
    def lines(self) -> dict:
        return self._lines

    @property
    def lines_without_labels(self) -> List[Line]:
        return list(self._lines.values())

    def add_line(self, alg: AlgType, color: Color, coords: Tuple[Point], line_id: int) -> None:
        self._lines[line_id] = Line(coords[0], coords[1], alg, color)

    def remove_line(self, line_id: int) -> None:
        self._lines.pop(line_id)
        insort(self.line_ids, line_id)

    def remove_all_lines(self) -> None:
        self._lines.clear()
        self.line_ids = [_ for _ in range(100)]

    def add_spectrum(self, center: Point, step: float, length: int, angles: Tuple[float], alg: AlgType, color: Color) -> None:
        if length == 0:
            spectrum: List[Line] = [Line(center, center, alg, color)]
        else:
            p_begin = Point(length, 0)
            p_ends: List[Point] = [algs.rotate_point(p_begin, radians(a)) for a in arange(angles[0], angles[1] + 1, step)]
            spectrum: List[Line] = [Line(center, center+point, alg, color) for point in p_ends]
            
        self.spectrums.append(spectrum)

    def remove_spectrums(self) -> None:
        self.spectrums.clear()
