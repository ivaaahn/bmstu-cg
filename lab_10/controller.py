from copy import copy
from timeit import timeit
from typing import List, Optional

from numpy import arange

from canvas import Canvas
from horizon import Horizon, Visible
from matrix import Matrix
from models.point import Point
from properties.color import Color
from properties.func import Func
from utils import Ranges, Axis


class Controller:
    def __init__(self, canvas: Canvas, func: Func, color: Color) -> None:
        self._canvas = canvas
        self._canvas.color = color
        self._func = func

        self._tr_matrix = Matrix()
        self._ranges = Ranges()
        self._horiz = Horizon()

        self.p_left: Optional[Point] = None
        self.p_right: Optional[Point] = None

        self._rendered: bool = False

        self._x_range = None
        self._z_range = None

    def edge_points_reset(self) -> None:
        self.p_left = None
        self.p_right = None

    def clear_all(self) -> None:
        self._canvas.clear()
        self._horiz.reset_all()
        self.edge_points_reset()
        self._rendered = False

    def handle_left_edge(self, p_curr: Point) -> None:
        if self.p_left is not None:
            self._horiz.fill(self.p_left, p_curr)

        self.p_left = copy(p_curr)

    def handle_right_edge(self, p_curr: Point) -> None:
        if self.p_right is not None:
            self._horiz.fill(self.p_right, p_curr)

        self.p_right = copy(p_curr)

    @staticmethod
    def find_intersect(p1: Point, p2: Point, hor: List[float]) -> Point:
        def sign(x) -> int:
            return 1 if (x > 0) else -1 if (x < 0) else 0

        if p2.x == p1.x:
            return Point(p1.x, hor[p1.x], p1.z)

        if p1.y == hor[p1.x]:
            return copy(p1)

        if p2.y == hor[p2.x]:
            return copy(p2)

        if p1.x > p2.x:
            p1, p2 = p2, p1

        y_sign = sign(p1.y - hor[p1.x])

        m = (p2.y - p1.y) / (p2.x - p1.x)
        tmp_x, tmp_y = p1.x + 1, p1.y + m
        tmp_sign = sign(tmp_y - hor[tmp_x])

        while tmp_sign == y_sign:
            tmp_y += m
            tmp_x += 1
            tmp_sign = sign(tmp_y - hor[tmp_x])

        if abs(tmp_y - m - hor[tmp_x - 1]) <= abs(tmp_y - hor[tmp_x]):
            tmp_y -= m
            tmp_x -= 1

        # ============DEBUG==============
        if tmp_x > p2.x:
            res = Point(tmp_x, tmp_y, p1.z).x_rnd()
            print("p1: ", p1)
            print("p2: ", p2)
            print("hor: ", [(x, y) for x, y in zip(range(p1.x, p2.x + 1), hor[p1.x:(p2.x + 1)])])
            print("res: ", res)
        # ============DEBUG==============

        return Point(tmp_x, tmp_y, p1.z)

    def draw_curve(self, z: float):
        transform = lambda x, y: self._tr_matrix.tr_point(Point(x, y, z)).x_rnd()

        all_x = self.range_x
        all_y = self.function.calculate(all_x, z)

        _points = [transform(x, y) for x, y in zip(all_x, all_y)]
        points = iter(_points)

        p_prev = next(points)
        while not p_prev.into_window():
            p_prev = next(points)

        self.handle_left_edge(p_prev)
        prev_visible = self._horiz.visibility_type(p_prev)

        draw = self._canvas.draw_line
        fill_horiz = self._horiz.fill

        for p_curr in points:
            if p_curr == p_prev or not p_curr.into_window():
                continue

            curr_visible = self._horiz.visibility_type(p_curr)

            if curr_visible == prev_visible:
                if curr_visible != Visible.NOT:
                    draw(p_prev, p_curr)
                    fill_horiz(p_prev, p_curr)
            else:
                if curr_visible is Visible.NOT:
                    if prev_visible is Visible.TOP:
                        res = self.find_intersect(p_prev, p_curr, self._horiz.top)
                    else:
                        res = self.find_intersect(p_prev, p_curr, self._horiz.bottom)

                    draw(p_prev, res)
                    fill_horiz(p_prev, res)

                elif curr_visible is Visible.TOP:
                    if prev_visible is Visible.NOT:
                        res = self.find_intersect(p_prev, p_curr, self._horiz.top)
                        draw(res, p_curr)
                        fill_horiz(res, p_curr)
                    else:
                        res = self.find_intersect(p_prev, p_curr, self._horiz.bottom)
                        draw(p_prev, res)
                        fill_horiz(p_prev, res)

                        res = self.find_intersect(p_prev, p_curr, self._horiz.top)
                        draw(res, p_curr)
                        fill_horiz(res, p_curr)
                else:
                    if prev_visible is Visible.NOT:
                        res = self.find_intersect(p_prev, p_curr, self._horiz.bottom)
                        draw(res, p_curr)
                        fill_horiz(res, p_curr)
                    else:
                        res = self.find_intersect(p_prev, p_curr, self._horiz.top)
                        draw(p_prev, res)
                        fill_horiz(p_prev, res)

                        res = self.find_intersect(p_prev, p_curr, self._horiz.bottom)
                        draw(res, p_curr)
                        fill_horiz(res, p_curr)

            p_prev = copy(p_curr)
            prev_visible = curr_visible

        self.handle_right_edge(p_prev)

    def render(self) -> None:
        self._rendered = True
        print(timeit(lambda: self.solve(), number=1))
        # self.solve()

    def solve(self):
        self._canvas.clear()
        self._horiz.reset_all()
        self.edge_points_reset()

        for z in self.range_z:
            self.draw_curve(z)

        self._canvas.update()

    def rotate(self, value: int, axis: Axis) -> None:
        self._tr_matrix.rotate(value, axis)

        if self._rendered:
            self.render()
            # self.solve()

    @property
    def ranges(self) -> Ranges:
        return self._ranges

    @ranges.setter
    def ranges(self, value: Ranges) -> None:
        self._ranges = value

        self._x_range = None
        self._z_range = None

        if self._rendered:
            self.render()

            # self.solve()

    @property
    def function(self) -> Func:
        return self._func

    @function.setter
    def function(self, func: Func) -> None:
        self._func = func

        if self._rendered:
            self.render()

            # self.solve()

    @property
    def scale_param(self) -> float:
        return self._tr_matrix.scale_param

    @scale_param.setter
    def scale_param(self, value: float) -> None:
        self._tr_matrix.scale_param = value

        if self._rendered:
            self.render()

            # self.solve()

    @property
    def color(self) -> Color:
        return self._canvas.color

    @color.setter
    def color(self, value: Color) -> None:
        self._canvas.color = value

        if self._rendered:
            self.render()
            # self.solve()

    @property
    def range_z(self) -> arange:
        if self._z_range is None:
            r = self.ranges
            self._z_range = arange(r.z_to, r.z_from - r.z_step, -r.z_step)

        return self._z_range

    @property
    def range_x(self) -> arange:
        if self._x_range is None:
            r = self.ranges
            self._x_range = arange(r.x_from, r.x_to + r.x_step, r.x_step)

        return self._x_range
