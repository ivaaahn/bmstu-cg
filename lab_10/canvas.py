from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QPen, QImage
from PyQt5.QtWidgets import QLabel

import utils
from models.point import Point
from properties.color import Color


class Canvas(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.clear()
        self._color = None

    @property
    def color(self) -> Color:
        return self._color

    @color.setter
    def color(self, value: Color) -> None:
        self._color = value

    def clear(self) -> None:
        self.img = self._new_image()
        self.update()

    @staticmethod
    def _new_image() -> QImage:
        img = QImage(utils.W, utils.H, QImage.Format_ARGB32_Premultiplied)
        img.fill(Qt.white)
        return img

    def update(self) -> None:
        self.pixmap = QPixmap().fromImage(self.img)
        self.setPixmap(self.pixmap)

    def draw_line(self, p1: Point, p2: Point, color: Color = None, with_update: bool = False) -> None:
        if not color:
            color = self.color

        qp = QPainter(self.img)
        qp.setPen(QPen(color.toQColor()))
        qp.drawLine(p1.to_qpointf(), p2.to_qpointf())

        qp.end()

        if with_update:
            self.update()

    def draw_point(self, p: Point, color: Color = None, with_update: bool = False) -> None:
        if not color:
            color = self.color

        qp = QPainter(self.img)
        qp.setPen(QPen(color.toQColor()))
        qp.drawPoint(p.to_qpoint())

        qp.end()

        if with_update:
            self.update()
