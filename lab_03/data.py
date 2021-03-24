from typing import List, NoReturn, Tuple, Dict
from enum import Enum
from bisect import insort
from loguru import logger

from math import cos, pi, sin, radians
import numpy as np

from line import Line, AlgType, Color
from point import Point


class Data:
    def __init__(self, test: bool = False) -> NoReturn:
        self._lines = dict()
        self.line_ids: List[int] = [_ for _ in range(100)]
        self.spectrums: List[List] = []

        self_test_mode = test
        # self._test_lines: List[Line] = []

    def _get_id(self) -> int:
        return self.line_ids.pop(0)

    @property
    def lines(self) -> dict:
        return self._lines

    @property
    def lines_without_labels(self) -> list:
        return list(self._lines.values())


  
        

    def add_line(self, alg: AlgType, color: Color, coords: Tuple[Point], line_id: int) -> NoReturn:
        self._lines[line_id] = Line(coords[0], coords[1], alg, color)

    def remove_line(self, line_id: int) -> NoReturn:
        self._lines.pop(line_id)
        insort(self.line_ids, line_id)

    def remove_all_lines(self) -> NoReturn:
        self._lines.clear()
        self.line_ids = [_ for _ in range(100)]
        
    def _rotate_point(self, point: Point, angle: float) -> Point:
        mtrx = np.array([[cos(angle),   sin(angle),    0],
                        [-sin(angle),   cos(angle),    0],
                        [0,              0,            1]])

        res = point.to_ndarray() @ mtrx
        return Point(int(res[0]), int(res[1]))

    def add_spectrum(self, offset: Point, step: float, length: int, angles: Tuple[float], alg: AlgType, color: Color) -> NoReturn:
        start_point = Point(length, 0)
        all_angles = np.arange(angles[0], angles[1] + 1, step)
        
        p_ends: List[Point] = [self._rotate_point(start_point, radians(angle)) for angle in all_angles]
        spectrum: List[Line] = [Line(offset, offset+point, alg, color) for point in p_ends]
        self.spectrums.append(spectrum)

    def remove_spectrums(self) -> NoReturn:
        self.spectrums.clear()