from PyQt5 import QtWidgets, QtCore
from points import Points
from circle import Circle
from point import Point
import numpy as np
from errors import ScaleInfo


class Drawer(QtWidgets.QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.coef = 40
        self.step = 1
        self.initDeltas()
        self.updateSizes()

    def initDeltas(self):
        self.dx = 0
        self.dy = 0

    def updateSizes(self):
        self.x_min = self.x() - 1
        self.y_min = self.y() - 2

        self.x_max = self.width() + self.x_min
        self.y_max = self.height() + self.y_min

        self.xc = (self.x_min + self.x_max) // 2
        self.yc = (self.y_min + self.y_max) // 2

        self.x0 = self.xc + self.dx
        self.y0 = self.yc + self.dy

        self.matr = np.array([[self.coef,       0,          0],
                              [0,      -self.coef,      0],
                              [self.x0,     self.y0,        1]])

        self.inv_matr = np.linalg.inv(self.matr)

    def addition_init(self, points_table, move_btn, point_btn):
        self.points_table = points_table
        self.point_btn = point_btn
        self.move_btn = move_btn

    def mousePressEvent(self, event):
        if self.point_btn.isChecked():
            point = Point(point=(event.pos().x() + self.x_min,
                                 event.pos().y()+self.y_min))
            self.points_table.add(self.fromCanv(point))
            self.repaint()
        else:
            self.last_point = event.pos()

    def mouseMoveEvent(self, event):
        if self.move_btn.isChecked():
            if event.buttons() & QtCore.Qt.LeftButton:
                dx_curr = self.last_point.x() - event.pos().x()
                dy_curr = self.last_point.y() - event.pos().y()

                self.last_point = event.pos()

                self.dx -= dx_curr
                self.dy -= dy_curr

                self.updateSizes()
                self.repaint()

    @staticmethod
    def _round(num: float) -> int:
        return int(num + (0.5 if num > 0 else -0.5))

    def toCanv(self, point: Point) -> Point:
        self.updateSizes()
        new_point = tuple(
            map(self._round, point.toNdarray().dot(self.matr)))[:-1]
        return Point(label=point.label, point=new_point)

    def valueToCanv(self, value: float) -> int:
        return self._round(self.coef * value)

    def fromCanv(self, point: Point) -> Point:
        self.updateSizes()
        new_point = tuple(
            map(lambda x: round(x, 3), point.toNdarray().dot(self.inv_matr)))[:-1]
        return Point(label=point.label, point=new_point)

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

        self.stepUpdate()
        self.repaint()

    def decrease(self):
        if self.coef >= 6:
            self.coef -= 5
        elif self.coef > 1:
            self.coef -= 1
        else:
            ScaleInfo('Вы достигли предельного масштаба')

        self.stepUpdate()
        self.repaint()

    def changeCenter(self, new_center: Point):
        new_center_canv = self.toCanv(new_center)

        self.dx -= new_center_canv.x - self.xc
        self.dy -= new_center_canv.y - self.yc
        self.repaint()

    def fullSize(self, point_min: Point, point_max: Point):
        point_min = self.toCanv(point_min)
        point_max = self.toCanv(point_max)

        dx_max = abs(point_max.x - point_min.x)
        dy_max = abs(point_max.y - point_min.y)

        kdx = self.width() / dx_max
        kdy = self.height() / dy_max

        self.coef = self._round(self.coef * min(kdx, kdy) / 1.1)

        self.stepUpdate()
        self.repaint()

    def scaleUp(self, circle: Circle):
        point_min = Point(x=circle.center.x - circle.radius,
                          y=circle.center.y - circle.radius)
        point_max = Point(x=circle.center.x + circle.radius,
                          y=circle.center.y + circle.radius)

        self.fullSize(point_min, point_max)
        self.changeCenter(circle.center)
