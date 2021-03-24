from timeit import timeit
from enum import Enum
from typing import List
import time
from numpy import float64, int64, double

from point import Point

COUNT = 5000

class AlgType(Enum):
    LIB = 0
    DDA = 1
    RB = 2
    IB = 3
    BIMP = 4
    WU = 5

    def __str__(self) -> str:
        interp = {
            AlgType.LIB: 'Библиотечная функция',
            AlgType.DDA: 'ЦДА',
            AlgType.RB: 'Брезенхем (действит.)',
            AlgType.IB: 'Брезенхем (целочисл.)',
            AlgType.BIMP: 'Брезенхем (устр. ступ)',
            AlgType.WU: 'Ву'
        }
        return interp[self]
    
    @staticmethod
    def get_all() -> list:
        return [AlgType(i) for i in range(len(AlgType))]

class testAlgs:
    def __init__(self) -> None:
        self.count = COUNT
        self.p_start = Point(321, 135)
        self.p_end = Point(789, 849)


    def start_test(self) -> dict:
        alg_types = AlgType.get_all()[1:]
        # alg_types = [AlgType(2), AlgType(3)]
        
        res = {}

        for alg_type in alg_types:
            alg = Algorithms.get_alg(alg_type)
            res[alg_type] = timeit(lambda: alg(self.p_start, self.p_end), number=self.count) / self.count * 1000
            
            # print(f'{alg_type} : {round(res * 1000, 5)} ms')

        return res

#   # TODO
#     def start_test(self, center: Point):
#         algs = [AlgType(i) for i in range(1, len(AlgType))]

#         START_ANGLE, END_ANGLE, STEP = 0, 360, 30
#         START_LEN, END_LEN, STEP = 10, 500, 10 
#         all_angles = range(START_ANGLE, END_ANGLE, STEP)
#         all_lens = range(START_LEN, END_LEN, STEP)

#         # LEN = 500
#         # ANGLE = 30

#         for length in all_lens:
#             start_point = Point(length, 0)
#             p_ends: List[Point] = [self._rotate_point(start_point, radians(angle)) for angle in all_angles]
#             spectrum: List[Line] = [Line(offset, offset+point, alg, color) for point in p_ends]





