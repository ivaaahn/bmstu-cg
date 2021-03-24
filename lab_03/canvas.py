from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from point import Point
from loguru import logger
from math import cos, sin


import numpy as np
import typing



class Canvas(QtWidgets.QLabel):
    def __init__(self, parent):
        super().__init__(parent)

        self.surf = QPixmap(3,3)
        self.surf.fill(Qt.white)

        self.coef = 40

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
     