from math import sqrt, sin, cos, pi
from numpy import arange
from timeit import timeit
from typing import Dict, List, Tuple, Callable, NewType, Union

from point import Point
from way import Way
from figure import Figure

import utils


class AlgsTesting:
    def __init__(self) -> None:
        self.CENTER: Point = Point(100, 100)
        self.START_RAD: int = 2
        self.END_RAD: int = 100
        self.STEP_RAD: int = 2
        self.COUNT: int = 10000

        self._circle_algs = Algorithms.get_circle_algs()
        self._ellipse_algs = Algorithms.get_ellipse_algs()

    def time_circle_test(self) -> Dict[Callable[[Point, int], List[Point]], float]:
        rads: Tuple[int] = tuple(r for r in range(
            self.START_RAD, self.END_RAD+1, self.STEP_RAD))
        result: Dict[Callable[[Point, int], List[Point]], float] = {}

        rad = 100
        for alg in self._circle_algs:
            # for rad in rads:
            result[alg] = timeit(lambda: alg(
                self.CENTER, rad), number=self.COUNT) / self.COUNT * 1000
        return result

    def time_ellipse_test(self) -> Dict[Callable[[Point, int, int], List[Point]], float]:
        rads: Tuple[int] = tuple(r for r in range(
            self.START_RAD, self.END_RAD+1, self.STEP_RAD))
        result: Dict[Callable[[Point, int, int], List[Point]], float] = {}

        for alg in self._ellipse_algs:
            for rad in rads:
                result[alg] = timeit(lambda: alg(
                    self.CENTER, rad, rad), number=self.COUNT) / self.COUNT * 1000
        return result


