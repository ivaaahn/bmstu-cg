import time
import numpy as np
from math import ceil, radians, sin, cos
from timeit import timeit
from enum import Enum
from typing import Dict, List, Tuple

from point import Point


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


class AlgsTesting:
    def __init__(self) -> None:
        self.alg_types = AlgType.get_all()[1:]

    def time_test(self) -> dict:
        count = 1000
        p_start = Point(321, 135)
        p_end = Point(789, 849)
        res = {}

        for alg_type in self.alg_types:
            alg = Algorithms.get_alg(alg_type)
            res[alg_type] = timeit(lambda: alg(
                p_start, p_end), number=count) / count * 1000

        return res

    def stairs_test(self) -> Tuple[Tuple, Dict]:
        length = 50
        start_point: Point = Point(length, 0)
        all_angles: Tuple[int] = tuple(range(0, 91, 5))
        p_ends: List[Point] = [Algorithms.rotate_point(
            start_point, radians(angle)) for angle in all_angles]
        center: Point = Point(0, 0)

        stairs = {}
        for alg_type in self.alg_types:
            alg = Algorithms.get_alg(alg_type)
            stairs[alg_type] = [alg(center, center+point)[1]
                                for point in p_ends]  # stairs

        return all_angles, stairs


class Algorithms:
    @staticmethod
    def get_alg(alg_type: AlgType):
        method = {
            AlgType.LIB: Algorithms._lib,
            AlgType.DDA: Algorithms._dda,
            AlgType.RB: Algorithms.bresenham_float,
            AlgType.IB: Algorithms.bresenham_integer,
            AlgType.BIMP: Algorithms.bresenham_antialiasing,
            AlgType.WU: Algorithms.wu,
        }

        return method[alg_type]

    def method():
        def decorator(func):
            def wrapper(*args, **kwargs):
                time.sleep(1e-16)
                return func(*args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def _lib(p_begin: Point, p_end: Point) -> Tuple[None, int]:
        return None, 0

    @staticmethod
    def _dda(p_begin: Point, p_end: Point) -> Tuple[List[Point], int]:
        def _round(num: float) -> int:
            return int(num + (0.5 if num > 0 else -0.5))

        values: List[Point] = []
        stairs: int = 0

        if p_begin == p_end:
            values.append(p_begin)
            return values, stairs

        length = max(abs(p_end.x - p_begin.x), abs(p_end.y - p_begin.y))
        dx = (p_end.x - p_begin.x) / length
        dy = (p_end.y - p_begin.y) / length


        curr_x, curr_y = p_begin.x, p_begin.y
        tmp_x, tmp_y = curr_x, curr_y

        for _ in range(1, length+2):

            values.append(Point(tmp_x, tmp_y))
            curr_x += dx
            curr_y += dy

            rx, ry = _round(curr_x), _round(curr_y)
            if tmp_x != rx and tmp_y != ry:
                stairs += 1
                stairs_flag = True
            else: 
                stairs_flag = False

            tmp_x, tmp_y = rx, ry

        if stairs_flag:
            stairs -= 1
        return values, stairs

    @staticmethod
    def bresenham_integer(p_begin: Point, p_end: Point) -> Tuple[List[Point], int]:
        def _sign(num: float) -> int:
            return 1 if num > 0 else -1 if num < 0 else 0

        values: List[Point] = []
        stairs: int = 0

        if p_begin == p_end:
            values.append(p_begin)
            return values, stairs

        x_sign, y_sign = _sign(p_end.x - p_begin.x), _sign(p_end.y - p_begin.y)
        dx, dy = abs(p_end.x - p_begin.x), abs(p_end.y - p_begin.y)

        swapped = False
        if dy > dx:
            dx, dy = dy, dx
            swapped = True

        err = int(2*dy-dx)
        ddx, ddy = int(2*dx), int(2*dy)
        curr_x, curr_y = p_begin.x, p_begin.y

        for _ in range(1, dx+2):
            tmp_x, tmp_y = curr_x, curr_y
            values.append(Point(curr_x, curr_y))
            
            if err >= 0:
                if swapped:
                    curr_x += x_sign
                else:
                    curr_y += y_sign

                err -= ddx

            if err < 0:
                if swapped:
                    curr_y += y_sign
                else:
                    curr_x += x_sign

            err += ddy

            if tmp_x != curr_x and tmp_y != curr_y:
                stairs += 1
                stairs_flag = True
            else:
                stairs_flag = False

        if stairs_flag:
            stairs -= 1

        return values, stairs

    @staticmethod
    @method()
    def bresenham_float(p_begin: Point, p_end: Point) -> Tuple[List[Point], int]:
        def _sign(num: float) -> int:
            return 1 if num > 0 else -1 if num < 0 else 0

        values: List[Point] = []
        stairs: int = 0

        if p_begin == p_end:
            values.append(p_begin)
            return values, stairs

        x_sign, y_sign = _sign(p_end.x - p_begin.x), _sign(p_end.y - p_begin.y)
        dx, dy = abs(p_end.x - p_begin.x), abs(p_end.y - p_begin.y)

        swapped = False
        if dy > dx:
            dx, dy = dy, dx
            swapped = True

        m = dy/dx
        err = m-0.5

        curr_x, curr_y = p_begin.x, p_begin.y
        for _ in range(1, dx+2):
            tmp_x, tmp_y = curr_x, curr_y
            values.append(Point(curr_x, curr_y))

            if err >= 0:
                if swapped:
                    curr_x += x_sign
                else:
                    curr_y += y_sign
                
                err -= 1.0

            if err < 0:
                if swapped:
                    curr_y += y_sign
                else:
                    curr_x += x_sign
            err += m

            if tmp_x != curr_x and tmp_y != curr_y:
                stairs, stairs_flag = stairs + 1, True
            else:
                stairs_flag = False

        if stairs_flag:
            stairs -= 1

        return values, stairs

    @staticmethod
    def bresenham_antialiasing(p_begin: Point, p_end: Point) -> Tuple[List[Point], int]:
        def _sign(num: float) -> int:
            return 1 if num > 0 else -1 if num < 0 else 0

        def _round(num: float) -> int:
            return int(num + (0.5 if num > 0 else -0.5))

        intens = 100

        values: List[Point] = []
        stairs: int = 0

        if p_begin == p_end:
            values.append(p_begin)
            return values, stairs

        x_sign, y_sign = _sign(p_end.x - p_begin.x), _sign(p_end.y - p_begin.y)
        dx, dy = abs(p_end.x - p_begin.x), abs(p_end.y - p_begin.y)

        swapped = False
        if dy > dx:
            dx, dy = dy, dx
            swapped = True

        m = dy/dx * intens
        err = intens/2
        w = intens - m

        curr_x, curr_y = p_begin.x, p_begin.y

        for _ in range(1, dx+2):
            tmp_x, tmp_y = curr_x, curr_y
            values.append(Point(curr_x, curr_y, _round(err)))
            if err >= w:
                if swapped:
                    curr_x += x_sign
                else:
                    curr_y += y_sign

                err -= intens

            if err < w:
                if swapped:
                    curr_y += y_sign
                else:
                    curr_x += x_sign

            err += m

            if tmp_x != curr_x and tmp_y != curr_y:
                stairs, stairs_flag = stairs + 1, True
            else:
                stairs_flag = False

        if stairs_flag:
            stairs -= 1

        return values, stairs

    @staticmethod
    def wu(p_begin: Point, p_end: Point) -> Tuple[List[Point], int]:
        def _fpart(num):
            return num - int(num)

        def _rfpart(num):
            return 1 - _fpart(num)

        pb, pe = p_begin.copy(), p_end.copy()
        values: List[Point] = []
        stairs: int = 0

        if pb == pe:
            values.append(pb)
            return values, stairs

        dx, dy = pe.x-pb.x, pe.y-pb.y

        swapped = False
        if abs(dy) > abs(dx):
            dx, dy = dy, dx
            pb.x, pb.y, pe.x, pe.y = pb.y, pb.x, pe.y, pe.x
            swapped = True
        if pb.x > pe.x:
            pb, pe = pe, pb


        m = dy/dx

        y_accum = float(pb.y)
        for x in range(pb.x, pe.x+1):
            last_y = y = int(y_accum)

            if swapped:
                values.append(Point(y, x, 100*_rfpart(y_accum)))
                values.append(Point(y+1, x, 100*_fpart(y_accum)))
            else:
                values.append(Point(x, y, 100*_rfpart(y_accum)))
                values.append(Point(x, y+1, 100*_fpart(y_accum)))

            y_accum += m
            
            if last_y != int(y_accum):
                stairs, stairs_flag = stairs + 1, True
            else:
                stairs_flag = False

        if stairs_flag:
            stairs -= 1

        return values, stairs

    @staticmethod
    def rotate_point(point: Point, angle: float) -> Point:
        mtrx = np.array([[cos(angle),   sin(angle),     0],
                         [-sin(angle),   cos(angle),    0],
                         [0,              0,            1]])

        res = point.to_ndarray() @ mtrx
        return Point(int(res[0]), int(res[1]))
