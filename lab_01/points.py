from PyQt5.QtWidgets import QTableWidgetItem
from itertools import combinations
from numpy import array, cross
from triangle import Triangle
from circle import Circle
from errors import ErrorCount
from point import Point


class Points():
    numbers = [x for x in range(1, 500)]

    best_triangle = None
    best_diff = None
    into_triangle = None
    outside_triangle = None

    data = dict()
    data_into = []
    data_outside = []
    need_update = True
    no_solve = True

    @classmethod
    def getLabel(cls):
        return 'P' + str(cls.numbers.pop(0))

    @classmethod
    def clearAns(cls):
        cls.data_into.clear()
        cls.data_outside.clear()

        cls.into_triangle = None
        cls.outside_triangle = None

        cls.best_triangle = None
        cls.best_diff = None

        cls.no_solve = True
        cls.need_update = True

    @classmethod
    def getMinMaxPoints(cls) -> list:
        points = cls.data.values()
        if len(points) > 0:
            x_points = [point.x for point in points]
            y_points = [point.y for point in points]

            p_min = Point(x=min(x_points), y=min(y_points))
            p_max = Point(x=max(x_points), y=max(y_points))

        return [p_min, p_max]

    @classmethod
    def updateSolve(cls):
        for a, b, c in combinations(cls.data.values(), 3):
            if a.value == b.value or b.value == c.value or a.value == c.value:
                continue

            if (c.x - a.x) * (b.y - a.y) == (b.x - a.x) * (c.y - a.y):
                continue

            into_triangle = 0
            into_circle = 0

            curr_triangle = Triangle([a, b, c])
            curr_circle = Circle(curr_triangle)
            curr_data_into = []
            curr_data_outside = []

            for point in cls.data.values():
                if curr_triangle.into(point):
                    into_triangle += 1
                    curr_data_into.append(point)

                elif curr_circle.into(point):
                    into_circle += 1
                    curr_data_outside.append(point)

            curr_diff = abs(into_circle - into_triangle)
            if cls.no_solve or curr_diff < cls.best_diff:
                Points.data_into = curr_data_into
                Points.data_outside = curr_data_outside
                cls.best_diff = curr_diff
                cls.into_triangle = into_triangle
                cls.outside_triangle = into_circle
                cls.best_triangle = curr_triangle
                cls.no_solve = False

                if cls.best_diff == 0:
                    break