class Algorithms:
    @staticmethod
    def get_method(figure: Figure, way: Way) -> Union[Callable[[Point, int], Union[List[Point], None]],
                                                      Callable[[Point, int, int], Union[List[Point], None]]]:
        method = {
            (Way.CAN, Figure.CIRCLE): Algorithms.canonical_circle,
            (Way.PARAM, Figure.CIRCLE): Algorithms.param_circle,
            (Way.BRES, Figure.CIRCLE): Algorithms.bresenham_circle,
            (Way.MIDP, Figure.CIRCLE): Algorithms.midpoint_circle,
            (Way.LIB, Figure.CIRCLE): Algorithms.library_circle,
            (Way.CAN, Figure.ELLIPSE): Algorithms.canonical_ellipse,
            (Way.PARAM, Figure.ELLIPSE): Algorithms.param_ellipse,
            (Way.BRES, Figure.ELLIPSE): Algorithms.bresenham_ellipse,
            (Way.MIDP, Figure.ELLIPSE): Algorithms.midpoint_ellipse,
            (Way.LIB, Figure.ELLIPSE): Algorithms.library_ellipse
        }
        return method[(way, figure)]

    @staticmethod
    def get_circle_algs() -> List[Callable[[Point, int], List[Point]]]:
        return [Algorithms.get_method(Figure.CIRCLE, way) for way in Way.get_all()[:-1]]

    @staticmethod
    def get_ellipse_algs() -> List[Callable[[Point, int, int], List[Point]]]:
        return [Algorithms.get_method(Figure.ELLIPSE, way) for way in Way.get_all()[:-1]]

    @staticmethod
    def _extend_with_mirrored_ext(points: List[Point], x: int, y: int, cx: int, cy: int):
        points.extend([
            Point(cx+x, cy+y),
            Point(cx+x, cy-y),
            Point(cx-x, cy+y),
            Point(cx-x, cy-y),

            Point(cx+y, cy+x),
            Point(cx+y, cy-x),
            Point(cx-y, cy+x),
            Point(cx-y, cy-x),
        ])

    @staticmethod
    def _extend_with_mirrored(points: List[Point], x: int, y: int, cx: int, cy: int):
        points.extend([
            Point(cx+x, cy+y),
            Point(cx+x, cy-y),
            Point(cx-x, cy+y),
            Point(cx-x, cy-y),
        ])

    def canonical_circle(center: Point, radius: int) -> List[Point]:
        if radius == 0:
            return [center.copy()]

        result: List[Point] = []
        rsqr: int = radius*radius

        for x in range(0, utils.round(radius / sqrt(2))+1):
            y = utils.round(sqrt(rsqr-x*x))
            Algorithms._extend_with_mirrored_ext(
                result, x, y, center.x, center.y)
        return result

    def param_circle(center: Point, radius: int) -> List[Point]:
        if radius == 0:
            return [center.copy()]

        result: List[Point] = []
        step: float = 1/radius

        for t in arange(0, pi/4+step, step):
            x = utils.round(radius*cos(t))
            y = utils.round(radius*sin(t))
            Algorithms._extend_with_mirrored_ext(
                result, x, y, center.x, center.y)
        return result

    def bresenham_circle(center: Point, radius: int) -> List[Point]:
        if radius == 0:
            return [center.copy()]

        result: List[Point] = []

        # delta - квадрат расстояния до идеальной окружности от диагонального пикселя
        # delta = (x_i + 1)^2 + (y_i - 1)^2 - R^2
        x, y, delta = 0, radius, 2*(1-radius)

        Algorithms._extend_with_mirrored_ext(result, x, y, center.x, center.y)

        # Только 1/8 окружности
        while x < y:
            if delta < 0:
                # delta_tmp - разность расстояний до горизонтального и диагональнго пикселей
                delta_tmp = 2*(delta+y)-1
                x += 1

                # Окружность ближе к горизонтальному пикселю
                if delta_tmp <= 0:      # x, y = x+1, y
                    delta += 2*x+1
                else:                   # x, y = x+1, y-1
                    y -= 1
                    delta += 2*(x-y+1)
            elif delta > 0:
                delta_tmp = 2*(delta-x)-1
                y -= 1

                if delta_tmp <= 0:      # x, y = x+1, y-1
                    x += 1
                    delta += 2*(x-y+1)
                else:                   # x, y = x, y-1
                    delta -= 2*y-1
            else:
                x, y = x+1, y-1
                delta += 2*(x-y+1)

            Algorithms._extend_with_mirrored_ext(
                result, x, y, center.x, center.y)

        return result

    def midpoint_circle(center: Point, radius: int) -> List[Point]:
        if radius == 0:
            return [center.copy()]

        result: List[Point] = []
        x, y, delta = 0, radius, 1.25-radius

        Algorithms._extend_with_mirrored_ext(result, x, y, center.x, center.y)
        while x < y:
            x += 1

            # Окружность выше средней точки
            if delta > 0:
                y -= 1
                delta -= 2 * y  # (2y-2)

            delta += 2 * x + 1  # (2x+3)

            Algorithms._extend_with_mirrored_ext(
                result, x, y, center.x, center.y)
        return result

    def library_circle(center: Point, radius: int) -> None:
        return None

    def canonical_ellipse(center: Point, rx: int, ry: int) -> List[Point]:
        result: List[Point] = []

        m: float = ry/rx
        rxsqr: int = rx**2
        rysqr: int = ry**2

        limit = utils.round(rxsqr/sqrt(rxsqr+rysqr))

        for x in range(limit+1):
            y = utils.round(m * sqrt(rxsqr-x*x))
            Algorithms._extend_with_mirrored(result, x, y, center.x, center.y)

        limit = utils.round(rysqr/sqrt(rxsqr+rysqr))
        m: float = rx/ry

        for y in range(limit+1):
            x = utils.round(m * sqrt(rysqr-y*y))
            Algorithms._extend_with_mirrored(result, x, y, center.x, center.y)

        return result

    def param_ellipse(center: Point, rx: int, ry: int) -> List[Point]:
        result: List[Point] = []

        limit_y = utils.round(ry*ry/sqrt(rx*rx+ry*ry))

        x, y, t = rx, 0, 0
        step_x: float = 1/rx
        step_y: float = 1/ry

        x_end = 0

        while x > x_end:
            x, y = utils.round(rx*cos(t)), utils.round(ry*sin(t))
            Algorithms._extend_with_mirrored(result, x, y, center.x, center.y)

            t += step_y if (y <= limit_y) else step_x

        return result

    def bresenham_ellipse(center: Point, a: int, b: int) -> List[Point]:
        pass

    def midpoint_ellipse(center: Point, a: int, b: int) -> List[Point]:
        pass

    def library_ellipse(center: Point,  a: int, b: int) -> None:
        return None

    # def method():
    #     def decorator(func):
    #         def wrapper(*args, **kwargs):
    #             time.sleep(1e-16)
    #             return func(*args, **kwargs)
    #         return wrapper
    #     return decorator
