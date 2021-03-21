from loguru import logger
from point import Point
from enum import Enum
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
    RED = 1
    BLUE = 2
    BLACK = 3

    def __str__(self) -> str:
        interp = {
            Color.BACK: 'Фоновый',
            Color.RED: 'Красный',
            Color.BLUE: 'Синий',
            Color.BLACK: 'Черный'
        }
        return interp[self]

class Line:
    def __init__(self, p_start: Point, p_end: Point, alg: Algorithm, color: Color):
        self.p_start, self.p_end = p_start, p_end
        self.alg = alg
        self.color = color

        self.need_draw = False
        self._points = self._calc_points()

        logger.info(f"ALG: {self.alg}, points = {self._points}")

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
            return num if not num else 1 if num > 0 else -1

        values: List[Point] = []

        length = max(abs(p_end.x - p_start.x), abs(p_end.y - p_start.y))

        dx = (p_end.x - p_start.x) / length
        dy = (p_end.y - p_start.y) / length

        x = p_start.x + 0.5 * _sign(dx)
        y = p_start.y + 0.5 * _sign(dy)

        i = 1
        while(i <= length):
            values.append(Point(int(x), int(y)))
            x += dx
            y += dy
            i += 1

        return values


    @staticmethod
    def _ibres(p_start: Point, p_end: Point) -> List[Point]:
        def _sign(num: float) -> int:
                return 1 if num > 0 else -1

        values: List[Point] = []
        x, y = p_start.x, p_start.y
        dx, dy = abs(p_end.x - p_start.x), abs(p_end.y - p_start.y)
        x_sign, y_sign = _sign(p_end.x - p_start.x), _sign(p_end.y - p_start.y)

        swap = False
        if dy > dx:
            dx, dy = dy, dx
            swap = True

        e = 2*dy - dx

        for _ in range(1, dx+1):
            values.append(Point(x, y))
            while (e >= 0):
                if swap:
                    x += x_sign
                else:
                    y += y_sign

                e -= 2*dx
            
            if swap:
                y += y_sign
            else:
                x += x_sign

            e += 2*dy

        return values

    @staticmethod
    def _rbres(p_start: Point, p_end: Point) -> List[Point]:
        def _sign(num: float) -> int:
            return 1 if num > 0 else -1

        values: List[Point] = []
        x, y = p_start.x, p_start.y
        dx, dy = abs(p_end.x - p_start.x), abs(p_end.y - p_start.y)
        x_sign, y_sign = _sign(p_end.x - p_start.x), _sign(p_end.y - p_start.y)

        swap = False
        if dy > dx:
            dx, dy = dy, dx
            swap = True

        e = dy/dx - 0.5

        for _ in range(1, dx+1):
            values.append(Point(x, y))
            while (e >= 0):
                if swap:
                    x += x_sign
                else:
                    y += y_sign

                e -= 1
            
            if swap:
                y += y_sign
            else:
                x += x_sign

            e += dy/dx

        return values

    # TODO
    @staticmethod
    def _bresimp(p_start: Point, p_end: Point) -> List[Point]:
        def _sign(num: float) -> int:
            return 1 if num > 0 else -1

        values: List[Point] = []
        x, y = p_start.x, p_start.y
        dx, dy = abs(p_end.x - p_start.x), abs(p_end.y - p_start.y)
        x_sign, y_sign = _sign(p_end.x - p_start.x), _sign(p_end.y - p_start.y)

        swap = False
        if dy > dx:
            dx, dy = dy, dx
            swap = True

        e = dy/dx - 0.5

        for _ in range(1, dx + 1):
            values.append(Point(x, y))
            while (e >= 0):
                if swap:
                    x += x_sign
                else:
                    y += y_sign

                e -= 1
            
            if swap:
                y += y_sign
            else:
                x += x_sign

            e += dy/dx

        return values


    # TODO
    @staticmethod
    def _wu(p_start: Point, p_end: Point) -> List[Point]:
        pass

