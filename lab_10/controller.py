import numpy as np
from PyQt5.QtCore import Qt
from numpy import arange

import utils
from canvas import Canvas
from horizont import Horizon
from matrix import Matrix
from models.point import Point
from models.segment import Segment
from properties.color import Color
from properties.func import Func
from utils import Ranges, Axis


class Controller:
    def __init__(self, canvas: Canvas, func: Func, color: Color) -> None:
        self._canvas = canvas

        self._func = func
        self._color = color

        self._transform_matrix = Matrix()
        self._ranges = Ranges()
        self._scale_param: float = 1.0

        self._horiz = Horizon()

    def clear_all(self) -> None:
        self._canvas.clear()
        self._horiz.reset_all()

    def _draw_horizon_part(self, p1: Point, p2: Point):
        if p1.x > p2.x:
            p1, p2 = p2, p1

        dx = p2.x - p1.x
        dy = p2.y - p1.y

        l = max(dx, dy)

        dx /= l
        dy /= l

        x, y = p1.x, p1.y

        for _ in range(int(l) + 1):
            if not (p := Point(utils.custom_round(x), y, 0)).is_visible():
                return

            if p.y > self._horiz.top[p.x]:
                self._horiz.top[p.x] = p.y
                self._canvas.draw_point(p, self._color)

            elif p.y < self._horiz.bottom[p.x]:
                self._horiz.bottom[p.x] = p.y
                self._canvas.draw_point(p, self._color)

            x, y = x + dx, y + dy

    def _draw_horizon(self, z: float):
        all_x = self.range_x
        all_y = self.function.calculate(all_x, z)

        prev = None
        for x, y in zip(all_x, all_y):
            curr = self._transform_matrix.transform_point(Point(x, y, z), self.scale_param)

            if prev is not None:
                self._draw_horizon_part(prev, curr)

            prev = curr

    def solve(self):
        self.clear_all()

        for z in self.range_z:
            self._draw_horizon(z)

        r = self.ranges
        f = self.function.calculate
        t_point = self._transform_matrix.transform_point

        for z in arange(r.z_from, r.z_to, r.z_step):
            p1 = t_point(Point(r.x_from, f(r.x_from, z), z), self.scale_param)
            p2 = t_point(Point(r.x_from, f(r.x_from, z + r.z_step), z + r.z_step), self.scale_param)
            self._canvas.draw_segments([Segment(p1, p2)], self._color)

            p1 = t_point(Point(r.x_to, f(r.x_to, z), z), self.scale_param)
            p2 = t_point(Point(r.x_to, f(r.x_to, z + r.z_step), z + r.z_step), self.scale_param)

            self._canvas.draw_segments([Segment(p1, p2)], self._color)

        self._canvas.update()

    def rotate(self, value: int, axis: Axis) -> None:
        self._transform_matrix.rotate(value, axis)
        self.solve()

    @property
    def ranges(self) -> Ranges:
        return self._ranges

    @ranges.setter
    def ranges(self, value: Ranges) -> None:
        self._ranges = value

    @property
    def function(self) -> Func:
        return self._func

    @function.setter
    def function(self, func: Func) -> None:
        self._func = func
        self.solve()

    @property
    def scale_param(self) -> float:
        return self._scale_param

    @scale_param.setter
    def scale_param(self, value: float) -> None:
        self._scale_param = value
        self.solve()
        # print("scale changed: ", self._scale_param)

    @property
    def color(self) -> Color:
        return self._color

    @color.setter
    def color(self, color: Color) -> None:
        self._color = color
        # self.solve()

    @property
    def range_z(self) -> arange:
        r = self.ranges
        return arange(r.z_from, r.z_to + r.z_step, r.z_step)

    @property
    def range_x(self) -> arange:
        r = self.ranges
        return arange(r.x_from, r.x_to + r.x_step, r.x_step)
