from math import sqrt, sin, cos, pi
from numpy import arange
from timeit import timeit
from typing import Dict, List, Tuple, Callable, NewType, Union, Optional

from point import Point
from way import Way
from figure import Figure
import utils


class AlgsTesting:
    def __init__(self) -> None:
        self.CENTER: Point = Point(0, 0)
        self.START_RAD: int = 5
        self.END_RAD: int = 100
        self.STEP_RAD: int = 5
        self.COUNT: int = 800

        self._circle_algs = Algorithms.get_circle_algs()
        self._ellipse_algs = Algorithms.get_ellipse_algs()

    def time_circle_test(self) -> Dict[Callable[[Point, int], List[Point]], float]:
        rads: Tuple[int] = tuple(r for r in range(
            self.START_RAD, self.END_RAD+1, self.STEP_RAD))
        result: Dict[Callable[[Point, int], List[Point]], float] = {}

        for alg in self._circle_algs:
            values: List[float] = []
            for rad in rads:
                time = timeit(lambda: alg(self.CENTER, rad),
                              number=self.COUNT) / self.COUNT * 1000000
                values.append(time)

            result[alg] = values

        return rads, result

    def time_ellipse_test(self) -> Dict[Callable[[Point, int, int], List[Point]], float]:
        rads_ry: Tuple[int] = tuple(r for r in range(
            self.START_RAD, self.END_RAD+1, self.STEP_RAD))
        result: Dict[Callable[[Point, int, int], List[Point]], float] = {}

        all_algorithms = self._ellipse_algs
        all_algorithms[-2] = Algorithms.bresenham_ellipse

        for alg in self._ellipse_algs:
            values: List[float] = []
            for ry in rads_ry:
                time = timeit(lambda: alg(self.CENTER, 2*ry, ry),
                              number=self.COUNT) / self.COUNT * 1000000
                values.append(time)

            result[alg] = values

        return rads_ry, result


