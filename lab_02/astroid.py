from PyQt5.QtCore import QRect
from math import pi, sin, cos
from numpy import arange, linspace
from loguru import logger

import sys
import typing
import numpy as np

from point import Point


class Astroid():
    def __init__(self, b: float = 2.0):
        self._b = b
        self._center = 0.0

        self._need_draw = False
        self._last_mtrx = None

        self._res_mtrx = np.eye(3)
        self._raw_values = []
        self._raw_rect_points = []

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, value: float):
        self._b = value
        self.clear_values()
    
    @property
    def center(self):
        logger.debug(f'center is {self._center}')
        return self.transformed(self._center)

    @property
    def border_points(self) -> list:
        if not self._need_draw:
            return []
        else:
            if not self._raw_rect_points:
                self._update_rect_points()
            return list(map(self.transformed, self._raw_rect_points))

    @property
    def values(self) -> list:
        if not self._need_draw:
            return []
        else:
            if not self._raw_values:
                self._update_values()
            return list(map(self.transformed, self._raw_values))

    def change_draw(self):
        self._need_draw = not self._need_draw

    def clear_values(self):
        self._raw_values.clear()
        self._raw_rect_points.clear()

    def move(self, data: typing.NamedTuple) -> typing.NoReturn:
        logger.debug(data)

        self._last_mtrx = self._res_mtrx
        self._res_mtrx = self._res_mtrx @ np.array([[1,           0,         0],
                                                    [0,           1,         0],
                                                    [data.dx,  data.dy,      1]])

    def scale(self, data: typing.NamedTuple) -> typing.NoReturn:
        logger.debug(data)

        to_start = np.array([[1,                     0,           0],
                             [0,                     1,           0],
                             [-data.center.x,  -data.center.y,    1]])

        scale = np.array([[data.coef,   0,     0],
                          [0,     data.coef,   0],
                          [0,      0,     1]])

        to_place = np.array([[1,                     0,         0],
                             [0,                     1,         0],
                             [data.center.x,  data.center.y,    1]])

        self._last_mtrx = self._res_mtrx
        self._res_mtrx = self._res_mtrx @ to_start @ scale @ to_place

    def rotate(self, data: typing.NamedTuple) -> typing.NoReturn:
        logger.debug(data)

        to_start = np.array([[1,                     0,           0],
                             [0,                     1,           0],
                             [-data.center.x,  -data.center.y,    1]])

        rotate = np.array([[cos(data.angle),    sin(data.angle),    0],
                           [-sin(data.angle),   cos(data.angle),    0],
                           [0,                         0,           1]])

        to_place = np.array([[1,                     0,         0],
                             [0,                     1,         0],
                             [data.center.x,  data.center.y,    1]])

        self._last_mtrx = self._res_mtrx
        self._res_mtrx = self._res_mtrx @ to_start @ rotate @ to_place

    def back(self) -> typing.NoReturn:
        if self._last_mtrx is not None:
            self._res_mtrx = self._last_mtrx
            self._last_mtrx = None
        

    def reset(self) -> typing.NoReturn:
        self._last_mtrx = self._res_mtrx
        self._res_mtrx = np.eye(3)

    def _update_rect_points(self):
        self._raw_rect_points = tmp = [
            Point(x=-self.b, y=self.b),
            Point(x=self.b, y=self.b),
            Point(x=-self.b, y=-self.b),
            Point(x=self.b, y=-self.b)
        ]

        self._center = (Point(x=-self.b, y=-self.b) + Point(x=self.b, y=self.b)) / 2


    def _update_values(self):
        def _x(t: float) -> float:
            return self._b * cos(t) ** 3

        def _y(t: float) -> float:
            return self._b * sin(t) ** 3

        for t in linspace(0, 2 * pi, 2000):
            self._raw_values.append(
                Point(x=_x(t), y=_y(t)))


    @logger.catch
    def transformed(self, point: Point) -> Point:
        return Point(point=tuple(point.to_ndarray().dot(self._res_mtrx)[:-1]))
        

    # def _update_center(self):
    #     bp = self.border_points
    #     if bp:
    #         p_min = Point(x=min([p.x for p in bp]), y=min([p.y for p in bp]))
    #         p_max = Point(x=max([p.x for p in bp]), y=max([p.y for p in bp]))
    #         p_c = (p_min + p_max) / 2
    #     return p_c
