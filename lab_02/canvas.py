from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from point import Point
from loguru import logger
from math import cos, sin

import numpy as np
import typing
import sys

from astroid import Astroid
from errors import ScaleInfo


class Canvas(QtWidgets.QLabel):
    def __init__(self, parent):
        super().__init__(parent)

        self.surf = QPixmap(3,3)
        self.surf.fill(Qt.white)

        self.coef = 40
        self.step = 1

        self.init_sizes = False

        self.dx = 0
        self.dy = 0

    def calc_sizes(self) -> typing.NoReturn:
        self.x_min = self.x()
        self.y_min = self.y()

        self.x_max = self.width() + self.x_min
        self.y_max = self.height() + self.y_min

        self.xc = (self.x_min + self.x_max) // 2
        self.yc = (self.y_min + self.y_max) // 2

        self.x0 = self.xc + self.dx
        self.y0 = self.yc + self.dy

        self.main_matr = np.array([[self.coef,       0,          0],
                                   [0,          -self.coef,      0],
                                   [self.x0,     self.y0,        1]])

    def mousePressEvent(self, event):
        self.last_point = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() & QtCore.Qt.LeftButton:
            dx_curr = self.last_point.x() - event.pos().x()
            dy_curr = self.last_point.y() - event.pos().y()

            self.last_point = event.pos()

            self.dx -= dx_curr
            self.dy -= dy_curr

            self.init_sizes = False
            self.repaint()

    @staticmethod
    def _round(num: float) -> int:
        return int(num + (0.5 if num > 0 else -0.5))

    def toCanv(self, point: Point) -> Point:
        new_point = tuple(
            map(self._round, point.to_ndarray().dot(self.main_matr)))[:-1]
        return Point(label=point.label, point=new_point)

    def valueToCanv(self, value: float) -> int:
        return self._round(self.coef * value)

    def fromCanv(self, point: Point) -> Point:
        pass
        # new_point = tuple(map(lambda x: round(x, 3), point.toNdarray().dot(self.inv_matr)))[:-1]
        # return Point(label=point.label, point=new_point)

    def stepUpdate(self):
        if self.coef >= 40:
            self.step = 1

        elif self.coef >= 20:
            self.step = 2

        elif self.coef >= 12:
            self.step = 5

        elif self.coef >= 5:
            self.step = 10

        else:
            self.step = 50

    def increase(self):
        if self.coef <= 500:
            self.coef += 5
        else:
            ScaleInfo('Вы достигли предельного масштаба')

        self.calc_sizes()
        self.stepUpdate()
        self.repaint()

    def decrease(self):
        if self.coef >= 6:
            self.coef -= 5
        elif self.coef > 1:
            self.coef -= 1
        else:
            ScaleInfo('Вы достигли предельного масштаба')

        self.init_sizes = False
        self.stepUpdate()
        self.repaint()

    def changeCenter(self, new_center: Point):
        new_center_canv = self.toCanv(new_center)
        logger.debug(f"canv_center: {new_center_canv}")

        self.dx -= new_center_canv.x - self.xc
        self.dy -= new_center_canv.y - self.yc
        self.init_sizes = False
        self.repaint()

    def fullSize(self, point_min: Point, point_max: Point):
        point_min = self.toCanv(point_min)
        point_max = self.toCanv(point_max)

        dx_max = abs(point_max.x - point_min.x)
        dy_max = abs(point_max.y - point_min.y)

        kdx = self.width() / dx_max
        kdy = self.height() / dy_max

        self.coef = self._round(self.coef * min(kdx, kdy) / 1.1)

        self.calc_sizes()
        self.stepUpdate()
        self.repaint()

    def scaleUp(self, astroid: Astroid):
        bp = astroid.border_points
        logger.debug(f'border_points: {bp}')

        if len(bp) > 0:
            tl, tr, bl, br = bp

            logger.debug(f"tl: {tl}, tr: {tr}, bl: {bl}, br: {br}")

            p_min = Point(x=min([p.x for p in bp]), y=min([p.y for p in bp]))
            p_max = Point(x=max([p.x for p in bp]), y=max([p.y for p in bp]))
            p_c = (p_min + p_max) / 2

            logger.debug(f"pc: {p_c}, pmin: {p_min}, pmax: {p_max}")

            if p_min != p_max:
                self.fullSize(p_min, p_max)
            else:
                logger.info("Try to scale zero-object")

            self.changeCenter(p_c)