class Algorithms:

    @staticmethod
    def get_method(figure: Figure, way: Way) -> Union[Callable[[Point, int], Optional[List[Point]]],
                                                      Callable[[Point, int, int], Optional[List[Point]]]]:
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

    def get_way_and_figure(method: Union[Callable[[Point, int], Optional[List[Point]]],
                                         Callable[[Point, int, int], Optional[List[Point]]]]) -> Tuple[Way, Figure]:
        wnf = {
            Algorithms.canonical_circle: (Way.CAN, Figure.CIRCLE),
            Algorithms.param_circle: (Way.PARAM, Figure.CIRCLE),
            Algorithms.bresenham_circle: (Way.BRES, Figure.CIRCLE),
            Algorithms.midpoint_circle: (Way.MIDP, Figure.CIRCLE),
            Algorithms.library_circle: (Way.LIB, Figure.CIRCLE),
            Algorithms.canonical_ellipse: (Way.CAN, Figure.ELLIPSE),
            Algorithms.param_ellipse: (Way.PARAM, Figure.ELLIPSE),
            Algorithms.bresenham_ellipse: (Way.BRES, Figure.ELLIPSE),
            Algorithms.midpoint_ellipse: (Way.MIDP, Figure.ELLIPSE),
            Algorithms.library_ellipse: (Way.LIB, Figure.ELLIPSE)
        }

        return wnf[method]

    @staticmethod
    def get_circle_algs() -> List[Callable[[Point, int], List[Point]]]:
        return [Algorithms.get_method(Figure.CIRCLE, way) for way in Way.get_all()[:-1]]

    @staticmethod
    def get_ellipse_algs() -> List[Callable[[Point, int, int], List[Point]]]:
        return [Algorithms.get_method(Figure.ELLIPSE, way) for way in Way.get_all()[:-1]]

    @staticmethod
    def Plot8CirclePoints(points: List[Point], x: int, y: int, cx: int, cy: int):
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
    def Plot4EllipsePoints(points: List[Point], x: int, y: int, cx: int, cy: int):
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

        for x in range(utils.round(radius / sqrt(2))+1):
            y = utils.round(sqrt(rsqr-x*x))
            Algorithms.Plot8CirclePoints(
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
            Algorithms.Plot8CirclePoints(
                result, x, y, center.x, center.y)
        return result

    def bresenham_circle(center: Point, radius: int) -> List[Point]:
        if radius == 0:
            return [center.copy()]

        result: List[Point] = []

        # delta - квадрат расстояния до идеальной окружности от диагонального пикселя
        # delta = (x_i + 1)^2 + (y_i - 1)^2 - R^2
        x, y, circle_error = 0, radius, 2*(1-radius)

        # Только 1/8 окружности
        while x <= y:
            Algorithms.Plot8CirclePoints(result, x, y, center.x, center.y)

            # Диагональный пиксель оказывается внутри реальной окружности
            x += 1

            # delta_tmp - разность расстояний до горизонтального и диагональнго пикселей
            delta = 2*(circle_error + y) - 1

            # Реальная окружность ближе к диагональному пикселю
            if delta > 0:
                y -= 1
                circle_error -= 2 * y - 1

            circle_error += 2 * x + 1

        return result

    def midpoint_circle(center: Point, radius: int) -> List[Point]:
        if radius == 0:
            return [center.copy()]

        result: List[Point] = []
        x, y, delta = 0, radius, 1-radius

        while x <= y:
            Algorithms.Plot8CirclePoints(result, x, y, center.x, center.y)
            x += 1

            if delta >= 0:
                y -= 1
                delta -= 2 * y

            delta += 2 * x + 1
        return result

    def library_circle(center: Point, radius: int) -> None:
        return None

    def canonical_ellipse(center: Point, rx: int, ry: int) -> List[Point]:
        result: List[Point] = []

        rxsqr, rysqr = rx*rx, ry*ry
        stopping_x = utils.round(rxsqr/sqrt(rxsqr+rysqr))
        stopping_y = utils.round(rysqr/sqrt(rxsqr+rysqr))

        m: float = ry/rx
        x: int = 0
        while x <= stopping_x:
            y = utils.round(m * sqrt(rxsqr-x*x))
            Algorithms.Plot4EllipsePoints(result, x, y, center.x, center.y)
            x += 1

        m: float = rx/ry
        y: int = stopping_y
        while y >= 0:
            x = utils.round(m * sqrt(rysqr-y*y))
            Algorithms.Plot4EllipsePoints(result, x, y, center.x, center.y)
            y -= 1

        return result

    def param_ellipse(center: Point, rx: int, ry: int) -> List[Point]:
        result: List[Point] = []

        rysqr, rxsqr = ry*ry, rx*rx

        limit_y = utils.round(rysqr/sqrt(rxsqr+rysqr))

        x, y, t = rx, 0, 0
        step_x: float = 1/rx
        step_y: float = 1/ry

        x_end = 0

        while x > x_end:
            x, y = utils.round(rx*cos(t)), utils.round(ry*sin(t))
            Algorithms.Plot4EllipsePoints(result, x, y, center.x, center.y)

            if y <= limit_y:
                t += step_y
            else:
                t += step_x

        return result

    def bresenham_ellipse(center: Point, rx: int, ry: int) -> List[Point]:
        if rx == 0 and ry == 0:
            return [center.copy()]

        result: List[Point] = []
        rxsqr, rysqr = rx*rx, ry*ry
        two_rxsqr, two_rysqr = 2*rxsqr, 2*rysqr

        # Error(x, y) = x^2 * ry^2 + y^2 * rx^2 - rx^2*ry^2
        # delta == Error(x+1, y-1)
        x, y, ellipse_error = 0, ry, rxsqr+rysqr-two_rxsqr*ry

        Algorithms.Plot4EllipsePoints(result, x, y, center.x, center.y)

        while y > 0:
            # Диагональный пиксель лежит внутри реального эллипса
            if ellipse_error <= 0:
                x += 1

                # Разность расстояний до горизонтального и диагональнго пикселей
                delta = 2*ellipse_error + rxsqr * (2 * y - 1)
                # f.write(f'delta = {delta}\n')

                # Реальный эллипс ближе к диагональному пикселю
                if delta >= 0:
                    y -= 1
                    ellipse_error += rxsqr * (1 - 2 * y)

                ellipse_error += rysqr * (2 * x + 1)

            # Диагональный пиксель лежит снаружи реального эллипса
            elif ellipse_error > 0:
                y -= 1

                # Разность расстояний до диагональнго и вертикального пикселей
                delta = 2*ellipse_error - rysqr * (2 * x + 1)

                # Реальный эллипс ближе к диагональному пикселю
                if delta < 0:
                    x += 1
                    ellipse_error += rysqr * (2 * x + 1)

                ellipse_error += rxsqr * (1 - 2 * y)

            Algorithms.Plot4EllipsePoints(result, x, y, center.x, center.y)

        return result

    def midpoint_ellipse(center: Point, rx: int, ry: int) -> List[Point]:
        if rx == 0 or ry == 0:
            return [center.copy()]

        result: List[Point] = []
        rxsqr, rysqr = rx*rx, ry*ry
        two_rxsqr, two_rysqr = 2*rx*rx, 2*ry*ry

        x, y = 0, ry
        delta = rysqr + rxsqr * (0.25 - ry)
        stopping_x = utils.round(rxsqr/sqrt(rxsqr+rysqr))
        while x <= stopping_x:
            Algorithms.Plot4EllipsePoints(result, x, y, center.x, center.y)
            x += 1

            # Реальная окружность лежит ниже средней точки
            if delta >= 0:
                y -= 1
                delta -= two_rxsqr * y

            delta += rysqr + two_rysqr * x

        x, y = rx, 0
        delta = rxsqr + rysqr * (0.25 - rx)
        stopping_y = utils.round(rysqr/sqrt(rxsqr+rysqr))
        while y <= stopping_y:
            Algorithms.Plot4EllipsePoints(result, x, y, center.x, center.y)
            y += 1

            if delta >= 0:
                x -= 1
                delta -= two_rysqr * x

            delta += rxsqr + two_rxsqr * y

        return result

    def library_ellipse(center: Point,  a: int, b: int) -> None:
        return None
