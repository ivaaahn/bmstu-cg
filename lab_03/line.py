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

        # self.need_draw = False
        self._points, self._stairs = self._start_alg()
        # print(self._stairs)

        # logger.info(f"ALG: {self.alg}, points = {self._points}")

    @property
    def points(self) -> List[Point]:
        return self._points

    def __repr__(self) -> str:
        return f"Line <{str(self.p_start)}, {str(self.p_end)}, {self.alg}, {self.color}>"

    # def show(self):
    #     self.need_draw = True

    # def hide(self):
    #     self.need_draw = False


    def _start_alg(self) -> Tuple[List[Point], int]:
        curr_alg = Algs.get_alg(self.alg)
        return curr_alg(self.p_start, self.p_end)

    # @staticmethod
    # def _lib(p_start: Point, p_end: Point) -> None:
    #     return None

    # @staticmethod
    # def _dda(p_start: Point, p_end: Point) -> List[Point]:
    #     def _round(num: float) -> int:
    #         return int(num + (0.5 if num > 0 else -0.5))

    #     values: List[Point] = []

    #     if p_start == p_end:
    #         values.append(p_start)
    #         return values

    #     length = max(abs(p_end.x - p_start.x), abs(p_end.y - p_start.y))

    #     dx = (p_end.x - p_start.x) / length
    #     dy = (p_end.y - p_start.y) / length

    #     x = p_start.x
    #     y = p_start.y

    #     for _ in range(1, length + 1):
    #         values.append(Point(_round(x), _round(y)))
    #         x += dx
    #         y += dy

    #     return values

    # @staticmethod
    # def _ibres(p_start: Point, p_end: Point) -> List[Point]:
    #     def _sign(num: float) -> int:
    #         return 1 if num > 0 else -1 if num < 0 else 0

    #     values: List[Point] = []

    #     if p_start == p_end:
    #         values.append(p_start)
    #         return values

    #     x_sign, y_sign = _sign(p_end.x - p_start.x), _sign(p_end.y - p_start.y)
    #     dx, dy = abs(p_end.x - p_start.x), abs(p_end.y - p_start.y)

    #     swap = False
    #     if dy > dx:
    #         dx, dy = dy, dx
    #         swap = True

    #     err = 2 * dy - dx

    #     x, y = p_start.x, p_start.y

    #     for _ in range(1, dx+1):
    #         values.append(Point(x, y))
    #         if err >= 0:
    #             if swap:
    #                 x += x_sign
    #             else:
    #                 y += y_sign

    #             err -= 2*dx

    #         if err < 0:
    #             if swap:
    #                 y += y_sign
    #             else:
    #                 x += x_sign

    #         err += 2*dy

    #     return values

    # @staticmethod
    # def _rbres(p_start: Point, p_end: Point) -> List[Point]:
    #     def _sign(num: float) -> int:
    #         return 1 if num > 0 else -1 if num < 0 else 0

    #     values: List[Point] = []

    #     if p_start == p_end:
    #         values.append(p_start)
    #         return values

    #     x_sign, y_sign = _sign(p_end.x - p_start.x), _sign(p_end.y - p_start.y)
    #     dx, dy = abs(p_end.x - p_start.x), abs(p_end.y - p_start.y)

    #     swap = False
    #     if dy > dx:
    #         dx, dy = dy, dx
    #         swap = True

    #     m = dy/dx
    #     err = m - 0.5
    #     x, y = p_start.x, p_start.y

    #     for _ in range(1, dx+1):
    #         values.append(Point(x, y))
    #         if err >= 0:
    #             if swap:
    #                 x += x_sign
    #             else:
    #                 y += y_sign

    #             err -= 1

    #         if err < 0:
    #             if swap:
    #                 y += y_sign
    #             else:
    #                 x += x_sign

    #         err += m

    #     return values

    # # TODO

    # @staticmethod
    # def _bresimp(p_start: Point, p_end: Point) -> List[Point]:
    #     def _sign(num: float) -> int:
    #         return 1 if num > 0 else -1 if num < 0 else 0

    #     def _round(num: float) -> int:
    #         return int(num + (0.5 if num > 0 else -0.5))

    #     intens: int = 100

    #     values: List[Point] = []

    #     if p_start == p_end:
    #         values.append(p_start)
    #         return values

    #     x_sign, y_sign = _sign(p_end.x - p_start.x), _sign(p_end.y - p_start.y)
    #     dx, dy = abs(p_end.x - p_start.x), abs(p_end.y - p_start.y)

    #     swap = False
    #     if dy > dx:
    #         dx, dy = dy, dx
    #         swap = True

    #     m = dy/dx * intens
    #     err = intens/2
    #     w = intens - m
    #     x, y = p_start.x, p_start.y

    #     values.append(Point(x, y, _round(err)))

    #     for _ in range(1, dx):
    #         if err >= w:
    #             if swap:
    #                 x += x_sign
    #             else:
    #                 y += y_sign

    #             err -= intens

    #         if err < w:
    #             if swap:
    #                 y += y_sign
    #             else:
    #                 x += x_sign

    #         err += m 

    #         values.append(Point(x, y, _round(err)))
    #     return values

    # # !OLD

    # # @staticmethod
    # # def _wu2(p_begin: Point, p_end: Point) -> List[Point]:
    # #     def _fpart(x):
    # #         return x - int(x)
        
    # #     def _rfpart(x):
    # #         return 1 - _fpart(x)

    # #     pb, pe = p_begin, p_end

    # #     print('START:', pb, pe)


    # #     values: List[Point] = []
        
    # #     if pb == pe:
    # #         values.append(pb)
    # #         return values

    # #     x1, y1 = pb.value
    # #     x2, y2 = pe.value
    # #     dx, dy = x2-x1, y2-y1
    # #     steep = abs(dy) > abs(dx)

    # #     def p_handler(steep, x, y, intens=100) -> Point:
    # #         res = ((x, y), (y, x))[steep]
    # #         return Point(res[0], res[1], intens)

    # #     # Делаем так, чтобы итерироваться по прямой слева направо и вдоль иксов было длиннее
    # #     if steep:
    # #         x1, y1, x2, y2, dx, dy = y1, x1, y2, x2, dy, dx
    # #     if x1 > x2:
    # #         x1, x2, y1, y2 = x2, x1, y2, y1
    
    # #     # print(f"pb: ({x1}, {y1}), pe: ({x2}, {y2})")

    # #     m: float = dy/dx
    # #     next_y: float = y1
    # #     for x in range(x1, x2+1):
    # #         y = int(next_y)
    # #         values.append(p_handler(steep, x, y, 100 *_rfpart(next_y)))
    # #         values.append(p_handler(steep, x, y+1, 100 *_fpart(next_y)))
    # #         next_y += m

    # #     return values



    # @staticmethod
    # def _wu(p_begin: Point, p_end: Point) -> List[Point]:
    #     def _fpart(num):
    #         return num - int(num)
        
    #     def _rfpart(num):
    #         return 1 - _fpart(num)

    #     pb, pe = p_begin.copy(), p_end.copy()
    #     values: List[Point] = []
        
    #     if pb == pe:
    #         values.append(pb)
    #         return values

    #     dx, dy = pe.x-pb.x, pe.y-pb.y

    #     swapped = False
    #     if abs(dy) > abs(dx):
    #         dx, dy = dy, dx
    #         pb.x, pb.y, pe.x, pe.y, = pb.y, pb.x, pe.y, pe.x 
    #         swapped = True
    #     if pb.x > pe.x:
    #         pb, pe = pe, pb

    #     m: float = dy/dx
    #     next_y: float = pb.y
    #     for x in range(pb.x, pe.x+1):
    #         y = int(next_y)
    #         if swapped:
    #             values.append(Point(y, x, 100*_rfpart(next_y)))
    #             values.append(Point(y+1, x, 100*_fpart(next_y)))
    #         else:
    #             values.append(Point(x, y, 100*_rfpart(next_y)))
    #             values.append(Point(x, y+1, 100*_fpart(next_y)))

    #         next_y += m

    #     return values