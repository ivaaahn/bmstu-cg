from typing import List, Tuple


from point import Point
from color import Color
from algorithms import AlgType
from algorithms import Algorithms as Algs


class Line:
    def __init__(self, p_start: Point, p_end: Point, alg: AlgType, color: Color):
        self.p_start, self.p_end = p_start, p_end
        self._alg_type = alg
        self._color = color
        self._points, self._stairs = self._get_points_and_stairs()

    @property
    def color(self) -> Color:
        return self._color

    @property
    def alg(self) -> AlgType:
        return self._alg_type

    @property
    def points(self) -> List[Point]:
        return self._points

    def __repr__(self) -> str:
        return f"Line <{str(self.p_start)}, {str(self.p_end)}, {self.alg}, {self.color}>"

    def _get_points_and_stairs(self) -> Tuple[List[Point], int]:
        curr_alg = Algs.get_alg(self.alg)
        return curr_alg(self.p_start, self.p_end)