class Algorithms:
    @staticmethod
    def get_alg(alg_type: AlgType):
        method = {
            AlgType.LIB: Algorithms._lib,
            AlgType.DDA: Algorithms._dda,
            AlgType.RB: Algorithms._rbres,
            AlgType.IB: Algorithms._ibres,
            AlgType.BIMP: Algorithms._bresimp,
            AlgType.WU: Algorithms._wu,
        }

        return method[alg_type]


    @staticmethod
    def _lib(p_start: Point, p_end: Point) -> None:
        return None


    @staticmethod
    def _dda(p_start: Point, p_end: Point) -> List[Point]:
        def _round(num: float) -> int:
            return int(num + (0.5 if num > 0 else -0.5))

        values: List[Point] = []
        stairs: int = 0

        if p_start == p_end:
            values.append(p_start)
            return values

        length = int(max(abs(p_end.x - p_start.x), abs(p_end.y - p_start.y)))

        dx = (p_end.x - p_start.x) / length
        dy = (p_end.y - p_start.y) / length

        x = p_start.x
        y = p_start.y

        for _ in range(1, length + 1):
            values.append(Point(_round(x), _round(y)))
            x += dx
            y += dy

        return values

    def wait(secs):
     def decorator(func):
         def wrapper(*args, **kwargs):
             time.sleep(secs)
             return func(*args, **kwargs)
         return wrapper
     return decorator

    @staticmethod
    def _ibres(p_start: Point, p_end: Point) -> List[Point]:
        def _sign(num: float) -> int:
            return 1 if num > 0 else -1 if num < 0 else 0

        values: List[Point] = []

        if p_start == p_end:
            values.append(p_start)
            return values

        x_sign, y_sign = _sign(p_end.x - p_start.x), _sign(p_end.y - p_start.y)
        dx, dy = abs(p_end.x - p_start.x), abs(p_end.y - p_start.y)

        swap = False
        if dy > dx:
            dx, dy = dy, dx
            swap = True

        err = int(2*dy-dx)

        ddx, ddy = int(2*dx), int(2*dy)
        x, y = p_start.x, p_start.y

        for _ in range(1, dx+1):
            values.append(Point(x, y))
            if err >= 0:
                if swap:
                    x += x_sign
                else:
                    y += y_sign

                err = err - ddx

            if err < 0:
                if swap:
                    y += y_sign
                else:
                    x += x_sign

            err = err + ddy

        return values

    @staticmethod
    @wait(1e-16)
    def _rbres(p_start: Point, p_end: Point) -> List[Point]:
        def _sign(num: float) -> int:
            return 1 if num > 0 else -1 if num < 0 else 0

        values: List[Point] = []

        if p_start == p_end:
            values.append(p_start)
            return values

        x_sign, y_sign = _sign(p_end.x - p_start.x), _sign(p_end.y - p_start.y)
        dx, dy = abs(p_end.x - p_start.x), abs(p_end.y - p_start.y)

        swap = False
        if dy > dx:
            dx, dy = dy, dx
            swap = True

        m = dy/dx
        err = m-0.5
        x, y = p_start.x, p_start.y

        for _ in range(1, dx+1):
            values.append(Point(x, y))
            if err >= 0:
                if swap:
                    x += x_sign
                else:
                    y += y_sign

                err = err - 1.0

            if err < 0:
                if swap:
                    y += y_sign
                else:
                    x += x_sign

            err = err + m

        return values

    @staticmethod
    def _bresimp(p_start: Point, p_end: Point) -> List[Point]:
        def _sign(num: float) -> int:
            return 1 if num > 0 else -1 if num < 0 else 0

        def _round(num: float) -> int:
            return int(num + (0.5 if num > 0 else -0.5))

        intens = 100

        values: List[Point] = []

        if p_start == p_end:
            values.append(p_start)
            return values

        x_sign, y_sign = _sign(p_end.x - p_start.x), _sign(p_end.y - p_start.y)
        dx, dy = abs(p_end.x - p_start.x), abs(p_end.y - p_start.y)

        swap = False
        if dy > dx:
            dx, dy = dy, dx
            swap = True

        m = dy/dx * intens
        err = intens/2
        w = intens - m
        x, y = p_start.x, p_start.y

        values.append(Point(x, y, _round(err)))

        for _ in range(1, dx):
            if err >= w:
                if swap:
                    x += x_sign
                else:
                    y += y_sign

                err -= intens

            if err < w:
                if swap:
                    y += y_sign
                else:
                    x += x_sign

            err += m 

            values.append(Point(x, y, _round(err)))
        return values

    @staticmethod
    def _wu(p_begin: Point, p_end: Point) -> List[Point]:
        def _fpart(num):
            return num - int(num)
        
        def _rfpart(num):
            return 1 - _fpart(num)

        pb, pe = p_begin.copy(), p_end.copy()
        values: List[Point] = []
        
        if pb == pe:
            values.append(pb)
            return values

        dx, dy = pe.x-pb.x, pe.y-pb.y

        swapped = False
        if abs(dy) > abs(dx):
            dx, dy = dy, dx
            pb.x, pb.y, pe.x, pe.y, = pb.y, pb.x, pe.y, pe.x 
            swapped = True
        if pb.x > pe.x:
            pb, pe = pe, pb

        m = dy/dx
        next_y = pb.y
        for x in range(pb.x, pe.x+1):
            y = int(next_y)
            if swapped:
                values.append(Point(y, x, 100*_rfpart(next_y)))
                values.append(Point(y+1, x, 100*_fpart(next_y)))
            else:
                values.append(Point(x, y, 100*_rfpart(next_y)))
                values.append(Point(x, y+1, 100*_fpart(next_y)))

            next_y += m

        return values


    # @staticmethod
    # def _dda(p_start: Point, p_end: Point) -> List[Point]:
    #     def _round(num: float) -> int64:
    #         return int64(num + (0.5 if num > 0 else -0.5))

    #     values: List[Point] = []

    #     if p_start == p_end:
    #         values.append(p_start)
    #         return values

    #     length = int64(max(abs(p_end.x - p_start.x), abs(p_end.y - p_start.y)))

    #     dx = float64((p_end.x - p_start.x) / length)
    #     dy = float64((p_end.y - p_start.y) / length)

    #     x = float64(p_start.x)
    #     y = float64(p_start.y)

    #     for _ in range(1, length + 1):
    #         values.append(Point(_round(x), _round(y)))
    #         x += dx
    #         y += dy

    #     return values

    # @staticmethod
    # def _ibres(p_start: Point, p_end: Point) -> List[Point]:
    #     def _sign(num: float) -> int64:
    #         return 1 if num > 0 else -1 if num < 0 else 0

    #     values: List[Point] = []

    #     if p_start == p_end:
    #         values.append(p_start)
    #         return values

    #     x_sign, y_sign = int64(_sign(p_end.x - p_start.x)), int64(_sign(p_end.y - p_start.y))
    #     dx, dy = int64(abs(p_end.x - p_start.x)), int64(abs(p_end.y - p_start.y))


    #     swap = False
    #     if dy > dx:
    #         dx, dy = dy, dx
    #         swap = True

    #     err = int64(2*dy-dx)

    #     ddx, ddy = int64(2*dx), int64(2*dy)
    #     x, y = int64(p_start.x), int64(p_start.y)

    #     for _ in range(1, dx+1):
    #         values.append(Point(x, y))
    #         if err >= 0:
    #             if swap:
    #                 x += x_sign
    #             else:
    #                 y += y_sign

    #             err = err - ddx

    #         if err < 0:
    #             if swap:
    #                 y += y_sign
    #             else:
    #                 x += x_sign

    #         err = err + ddy

    #     return values

    # @staticmethod
    # def _rbres(p_start: Point, p_end: Point) -> List[Point]:
    #     def _sign(num: float) -> int:
    #         return 1 if num > 0 else -1 if num < 0 else 0

    #     values: List[Point] = []

    #     if p_start == p_end:
    #         values.append(p_start)
    #         return values

    #     x_sign, y_sign = int64(_sign(p_end.x - p_start.x)), int64(_sign(p_end.y - p_start.y))
    #     dx, dy = int64(abs(p_end.x - p_start.x)), int64(abs(p_end.y - p_start.y))

    #     swap = False
    #     if dy > dx:
    #         dx, dy = dy, dx
    #         swap = True

    #     m = float64(dy/dx)
    #     err = float64(m-0.5)
    #     x, y = int64(p_start.x), int64(p_start.y)

    #     for _ in range(1, dx+1):
    #         values.append(Point(x, y))
    #         if err >= 0:
    #             if swap:
    #                 x += x_sign
    #             else:
    #                 y += y_sign

    #             err = err - 1.0

    #         if err < 0:
    #             if swap:
    #                 y += y_sign
    #             else:
    #                 x += x_sign

    #         err = err + m

    #     return values

    # # TODO

    # @staticmethod
    # def _bresimp(p_start: Point, p_end: Point) -> List[Point]:
    #     def _sign(num: float) -> int:
    #         return 1 if num > 0 else -1 if num < 0 else 0

    #     def _round(num: float) -> int:
    #         return int(num + (0.5 if num > 0 else -0.5))

    #     intens = 100

    #     values: List[Point] = []

    #     if p_start == p_end:
    #         values.append(p_start)
    #         return values

    #     x_sign, y_sign = int64(_sign(p_end.x - p_start.x)), int64(_sign(p_end.y - p_start.y))
    #     dx, dy = int64(abs(p_end.x - p_start.x)), int64(abs(p_end.y - p_start.y))

    #     swap = False
    #     if dy > dx:
    #         dx, dy = dy, dx
    #         swap = True

    #     m = float64(dy/dx * intens)
    #     err = float64(intens/2)
    #     w = float64(intens - m)
    #     x, y = int64(p_start.x), int64(p_start.y)

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

    # @staticmethod
    # def _wu(p_begin: Point, p_end: Point) -> List[Point]:
    #     def _fpart(num):
    #         return num - int64(num)
        
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

    #     m = float64(dy/dx)
    #     next_y = float64(pb.y)
    #     for x in range(int64(pb.x), int64(pe.x+1)):
    #         y = int64(next_y)
    #         if swapped:
    #             values.append(Point(y, x, 100*_rfpart(next_y)))
    #             values.append(Point(y+1, x, 100*_fpart(next_y)))
    #         else:
    #             values.append(Point(x, y, 100*_rfpart(next_y)))
    #             values.append(Point(x, y+1, 100*_fpart(next_y)))

    #         next_y += m

    #     return values