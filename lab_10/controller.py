from copy import copy
from typing import List, Optional

from numpy import arange

from canvas import Canvas
from models.horizon import Horizon, Visible
from models.matrix import Matrix
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

        self._x_range: Optional[arange] = None
        self._z_range: Optional[arange] = None

        self._rendered: bool = False

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

            # -> Отрисовки ребер в Роджерсе нет, но Куров хочет.
            # -> В таком случае будут видны невидимые линии ребер
            # -> Куров об этом особо ничего не говорил не говорил фиксить
            # -> Я решил это пофиксить  способом, от которого мы ушли при отрисовке всего остального.
            # -> Я считаю, что для ребер можно заюзать и этот метод прокатит...
            if self._horiz.visibility_type(p_curr) is not Visible.NOT:
                self._canvas.draw_line(self.p_left, p_curr)

        self.p_left = copy(p_curr)

    def handle_right_edge(self, p_curr: Point) -> None:
        if self.p_right is not None:
            self._horiz.fill(self.p_right, p_curr)

            # см комментарий в handle_left_edge()
            if self._horiz.visibility_type(p_curr) is not Visible.NOT:
                self._canvas.draw_line(self.p_right, p_curr)

        self.p_right = copy(p_curr)

    @staticmethod
    def find_intersect2(p1: Point, p2: Point, hor: List[float]) -> Point:
        """
        Это второй вариант реализации поиска пересечения отрезка с горизонтом.
        В Роджерсе по-дефолту приведен способ, реализованный в методе find_intersect,
        однако Куров приводил данный способ (в Роджерсе он тоже есть).

        :param p1: точка начала отрезка
        :param p2: точка конца отрезка
        :param hor: горизонт, с которым ищем пересечение
        :return: точка пересечения отрезка с горизонтом
        """

        if p2.x == p1.x:
            return Point(p1.x, hor[p1.x], p1.z)

        if abs(p1.y - hor[p1.x]) < 1e-5:
            return copy(p1)

        if abs(p2.y - hor[p2.x]) < 1e-5:
            return copy(p2)

        # p - previous, c - current

        x1p, y1p = p1.x, hor[p1.x]
        x2p, y2p = p2.x, hor[p2.x]

        x1c, y1c = p1.x, p1.y
        x2c, y2c = p2.x, p2.y

        dyp = y2p - y1p
        dyc = y2c - y1c

        dx = x2c - x1c

        m = dyc / dx

        x = x1c - dx * (y1p - y1c) / (dyp - dyc)

        y = m * (x - x1c) + y1c

        return Point(x, y).x_rnd()

    @staticmethod
    def find_intersect(p1: Point, p2: Point, hor: List[float]) -> Point:
        """
        Это первый вариант реализации поиска пересечения отрезка с горизонтом.
        Данная реализация приведена в Роджерсе в качестве дефолтной

        :param p1: точка начала отрезка
        :param p2: точка конца отрезка
        :param hor: горизонт, с которым ищем пересечение
        :return: точка пересечения отрезка с горизонтом
        """

        def sign(x) -> int:
            return 1 if (x > 0) else -1 if (x < 0) else 0

        if p2.x == p1.x:
            return Point(p1.x, hor[p1.x], p1.z)

        if abs(p1.y - hor[p1.x]) < 1e-5:
            return copy(p1)

        if abs(p2.y - hor[p2.x]) < 1e-5:
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
        # if tmp_x > p2.x:
        #     res = Point(tmp_x, tmp_y, p1.z).x_rnd()
        #     print("p1: ", p1)
        #     print("p2: ", p2)
        #     print("hor: ", [(x, y) for x, y in zip(range(p1.x, p2.x + 1), hor[p1.x:(p2.x + 1)])])
        #     print("res: ", res)
        # ============DEBUG==============

        return Point(tmp_x, tmp_y, p1.z)

    def draw_curve(self, z: float):
        build_point = lambda x, y: self._tr_matrix.tr_point(Point(x, y, z)).x_rnd()

        all_x = self.range_x
        all_y = self.function.calculate(all_x, z)

        _points = [build_point(x, y) for x, y in zip(all_x, all_y)]
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

            # ================DEBUG====================
            # self._canvas.draw_point(p_curr, color=Color.RED, with_update=True)
            # ================DEBUG====================

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

            # ================DEBUG====================
            # utils.delay()
            # self._canvas.update()
            # ================DEBUG====================

        self.handle_right_edge(p_prev)

    def render(self) -> None:
        self._rendered = True
        self.solve()

        # ================DEBUG====================
        # print(timeit(lambda: self.solve(), number=1))
        # ================DEBUG====================

    def solve(self):
        self._canvas.clear()
        self._horiz.reset_all()
        self.edge_points_reset()

        # ================DEBUG====================
        # y-rot = 35; z-rot = 60; scale=50; func=exp(...)
        # x = 651
        # self._canvas.draw_line(Point(x, 0), Point(x, utils.H), color=Color.RED, with_update=True)
        # ================DEBUG====================

        for z in self.range_z:
            self.draw_curve(z)
            # ================DEBUG====================
            # utils.delay()
            # self._canvas.update()
            # ================DEBUG====================

        self._canvas.update()

    def rotate(self, value: int, axis: Axis) -> None:
        self._tr_matrix.rotate(value, axis)

        if self._rendered:
            self.solve()

    @property
    def ranges(self) -> Ranges:
        return self._ranges

    @ranges.setter
    def ranges(self, value: Ranges) -> None:
        self._ranges = value

        self._x_range = None
        self._z_range = None

        if self._rendered:
            self.solve()

    @property
    def function(self) -> Func:
        return self._func

    @function.setter
    def function(self, func: Func) -> None:
        self._func = func

        if self._rendered:
            self.solve()

    @property
    def scale_param(self) -> float:
        return self._tr_matrix.scale_param

    @scale_param.setter
    def scale_param(self, value: float) -> None:
        self._tr_matrix.scale_param = value

        if self._rendered:
            self.solve()

    @property
    def color(self) -> Color:
        return self._canvas.color

    @color.setter
    def color(self, value: Color) -> None:
        self._canvas.color = value

        if self._rendered:
            self.solve()

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
