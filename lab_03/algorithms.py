import numpy as np
from math import radians, sin, cos
from timeit import timeit
from enum import Enum
from typing import Dict, List, Tuple
import time

from loguru import logger
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

class testAlgs:
    def __init__(self) -> None:
        self.alg_types = AlgType.get_all()[1:6]


    def time_test(self) -> dict:
        count = 1000
        p_start = Point(321, 135)
        p_end = Point(789, 849)
        res = {}

        for alg_type in self.alg_types:
            alg = Algorithms.get_alg(alg_type)
            res[alg_type] = timeit(lambda: alg(p_start, p_end), number=count) / count * 1000
            
        return res

    def stairs_test(self) -> Tuple[Tuple, Dict]:
        length = 100
        start_point: Point = Point(length, 0)
        all_angles: Tuple[int] = tuple(range(0, 91, 1))
        p_ends: List[Point] = [Algorithms.rotate_point(start_point, radians(angle)) for angle in all_angles]
        center: Point = Point(0,0)

        res = {}
        for alg_type in self.alg_types:
            alg = Algorithms.get_alg(alg_type)
            res[alg_type] = [alg(center, center+point)[1] for point in p_ends] # stairs

        return all_angles, res


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
        return None, 0


    @staticmethod
    def _dda(p_start: Point, p_end: Point) -> List[Point]:
        def _round(num: float) -> int:
            return int(num + (0.5 if num > 0 else -0.5))

        values: List[Point] = []
        stairs: int = 0

        if p_start == p_end:
            values.append(p_start)
            return values

        length = max(abs(p_end.x - p_start.x), abs(p_end.y - p_start.y))

        along_x = abs(p_end.x - p_start.x) >= abs(p_end.y - p_start.y)


        dx = (p_end.x - p_start.x) / length
        dy = (p_end.y - p_start.y) / length

        x, y = p_start.x, p_start.y
        
        last = _round(y) if along_x else _round(x)

        if along_x:
            for _ in range(1, length+1):
                rx, ry = _round(x), _round(y)

                if ry != last:
                    stairs += 1
                    last = ry

                values.append(Point(rx, ry))
                x, y = x+dx, y+dy

        else:
            for _ in range(1, length+1):
                rx, ry = _round(x), _round(y)

                if rx != last:
                    stairs += 1
                    last = rx

                values.append(Point(rx, ry))
                x, y = x+dx, y+dy


        return values, stairs

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
        stairs: int = 0
        new_stair = 0

        if p_start == p_end:
            values.append(p_start)
            return values

        x_sign, y_sign = _sign(p_end.x - p_start.x), _sign(p_end.y - p_start.y)
        dx, dy = abs(p_end.x - p_start.x), abs(p_end.y - p_start.y)

        swapped = False
        if dy > dx:
            dx, dy = dy, dx
            swapped = True

        err = int(2*dy-dx)

        ddx, ddy = int(2*dx), int(2*dy)
        x, y = p_start.x, p_start.y


        values.append(Point(x, y))
        for _ in range(1, dx):
            if err > 0:
                stairs += 1
                if swapped:
                    x += x_sign
                else:
                    y += y_sign

                err -= ddx

            if err <= 0:
                if swapped:
                    y += y_sign
                else:
                    x += x_sign

            err += ddy
            values.append(Point(x, y))

        return values, stairs

    @staticmethod
    @wait(1e-16)
    def _rbres(p_start: Point, p_end: Point) -> List[Point]:
        def _sign(num: float) -> int:
            return 1 if num > 0 else -1 if num < 0 else 0

        values: List[Point] = []
        stairs: int = 0
        new_stair = 0

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

        values.append(Point(x, y))
        for _ in range(1, dx):
            if err > 0:
                stairs += 1

                if swap:
                    x += x_sign
                else:
                    y += y_sign

                err = err - 1.0

            if err <= 0:
                if swap:
                    y += y_sign
                else:
                    x += x_sign

            err = err + m
            values.append(Point(x, y))

        return values, stairs

    @staticmethod
    def _bresimp(p_start: Point, p_end: Point) -> List[Point]:
        def _sign(num: float) -> int:
            return 1 if num > 0 else -1 if num < 0 else 0

        def _round(num: float) -> int:
            return int(num + (0.5 if num > 0 else -0.5))

        intens = 100

        values: List[Point] = []
        stairs: int = 0

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
                stairs += 1

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

        return values, stairs

    @staticmethod
    def _wu(p_begin: Point, p_end: Point) -> List[Point]:
        def _fpart(num):
            return num - int(num)
        
        def _rfpart(num):
            return 1 - _fpart(num)

        pb, pe = p_begin.copy(), p_end.copy()
        values: List[Point] = []
        stairs: int = 0
        
        if pb == pe:
            values.append(pb)
            return values

        dx, dy = pe.x-pb.x, pe.y-pb.y

        swapped = False
        if abs(dy) > abs(dx):
            dx, dy = dy, dx
            pb.x, pb.y, pe.x, pe.y = pb.y, pb.x, pe.y, pe.x 
            swapped = True
        if pb.x > pe.x:
            pb, pe = pe, pb

        m = dy/dx
        last_y = next_y = pb.y
        for x in range(pb.x, pe.x+1):

            y = int(next_y)

            if y > last_y:
                stairs += 1
                last_y = y


            if swapped:
                values.append(Point(y, x, 100*_rfpart(next_y)))
                values.append(Point(y+1, x, 100*_fpart(next_y)))
            else:
                values.append(Point(x, y, 100*_rfpart(next_y)))
                values.append(Point(x, y+1, 100*_fpart(next_y)))

            next_y += m

        return values, stairs


    @staticmethod
    def rotate_point(point: Point, angle: float) -> Point:
        mtrx = np.array([[cos(angle),   sin(angle),    0],
                        [-sin(angle),   cos(angle),    0],
                        [0,              0,            1]])

        res = point.to_ndarray() @ mtrx
        return Point(int(res[0]), int(res[1]))
