from loguru import logger
from point import Point
from enum import Enum
from typing import NoReturn, List, Tuple

from color import Color
from algorithms import AlgType
from algorithms import Algorithms as Algs


class Line:
    def __init__(self, p_start: Point, p_end: Point, alg: AlgType, color: Color):
        self.p_start, self.p_end = p_start, p_end
        self.alg = alg
        self.color = color
        self._points, self._stairs = self._start_alg()

    @property
    def points(self) -> List[Point]:
        return self._points

    def __repr__(self) -> str:
        return f"Line <{str(self.p_start)}, {str(self.p_end)}, {self.alg}, {self.color}>"


    def _start_alg(self) -> Tuple[List[Point], int]:
        curr_alg = Algs.get_alg(self.alg)
        return curr_alg(self.p_start, self.p_end)
