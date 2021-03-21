from PyQt5.QtCore import QPoint
from loguru import logger
from point import Point
from enum import Enum
import typing
from typing import NoReturn, List

class Algorithm(Enum):
    LIB = 0
    DDA = 1
    RB = 2
    IB = 3
    BIMP = 4
    WU = 5

    def __str__(self) -> str:
        interp = {
            Algorithm.LIB: 'Библиотечная функция',
            Algorithm.DDA: 'ЦДА',
            Algorithm.RB: 'Брезенхем (действит.)',
            Algorithm.IB: 'Брезенхем (целочисл.)',
            Algorithm.BIMP: 'Брезенхем (устр. ступ)',
            Algorithm.WU: 'Ву'
        }
        return interp[self]


class Color(Enum):
    BACK = 0
    MAIN = 1

    def __str__(self) -> str:
        interp = {
            Color.BACK: 'Фоновый',
            Color.MAIN: 'Красный'
        }
        return interp[self]

class Line:
    def __init__(self, p_start: Point, p_end: Point, alg: Algorithm, color: Color):
        self.p_start, self.p_end = p_start, p_end
        self.alg = alg
        self.color = color

        self.need_draw = False
        self._points = self._calc_points()

        logger.info(f"points = {self._points}")

    @property
    def points(self) -> List[Point]:
        return self._points

    def __repr__(self) -> str:
        return f"Line <{str(self.p_start)}, {str(self.p_end)}, {self.alg}, {self.color}>"

    def show(self):
        self.need_draw = True

    def hide(self):
        self.need_draw = False

    def _calc_points(self) -> List[Point]:
        method = {
            Algorithm.LIB   : self._lib,
            Algorithm.DDA   : self._dda,
            Algorithm.RB    : self._rbres,
            Algorithm.IB    : self._ibres,
            Algorithm.BIMP  : self._bresimp,
            Algorithm.WU    : self._wu,
        }

        return method[self.alg](self.p_start, self.p_end)


    @staticmethod
    def _lib(p_start: Point, p_end: Point) -> None:
        return None


    @staticmethod
    def _dda(p_start: Point, p_end: Point) -> List[Point]:
        def _sign(num: float) -> int:
                return 1 if num > 0 else -1

        values: List[Point] = []

        length = max(abs(p_end.x - p_start.x), abs(p_end.y - p_start.y))

        dx = (p_end.x - p_start.x) / length
        dy = (p_end.y - p_start.y) / length

        x = int(p_start.x + 0.5 * _sign(dx))
        y = int(p_start.y + 0.5 * _sign(dy))

        i = 1
        while(i <= length):
            values.append(Point(x, y))
            x += dx
            y += dy
            i += 1

        return values



    @staticmethod
    def _ibres(p_start: Point, p_end: Point) -> List[Point]:
        pass

    @staticmethod
    def _rbres(p_start: Point, p_end: Point) -> List[Point]:
        pass

    @staticmethod
    def _bresimp(p_start: Point, p_end: Point) -> List[Point]:
        pass

    @staticmethod
    def _wu(p_start: Point, p_end: Point) -> List[Point]:
        pass



class DDA:
    def __init__(self):
        self._need_draw = False
        self._values = []
        
    @property
    def values(self) -> list:
        if not self._need_draw:
            return []
        else:
            if not self._raw_values:
                self._update_values()
            return self._values

    def _update_values(self) -> typing.NoReturn:
        pass


class Wu:
    def __init__(self):
        self._need_draw = False
        self._values = []
    
    @property
    def values(self) -> list:
        if not self._need_draw:
            return []
        else:
            if not self._raw_values:
                self._update_values()
            return self._values

    def _update_values(self) -> typing.NoReturn:
        pass

class RBresenham:
    def __init__(self):
        self._need_draw = False
        self._values = []
        
    @property
    def values(self) -> list:
        if not self._need_draw:
            return []
        else:
            if not self._raw_values:
                self._update_values()
            return self._values

    def _update_values(self) -> typing.NoReturn:
        pass


class IBresenham:
    def __init__(self):
        self._need_draw = False
        self._values = []
    
    @property
    def values(self) -> list:
        if not self._need_draw:
            return []
        else:
            if not self._raw_values:
                self._update_values()
            return self._values

    def _update_values(self) -> typing.NoReturn:
        pass

class BresenhamImproved:
    def __init__(self):
        self._need_draw = False
        self._values = []
        
    @property
    def values(self) -> list:
        if not self._need_draw:
            return []
        else:
            if not self._raw_values:
                self._update_values()
            return self._values

    def _update_values(self) -> typing.NoReturn:
        pass

