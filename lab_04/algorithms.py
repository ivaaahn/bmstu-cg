from timeit import timeit
from typing import Dict, List, Tuple, Callable, NewType, Union

from point import Point
from way import Way
from figure import Figure


class AlgsTesting:
    def __init__(self) -> None:
        self.CENTER: Point = Point(100, 100)
        self.START_RAD: int = 2
        self.END_RAD: int = 100
        self.STEP_RAD: int = 2
        self.COUNT: int = 1

        self._circle_algs: List[Callable[[Point, int],
                                         List[Point]]] = Algorithms.get_circle_algs()
        self._ellipse_algs: List[Callable[[Point, int, int],
                                          List[Point]]] = Algorithms.get_ellipse_algs()

    def time_circle_test(self) -> Dict[Callable[[Point, int], List[Point]], float]:
        rads: Tuple[int] = tuple(r for r in range(
            self.START_RAD, self.END_RAD+1, self.STEP_RAD))
        result: Dict[Callable[[Point, int], List[Point]], float] = {}

        for alg in self._circle_algs:
            for rad in rads:
                result[alg] = timeit(lambda: alg(
                    self.CENTER, rad), number=self.COUNT) / self.COUNT * 1000
        return result


    def time_ellipse_test(self) -> Dict[Callable[[Point, int, int], List[Point]], float]:
        rads: Tuple[int] = tuple(r for r in range(self.START_RAD, self.END_RAD+1, self.STEP_RAD))
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

    def canonical_circle(center: Point, radius: int) -> List[Point]:
        pass

    def param_circle(center: Point, radius: int) -> List[Point]:
        pass

    def bresenham_circle(center: Point, radius: int) -> List[Point]:
        pass

    def midpoint_circle(center: Point, radius: int) -> List[Point]:
        pass

    def library_circle(center: Point, radius: int) -> None:
        return None

    def canonical_ellipse(center: Point, a: int, b: int) -> List[Point]:
        pass

    def param_ellipse(center: Point, a: int, b: int) -> List[Point]:
        pass

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
