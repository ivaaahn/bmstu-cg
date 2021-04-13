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

        for x in range(0, utils.round(radius / sqrt(2))+1):
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

        Algorithms.Plot8CirclePoints(result, x, y, center.x, center.y)

        # Только 1/8 окружности
        while x < y:

            # Диагональный пиксель оказывается внутри реальной окружности
            if circle_error <= 0:
                x += 1
                
                # delta_tmp - разность расстояний до горизонтального и диагональнго пикселей
                delta = 2*(circle_error + y) - 1

                # Реальная окружность ближе к диагональному пикселю
                if delta > 0:
                    y -= 1
                    circle_error -= 2 * y - 1
                
                circle_error += 2 * x + 1


            # Диагональный пиксель лежит вне реальной окружности
            elif circle_error > 0:
                y -= 1

                # delta_tmp - разность расстояний до диагональнго и вертикального пикселей
                delta = 2*(circle_error - x) - 1

                # Реальная окружность ближе к диагональному пикселю
                if delta <= 0:
                    x += 1 
                    circle_error += 2 * x + 1 
                    
                circle_error -= 2 * y - 1

            Algorithms.Plot8CirclePoints(
                result, x, y, center.x, center.y)

        return result

    def midpoint_circle(center: Point, radius: int) -> List[Point]:
        if radius == 0:
            return [center.copy()]

        result: List[Point] = []
        x, y, delta = 0, radius, 1-radius

        Algorithms.Plot8CirclePoints(result, x, y, center.x, center.y)
        while x < y:
            x += 1

            if delta >= 0:
                y -= 1
                delta -= 2 * y  # (2y-2)

            delta += 2 * x + 1  # (2x+3)

            Algorithms.Plot8CirclePoints(
                result, x, y, center.x, center.y)
        return result

    def library_circle(center: Point, radius: int) -> None:
        return None

    def canonical_ellipse(center: Point, rx: int, ry: int) -> List[Point]:
        result: List[Point] = []

        f = open('test.txt', 'w')

        rxsqr, rysqr = rx*rx, ry*ry        
        stopping_x = utils.round(rxsqr/sqrt(rxsqr+rysqr))
        stopping_y = utils.round(rysqr/sqrt(rxsqr+rysqr))

        m: float = ry/rx
        x: int = 0
        while x <= stopping_x:
            f.write(f'Non-round = {m*sqrt(rxsqr-x*x)}\n')

            y = utils.round(m * sqrt(rxsqr-x*x))
            f.write(f'({x}, {y})\n')
            Algorithms.Plot4EllipsePoints(result, x, y, center.x, center.y)
            x += 1

        f.write('CHANGE\n')

        m: float = rx/ry
        y: int = 0
        while y < stopping_y:
            x = utils.round(m * sqrt(rysqr-y*y))
            f.write(f'({x}, {y})\n')
            Algorithms.Plot4EllipsePoints(result, x, y, center.x, center.y)
            y += 1

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

            t += step_y if (y <= limit_y) else step_x

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

        f = open('bres.txt', 'w')

        Algorithms.Plot4EllipsePoints(result, x, y, center.x, center.y)
        f.write(f'({x}, {y})\n')

        while y > 0:
            # Диагональный пиксель лежит внутри реального эллипса
            if ellipse_error <= 0:
                x += 1

                # Разность расстояний до горизонтального и диагональнго пикселей
                delta = 2*ellipse_error + rxsqr * (2 * y - 1)
                f.write(f'delta = {delta}\n')
                

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

            f.write(f'({x}, {y})\n')
            Algorithms.Plot4EllipsePoints(result, x, y, center.x, center.y)

        return result


    # def bresenham_ellipse(center: Point, rx: int, ry: int) -> List[Point]:
    #     if rx == 0 and ry == 0:
    #         return [center.copy()]

    #     result: List[Point] = []
    #     rx_sqr, ry_sqr = rx*rx, ry*ry
    #     two_rx_sqr, two_ry_sqr = 2*rx*rx, 2*ry*ry

    #     # Error(x, y) = x^2 * ry^2 + y^2 * rx^2 - rx^2*ry^2
    #     # delta == Error(x+1, y-1)

    #     x, y = rx, 0
    #     x_change, y_change = ry_sqr*(1-2*rx), rx_sqr
    #     delta = 0
    #     stop_x, stop_y = two_ry_sqr*rx, 0

    #     while(stop_x >= stop_y):
    #         Algorithms.Plot4EllipsePoints(result, x, y, center.x, center.y)

    #         y += 1
    #         stop_y += two_rx_sqr
    #         delta += y_change
    #         y_change += two_rx_sqr

    #         if 2*delta + x_change > 0:
    #             x -= 1
    #             stop_x -= two_ry_sqr
    #             delta += x_change
    #             x_change += two_ry_sqr

    #     x, y = 0, ry
    #     x_change, y_change = ry_sqr, rx_sqr*(1-2*ry)
    #     delta = 0
    #     stop_x, stop_y = 0, two_rx_sqr*ry
        
    #     while(stop_x <= stop_y):
    #         Algorithms.Plot4EllipsePoints(result, x, y, center.x, center.y)

    #         x += 1
    #         stop_x += two_ry_sqr
    #         delta += x_change
    #         x_change += two_ry_sqr

    #         if 2*delta + y_change > 0:
    #             y -= 1
    #             stop_y -= two_rx_sqr
    #             delta += y_change
    #             y_change += two_rx_sqr

    #     return result



    def midpoint_ellipse(center: Point, rx: int, ry: int) -> List[Point]:
        pass
        # if rx == 0 or ry == 0:
        #     return [center.copy()]


        # result: List[Point] = []
        # rxsqr, rysqr = rx*rx, ry*ry
        # x, y, delta = 0, ry, rysqr - rxsqr*

        # Algorithms.Plot8CirclePoints(result, x, y, center.x, center.y)
        # while x < y:
        #     x += 1

        #     if delta >= 0:
        #         y -= 1
        #         delta -= 2 * y  # (2y-2)

        #     delta += 2 * x + 1  # (2x+3)

        #     Algorithms.Plot8CirclePoints(
        #         result, x, y, center.x, center.y)
        # return result

    def library_ellipse(center: Point,  a: int, b: int) -> None:
        return None

    # def method():
    #     def decorator(func):
    #         def wrapper(*args, **kwargs):
    #             time.sleep(1e-16)
    #             return func(*args, **kwargs)
    #         return wrapper
    #     return decorator
