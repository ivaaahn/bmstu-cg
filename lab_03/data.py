from typing import List, NoReturn, Tuple
from enum import Enum

from line import Line, Algorithm, Color
from point import Point

class Action(Enum):
    ADD_LINE = 0



class Data:
    def __init__(self) -> NoReturn:
        self.lines: List[Line] = []
        

    def add_line(self, alg: Algorithm, color: Color, coords: Tuple[Point]) -> NoReturn:
        self.lines.append(Line(coords[0], coords[1], alg, color))

    