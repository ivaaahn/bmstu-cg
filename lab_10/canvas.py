from typing import List

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QPainter, QPen, QImage
from PyQt5.QtWidgets import QLabel

import utils
from models.point import Point
from models.segment import Segment
from properties.color import Color


class Canvas(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.clear()

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

    def draw_segments(self, segments: List[Segment], color: Color) -> None:
        qp = QPainter(self.img)
        qp.setPen(QPen(color.toQColor()))

        for segment in segments:
            qp.drawLine(segment.to_qline())

        qp.end()

    def draw_point(self, p: Point, color: Color) -> None:
        qp = QPainter(self.img)
        qp.setPen(QPen(color.toQColor()))

        qp.drawPoint(p.to_qpoint())

        qp.end()
