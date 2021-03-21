from typing import List, NoReturn, Tuple, Dict
from enum import Enum
from bisect import insort
from loguru import logger

from line import Line, Algorithm, Color
from point import Point

class Action(Enum):
    ADD_LINE = 0



class Data:
    def __init__(self) -> NoReturn:
        self.lines = dict()
        self.ids = [_ for _ in range(100)]
        # self.lines: List[Line] = []
        

    def _get_id(self) -> int:
        return self.ids.pop(0)
        

    def add_line(self, alg: Algorithm, color: Color, coords: Tuple[Point], line_id: int) -> NoReturn:
        self.lines[line_id] = Line(coords[0], coords[1], alg, color)


    def remove_line(self, line_id: int) -> NoReturn:
        self.lines.pop(line_id)
        insort(self.ids, line_id)
        logger.debug(f"self.ids = {self.ids}")

    def remove_all_lines(self) -> NoReturn:
        self.lines.clear()
        self.ids = [_ for _ in range(100)]


    